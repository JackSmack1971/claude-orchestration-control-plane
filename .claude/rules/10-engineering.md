# Engineering rules

- Prefer the smallest change that satisfies the validated acceptance criteria.
- Preserve existing architecture and public behavior unless the plan explicitly changes them.
- Inspect existing behavior before modifying it.
- Do not broaden scope while implementing an atomic task. Record newly discovered work as a follow-up or blocker.
- Keep dependencies directional and explicit. Avoid circular ownership between modules and workflow components.
- Do not edit generated, vendored, dependency, or build-output directories directly.
- Update documentation when public behavior, workflow behavior, or operator commands change.
