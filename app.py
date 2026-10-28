"""
app.py - Streamlit entry point (the web page).

WHO OWNS THIS: lead only. Beginners never edit this file.
Run:  python start.py     (or: streamlit run app.py)

All the thinking happens in vulnpilot/pipeline.py. This file only shows the results.
Flow for the visitor: pick a sample log (one click) or upload a log -> read the findings and the AI report
-> anchor the fingerprint -> verify it -> try the tamper test.
Look: black and white, thin borders, small radius (the CSS is in the STYLE string below).
"""

import html
import os

import pandas as pd
import streamlit as st

from vulnpilot import chain
from vulnpilot.charts import make_timeline_chart
from vulnpilot.pipeline import compute_hash, run_analysis

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_logs")
SAMPLES = {"attack": "auth_attack.log", "clean": "clean.log"}

st.set_page_config(page_title="VulnPilot - provable incident reports", page_icon="🛡️", layout="centered",
                   initial_sidebar_state="collapsed")

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap');
:root { --bg:#000; --panel:#0a0a0a; --line:#262626; --text:#ededed; --muted:#a1a1a1; --faint:#6b6b6b; }
html, body, .stApp, .stMarkdown, button, input, textarea { font-family: 'Geist', -apple-system, 'Segoe UI', Roboto, sans-serif; }
[data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important; }
.stApp { background: var(--bg); color: var(--text); }
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1040px; padding: 4rem 1.5rem 5rem; }
h1, h2, h3 { letter-spacing: -0.03em; font-weight: 600; }
a { color: var(--text); }

.vp-eyebrow { font-family: 'Geist Mono', monospace; font-size: .75rem; letter-spacing: .12em; color: var(--muted); text-transform: uppercase; }
.vp-h1 { font-size: clamp(2rem, 5.5vw, 3.6rem); line-height: 1.05; letter-spacing: -0.045em; font-weight: 650; margin: .6rem 0 1rem; }
.vp-sub { color: var(--muted); font-size: 1.1rem; line-height: 1.55; max-width: 640px; margin-bottom: 1.75rem; }
.vp-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: .6rem 0 2.25rem; }
.vp-step { border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px; background: var(--panel); }
.vp-step .no { font-family: 'Geist Mono', monospace; color: var(--faint); font-size: .8rem; }
.vp-step .t { font-weight: 600; margin: 6px 0 2px; }
.vp-step .d { color: var(--muted); font-size: .9rem; line-height: 1.45; }

[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line) !important; border-radius: 10px !important; background: var(--panel); }
.vp-label { font-weight: 600; font-size: 1rem; margin-bottom: 2px; }
.vp-hint { color: var(--muted); font-size: .88rem; margin-bottom: 12px; }

