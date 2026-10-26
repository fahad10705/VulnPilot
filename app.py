"""
app.py - Streamlit entry point. Wires all modules together.

Run:  streamlit run app.py
Flow: upload log -> parse -> detect -> IOCs/MITRE/timeline -> AI investigation
      -> report -> anchor hash on chain -> Verify button.

Owner: lead
Status: working with dummy data
"""

import os

import pandas as pd
import streamlit as st

from vulnpilot.ai_investigator import investigate
from vulnpilot.chain import anchor_hash, make_hash, verify_hash
from vulnpilot.detections import run_detections
from vulnpilot.ioc import extract_iocs
from vulnpilot.mitre import map_to_mitre
from vulnpilot.parser import parse_log
from vulnpilot.report import build_report
from vulnpilot.timeline import build_timeline, make_timeline_chart

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "sample_logs", "auth_attack.log")

st.set_page_config(page_title="VulnPilot", layout="wide")
st.title("VulnPilot")
st.caption("An AI security analyst whose incident reports are provably untampered.")

uploaded = st.file_uploader("Upload an authentication log", type=["log", "txt"])
use_sample = st.button("Use sample log")

if uploaded is not None:
    st.session_state["log_text"] = uploaded.getvalue().decode("utf-8", errors="replace")
elif use_sample:
    with open(SAMPLE_PATH) as f:
        st.session_state["log_text"] = f.read()

log_text = st.session_state.get("log_text")
if not log_text:
    st.info("Upload a log or click 'Use sample log' to start.")
    st.stop()

# Run the pipeline
events = parse_log(log_text)
findings = run_detections(events)
iocs = extract_iocs(findings, events)
timeline = build_timeline(findings, events)
mitre = map_to_mitre(findings)
investigation = investigate(findings)
report_text = build_report(findings, iocs, timeline, mitre, investigation)
evidence = [line for f in findings for line in f.evidence_lines]

tab_find, tab_ioc, tab_time, tab_ai, tab_report = st.tabs(
    ["Findings", "IOCs & MITRE", "Timeline", "AI investigation", "Report & proof"]
)

with tab_find:
    for f in findings:
        st.subheader(f"{f.title} [{f.severity}]")
        st.write(f.description)
        st.code("\n".join(f.evidence_lines))

with tab_ioc:
    st.dataframe(pd.DataFrame([vars(i) for i in iocs]))
    st.dataframe(pd.DataFrame(mitre))

with tab_time:
    st.plotly_chart(make_timeline_chart(timeline), width="stretch")

with tab_ai:
    st.metric("Risk level", investigation.risk_level)
    st.write(investigation.summary)
    st.markdown("**Confirmed**")
    for item in investigation.confirmed:
        st.write("- " + item)
    st.markdown("**Hypotheses**")
    for item in investigation.hypotheses:
        st.write("- " + item)
    st.markdown("**Actions**")
    for item in investigation.actions:
        st.write("- " + item)

with tab_report:
    st.download_button("Download report (.md)", report_text, file_name="vulnpilot_report.md")
    report_hash = make_hash(report_text, evidence)
    st.code(report_hash, language=None)
    if st.button("Anchor on Sepolia"):
        st.session_state["anchor"] = anchor_hash(report_hash)
    if "anchor" in st.session_state:
        st.write(st.session_state["anchor"]["explorer_url"])
    if st.button("Verify"):
        result = verify_hash(report_hash)
        if result["found"]:
            st.success("Verified: this report matches the hash anchored on-chain.")
        else:
            st.error("NOT verified: this report/evidence does not match any anchored hash.")
