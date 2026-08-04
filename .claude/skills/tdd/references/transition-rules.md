# TDD transition rules

- `SELECTED -> UNDERSTAND_EXISTING_BEHAVIOR`: inspect affected code/tests first.
- `UNDERSTAND_EXISTING_BEHAVIOR -> TEST_WRITTEN`: define the failing behavioral check.
- `TEST_WRITTEN -> RED_CONFIRMED`: only after an actual expected failure is recorded.
- `RED_CONFIRMED -> IMPLEMENT_MINIMAL`: implementation may now begin.
- `IMPLEMENT_MINIMAL -> GREEN_CONFIRMED`: only after targeted behavior passes.
- `GREEN_CONFIRMED -> REFACTOR`: clean up while retaining behavior.
- `REFACTOR -> RELATED_VERIFIED`: run surrounding verification.
- `RELATED_VERIFIED -> COMPLETE`: only when task acceptance criteria are satisfied.

Forbidden shortcuts: RED -> COMPLETE, IMPLEMENT_MINIMAL -> COMPLETE, GREEN_CONFIRMED -> COMPLETE.
