"""Exercise real archives, cross-file references and publisher-input failures."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import uuid
import zipfile
import zlib

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/build_mcp_distribution.py'


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


def icon(path, side):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'
                     + chunk(b'IHDR', struct.pack('>IIBBBBB', side, side, 8, 6, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress((b'\0' + b'\xff\xff\xff\0' * side) * side))
                     + chunk(b'IEND', b''))
    return path


def copilot_args(tmp_path):
    return ['--copilot-app-id', str(uuid.uuid4()),
            '--copilot-oauth-reference-id', 'fixture-vault-registration',
            '--copilot-color-icon', icon(tmp_path / 'color.png', 192),
            '--copilot-outline-icon', icon(tmp_path / 'outline.png', 32)]


def test_kit_is_reproducible_and_uses_only_public_packages(tmp_path):
    outputs = [tmp_path / 'one.zip', tmp_path / 'two.zip']
    for output in outputs:
        result = run('--output', output)
        assert result.returncode == 0, result.stderr
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    with zipfile.ZipFile(outputs[0]) as archive:
        names = archive.namelist()
        assert 'server.json' in names
        assert 'distribution/APPLICATIONS.md' in names
        assert '.cursor-plugin/marketplace.json' in names
        assert 'plugins/buildbetter-grok/plugin.json' in names
        assert 'distribution/microsoft365/ai-plugin.template.json' in names
        assert not any(name.endswith('manifest.json') for name in names)
        assert not any('/hooks/' in name or '/.git/' in name for name in names)
        assert not any('buildbetter-codex' in name for name in names)
        registry = json.loads(archive.read('server.json'))
        assert registry['remotes'] == [{'type': 'streamable-http', 'url': 'https://mcp.buildbetter.app'}]
        assert 'packages' not in registry
        config = json.loads(archive.read('plugins/buildbetter-grok/mcp.json'))
        assert config['mcpServers']['buildbetter'] == {
            'type': 'streamable-http', 'url': 'https://mcp.buildbetter.app'}


def test_google_console_copy_meets_published_field_requirements():
    listing = json.loads((ROOT / 'distribution/google/listing.json').read_text())
    assert len(listing['description'].split()) < 30
    assert len(listing['capabilities']) >= 3
    prompts = listing['example_prompts']
    assert len(prompts) >= 3
    assert sum(prompt.startswith('@BuildBetter') for prompt in prompts) >= 2
    assert any('BuildBetter' in prompt and not prompt.startswith('@BuildBetter')
               for prompt in prompts)


def test_copilot_zip_has_registered_oauth_and_working_cross_file_references(tmp_path):
    args = copilot_args(tmp_path)
    outputs = [tmp_path / 'copilot.zip', tmp_path / 'again.zip']
    for output in outputs:
        result = run('--copilot', '--output', output, *args)
        assert result.returncode == 0, result.stderr
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    with zipfile.ZipFile(outputs[0]) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        agent = json.loads(archive.read(manifest['copilotAgents']['declarativeAgents'][0]['file']))
        action = json.loads(archive.read(agent['actions'][0]['file']))
        assert manifest['id'] == args[1]
        assert 0 < len(manifest['description']['short']) <= 80
        runtime = action['runtimes'][0]
        assert runtime['auth'] == {'type': 'OAuthPluginVault', 'reference_id': args[3]}
        assert runtime['spec']['url'] == 'https://mcp.buildbetter.app'
        assert action['functions'] == []
        assert runtime['run_for_functions'] == ['*']
        assert manifest['icons'] == {'color': 'color.png', 'outline': 'outline.png'}
        assert set(archive.namelist()) == {'manifest.json', 'declarativeAgent.json',
                                           'ai-plugin.json', 'color.png', 'outline.png'}


@pytest.mark.parametrize('mutation', ['missing', 'bad-id', 'bad-reference', 'wrong-icon', 'truncated-icon'])
def test_bad_inputs_preserve_previous_archive(tmp_path, mutation):
    output = tmp_path / 'previous.zip'
    output.write_bytes(b'previous archive')
    args = copilot_args(tmp_path)
    if mutation == 'missing':
        args = []
    elif mutation == 'bad-id':
        args[1] = 'NOT-REGISTERED'
    elif mutation == 'bad-reference':
        args[3] = 'Bearer private-token'
    elif mutation == 'wrong-icon':
        icon(tmp_path / 'color.png', 512)
    else:
        (tmp_path / 'color.png').write_bytes(b'\x89PNG\r\n\x1a\n')
    assert run('--copilot', '--output', output, *args).returncode != 0
    assert output.read_bytes() == b'previous archive'


def test_registration_options_are_never_silently_ignored(tmp_path):
    output = tmp_path / 'kit.zip'
    assert run('--output', output, *copilot_args(tmp_path)).returncode != 0
    assert not output.exists()


def test_symlink_output_and_icon_cannot_modify_other_files(tmp_path):
    target = tmp_path / 'untouched'
    target.write_bytes(b'keep')
    link = tmp_path / 'output.zip'
    link.symlink_to(target)
    assert run('--output', link).returncode != 0
    assert target.read_bytes() == b'keep'
    args = copilot_args(tmp_path)
    (tmp_path / 'color.png').unlink()
    (tmp_path / 'color.png').symlink_to(tmp_path / 'outline.png')
    assert run('--copilot', '--output', tmp_path / 'no.zip', *args).returncode != 0


def test_public_source_symlink_is_rejected(tmp_path):
    spec = importlib.util.spec_from_file_location('distribution_builder', SCRIPT)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    source = tmp_path / 'private'
    source.write_bytes(b'private')
    link = tmp_path / 'public.json'
    link.symlink_to(source)
    with pytest.raises(ValueError, match='symlink'):
        builder.read_public(link)
