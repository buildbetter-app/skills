"""Tests for packaged Codex plugins."""

import json
from pathlib import Path
import re

import yaml


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


def test_specialized_buildbetter_skills_are_portable_and_in_sync():
    codex_root = REPO_ROOT / "plugins" / "buildbetter-codex" / "skills"
    claude_root = REPO_ROOT / "plugins" / "buildbetter-claude" / "skills"
    codex_skills = {path.name for path in codex_root.iterdir() if path.is_dir()}
    claude_skills = {path.name for path in claude_root.iterdir() if path.is_dir()}

    assert codex_skills == claude_skills

    for skill_name in sorted(codex_skills - {"buildbetter"}):
        codex_dir = codex_root / skill_name
        claude_dir = claude_root / skill_name
        codex_files = {
            path.relative_to(codex_dir)
            for path in codex_dir.rglob("*")
            if path.is_file()
        }
        claude_files = {
            path.relative_to(claude_dir)
            for path in claude_dir.rglob("*")
            if path.is_file()
        }

        assert codex_files == claude_files
        for relative_path in codex_files:
            assert (codex_dir / relative_path).read_bytes() == (
                claude_dir / relative_path
            ).read_bytes()

        skill_text = (codex_dir / "SKILL.md").read_text()
        frontmatter_match = re.match(r"^---\n(.*?)\n---", skill_text, re.DOTALL)
        assert frontmatter_match
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        assert set(frontmatter) == {"name", "description"}
        assert frontmatter["name"] == skill_name
        portable_text = "\n".join(
            (codex_dir / relative_path).read_text()
            for relative_path in codex_files
            if relative_path.suffix in {".md", ".yaml", ".yml"}
        )
        assert not re.search(
            r"(?:/Users/|/home/|/private/|[A-Za-z]:\\Users\\)",
            portable_text,
        )
        emails = re.findall(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            portable_text,
            re.IGNORECASE,
        )
        assert all(email.lower().endswith("@example.com") for email in emails)
        assert not re.search(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            portable_text,
            re.IGNORECASE,
        )
        assert not re.search(
            r"\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
            r"\b\s*[:=]\s*[\"']?[A-Za-z0-9]",
            portable_text,
            re.IGNORECASE,
        )

        feature_scoped_or_mutating_tools = {
            "apply-smart-tag-setup",
            "attach-knowledge-gap-to-project",
            "enqueue-smart-tag-replay",
            "get-skill",
            "get-linear-ticket",
            "list-knowledge-gaps",
            "list-linear-projects",
            "list-linear-teams",
            "list-linear-tickets",
            "list-linear-workflow-states",
            "list-skills",
            "list-skillsets",
            "preview-smart-tag-classification",
            "preview-smart-tag-replay",
            "preview-smart-tag-setup",
            "promote-linear-tickets",
            "promote-triage-item",
            "propose-skill-update",
            "recheck-knowledge-gap",
            "review-knowledge-gap",
        }
        for tool_name in feature_scoped_or_mutating_tools:
            assert f"`{tool_name}`" not in portable_text
        assert "search-signals.query" not in portable_text
        assert '"page":' not in portable_text

        for reference in re.findall(r"`(references/[^`]+)`", skill_text):
            assert (codex_dir / reference).is_file()

        openai_yaml = yaml.safe_load((codex_dir / "agents" / "openai.yaml").read_text())
        interface = openai_yaml["interface"]
        assert 25 <= len(interface["short_description"]) <= 64
        assert f"${skill_name}" in interface["default_prompt"]
