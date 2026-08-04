# Testing and verification rules

- For behavior-changing tasks, follow RED -> GREEN -> REFACTOR -> RELATED VERIFICATION unless the task graph records a specific TDD exception.
- RED must demonstrate that the intended test fails for the expected reason, not because the test harness is broken.
- GREEN must be produced by the minimum implementation needed to satisfy the targeted behavior.
- After refactoring, rerun targeted tests and then related checks.
- Never convert a failing test into a passing one by weakening the assertion unless the validated requirement itself changed.
- Do not delete or skip a relevant test to make verification pass.
- Final verification commands come from `.claude/project-checks.json` and must record command, exit code, output, and time.
