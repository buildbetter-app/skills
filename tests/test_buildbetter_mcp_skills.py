"""Tests for BuildBetter MCP skill guidance."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOTS = [
    REPO_ROOT / "plugins" / "buildbetter-codex",
    REPO_ROOT / "plugins" / "buildbetter-claude",
]
BUILDBETTER_SKILL_NAMES = [
    "buildbetter",
    "buildbetter-customer-voice",
    "buildbetter-mcp-research",
]

CURRENT_MCP_TOOLS = {
    "build-query",
    "find-fields",
    "get-call",
    "get-call-transcript",
    "get-document",
    "get-folder",
    "get-knowledge-page",
    "get-linear-ticket",
    "get-project",
    "get-skill",
    "get-triage-item",
    "get-list-extractions-schema",
    "list-extraction-filter-fields",
    "list-extractions",
    "list-knowledge-pages",
    "list-linear-projects",
    "list-linear-teams",
    "list-linear-tickets",
    "list-linear-workflow-states",
    "list-project-types",
    "list-projects",
    "list-signal-properties",
    "list-signal-types",
    "list-skills",
    "list-skillsets",
    "list-triage-items",
    "promote-linear-tickets",
    "promote-triage-item",
    "propose-skill-update",
    "run-query",
    "search-calls",
    "search-documents",
    "search-extractions",
    "search-knowledge-pages",
    "search-people",
    "search-people-properties",
    "search-signal-property-values",
    "search-signals",
    "triage-count",
}


def _buildbetter_markdown_files() -> list[Path]:
    markdown_files: list[Path] = []
    for plugin_root in PLUGIN_ROOTS:
        skill_root = plugin_root / "skills"
        for skill_name in BUILDBETTER_SKILL_NAMES:
            skill_dir = skill_root / skill_name
            markdown_files.extend(sorted(skill_dir.rglob("*.md")))
    return markdown_files


def test_buildbetter_skill_json_examples_parse() -> None:
    for markdown_file in _buildbetter_markdown_files():
        text = markdown_file.read_text(encoding="utf-8")
        for match in re.finditer(r"```json\s*\n(.*?)\n```", text, re.DOTALL):
            json.loads(match.group(1))


def test_buildbetter_mcp_research_documents_current_tool_surface() -> None:
    for plugin_root in PLUGIN_ROOTS:
        skill_dir = plugin_root / "skills" / "buildbetter-mcp-research"
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(skill_dir.rglob("*.md"))
        )

        missing = sorted(tool for tool in CURRENT_MCP_TOOLS if f"`{tool}`" not in docs)
        assert missing == []


def test_buildbetter_mcp_research_prioritizes_domain_tools() -> None:
    for plugin_root in PLUGIN_ROOTS:
        skill_text = (
            plugin_root
            / "skills"
            / "buildbetter-mcp-research"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        assert "Use BuildBetter domain tools first" in skill_text
        assert "Use GraphQL helpers and `run-query` only" in skill_text
        assert "Mutating tools require explicit user approval" in skill_text


def test_buildbetter_customer_voice_guardrails_are_documented() -> None:
    for plugin_root in PLUGIN_ROOTS:
        skill_text = (
            plugin_root
            / "skills"
            / "buildbetter-customer-voice"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        assert "person.boundary: external" in skill_text
        assert "Do not treat `customerInsight` as direct customer voice by default" in skill_text
        assert "byte-identical results" in skill_text
        assert '"exactQuote": { "contains": "pricing" }' in skill_text


def test_buildbetter_customer_voice_and_mcp_research_stay_in_plugin_parity() -> None:
    for skill_name in ("buildbetter-customer-voice", "buildbetter-mcp-research"):
        codex_dir = (
            REPO_ROOT
            / "plugins"
            / "buildbetter-codex"
            / "skills"
            / skill_name
        )
        claude_dir = (
            REPO_ROOT
            / "plugins"
            / "buildbetter-claude"
            / "skills"
            / skill_name
        )

        codex_files = {
            path.relative_to(codex_dir): path.read_text(encoding="utf-8")
            for path in sorted(codex_dir.rglob("*"))
            if path.is_file()
        }
        claude_files = {
            path.relative_to(claude_dir): path.read_text(encoding="utf-8")
            for path in sorted(claude_dir.rglob("*"))
            if path.is_file()
        }

        assert codex_files == claude_files
