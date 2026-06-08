"""Codex CLI adapter — SKILL.md passthrough with multi-file support."""

import json
import os
import re
import sys
import tomllib
from pathlib import Path

from bb_skills_adapters.base import BaseAdapter


_BARE_TOML_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_TOML_TABLE_RE = re.compile(r"^\s*\[([^\]]+)\]\s*(?:#.*)?$")
_TOML_KEY_PART = r'(?:"[^"]+"|[A-Za-z0-9_-]+)'
_TOML_ASSIGNMENT_RE = re.compile(rf"^\s*({_TOML_KEY_PART}(?:\s*\.\s*{_TOML_KEY_PART})*)\s*=")


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


def _split_toml_path(path: str) -> tuple[str, ...]:
    parts = []
    current = []
    in_quote = False
    escaped = False
    for char in path:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\" and in_quote:
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if char == "." and not in_quote:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    parts.append("".join(current).strip())
    return tuple(part for part in parts if part)


def _toml_table_path(line: str) -> tuple[str, ...] | None:
    match = _TOML_TABLE_RE.match(line)
    if not match:
        return None
    return _split_toml_path(match.group(1))


def _toml_assignment_path(line: str) -> tuple[str, ...] | None:
    match = _TOML_ASSIGNMENT_RE.match(line)
    if not match:
        return None
    return _split_toml_path(match.group(1))


def _remove_malformed_mcp_config(
    text: str,
    malformed_server_names: set[str],
    remove_top_level_mcp_servers: bool,
) -> str:
    lines: list[str] = []
    current_table: tuple[str, ...] = ()
    skipping_malformed_server_section = False

    for line in text.splitlines(keepends=True):
        table_path = _toml_table_path(line)
        if table_path is not None:
            current_table = table_path
            skipping_malformed_server_section = (
                len(table_path) >= 2
                and table_path[0] == "mcp_servers"
                and table_path[1] in malformed_server_names
            )
            if skipping_malformed_server_section:
                continue
            lines.append(line)
            continue

        if skipping_malformed_server_section:
            continue

        assignment_path = _toml_assignment_path(line)
        if assignment_path is None:
            lines.append(line)
            continue

        if assignment_path == ("mcp_servers",) and current_table == () and remove_top_level_mcp_servers:
            continue
        if assignment_path[0] in malformed_server_names and current_table == ("mcp_servers",):
            continue
        if (
            len(assignment_path) >= 2
            and assignment_path[0] == "mcp_servers"
            and assignment_path[1] in malformed_server_names
            and current_table == ()
        ):
            continue

        lines.append(line)

    return "".join(lines)


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

    def _mcp_server_is_configured(self, name: str, server: object) -> bool:
        if not isinstance(server, dict):
            print(
                f"Warning: Codex MCP server '{name}' config is not a TOML table. "
                "Treating it as missing.",
                file=sys.stderr,
            )
            return False
        if not isinstance(server.get("command"), str) and not isinstance(server.get("url"), str):
            print(
                f"Warning: Codex MCP server '{name}' config does not define command or url. "
                "Treating it as missing.",
                file=sys.stderr,
            )
            return False
        return True

    def get_missing_mcp_servers(self, required: dict[str, dict]) -> dict[str, dict]:
        config = self._load_config()
        existing = self._mcp_servers(config)
        return {
            name: server
            for name, server in required.items()
            if name not in existing or not self._mcp_server_is_configured(name, existing[name])
        }

    def add_mcp_servers(self, servers: dict[str, dict]) -> None:
        config = self._load_config()
        existing = self._mcp_servers(config)
        missing = {
            name: server
            for name, server in servers.items()
            if name not in existing or not self._mcp_server_is_configured(name, existing[name])
        }
        if not missing:
            return
        malformed_server_names = {name for name in missing if name in existing}
        remove_top_level_mcp_servers = not isinstance(config.get("mcp_servers", {}), dict)

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
                        "Replacing only the malformed MCP server config.",
                        file=sys.stderr,
                    )
                    remove_top_level_mcp_servers = True
                text = _remove_malformed_mcp_config(
                    text,
                    malformed_server_names,
                    remove_top_level_mcp_servers,
                )
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
