#!/usr/bin/env python3
"""Generate a credential-free Grok Bot/Cursor package from maintained skills."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'plugins' / 'buildbetter-codex'
DEFAULT_OUTPUT = ROOT / 'plugins' / 'buildbetter-grok'

FOUNDATION = '''---
name: buildbetter
description: Research customer feedback, imported support, surveys, analytics, recordings, signals, and Knowledge using the connected BuildBetter workspace.
---

# BuildBetter

Use buildbetter-start to choose a focused workflow. Connect the remote BuildBetter MCP through the host's OAuth flow; never ask for credentials in chat. Use only the authenticated user's accessible workspace. Discover actual tools before promising a capability.

Complete supported research in chat, including filters, pagination, evidence selection and citations. UI is optional and useful only when the host supports it and it reduces effort. If MCP Apps rendering or Events are unsupported, use ordinary read tools and report the limitation. A scheduled Bot routine is not an MCP Events subscription.

Search organization skills with list-skills and read relevant guidance with get-skill. These runtime instructions remain private and are never bundled in this public package. Publishing, sending, paid processing, access changes and other external writes retain their explicit approval boundaries.

The package connects to https://mcp.buildbetter.app. Use a separate custom connection to https://mcp-staging.buildbetter.app for staging QA; never change the public package to staging. Disconnect or revoke access through the host and BuildBetter settings when needed.
'''


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def files():
    original = json.loads((SOURCE / '.codex-plugin' / 'plugin.json').read_text())
    manifest = {key: original[key] for key in
                ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords')}
    manifest['$schema'] = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    manifest['description'] = 'Research customer feedback, support, surveys and product usage in your connected BuildBetter workspace. Chat-first workflows with source citations.'
    cursor = {key: value for key, value in manifest.items() if key != '$schema'}
    cursor.update({'logo': './assets/buildbetter-app-icon.svg', 'skills': './skills/', 'mcpServers': './mcp.cursor.json'})
    server = {'url': 'https://mcp.buildbetter.app'}
    result = {
        'plugin.json': encoded(manifest),
        'mcp.json': encoded({'$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
                            'mcpServers': {'buildbetter': {'type': 'streamable-http', **server}}}),
        '.cursor-plugin/plugin.json': encoded(cursor),
        'mcp.cursor.json': encoded({'mcpServers': {'buildbetter': server}}),
        'assets/buildbetter-app-icon.svg': (SOURCE / 'assets' / 'buildbetter-app-icon.svg').read_bytes(),
        'skills/buildbetter/SKILL.md': FOUNDATION.encode(),
    }
    for path in sorted((SOURCE / 'skills').rglob('*')):
        if not path.is_file() or path.relative_to(SOURCE / 'skills').parts[0] == 'buildbetter':
            continue
        if path.is_symlink():
            raise ValueError('Public skills cannot contain symlinks')
        content = path.read_text()
        # Workflow references are names, not Codex-specific dollar invocations.
        content = re.sub(r'\$(buildbetter[\w-]*)', r'\1', content)
        result[path.relative_to(SOURCE).as_posix()] = content.encode()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = files()
    if args.output.is_symlink():
        parser.error('Generated output cannot be a symlink')
    paths = list(args.output.rglob('*'))
    if any(path.is_symlink() for path in paths):
        parser.error('Generated output cannot contain symlinks')
    actual = {p.relative_to(args.output).as_posix() for p in paths if p.is_file()}
    obsolete = sorted(actual - expected.keys() - {'README.md'})
    if args.check:
        changed = [name for name, content in expected.items()
                   if not (args.output / name).is_file() or (args.output / name).read_bytes() != content]
        # README is hand-authored; every other file is generated.
        changed += obsolete
        if changed:
            parser.exit(1, 'Generated Grok package differs: ' + ', '.join(changed) + '\n')
        print('Grok package matches maintained public skills')
        return
    for name, content in expected.items():
        path = args.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    for name in obsolete:
        (args.output / name).unlink()
    print(f'Generated {len(expected)} public package files')


if __name__ == '__main__':
    main()
