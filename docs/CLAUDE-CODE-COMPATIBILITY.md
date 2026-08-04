# Claude Code compatibility notes

The control plane uses current project-level Claude Code configuration shapes:

- project skills: `.claude/skills/<name>/SKILL.md`;
- project subagents: `.claude/agents/<name>.md`;
- modular project rules: `.claude/rules/*.md`, including `paths:` scoped rules;
- project settings and lifecycle/tool hooks: `.claude/settings.json`;
- legacy-compatible human commands: `.claude/commands/*.md` for small operator actions.

Skills are the primary workflow/procedure mechanism. The three command files are intentionally limited to read-only/diagnostic operator entry points so the project does not duplicate the main workflow in legacy command wrappers.

The `researcher` and critics are custom project-aware subagents rather than built-in Explore/Plan workers. Project settings deny `Agent(Explore)` and `Agent(Plan)` because this workflow depends on project policy and preloaded procedure context.

The repository assumes Python 3.11+ for deterministic hooks and workflow enforcement. Claude Code itself is not required for the Python unit/smoke tests, so CI can validate the control plane without an Anthropic login.