[data-testid="stBaseButton-primary"] { background: #ededed; color: #000; border: 1px solid #ededed; border-radius: 6px; height: 46px; font-weight: 600; width: 100%; }
[data-testid="stBaseButton-primary"]:hover { background: #fff; border-color: #fff; color: #000; }
[data-testid="stBaseButton-secondary"] { background: transparent; color: var(--text); border: 1px solid #333; border-radius: 6px; height: 46px; font-weight: 500; width: 100%; }
[data-testid="stBaseButton-secondary"]:hover { border-color: #888; color: #fff; background: #111; }
[data-testid="stFileUploaderDropzone"] { background: #050505; border: 1px dashed #3a3a3a; border-radius: 8px; }
[data-testid="stFileUploaderDropzone"] button { border-radius: 6px; }

[data-baseweb="tab-list"] { gap: 22px; border-bottom: 1px solid var(--line); }
[data-baseweb="tab"] { color: var(--muted); padding: 10px 2px; }
[data-baseweb="tab"][aria-selected="true"] { color: #fff; }
[data-baseweb="tab-highlight"] { background: #ededed; height: 2px; }
[data-baseweb="tab-border"] { display: none; }
[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 8px; background: var(--panel); }
pre, code { font-family: 'Geist Mono', monospace !important; font-size: .8rem !important; }

.vp-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin: 2.5rem 0 1rem; }
.vp-head .k { color: var(--muted); font-size: .8rem; font-family: 'Geist Mono', monospace; }
.vp-head .v { font-size: 1.3rem; font-weight: 600; letter-spacing: -0.02em; }
.vp-badge { display: inline-block; font-family: 'Geist Mono', monospace; font-size: .75rem; letter-spacing: .06em; padding: 4px 10px; border-radius: 999px; border: 1px solid; text-transform: uppercase; }
.vp-low { color: #3ecf8e; border-color: #1f5f45; } .vp-medium { color: #f5c542; border-color: #6b5316; }
.vp-high { color: #ff9a3c; border-color: #6e4212; } .vp-critical { color: #ff5d5d; border-color: #7a2323; }
.vp-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 1.5rem; }
.vp-stat { border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; background: var(--panel); }
.vp-stat .n { font-size: 1.9rem; font-weight: 600; letter-spacing: -0.03em; line-height: 1.1; }
.vp-stat .l { color: var(--muted); font-size: .8rem; margin-top: 4px; }
.vp-note { color: var(--faint); font-size: .8rem; font-family: 'Geist Mono', monospace; }
.vp-banner { border: 1px solid #3a3a3a; border-radius: 8px; padding: 10px 14px; color: var(--muted); font-size: .88rem; margin-bottom: 1rem; }
.vp-result { border-radius: 8px; padding: 18px 20px; border: 1px solid; margin: 12px 0; }
.vp-result b { font-size: 1.15rem; letter-spacing: -0.02em; display: block; margin-bottom: 4px; }
.vp-result.ok { border-color: #1f5f45; background: #04140d; color: #7be0b3; }
.vp-result.bad { border-color: #7a2323; background: #160606; color: #ff8a8a; }
.vp-step-title { font-weight: 600; margin-top: 1.6rem; }
.vp-footer { color: var(--faint); font-size: .78rem; font-family: 'Geist Mono', monospace; margin-top: 3rem; border-top: 1px solid var(--line); padding-top: 1rem; }

@media (max-width: 640px) {
  .block-container { padding: 2rem 1rem 4rem; }
  .vp-sub { font-size: 1rem; }
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)


def read_sample(kind):
    with open(os.path.join(SAMPLE_DIR, SAMPLES[kind])) as f:
        return f.read()


def run_and_store(text, name):
    """Run the whole analysis (this can take up to a minute while the AI writes) and remember it."""
    with st.spinner("Analyzing the log. The AI step can take a few seconds to a minute ..."):
        st.session_state["result"] = run_analysis(text)
    st.session_state["log_name"] = name
    st.session_state.pop("anchor", None)
    st.rerun()  # draw the results right away (without this the first click seemed to do nothing)


def start_panel():
    """The 'what do I do now' panel: one big button, a second sample, or an upload."""
    with st.container(border=True):
        left, right = st.columns([1, 1], gap="large")
        with left:
            st.markdown('<div class="vp-label">Try it in one click</div>'
                        '<div class="vp-hint">No file needed. We use a sample SSH log that contains a real-looking attack.</div>',
                        unsafe_allow_html=True)
            if st.button("Analyze the sample attack log  →", type="primary", key="go_attack", width="stretch"):
                run_and_store(read_sample("attack"), SAMPLES["attack"])
            if st.button("Or try a clean log (no attacks)", key="go_clean", width="stretch"):
                run_and_store(read_sample("clean"), SAMPLES["clean"])
        with right:
            st.markdown('<div class="vp-label">Or upload your own log</div>'
                        '<div class="vp-hint">An SSH authentication log (.log or .txt). Analysis starts right after the upload.</div>',
                        unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload an SSH authentication log", type=["log", "txt"], label_visibility="collapsed")
            if uploaded is not None and st.session_state.get("last_upload") != uploaded.file_id:
                st.session_state["last_upload"] = uploaded.file_id
                run_and_store(uploaded.getvalue().decode("utf-8", errors="replace"), uploaded.name)


def stat(number, label):
    return f'<div class="vp-stat"><div class="n">{number}</div><div class="l">{label}</div></div>'


# ---------- hero ----------
result = st.session_state.get("result")

if result:
    st.markdown('<div class="vp-eyebrow">VulnPilot &nbsp;·&nbsp; AI security analyst</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="vp-eyebrow">VulnPilot &nbsp;·&nbsp; AI security analyst</div>'
                '<h1 class="vp-h1">Security reports you can prove were never edited.</h1>'
                '<div class="vp-sub">Give it an SSH login log. It finds the attacks, an AI writes the investigation, '
                'and a fingerprint of the report is saved on a blockchain, so any later change is caught.</div>',
                unsafe_allow_html=True)

if not result:
    start_panel()
    st.markdown("""
<div class="vp-eyebrow" style="margin-top:2.5rem">How it works</div>
<div class="vp-steps">
  <div class="vp-step"><div class="no">01</div><div class="t">Pick or upload a log</div><div class="d">Click the sample, or drop in your own SSH log.</div></div>
  <div class="vp-step"><div class="no">02</div><div class="t">Read the findings</div><div class="d">Attacks, the exact log lines as evidence, and an AI report.</div></div>
  <div class="vp-step"><div class="no">03</div><div class="t">Prove it</div><div class="d">Anchor the fingerprint, verify it, then try to tamper with it.</div></div>
</div>
""", unsafe_allow_html=True)
    st.markdown('<div class="vp-footer">Runs on Streamlit · AI via OpenRouter, Groq or Google · fingerprints anchored on the Sepolia test network</div>',
                unsafe_allow_html=True)
    st.stop()

# ---------- results header ----------
risk = result.risk
st.markdown(f'<div class="vp-head"><div><div class="k">ANALYSIS OF</div><div class="v">{html.escape(st.session_state.get("log_name", "log"))}</div></div>'
            f'<div><span class="vp-badge vp-{html.escape(risk.level)}">{html.escape(risk.level)} risk · {risk.score}/100</span></div></div>',
            unsafe_allow_html=True)

if any(row["status"] in ("dummy", "error") for row in result.statuses):
    st.markdown('<div class="vp-banner">Some analysis modules are still placeholders, so parts of this page show sample data. '
                'See "Build status" at the bottom.</div>', unsafe_allow_html=True)

high_priority = [f for f in result.findings if f.severity in ("high", "critical")]
st.markdown('<div class="vp-stats">' + stat(len(result.events), "Events analyzed") + stat(len(result.evidence_lines), "Suspicious events")
            + stat(len(high_priority), "High priority findings") + stat(len(result.indicators), "Indicators") + '</div>',
            unsafe_allow_html=True)

with st.expander("Analyze another log"):
    start_panel()

tab_find, tab_time, tab_mitre, tab_ai, tab_proof = st.tabs(["Findings", "Timeline", "MITRE ATT&CK", "AI investigation", "Proof"])

with tab_find:
    if not result.findings:
        st.markdown('<div class="vp-result ok"><b>Nothing suspicious found.</b>The rules found no attack patterns in this log.</div>',
                    unsafe_allow_html=True)
    for finding in result.findings:
        with st.expander(f"{finding.severity.upper()}  ·  {finding.title}"):
            st.write(finding.description)
            st.caption(f"Source IP {finding.source_ip or '-'}  ·  users: {', '.join(finding.users) or '-'}  ·  {len(finding.evidence_lines)} evidence line(s)")
            st.code("\n".join(finding.evidence_lines), language=None)
    if result.indicators:
        st.markdown("##### Indicators of compromise")
        st.dataframe(pd.DataFrame([vars(i) for i in result.indicators]), hide_index=True, width="stretch")
    st.markdown("##### Why this risk level")
    for reason in result.risk.reasons:
        st.write("- " + reason)

with tab_time:
    if result.timeline:
        st.plotly_chart(make_timeline_chart(result.timeline), width="stretch")
        st.dataframe(pd.DataFrame([vars(e) for e in result.timeline]), hide_index=True, width="stretch")
    else:
        st.write("No suspicious events, so there is no timeline.")

with tab_mitre:
    st.caption("MITRE ATT&CK is a public catalogue of attacker techniques. Each finding is mapped to one.")
    if result.mitre:
        st.dataframe(pd.DataFrame(result.mitre), hide_index=True, width="stretch")
    else:
        st.write("No MITRE techniques to show.")

with tab_ai:
    st.markdown(f'<div class="vp-note">AI model used: {html.escape(result.investigation.source)}</div>', unsafe_allow_html=True)
    if result.investigation.notes:
        with st.expander("How this answer was produced"):
            for note in result.investigation.notes:
                st.write("- " + note + ", so the next service was tried")
    st.write(result.investigation.summary)
    st.markdown("##### Confirmed observations")
    st.caption("Each one quotes a real log line.")
    for item in result.investigation.confirmed:
        st.write("- " + item)
    st.markdown("##### Hypotheses")
    st.caption("Guesses, not proven by the log.")
    for item in result.investigation.hypotheses:
        st.write("- " + item)
    st.markdown("##### Recommended actions")
    for item in result.investigation.actions:
        st.write("- " + item)

with tab_proof:
    st.markdown("Every change to this report or its evidence changes its fingerprint. We save the fingerprint on a blockchain, "
                "so nobody can quietly edit the report later.")

    st.markdown('<div class="vp-step-title">1 · The fingerprint</div>', unsafe_allow_html=True)
    st.caption("A SHA-256 hash of the report plus the evidence lines.")
    st.code(result.report_hash, language=None)
    st.download_button("Download the report (.md)", result.report_text, file_name="vulnpilot_report.md")

    st.markdown('<div class="vp-step-title">2 · Anchor it</div>', unsafe_allow_html=True)
    if chain.chain_mode() == "demo":
        st.caption("Demo mode: the fingerprint is saved in a local file instead of the Sepolia test blockchain.")
    else:
        st.caption("Writes the fingerprint to the Sepolia test blockchain (costs free test coins).")
    if st.button("Anchor this fingerprint", type="primary", key="btn_anchor", width="stretch"):
        st.session_state["anchor"] = chain.anchor(result.report_hash)
    anchor = st.session_state.get("anchor")
    if anchor:
        (st.success if anchor["ok"] else st.error)(anchor["message"])
        if anchor.get("explorer_url"):
            st.markdown(f"[See the transaction on Etherscan]({anchor['explorer_url']})")

    st.markdown('<div class="vp-step-title">3 · Verify, then try to cheat</div>', unsafe_allow_html=True)
    st.caption("Verify recomputes the fingerprint and looks for it on the chain. Switch on the tamper test to change "
               "one character of the evidence first: verification must then fail.")
    tamper = st.toggle("Tamper test: change one character of the evidence")
    if st.button("Verify", key="btn_verify", width="stretch"):
        evidence = list(result.evidence_lines)
        if tamper and evidence:
            evidence[0] = "X" + evidence[0][1:]  # flip one character of the first evidence line
        current_hash, _ = compute_hash(result.report_text, evidence)
        check = chain.verify(current_hash)
        if not check["ok"]:
            st.error(check["message"])
        elif check["found"]:
            st.markdown('<div class="vp-result ok"><b>Verified</b>This report and its evidence match what was anchored. Nothing was changed.</div>',
                        unsafe_allow_html=True)
        else:
            why = ("The evidence was changed by one character, so the fingerprint no longer matches." if tamper
                   else "This fingerprint was never anchored. Click 'Anchor this fingerprint' first.")
            st.markdown(f'<div class="vp-result bad"><b>Not verified</b>{why}</div>', unsafe_allow_html=True)
        st.caption(check["message"])

# ---------- team status and footer ----------
with st.expander("Build status (for the team)"):
    st.dataframe(pd.DataFrame(result.statuses)[["module", "status", "note"]], hide_index=True, width="stretch")
    done = sum(1 for row in result.statuses if row["status"] == "real")
    st.caption(f"{done} of {len(result.statuses)} modules are real. 'dummy' = not written yet, 'error' = it crashed.")
    for warning in result.warnings:
        st.warning(warning)

mode = "demo mode" if chain.chain_mode() == "demo" else "live on Sepolia"
st.markdown(f'<div class="vp-footer">VulnPilot · blockchain: {mode} · AI: {html.escape(result.investigation.source)}</div>', unsafe_allow_html=True)
