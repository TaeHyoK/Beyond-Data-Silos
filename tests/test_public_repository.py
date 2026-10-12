"""Check the code-only public release without private data or paid API calls."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_release_has_one_current_implementation():
    for name in ("run_config", "ablation_suite", "ablation_evaluation", "real_report_evaluation"):
        assert (ROOT / "ablation" / name).is_dir()
    assert (ROOT / "src/orchestration/full_report_pipeline.py").is_file()
    assert (ROOT / "src/Agent_Team/Strategy_Agent/agent.py").is_file()
    assert not (ROOT / "ablation/run_config/recover_amore_writer_r03.py").exists()


def test_runtime_results_and_private_history_are_not_published():
    forbidden = (
        "final_reports", "final_reports_redesigned", "ablation/results",
        "docs/history", "docs/ablation_handoff", "private_audit",
    )
    if (ROOT / ".git").exists():
        tracked = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT, text=True
        ).split("\0")
        assert "configs/.env" not in tracked
        for relative in forbidden:
            assert not any(name.startswith(relative + "/") for name in tracked)
    assert "configs/.env" in (ROOT / ".gitignore").read_text().splitlines()
    assert (ROOT / "configs/.env.example").is_file()


def test_paper_title_and_current_framework_asset():
    readme = (ROOT / "README.md").read_text()
    assert readme.startswith(
        "# Beyond Data Silos: Cross-Domain Context and Peer Analysis "
        "for Multi-Agent Financial Research\n"
    )
    assert "https://github.com/TaeHyoK/Beyond-Data-Silos.git" in readme
    assert "docs/assets/multi_agent_financial_framework.png" in readme
    assert (ROOT / "docs/assets/multi_agent_financial_framework.png").is_file()
    assert not (ROOT / "docs/assets/pipeline_architecture.jpg").exists()
    assert not (ROOT / "docs/assets/multi_agent_financial_framework.jpg").exists()
    assert "redesigned" not in readme.lower()
    assert "paper-generation" not in readme
    assert "paper-collection" not in readme


def test_collection_manifest_uses_current_local_main():
    manifest = json.loads((ROOT / "ablation/run_config/collection_manifest.json").read_text())
    assert manifest["repository"] == {"path": ".", "ref": "main"}
    assert manifest["workspace"] == "."
    assert manifest["environment_file"] == "configs/.env"


def test_gitignore_excludes_generated_reports_and_results():
    ignore = (ROOT / ".gitignore").read_text().splitlines()
    for pattern in ("/final_reports*/", "/ablation/results/", "*.zip", "*.pem", "*.key"):
        assert pattern in ignore
