#!/usr/bin/env python3
"""Build a reproducible public plugin ZIP without exporting local configuration."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
from urllib.parse import urlsplit
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LOCAL_SERVER_FIELDS = {'title', 'description', 'url', 'oauth_resource',
                       'startup_timeout_sec', 'tool_timeout_sec'}


def public_url(value):
    if not isinstance(value, str):
        raise ValueError('Public URL must be a string')
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment):
        raise ValueError('Public URLs must be credential-free HTTPS URLs')
    return value


def package_path(value):
    if not isinstance(value, str) or not value.startswith('./') or '\\' in value:
        raise ValueError('Package references must use ./ relative paths')
    path = PurePosixPath(value[2:])
    if '..' in path.parts or not path.parts or path.is_absolute():
        raise ValueError('Package reference escapes the plugin')
    return path.as_posix()


def validate_image(name, content):
    suffix = PurePosixPath(name).suffix.lower()
    if suffix == '.svg':
        try:
            root = ET.fromstring(content)
        except ET.ParseError as error:
            raise ValueError(f'Invalid SVG asset: {name}') from error
        if root.tag not in ('svg', '{http://www.w3.org/2000/svg}svg'):
            raise ValueError(f'Invalid SVG asset: {name}')
    elif suffix == '.png':
        if not content.startswith(b'\x89PNG\r\n\x1a\n') or content[12:16] != b'IHDR':
            raise ValueError(f'Invalid PNG asset: {name}')
    elif suffix in ('.jpg', '.jpeg'):
        if not content.startswith(b'\xff\xd8\xff') or not content.endswith(b'\xff\xd9'):
            raise ValueError(f'Invalid JPEG asset: {name}')
    elif suffix == '.webp':
        if content[:4] != b'RIFF' or content[8:12] != b'WEBP':
            raise ValueError(f'Invalid WebP asset: {name}')
    else:
        raise ValueError(f'Unsupported image asset: {name}')


def payloads(source):
    source = source.resolve()
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Symlinks are not allowed in the public package source')
    manifest_path = source / 'plugin.json'
    if not manifest_path.is_file():
        manifest_path = source / '.codex-plugin' / 'plugin.json'
    manifest = json.loads(manifest_path.read_text())
    if any(k in manifest for k in ('apps', 'hooks')) or (source / '.app.json').exists():
        raise ValueError('Public submission does not support app references or lifecycle hooks')
    if (source / 'hooks').exists():
        raise ValueError('Public submission does not support lifecycle hooks')
    if manifest.get('mcpServers') != './.mcp.json' or manifest.get('skills') != './skills/':
        raise ValueError('Expected the maintained skills directory and MCP configuration')
    interface = manifest['interface']
    for key, maximum in (('shortDescription', 30), ('longDescription', 4000)):
        if not isinstance(interface.get(key), str) or not 0 < len(interface[key]) <= maximum:
            raise ValueError(f'{key} must contain 1–{maximum} characters')
    prompts = interface['defaultPrompt']
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError('Submission requires one to three starter prompts')
    if any(not isinstance(p, str) or not 0 < len(p) <= 128 for p in prompts):
        raise ValueError('Starter prompts must contain 1–128 characters')
    for key in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        public_url(interface[key])
    ext = manifest['extensions']['com.openai']
    cases = ext['review']['test_cases']
    for kind, required in (('positive', 5), ('negative', 3)):
        if not isinstance(cases.get(kind), list) or len(cases[kind]) != required:
            raise ValueError(f'Review needs exactly {required} {kind} cases')
        for case in cases[kind]:
            if not all(isinstance(case.get(k), str) and case[k].strip()
                       for k in ('description', 'prompt', 'expected_behavior')):
                raise ValueError('Review cases require a prompt and expected behavior')
    config = json.loads((source / '.mcp.json').read_text())
    servers = config.get('mcp_servers', config.get('mcpServers'))
    if not isinstance(servers, dict) or len(servers) != 1:
        raise ValueError('Submission connects exactly one MCP server')
    normalized = {}
    for name, server in servers.items():
        if not isinstance(server, dict) or set(server) - LOCAL_SERVER_FIELDS:
            raise ValueError('Remote MCP config contains unsupported or private fields')
        normalized[name] = {'url': public_url(server['url'])}
    manifest_bytes = (json.dumps(manifest, indent=2) + '\n').encode()
    files = {
        'plugin.json': manifest_bytes,
        '.codex-plugin/plugin.json': manifest_bytes,
        '.mcp.json': (json.dumps({'mcpServers': normalized}, indent=2) + '\n').encode(),
    }
    for directory in ('skills', 'assets'):
        for path in sorted((source / directory).rglob('*')):
            if path.is_file():
                if any(part.startswith('.') or part == '__pycache__'
                       for part in path.relative_to(source).parts):
                    continue
                files[path.relative_to(source).as_posix()] = path.read_bytes()
    refs = [interface['composerIcon'], interface['logo'], ext['onboardingSkill'],
            *interface['screenshots']]
    for ref in refs:
        if package_path(ref) not in files:
            raise ValueError(f'Missing referenced package asset: {ref}')
    for ref in [interface['composerIcon'], interface['logo'], *interface['screenshots']]:
        validate_image(package_path(ref), files[package_path(ref)])
    if not any(name.endswith('/SKILL.md') for name in files):
        raise ValueError('Submission needs bundled skills')
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'plugins' / 'buildbetter-codex')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        files = payloads(args.source)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=args.output.parent, suffix='.zip', delete=False) as tmp:
            temporary = Path(tmp.name)
        try:
            with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in sorted(files.items()):
                    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, content)
            os.replace(temporary, args.output)
        finally:
            temporary.unlink(missing_ok=True)
        digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
        print(f'{args.output.name}: {len(files)} files; SHA256 {digest}')
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Invalid submission package: {error}\n')


if __name__ == '__main__':
    main()
