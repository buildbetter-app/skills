"""Tests for packaged Codex plugins."""

import json
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_PLUGIN_DIRS = [
    REPO_ROOT / "plugins" / "skills",
    REPO_ROOT / "plugins" / "buildbetter-codex",
]
SUBMISSION_DOCS = [
    REPO_ROOT / "docs" / "plugin-submission" / "overview.md",
    REPO_ROOT / "docs" / "plugin-submission" / "hero-prompts.md",
    REPO_ROOT / "docs" / "plugin-submission" / "eval-plan.md",
    REPO_ROOT / "docs" / "plugin-submission" / "review-account.md",
    REPO_ROOT / "docs" / "plugin-submission" / "tool-audit.md",
    REPO_ROOT / "docs" / "plugin-submission" / "install-smoke-test.md",
    REPO_ROOT / "docs" / "plugin-submission" / "submission-checklist.md",
]


def test_codex_plugin_mcp_files_use_codex_server_wrapper():
    for plugin_dir in CODEX_PLUGIN_DIRS:
        manifest = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text())
        assert manifest["mcpServers"] == "./.mcp.json"

        mcp_config = json.loads((plugin_dir / ".mcp.json").read_text())
        assert "mcpServers" not in mcp_config
        assert isinstance(mcp_config.get("mcp_servers"), dict)
        assert mcp_config["mcp_servers"]


def test_codex_plugin_manifest_assets_exist():
    for plugin_dir in CODEX_PLUGIN_DIRS:
        manifest = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text())
        interface = manifest["interface"]

        for field in ("composerIcon", "logo"):
            asset_path = plugin_dir / interface[field]
            assert asset_path.exists(), f"{manifest['name']} missing {field}: {asset_path}"

        assert interface["screenshots"], f"{manifest['name']} should include listing screenshots"
        for screenshot in interface["screenshots"]:
            screenshot_path = plugin_dir / screenshot
            assert screenshot_path.exists(), (
                f"{manifest['name']} missing screenshot: {screenshot_path}"
            )


def test_hosted_codex_install_commands_include_all_sparse_paths():
    expected_sparse_paths = {
        "--sparse .agents/plugins",
        "--sparse plugins/skills",
        "--sparse plugins/buildbetter-codex",
    }
    docs = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "plugins" / "README.md",
        REPO_ROOT / "plugins" / "buildbetter-codex" / "README.md",
        REPO_ROOT / "plugins" / "buildbetter-codex" / "skills" / "buildbetter" / "SKILL.md",
        REPO_ROOT / "docs" / "plugin-submission" / "overview.md",
        REPO_ROOT / "docs" / "plugin-submission" / "install-smoke-test.md",
    ]

    for doc in docs:
        text = doc.read_text()
        commands = re.findall(r"codex plugin marketplace add buildbetter-app/skills[^\n]+", text)
        assert commands, f"{doc} should document hosted Codex marketplace install"
        for command in commands:
            for sparse_path in expected_sparse_paths:
                assert sparse_path in command, f"{doc} command missing {sparse_path}"


def test_submission_dossier_and_eval_cases_are_complete():
    for doc in SUBMISSION_DOCS:
        assert doc.exists(), f"Missing submission doc: {doc}"
        assert doc.read_text().strip(), f"Submission doc is empty: {doc}"

    cases = json.loads((REPO_ROOT / "evals" / "plugin-submission" / "hero-cases.json").read_text())
    assert len(cases) >= 8

    required_fields = {
        "id",
        "plugin",
        "prompt",
        "expected_output",
        "required_facts",
        "expected_tool_path",
        "safety_behavior",
        "fixture_state",
        "grading_criteria",
    }
    case_ids = set()
    for case in cases:
        assert required_fields <= case.keys()
        assert case["id"] not in case_ids
        case_ids.add(case["id"])
        assert case["prompt"]
        assert case["grading_criteria"]
        assert isinstance(case["required_facts"], list)
        assert isinstance(case["expected_tool_path"], list)

    assert any(case["plugin"] == "none" for case in cases)
