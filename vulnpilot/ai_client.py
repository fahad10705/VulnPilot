"""
ai_client.py - asks an AI model to write the investigation. Tries several AI services in order.

WHO OWNS THIS: lead only. Beginners never edit this file and never need an API key.

investigate(findings, risk, system_prompt, user_prompt) -> Investigation

Order of services (a service is used only if its key is set):
  1. Nebius Token Factory  (NEBIUS_API_KEY + NEBIUS_MODEL)           NVIDIA Nemotron, the hackathon platform
  2. OpenRouter            (OPENROUTER_API_KEY)                      free NVIDIA Nemotron models
  3. Groq                  (GROQ_API_KEY)                            free gpt-oss models, very fast
  4. Google AI Studio      (GOOGLE_API_KEY)                          free Gemini model
  5. OFFLINE SAMPLE        (no key needed)                           built from the findings, clearly labelled

If a service fails (error, rate limit, timeout, empty or broken answer) the next one is tried, so the app
always gives an answer. Every service speaks the same "OpenAI" API, so one code path serves all of them.
The model that answered is written in Investigation.source, and the UI shows it.

Grounding check: every CONFIRMED claim must quote an evidence line that really exists. A claim whose quote
is not in the evidence is moved to HYPOTHESES (the AI cannot invent evidence).
"""

import hashlib
import json
import re
import time

from vulnpilot.config import get_setting
from vulnpilot.models import Investigation

OFFLINE = "OFFLINE SAMPLE (not written by the AI)"

MAX_TOKENS = 4000            # room for the answer
CALL_TIMEOUT = 40            # seconds one attempt may take
TOTAL_BUDGET = 110           # seconds for all attempts together, then we use the offline sample

# Default models. Each can be replaced with a setting (NEBIUS_MODEL, OPENROUTER_MODEL, GROQ_MODEL, GOOGLE_MODEL).
# "reasoning" is switched off or turned low on purpose: otherwise these models "think" for minutes.
OPENROUTER_MODELS = ["nvidia/nemotron-3.5-super-vl:free", "nvidia/nemotron-3-ultra-550b-a55b:free",
                     "nvidia/nemotron-3.5-lightning:free"]
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
GOOGLE_MODELS = ["gemini-3.5-flash"]

_CACHE = {}                  # same prompt -> same answer, so repeated clicks do not use up free limits


def clear_cache():
    _CACHE.clear()


def _models(setting_name, defaults):
    """The setting (if given) goes first, then the built-in defaults."""
    chosen = get_setting(setting_name)
    return ([chosen] if chosen else []) + [m for m in defaults if m != chosen]


def _providers():
    """The services that have a key, in the order we try them."""
    found = []
    if get_setting("NEBIUS_API_KEY") and get_setting("NEBIUS_MODEL"):
        found.append({"name": "Nebius", "base_url": get_setting("NEBIUS_BASE_URL"), "api_key": get_setting("NEBIUS_API_KEY"),
                      "models": [get_setting("NEBIUS_MODEL")], "extra": {}})
    if get_setting("OPENROUTER_API_KEY"):
        found.append({"name": "OpenRouter", "base_url": "https://openrouter.ai/api/v1", "api_key": get_setting("OPENROUTER_API_KEY"),
                      "models": _models("OPENROUTER_MODEL", OPENROUTER_MODELS),
                      "extra": {"extra_body": {"reasoning": {"enabled": False}}}})
    if get_setting("GROQ_API_KEY"):
        found.append({"name": "Groq", "base_url": "https://api.groq.com/openai/v1", "api_key": get_setting("GROQ_API_KEY"),
                      "models": _models("GROQ_MODEL", GROQ_MODELS), "extra": {"reasoning_effort": "low"}})
    if get_setting("GOOGLE_API_KEY"):
        found.append({"name": "Google", "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
                      "api_key": get_setting("GOOGLE_API_KEY"), "models": _models("GOOGLE_MODEL", GOOGLE_MODELS),
                      "extra": {"reasoning_effort": "low"}})
    return found


