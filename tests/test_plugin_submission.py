"""Exercise the actual public ZIP boundary, independently of local install config."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / 'scripts' / 'build_plugin_submission.py'
SOURCE = ROOT / 'plugins' / 'buildbetter-codex'


def build(source, output):
    return subprocess.run([sys.executable, str(BUILDER), '--source', str(source),
                           '--output', str(output)], capture_output=True, text=True)


def test_submission_zip_is_installable_and_local_config_is_untouched(tmp_path):
    before = (SOURCE / '.mcp.json').read_bytes()
    output = tmp_path / 'buildbetter.zip'
    result = build(SOURCE, output)
    assert result.returncode == 0, result.stderr
    assert before == (SOURCE / '.mcp.json').read_bytes()
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read('.codex-plugin/plugin.json'))
        servers = json.loads(archive.read('.mcp.json'))['mcpServers']
        assert len(servers) == 1
        assert servers['buildbetter'] == {'url': 'https://mcp.buildbetter.app'}
        assert not any(n.startswith(('.git/', 'hooks/', 'scripts/')) for n in names)
        assert '.app.json' not in names
        interface = manifest['interface']
        assert len(interface['shortDescription']) <= 30
        assert len(interface['longDescription']) <= 4000
        assert len(interface['defaultPrompt']) <= 3
        assert all(len(p) <= 128 for p in interface['defaultPrompt'])
        for key in ('composerIcon', 'logo'):
            assert interface[key].removeprefix('./') in names
        for path in interface['screenshots']:
            assert path.removeprefix('./') in names
        ext = manifest['extensions']['com.openai']
        assert ext['onboardingSkill'].removeprefix('./') in names
        cases = ext['review']['test_cases']
        assert len(cases['positive']) == 5
        assert len(cases['negative']) == 3
        assert len([n for n in names if n.endswith('/SKILL.md')]) >= 8
    second = tmp_path / 'second.zip'
    assert build(SOURCE, second).returncode == 0
    assert output.read_bytes() == second.read_bytes()


@pytest.mark.parametrize('mutation', ['path', 'symlink', 'hooks', 'apps', 'credentials', 'prompts'])
def test_invalid_package_is_rejected_without_replacing_existing_output(tmp_path, mutation):
    source = tmp_path / 'source'
    shutil.copytree(SOURCE, source)
    manifest_path = source / '.codex-plugin' / 'plugin.json'
    manifest = json.loads(manifest_path.read_text())
    if mutation == 'path':
        manifest['interface']['logo'] = '../private.txt'
    elif mutation == 'symlink':
        secret = tmp_path / 'private.txt'
        secret.write_text('private fixture')
        (source / 'skills' / 'private.md').symlink_to(secret)
    elif mutation == 'hooks':
        manifest['hooks'] = './hooks/hooks.json'
    elif mutation == 'apps':
        manifest['apps'] = './.app.json'
    elif mutation == 'credentials':
        config_path = source / '.mcp.json'
        config = json.loads(config_path.read_text())
        config['mcp_servers']['buildbetter']['headers'] = {'Authorization': 'fixture'}
        config_path.write_text(json.dumps(config))
    else:
        manifest['interface']['defaultPrompt'] = ['Find feedback'] * 4
    manifest_path.write_text(json.dumps(manifest))
    output = tmp_path / 'previous.zip'
    output.write_bytes(b'previous artifact')
    result = build(source, output)
    assert result.returncode != 0
    assert output.read_bytes() == b'previous artifact'


@pytest.mark.parametrize('directory', ['skills/buildbetter-start/.private', 'assets/.cache'])
def test_hidden_directory_descendants_never_enter_zip(tmp_path, directory):
    source = tmp_path / 'source'
    shutil.copytree(SOURCE, source)
    private = source / directory
    private.mkdir(parents=True)
    (private / 'credentials.txt').write_text('private fixture')
    output = tmp_path / 'buildbetter.zip'
    result = build(source, output)
    assert result.returncode == 0, result.stderr
    with zipfile.ZipFile(output) as archive:
        assert not any(n.endswith('credentials.txt') for n in archive.namelist())


def test_mislabeled_screenshot_is_rejected(tmp_path):
    source = tmp_path / 'source'
    shutil.copytree(SOURCE, source)
    manifest = json.loads((source / '.codex-plugin/plugin.json').read_text())
    screenshot = source / manifest['interface']['screenshots'][0].removeprefix('./')
    screenshot.write_bytes(b'not an image')
    result = build(source, tmp_path / 'buildbetter.zip')
    assert result.returncode != 0


def test_portable_root_manifest_builds_without_workspace_extensions(tmp_path):
    source = tmp_path / 'source'
    shutil.copytree(SOURCE, source)
    manifest = source / '.codex-plugin/plugin.json'
    manifest.rename(source / 'plugin.json')
    result = build(source, tmp_path / 'buildbetter.zip')
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('kind,count', [('positive', 4), ('positive', 6), ('negative', 2), ('negative', 4)])
def test_submission_rejects_wrong_review_case_count(tmp_path, kind, count):
    source = tmp_path / 'source'
    shutil.copytree(SOURCE, source)
    path = source / '.codex-plugin/plugin.json'
    manifest = json.loads(path.read_text())
    cases = manifest['extensions']['com.openai']['review']['test_cases']
    cases[kind] = [cases[kind][0]] * count
    path.write_text(json.dumps(manifest))
    output = tmp_path / 'previous.zip'
    output.write_bytes(b'previous artifact')
    result = build(source, output)
    assert result.returncode != 0
    assert 'exactly' in result.stderr
    assert output.read_bytes() == b'previous artifact'
