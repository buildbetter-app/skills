# App Navigator: Codebase Analysis

You are analyzing the web application codebase to map routes to source components.

## Your Task

Given the following list of routes and page names discovered from browser navigation:

{DISCOVERED_ROUTES}

For each route, find:
1. The React component that renders it
2. The file path where that component is defined
3. Any sub-components that are significant (data tables, forms, modals)

## Where to Look

- Route definitions: search the frontend source tree (for example `src/` or `app/`) for router configuration files
  - Look for `createBrowserRouter`, `Route`, `path:` patterns, or file-based routes
- Page components: typically in a `pages/`, `routes/`, or `app/` directory
- Layouts: check for layout wrappers in the route config

## Output Format

Return a markdown table:

| Route | URL | Component | File Path | Key Sub-Components |
|-------|-----|-----------|-----------|-------------------|
| ... | ... | ... | ... | ... |
