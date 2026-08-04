# Task DAG contract

- Phase ids and task ids are unique.
- Every dependency references an existing earlier/equivalent-layer node and the graph is acyclic.
- Cross-phase dependencies point only backward.
- A task objective describes one independently reviewable change.
- Every behavior-changing task defines a test-first action or an explicit TDD exception.
- Verification commands are concrete, not phrases like "run tests".
- Acceptance criteria are observable and do not merely restate implementation details.
- Non-goals bound the task so implementation cannot silently expand scope.
