"""
app.py - Streamlit entry point (the web page).

WHO OWNS THIS: lead only. Beginners never edit this file.
Run:  python start.py     (or: streamlit run app.py)

All the thinking happens in vulnpilot/pipeline.py. This file only shows the results:
upload a log -> Run analysis -> metrics, findings, timeline, MITRE, AI investigation, report, Anchor / Verify / Tamper test.
"""

import os

import pandas as pd
import streamlit as st

from vulnpilot import chain
from vulnpilot.charts import make_timeline_chart
from vulnpilot.pipeline import compute_hash, run_analysis

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_logs")
SAMPLES = {"Sample: attack log": "auth_attack.log", "Sample: clean log (no attacks)": "clean.log"}

st.set_page_config(page_title="VulnPilot", layout="wide")
st.title("VulnPilot")
st.caption("An AI security analyst whose incident reports are provably untampered.")

# ---------- choose a log ----------
choice = st.radio("Which log do you want to analyse?", list(SAMPLES) + ["Upload my own log"], horizontal=True)
log_text = ""
if choice == "Upload my own log":
    uploaded = st.file_uploader("Upload an SSH authentication log", type=["log", "txt"])
    if uploaded is not None:
        log_text = uploaded.getvalue().decode("utf-8", errors="replace")
else:
    with open(os.path.join(SAMPLE_DIR, SAMPLES[choice])) as f:
        log_text = f.read()

if st.button("Run analysis", type="primary", disabled=not log_text):
    st.session_state["result"] = run_analysis(log_text)
    st.session_state.pop("anchor", None)

result = st.session_state.get("result")

# ---------- sidebar: status table and warnings ----------
with st.sidebar:
    st.header("Module status")
    if result:
        st.dataframe(pd.DataFrame(result.statuses)[["module", "status", "note"]], hide_index=True, width="stretch")
        done = sum(1 for row in result.statuses if row["status"] == "real")
        st.caption(f"{done} of {len(result.statuses)} modules are real. 'dummy' = not written yet, 'error' = it crashed.")
        for warning in result.warnings:
            st.warning(warning)
    else:
        st.write("Run an analysis to see which modules are real, dummy or broken.")
    st.divider()
    if chain.chain_mode() == "demo":
        st.info("Blockchain: DEMO MODE (no keys set). Anchoring is simulated.")
    else:
        st.success("Blockchain: LIVE on Sepolia testnet.")

if not result:
    st.info("Pick a log and click 'Run analysis'.")
    st.stop()

if any(row["status"] in ("dummy", "error") for row in result.statuses):
    st.warning("Some modules are still dummy, so parts of this page show placeholder data. See the sidebar.")

# ---------- metrics ----------
suspicious_lines = result.evidence_lines
high_priority = [f for f in result.findings if f.severity in ("high", "critical")]
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Events analyzed", len(result.events))
c2.metric("Suspicious events", len(suspicious_lines))
c3.metric("High priority findings", len(high_priority))
c4.metric("Indicators", len(result.indicators))
c5.metric("Risk", f"{result.risk.level.upper()} ({result.risk.score})")

tab_find, tab_time, tab_mitre, tab_ai, tab_report = st.tabs(
    ["Findings", "Attack timeline", "MITRE ATT&CK", "AI investigation", "Report & proof"])

with tab_find:
    if not result.findings:
        st.success("Nothing suspicious found in this log.")
    else:
        st.dataframe(pd.DataFrame([{"severity": f.severity, "finding": f.title, "source IP": f.source_ip,
                                    "users": ", ".join(f.users), "evidence lines": len(f.evidence_lines)}
                                   for f in result.findings]), hide_index=True, width="stretch")
        for finding in result.findings:
            with st.expander(f"{finding.title}  [{finding.severity}]"):
                st.write(finding.description)
                st.code("\n".join(finding.evidence_lines), language=None)
    st.subheader("Indicators of compromise")
    st.dataframe(pd.DataFrame([vars(i) for i in result.indicators]), hide_index=True, width="stretch")
    st.subheader("Why this risk level")
    for reason in result.risk.reasons:
        st.write("- " + reason)

with tab_time:
    if result.timeline:
        st.plotly_chart(make_timeline_chart(result.timeline), width="stretch")
        st.dataframe(pd.DataFrame([vars(e) for e in result.timeline]), hide_index=True, width="stretch")
    else:
        st.write("No suspicious events, so there is no timeline.")

with tab_mitre:
    if result.mitre:
        st.dataframe(pd.DataFrame(result.mitre), hide_index=True, width="stretch")
    else:
        st.write("No MITRE techniques to show.")

with tab_ai:
    st.caption(f"Source: {result.investigation.source}")
    st.write(result.investigation.summary)
    st.markdown("**Confirmed observations** (each one quotes a real log line)")
    for item in result.investigation.confirmed:
        st.write("- " + item)
    st.markdown("**Hypotheses** (guesses, not proven)")
    for item in result.investigation.hypotheses:
        st.write("- " + item)
    st.markdown("**Recommended actions**")
    for item in result.investigation.actions:
        st.write("- " + item)

with tab_report:
    st.download_button("Download incident report (.md)", result.report_text, file_name="vulnpilot_report.md")
    with st.expander("Show the report"):
        st.markdown(result.report_text)
    st.subheader("Proof that it was not edited")
    st.write("SHA-256 fingerprint of the report plus the evidence lines:")
    st.code(result.report_hash, language=None)

    if st.button("Anchor this fingerprint"):
        st.session_state["anchor"] = chain.anchor(result.report_hash)
    anchor = st.session_state.get("anchor")
    if anchor:
        (st.success if anchor["ok"] else st.error)(anchor["message"])
        if anchor.get("explorer_url"):
            st.markdown(f"[See the transaction on Etherscan]({anchor['explorer_url']})")

    tamper = st.checkbox("Tamper test: change ONE character of the evidence, then verify")
    if st.button("Verify"):
        evidence = list(result.evidence_lines)
        if tamper and evidence:
            evidence[0] = "X" + evidence[0][1:]  # flip one character of the first evidence line
            st.caption("The first evidence line was edited by one character before hashing.")
        current_hash, _ = compute_hash(result.report_text, evidence)
        check = chain.verify(current_hash)
        if not check["ok"]:
            st.error(check["message"])
        elif check["found"]:
            st.success("VERIFIED: this report and evidence match what was anchored. Nothing was changed.")
        else:
            st.error("NOT VERIFIED: this fingerprint was never anchored. The report or evidence was changed "
                     "(or you have not clicked 'Anchor this fingerprint' yet).")
        st.caption(check["message"])
