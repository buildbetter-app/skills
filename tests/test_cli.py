"""Tests for bb-skills CLI."""

import json
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bb_skills_cli.manifest import Manifest


class TestManifest:
    def test_load_missing_file(self, tmp_path):
        m = Manifest(tmp_path / "manifest.json")
        assert m.version is None
        assert m.packs == {}
        assert m.platforms == []

    def test_save_and_load(self, tmp_path):
        path = tmp_path / "manifest.json"
        m = Manifest(path)
        m.version = "1.0.0"
        m.packs = {"testing": {"skills": ["app-navigator", "trust-but-verify"]}}
        m.platforms = ["claude", "codex"]
        m.save()

        loaded = Manifest(path)
        assert loaded.version == "1.0.0"
        assert loaded.packs == {"testing": {"skills": ["app-navigator", "trust-but-verify"]}}
        assert loaded.platforms == ["claude", "codex"]

    def test_add_pack(self, tmp_path):
        m = Manifest(tmp_path / "manifest.json")
        m.add_pack("testing", ["app-navigator", "trust-but-verify"])
        assert "testing" in m.packs
        assert m.packs["testing"]["skills"] == ["app-navigator", "trust-but-verify"]

    def test_remove_pack(self, tmp_path):
        m = Manifest(tmp_path / "manifest.json")
        m.add_pack("testing", ["app-navigator"])
        m.remove_pack("testing")
        assert "testing" not in m.packs

    def test_remove_nonexistent_pack(self, tmp_path):
        m = Manifest(tmp_path / "manifest.json")
        m.remove_pack("nope")  # Should not raise

    def test_has_skill(self, tmp_path):
        m = Manifest(tmp_path / "manifest.json")
        m.add_pack("testing", ["app-navigator", "trust-but-verify"])
        assert m.has_skill("app-navigator") is True
        assert m.has_skill("nonexistent") is False

    def test_default_path(self):
        m = Manifest()
        assert m.path == Path.home() / ".bb-skills" / "manifest.json"


from typer.testing import CliRunner
from bb_skills_cli import create_app

runner = CliRunner()


class TestCLIList:
    def test_list_available(self, tmp_path):
        app = create_app(skills_dir=tmp_path)
        pack_dir = tmp_path / "testing"
        pack_dir.mkdir()
        (pack_dir / "pack.yml").write_text(
            "name: testing\ndisplay_name: Browser Testing\n"
            "description: Test skills\nversion: 1.0.0\n"
            "skills:\n  - app-navigator\ndependencies: []\n"
        )
        skill_dir = pack_dir / "app-navigator"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: app-navigator\ndescription: Map app\n---\n\n# Nav")

        result = runner.invoke(app, ["list", "--available"])
        assert result.exit_code == 0
        assert "testing" in result.output
        assert "app-navigator" in result.output


class TestCLIPlatforms:
    def test_platforms_command(self):
        app = create_app()
        result = runner.invoke(app, ["platforms"])
        assert result.exit_code == 0
        assert "Platform" in result.output or "Claude" in result.output


class TestCLIMcpConfiguration:
    def test_install_skips_mcp_prompt_when_stdin_non_interactive(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Manifest, "DEFAULT_PATH", tmp_path / ".bb-skills" / "manifest.json")
        skills_dir = tmp_path / "skills"

        core_dir = skills_dir / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "pack.yml").write_text(
            "name: core\n"
            "display_name: Core\n"
            "description: Core skills\n"
            "version: 1.0.0\n"
            "skills:\n"
            "  - bb-skills-update\n"
            "dependencies: []\n"
        )
        core_skill_dir = core_dir / "bb-skills-update"
        core_skill_dir.mkdir()
        (core_skill_dir / "SKILL.md").write_text(
            "---\nname: bb-skills-update\ndescription: Update skills\n---\n\n# Update"
        )

        testing_dir = skills_dir / "testing"
        testing_dir.mkdir()
        (testing_dir / "pack.yml").write_text(
            "name: testing\n"
            "display_name: Browser Testing\n"
            "description: Test skills\n"
            "version: 1.0.0\n"
            "skills:\n"
            "  - app-navigator\n"
            "dependencies:\n"
            "  - core\n"
            "mcp_servers:\n"
            "  playwright:\n"
            "    command: npx\n"
            "    args: ['@playwright/mcp@0.0.75']\n"
        )
        skill_dir = testing_dir / "app-navigator"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: app-navigator\ndescription: Map app\n---\n\n# Nav"
        )

        app = create_app(skills_dir=skills_dir)
        result = runner.invoke(app, ["install", "testing", "--platform", "claude"], env={"HOME": str(tmp_path)})

        assert result.exit_code == 0
        assert "stdin is non-interactive" in result.output
        assert not (tmp_path / ".claude" / "settings.json").exists()
