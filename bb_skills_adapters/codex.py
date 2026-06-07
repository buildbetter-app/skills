"""Codex CLI adapter — SKILL.md passthrough with multi-file support."""

import json
import os
import re
import sys
import tomllib
from pathlib import Path

from bb_skills_adapters.base import BaseAdapter


_BARE_TOML_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _toml_key(key: str) -> str:
    if _BARE_TOML_KEY_RE.match(key):
        return key
    return json.dumps(key)


def _toml_value(value) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    return json.dumps(str(value))


class CodexAdapter(BaseAdapter):
    @property
    def name(self) -> str:
        return "codex"

    @property
    def display_name(self) -> str:
        return "Codex CLI"

    def convert(self, skill_content: str, supporting_files: dict[str, str]) -> dict[str, str]:
        result = {"SKILL.md": skill_content}
        result.update(supporting_files)
        return result

    def install_path(self, skill_name: str) -> Path:
        return Path.home() / ".codex" / "skills" / skill_name

    def is_available(self) -> bool:
        return (Path.home() / ".codex").is_dir()

    @property
    def supports_slash_commands(self) -> bool:
        return True

    @property
    def supports_multi_file(self) -> bool:
        return True

    def config_path(self) -> Path:
        return Path.home() / ".codex" / "config.toml"

    def _load_config(self) -> dict:
        path = self.config_path()
        if not path.exists():
            return {}
        try:
            config = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as error:
            print(
                f"Warning: Could not parse {path}: {error}. "
                "Treating Codex MCP config as empty for detection.",
                file=sys.stderr,
            )
            return {}
        if not isinstance(config, dict):
            print(
                f"Warning: {path} does not contain a TOML table. "
                "Treating Codex MCP config as empty for detection.",
                file=sys.stderr,
            )
            return {}
        return config

    def _mcp_servers(self, config: dict) -> dict:
        existing = config.get("mcp_servers", {})
        if isinstance(existing, dict):
            return existing
        print(
            "Warning: Codex MCP server config is not a TOML table. "
            "Treating it as empty for MCP detection.",
            file=sys.stderr,
        )
        return {}

    def get_missing_mcp_servers(self, required: dict[str, dict]) -> dict[str, dict]:
        config = self._load_config()
        existing = self._mcp_servers(config)
        return {name: server for name, server in required.items() if name not in existing}

    def add_mcp_servers(self, servers: dict[str, dict]) -> None:
        config = self._load_config()
        existing = self._mcp_servers(config)
        missing = {name: server for name, server in servers.items() if name not in existing}
        if not missing:
            return

        path = self.config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        existed = path.exists()
        text = ""
        if existed:
            text = path.read_text(encoding="utf-8")
            try:
                parsed = tomllib.loads(text)
            except tomllib.TOMLDecodeError as error:
                print(
                    f"Warning: Could not parse {path}: {error}. "
                    "Replacing Codex config with MCP server config.",
                    file=sys.stderr,
                )
                text = ""
            else:
                parsed_mcp_servers = parsed.get("mcp_servers", {})
                if not isinstance(parsed_mcp_servers, dict):
                    print(
                        "Warning: Codex MCP server config is not a TOML table. "
                        "Replacing Codex config with MCP server config.",
                        file=sys.stderr,
                    )
                    text = ""
        if text and not text.endswith("\n"):
            text += "\n"

        for name, server in missing.items():
            text += f"\n[mcp_servers.{_toml_key(name)}]\n"
            nested_sections = {}
            for key, value in server.items():
                if isinstance(value, dict):
                    nested_sections[key] = value
                    continue
                text += f"{_toml_key(key)} = {_toml_value(value)}\n"
            for key, values in nested_sections.items():
                text += f"\n[mcp_servers.{_toml_key(name)}.{_toml_key(key)}]\n"
                for nested_key, nested_value in values.items():
                    text += f"{_toml_key(nested_key)} = {_toml_value(nested_value)}\n"

        path.write_text(text, encoding="utf-8")
        if not existed and os.name != "nt":
            path.chmod(0o600)
