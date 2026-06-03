#!/usr/bin/env bash
set -euo pipefail

repo_root="${1:-${BUILDBETTER_REPO_ROOT:-}}"

if [[ -z "$repo_root" ]]; then
  if [[ -f "packages/apps/cli-go/package.json" ]]; then
    repo_root="$PWD"
  else
    echo "Usage: install-bb-cli.sh /path/to/buildbetter-app" >&2
    echo "Or set BUILDBETTER_REPO_ROOT=/path/to/buildbetter-app." >&2
    exit 2
  fi
fi

repo_root="$(cd "$repo_root" && pwd)"
cli_package="$repo_root/packages/apps/cli-go"

if [[ ! -f "$cli_package/package.json" ]]; then
  echo "Could not find packages/apps/cli-go under $repo_root." >&2
  exit 2
fi

pnpm --dir "$cli_package" build
mkdir -p "$HOME/.local/bin"
install -m 0755 "$cli_package/dist/bb" "$HOME/.local/bin/bb"
"$HOME/.local/bin/bb" --version
