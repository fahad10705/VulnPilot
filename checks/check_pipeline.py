"""Lead check: runs the whole pipeline on both sample logs with no keys set.  Run:  python checks/check_pipeline.py"""
import os
import tempfile

for name in ("NEBIUS_API_KEY", "NEBIUS_MODEL", "SEPOLIA_RPC_URL", "CONTRACT_ADDRESS", "WALLET_PRIVATE_KEY"):
    os.environ[name] = ""  # make sure we test demo mode, whatever is in .env

from common import PASS, main, read_text
from vulnpilot import chain, pipeline


def check():
    chain.DEMO_FILE = os.path.join(tempfile.mkdtemp(), "demo_chain.json")  # do not touch the real record
    assert chain.chain_mode() == "demo", "With no keys the chain must be in demo mode"
    for log in ("auth_attack.log", "clean.log"):
        result = pipeline.run_analysis(read_text("sample_logs/" + log))
        assert len(result.statuses) == 13, f"{log}: expected 13 status rows, got {len(result.statuses)}"
        assert result.report_text.startswith("# "), f"{log}: report must start with '# '"
        assert len(result.report_hash) == 64, f"{log}: report_hash must be 64 characters"
        assert result.investigation.source.startswith("OFFLINE"), f"{log}: with no key the AI must be in offline mode"
    anchored = chain.anchor(result.report_hash)
    assert anchored["ok"] and anchored["mode"] == "demo", f"Demo anchoring failed: {anchored}"
    assert chain.verify(result.report_hash)["found"], "The anchored hash must verify"
    tampered, _ = pipeline.compute_hash(result.report_text, ["X" + result.evidence_lines[0]] + result.evidence_lines[1:])
    assert not chain.verify(tampered)["found"], "A tampered hash must NOT verify"
    return PASS


if __name__ == "__main__":
    main("pipeline (lead)", check)
