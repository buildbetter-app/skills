"""Validate the generated distribution boundary, including stale skill detection."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'plugins' / 'buildbetter-grok'


def test_grok_package_matches_maintained_workflows():
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--check'],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert len(list((PACKAGE / 'skills').glob('*/SKILL.md'))) == 9


def test_grok_package_uses_client_managed_auth_and_public_endpoint():
    manifest = json.loads((PACKAGE / 'plugin.json').read_text())
    assert manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    config = json.loads((PACKAGE / 'mcp.json').read_text())
    assert config['mcpServers'] == {
        'buildbetter': {'type': 'streamable-http', 'url': 'https://mcp.buildbetter.app'}
    }
    assert not any((PACKAGE / name).exists() for name in ('hooks', '.app.json'))
    marketplace = json.loads((ROOT / '.cursor-plugin' / 'marketplace.json').read_text())
    assert marketplace['plugins'][0]['source'] == './plugins/buildbetter-grok'
    foundation = (PACKAGE / 'skills' / 'buildbetter' / 'SKILL.md').read_text()
    assert 'OAuth' in foundation
    assert 'never ask for credentials in chat' in foundation


def test_grok_check_detects_modified_generated_skill(tmp_path):
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path)],
        check=True,
    )
    skill = tmp_path / 'skills' / 'buildbetter-start' / 'SKILL.md'
    skill.write_text(skill.read_text() + '\nUnmaintained edit\n')
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path), '--check'],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert 'buildbetter-start/SKILL.md' in result.stderr
