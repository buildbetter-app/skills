---
name: bb-skills-update
description: Check for and install BB-Skills updates. Use when the user asks to "update skills", "check for updates", or "upgrade bb-skills".
argument-hint: "[--check]"
---

# BB-Skills Update

Check for available updates to the optional BB-Skills CLI installation.

## Instructions

1. Read the manifest at `~/.bb-skills/manifest.json` to find the current installed CLI version
2. If the manifest doesn't exist, explain that this updater applies to the optional `bb-skills` CLI, not the Codex plugin package itself
3. Run: `bb-skills update` (or `bb-skills update --check` if user only wants to check without installing)
4. Report the result to the user

## If bb-skills CLI is not installed

Tell the user:
> BB-Skills CLI is not installed. This skill updates the optional CLI distribution, not the Codex plugin package. If you want the CLI too, install it with:
> ```
> pip install bb-skills
> ```
> Then run `bb-skills install <pack>` to install skill packs.
