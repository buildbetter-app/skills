"""Validate the generated distribution boundary, including stale skill detection."""
import json
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'plugins' / 'buildbetter-grok'


def load_generator():
    spec = importlib.util.spec_from_file_location('grok_generator', ROOT / 'scripts' / 'build_grok_plugin.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_regeneration_handles_file_directory_replacements(tmp_path):
    command = [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path)]
    subprocess.run(command, check=True)
    workflow = tmp_path / 'skills' / 'buildbetter-start'
    shutil.rmtree(workflow)
    workflow.write_bytes(b'former file')
    config = tmp_path / 'mcp.cursor.json'
    config.unlink()
    config.mkdir()
    (config / 'retired.txt').write_bytes(b'former directory')
    subprocess.run(command, check=True)
    assert (workflow / 'SKILL.md').is_file()
    assert json.loads(config.read_text())['mcpServers']['buildbetter']['url'] == 'https://mcp.buildbetter.app'
    subprocess.run(command + ['--check'], check=True)


@pytest.mark.parametrize('broken', [False, True])
def test_source_directory_and_broken_symlinks_are_rejected(tmp_path, broken):
    generator = load_generator()
    source = tmp_path / 'source'
    shutil.copytree(generator.SOURCE, source)
    target = tmp_path / 'target'
    if not broken:
        target.mkdir()
        (target / 'SKILL.md').write_text('linked workflow')
    (source / 'skills' / 'linked-workflow').symlink_to(target, target_is_directory=True)
    generator.SOURCE = source
    with pytest.raises(ValueError, match='symlinks'):
        generator.files()


def test_binary_skill_assets_are_preserved_and_markdown_is_rewritten(tmp_path):
    generator = load_generator()
    source = tmp_path / 'source'
    shutil.copytree(generator.SOURCE, source)
    resources = source / 'skills' / 'buildbetter-start' / 'references'
    resources.mkdir(exist_ok=True)
    payload = b'\x89PNG\r\n\x1a\n\xff$buildbetter-start'
    (resources / 'fixture.png').write_bytes(payload)
    (resources / 'guide.md').write_text('Use $buildbetter-start')
    generator.SOURCE = source
    generated = generator.files()
    assert generated['skills/buildbetter-start/references/fixture.png'] == payload
    assert generated['skills/buildbetter-start/references/guide.md'] == b'Use buildbetter-start'


@pytest.mark.parametrize('marker', [None, 'not a BuildBetter generated directory'])
def test_generator_refuses_unowned_output_without_mutating_files(tmp_path, marker):
    unrelated = tmp_path / 'another-plugin' / 'private.txt'
    unrelated.parent.mkdir()
    unrelated.write_text('unpublished work')
    if marker is not None:
        (tmp_path / '.buildbetter-grok-generated').write_text(marker)
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert 'empty or marked' in result.stderr
    assert before == {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_generated_cursor_author_matches_closed_host_contract(tmp_path):
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path)],
        check=True,
    )
    cursor = json.loads((tmp_path / '.cursor-plugin' / 'plugin.json').read_text())
    portable = json.loads((tmp_path / 'plugin.json').read_text())
    assert cursor['author'] == {'name': 'BuildBetter', 'email': 'eng@buildbetter.app'}
    assert 'url' in portable['author']
    assert cursor['homepage'] == portable['homepage']


def test_regeneration_removes_obsolete_files_and_preserves_readme(tmp_path):
    command = [sys.executable, str(ROOT / 'scripts' / 'build_grok_plugin.py'), '--output', str(tmp_path)]
    subprocess.run(command, check=True)
    obsolete = tmp_path / 'skills' / 'retired' / 'SKILL.md'
    obsolete.parent.mkdir()
    obsolete.write_text('retired workflow')
    support = tmp_path / 'assets' / 'retired.txt'
    support.write_text('retired support file')
    readme = tmp_path / 'README.md'
    readme.write_text('hand-authored documentation')
    subprocess.run(command, check=True)
    assert not obsolete.exists()
    assert not support.exists()
    assert readme.read_text() == 'hand-authored documentation'
    subprocess.run(command + ['--check'], check=True)


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
