Fix the behavior of `more_itertools.sliced` for negative slice sizes.

Requirements:
- Calling `list(more_itertools.sliced(seq, n))` with any negative integer `n` must raise `ValueError`.
- The same negative-size behavior must apply when `strict=True`.
- Preserve the existing behavior for `n == 0`.
- Preserve existing behavior for positive `n`, including strict-mode divisibility checks.
- Keep the product change bounded to the existing `sliced` implementation and its directly relevant tests.
- Do not change public APIs, unrelated functions, documentation, packaging, or dependencies.

Use the repository's existing test and formatting conventions. Implement the smallest correct change and leave the workspace in a passing state.
