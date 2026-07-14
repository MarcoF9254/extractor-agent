# AGENTS.md

## Repository intent

Build a governed extraction agent while preserving evidence/authority separation.

## Hard boundaries

- Treat files under `specs/drafts/` and `profiles/drafts/` as proposals, not authority.
- Treat `tests/fixtures/` as observational evidence, not golden truth unless a later decision explicitly promotes a fixture.
- Do not assign maturity, canonical identity, promotion status, or publication authority during extraction.
- Do not change a frozen baseline to make an implementation pass.
- Prefer specification and decision records before implementation when behavior is ambiguous.
- Keep source evidence immutable; derived artifacts must be reproducible and separately stored.

## Change workflow

1. Inspect repository state and relevant authority documents.
2. State the decision or requirement being implemented.
3. Make the smallest scoped change.
4. Add or update proportional tests.
5. Report evidence, limitations, and any owner-gated decisions.
