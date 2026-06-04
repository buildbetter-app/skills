"""Tests for packaged Codex plugins."""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_PLUGIN_DIRS = [
    REPO_ROOT / "plugins" / "bb-skills",
    REPO_ROOT / "plugins" / "buildbetter-codex",
]


def test_codex_plugin_mcp_files_use_codex_server_wrapper():
    for plugin_dir in CODEX_PLUGIN_DIRS:
        manifest = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text())
        assert manifest["mcpServers"] == "./.mcp.json"

        mcp_config = json.loads((plugin_dir / ".mcp.json").read_text())
        assert "mcpServers" not in mcp_config
        assert isinstance(mcp_config.get("mcp_servers"), dict)
        assert mcp_config["mcp_servers"]