def _ask(provider, model, system_prompt, user_prompt, timeout):
    """One call to one model. Returns the answer text. Raises on any problem (the caller moves on)."""
    from openai import BadRequestError, OpenAI
    client = OpenAI(base_url=provider["base_url"], api_key=provider["api_key"], timeout=timeout, max_retries=0)
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    try:
        response = client.chat.completions.create(model=model, messages=messages, temperature=0.2,
                                                  max_tokens=MAX_TOKENS, **provider["extra"])
    except BadRequestError:
        if not provider["extra"]:
            raise
        # this model does not know the "reasoning" option: try again without it
        response = client.chat.completions.create(model=model, messages=messages, temperature=0.2, max_tokens=MAX_TOKENS)
    text = response.choices[0].message.content or ""
    if not text.strip():
        raise ValueError("empty answer")
    return text


def investigate(findings, risk, system_prompt, user_prompt):
    """Return an Investigation. Never raises: falls back through the services, then to the offline sample."""
    key = hashlib.sha256((system_prompt + "\n" + user_prompt).encode("utf-8")).hexdigest()
    if key in _CACHE:
        return _CACHE[key]

    providers = _providers()
    if not providers:
        return offline_investigation(findings, risk, "no AI key is set")

    notes = []
    started = time.monotonic()
    for provider in providers:
        for model in provider["models"]:
            remaining = TOTAL_BUDGET - (time.monotonic() - started)
            if remaining < 5:
                notes.append("time budget used up")
                return offline_investigation(findings, risk, "the AI services took too long", notes)
            try:
                text = _ask(provider, model, system_prompt, user_prompt, min(CALL_TIMEOUT, remaining))
                answer = parse_answer(text, findings, f"{model} via {provider['name']}")
                answer.notes = notes
                _CACHE[key] = answer
                return answer
            except Exception as error:
                notes.append(f"{provider['name']} {model} failed ({type(error).__name__})")
    return offline_investigation(findings, risk, "every AI service failed", notes)


def _is_grounded(quote, known_lines):
    """True if the quote is (part of) a real evidence line."""
    quote = quote.strip()
    if len(quote) < 15:
        return False
    for line in known_lines:
        if quote in line or line in quote:
            return True
    return False


def parse_answer(answer_text, findings, source):
    """Turn the model's JSON text into an Investigation, checking every quote against the evidence."""
    text = re.sub(r"<think>.*?</think>", "", answer_text, flags=re.S)  # some models print their thinking
    start = text.find("{")
    end = text.rfind("}")
    data = json.loads(text[start:end + 1])
    if not isinstance(data, dict) or not data.get("summary"):
        raise ValueError("the answer has no summary")

    known_lines = []
    for finding in findings:
        known_lines += finding.evidence_lines

    confirmed = []
    hypotheses = [str(item) for item in data.get("hypotheses", [])]
    for item in data.get("confirmed", []):
        claim = str(item.get("claim", "")) if isinstance(item, dict) else str(item)
        quote = str(item.get("evidence_line", "")) if isinstance(item, dict) else ""
        if _is_grounded(quote, known_lines):
            confirmed.append(f"{claim}  [evidence: {quote.strip()}]")
        else:
            hypotheses.append(f"{claim} (unverified: the quoted log line was not found in the evidence)")
    return Investigation(
        summary=str(data["summary"]),
        confirmed=confirmed[:8],
        hypotheses=hypotheses[:6],
        actions=[str(item) for item in data.get("actions", [])][:6],
        source=source,
    )


def offline_investigation(findings, risk, reason, notes=None):
    """A clearly labelled sample built straight from the findings (no AI involved)."""
    confirmed = []
    for finding in findings:
        if finding.evidence_lines:
            confirmed.append(f"{finding.title}: {finding.description}  [evidence: {finding.evidence_lines[0]}]")
    if findings:
        actions = ["Reset the passwords of the accounts involved.",
                   "Block the attacking IP addresses at the firewall.",
                   "Review what the logged-in account did after the successful login."]
    else:
        actions = ["No action needed. Keep monitoring."]
    summary = (f"OFFLINE SAMPLE ({reason}). Overall risk is {risk.level}. "
               f"{len(findings)} finding(s) were detected by the rules.")
    return Investigation(summary=summary, confirmed=confirmed,
                         hypotheses=["Offline mode: no AI hypotheses were generated."],
                         actions=actions, source=OFFLINE, notes=notes or [])
