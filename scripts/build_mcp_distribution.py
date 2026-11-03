#!/usr/bin/env python3
"""Build public distribution or a registered Microsoft 365 app without network access."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import struct
import tempfile
import uuid
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ENDPOINT = 'https://mcp.buildbetter.app'
PUBLIC_FILES = (
    'LICENSE', 'server.json', '.cursor-plugin/marketplace.json', 'distribution/README.md',
    'distribution/APPLICATIONS.md',
    'distribution/submissions.json', 'distribution/REVIEWER-INSTRUCTIONS.md',
    'distribution/assets/README.md',
    'distribution/assets/buildbetter-512.png', 'distribution/assets/buildbetter-192.png',
    'distribution/listing.json', 'distribution/google/listing.json',
    'distribution/microsoft365/declarativeAgent.json',
    'distribution/microsoft365/ai-plugin.template.json',
)


def read_public(path):
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('Public input cannot be a symlink')
    return path.read_bytes()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def distribution_files():
    result = {name: read_public(ROOT / name) for name in PUBLIC_FILES}
    registry = json.loads(result['server.json'])
    if registry['remotes'] != [{'type': 'streamable-http', 'url': PUBLIC_ENDPOINT}]:
        raise ValueError('Registry must use only the production OAuth endpoint')
    if len(registry['description']) > 100:
        raise ValueError('Registry description exceeds 100 characters')
    spec = importlib.util.spec_from_file_location('grok_package', ROOT / 'scripts/build_grok_plugin.py')
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    for name, content in generator.files().items():
        if name != generator.OUTPUT_MARKER:
            result['plugins/buildbetter-grok/' + name] = content
    result['plugins/buildbetter-grok/README.md'] = read_public(ROOT / 'plugins/buildbetter-grok/README.md')
    return result


def png_icon(path, side):
    payload = read_public(path)
    if len(payload) > 1024 * 1024 or payload[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Icon must be a PNG under 1 MiB')
    offset, chunks, dimensions = 8, [], None
    while offset + 12 <= len(payload):
        size = struct.unpack('>I', payload[offset:offset + 4])[0]
        end = offset + 12 + size
        if end > len(payload):
            raise ValueError('Truncated PNG icon')
        kind, data = payload[offset + 4:offset + 8], payload[offset + 8:offset + 8 + size]
        crc = struct.unpack('>I', payload[offset + 8 + size:end])[0]
        if zlib.crc32(kind + data) != crc:
            raise ValueError('Invalid PNG checksum')
        if kind == b'IHDR' and size == 13 and not chunks:
            dimensions = struct.unpack('>II', data[:8])
        chunks.append(kind)
        offset = end
        if kind == b'IEND':
            break
    if (dimensions != (side, side) or b'IDAT' not in chunks or not chunks
            or chunks[-1] != b'IEND' or offset != len(payload)):
        raise ValueError(f'Icon must be a complete {side}x{side} PNG')
    return payload


def copilot_files(args):
    required = (args.copilot_app_id, args.copilot_oauth_reference_id,
                args.copilot_color_icon, args.copilot_outline_icon)
    if not all(required):
        raise ValueError('Copilot requires registered app and OAuth vault IDs plus color/outline icons')
    try:
        app_id = str(uuid.UUID(args.copilot_app_id))
    except ValueError:
        raise ValueError('Copilot app ID must be a registered UUID') from None
    reference = args.copilot_oauth_reference_id
    if (not re.fullmatch(r'[A-Za-z0-9._-]{1,128}', reference)
            or reference == 'REQUIRES_OAUTH_VAULT_REGISTRATION'):
        raise ValueError('Supply an OAuth vault registration ID, not a credential or placeholder')
    listing = json.loads(read_public(ROOT / 'distribution/listing.json'))
    plugin = json.loads(read_public(ROOT / 'distribution/microsoft365/ai-plugin.template.json'))
    plugin['runtimes'][0]['auth']['reference_id'] = reference
    manifest = {
        '$schema': 'https://developer.microsoft.com/json-schemas/teams/v1.22/MicrosoftTeams.schema.json',
        'manifestVersion': '1.22', 'version': '0.1.0', 'id': app_id,
        'developer': {'name': 'BuildBetter', 'websiteUrl': listing['website'],
                      'privacyUrl': listing['privacy_policy_url'],
                      'termsOfUseUrl': listing['terms_of_service_url']},
        'name': {'short': 'BuildBetter', 'full': 'BuildBetter Customer Research'},
        'description': {
            'short': 'Research customer feedback, surveys and product usage with source citations.',
            'full': listing['details'],
        },
        'icons': {'color': 'color.png', 'outline': 'outline.png'},
        'accentColor': '#FFFFFF', 'validDomains': ['mcp.buildbetter.app'],
        'copilotAgents': {'declarativeAgents': [{'id': 'buildbetter', 'file': 'declarativeAgent.json'}]},
    }
    return {
        'manifest.json': encoded(manifest), 'ai-plugin.json': encoded(plugin),
        'declarativeAgent.json': read_public(ROOT / 'distribution/microsoft365/declarativeAgent.json'),
        'color.png': png_icon(args.copilot_color_icon, 192),
        'outline.png': png_icon(args.copilot_outline_icon, 32),
    }


def submission_files():
    public = distribution_files()
    listing = json.loads(public['distribution/listing.json'])
    applications = json.loads(public['distribution/submissions.json'])
    index = '# BuildBetter prepared applications\n\n'
    index += ('Each folder has a copy-ready FORM.json draft and its available attachments.\n'
              'Forms are not provider upload schemas, submitted listings or approvals.\n'
              'Complete every missing_inputs item before submitting. Null fields require\n'
              'real publisher details; native-host QA and agreements remain separate.\n\n')
    index += '\n'.join(f'- [{name}](platforms/{name}/FORM.json)' for name in applications)
    index += ('\n\nRead REVIEWER-INSTRUCTIONS.md and ASSET-SOURCES.md.\n'
              'Verify file integrity with: shasum -a 256 -c SHA256SUMS\n'
              'Source: https://github.com/buildbetter-app/skills\n'
              'Application guide: distribution/APPLICATIONS.md at the submitted revision.\n')
    result = {
        'README.md': index.encode('utf-8'),
        'REVIEWER-INSTRUCTIONS.md': public['distribution/REVIEWER-INSTRUCTIONS.md'],
        'ASSET-SOURCES.md': public['distribution/assets/README.md'],
        'LICENSE': public['LICENSE'],
    }
    for platform, application in applications.items():
        if not re.fullmatch(r'[a-z0-9-]+', platform):
            raise ValueError('Invalid platform folder name')
        prefix = f'platforms/{platform}/'
        result[prefix + 'FORM.json'] = encoded({
            'purpose': 'Application preparation; not a submitted or approved listing',
            'application_url': application['application_url'],
            'shared_fields': listing,
            'platform_fields': application['fields'],
            'missing_inputs': application['missing_inputs'],
            'reviewer_instructions': '../../REVIEWER-INSTRUCTIONS.md',
        })
        if platform == 'mcp-registry':
            result[prefix + 'server.json'] = public['server.json']
        elif platform in ('cursor', 'grok'):
            plugin_prefix = 'plugins/buildbetter-grok/'
            for name, content in public.items():
                if name.startswith(plugin_prefix):
                    result[prefix + 'plugin/' + name[len(plugin_prefix):]] = content
            result[prefix + 'plugin/LICENSE'] = public['LICENSE']
            if platform == 'cursor':
                result[prefix + 'marketplace.json'] = public['.cursor-plugin/marketplace.json']
        elif platform == 'google':
            result[prefix + 'LISTING.json'] = public['distribution/google/listing.json']
            result[prefix + 'icon-512.png'] = png_icon(ROOT / 'distribution/assets/buildbetter-512.png', 512)
        elif platform == 'microsoft365':
            result[prefix + 'color-192.png'] = png_icon(ROOT / 'distribution/assets/buildbetter-192.png', 192)
            for name in ('declarativeAgent.json', 'ai-plugin.template.json'):
                result[prefix + name] = public['distribution/microsoft365/' + name]
    result['SHA256SUMS'] = ''.join(
        f'{hashlib.sha256(content).hexdigest()}  {name}\n'
        for name, content in sorted(result.items())
    ).encode('utf-8')
    return result


def write_archive(output, files):
    if any(part.is_symlink() for part in (output, *output.parents)):
        raise ValueError('Output cannot be a symlink or pass through one')
    if output.exists() and not output.is_file():
        raise ValueError('Output must be a ZIP file path')
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix='.mcp-distribution-', suffix='.zip', dir=output.parent)
    try:
        with os.fdopen(handle, 'wb') as stream:
            with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in sorted(files.items()):
                    info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    info.external_attr = 0o100644 << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, content)
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/mcp-distribution.zip')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--copilot', action='store_true', help='Build only the registered Microsoft app ZIP')
    mode.add_argument('--submissions', action='store_true', help='Prepare eight separate application folders')
    parser.add_argument('--copilot-app-id')
    parser.add_argument('--copilot-oauth-reference-id', help='Non-secret Developer Portal vault configuration ID')
    parser.add_argument('--copilot-color-icon', type=Path)
    parser.add_argument('--copilot-outline-icon', type=Path)
    args = parser.parse_args()
    if not args.copilot and any((args.copilot_app_id, args.copilot_oauth_reference_id,
                                 args.copilot_color_icon, args.copilot_outline_icon)):
        parser.error('Copilot registration options require --copilot')
    try:
        files = (copilot_files(args) if args.copilot else
                 submission_files() if args.submissions else distribution_files())
        write_archive(args.output, files)
    except (ValueError, OSError, KeyError) as error:
        parser.error(str(error))
    print(f'Built {len(files)} public files: {args.output}')
    print('Package preparation only; native-host QA and provider submission are separate.')


if __name__ == '__main__':
    main()
