# BuildBetter workspace Skill Sets

Every BuildBetter workspace mirrors this repository. Each `*.json` file here is
one read-only Skill Set in every workspace; a merge to `main` reaches them all.

- `skills` lists skill folders. A bare name means `skills/<name>`; a path is
  repository-relative. An object can set the workspace display `name`.
- `featureFlag` limits the Skill Set to workspaces with that BuildBetter flag.
- Removing a skill from every manifest archives it in every workspace.
- A malformed manifest or a listed folder without a valid `SKILL.md` blocks the
  whole commit: workspaces keep the last good state.

Skills not listed here (for example `skills/support/`) are not mirrored.
