# extractor-agent

A governance-first agent for extracting reusable knowledge from conversations, project stages, and other bounded evidence sources.

## Repository status

This repository is initialized for specification and architecture work. No runtime architecture or model provider has been approved yet.

| Area | Authority status |
|---|---|
| `specs/baselines/` | Historical frozen baseline used for the Stage 1–7 test runs |
| `specs/drafts/` | Proposed contracts; not frozen or authoritative |
| `profiles/drafts/` | Proposed domain profiles; not frozen or authoritative |
| `tests/fixtures/stage-outputs/` | Observed extraction outputs retained as test evidence, not canonical knowledge |
| `src/` | Reserved for implementation after architecture approval |
| `docs/` | Architecture, decisions, and source-status records |

## Boundary

Extraction operates on one bounded source and produces grounded candidate knowledge. Cross-source consolidation, maturity assessment, canonical identity, promotion, and publication authority are downstream concerns and must not be silently performed during extraction.

## Immediate next stage

1. Freeze the extraction contract and at least one profile.
2. Define an output schema and machine-checkable invariants.
3. Turn the Stage 1–7 outputs into an explicit evaluation corpus.
4. Select the smallest vertical slice before choosing production infrastructure.

See [docs/source-material-status.md](docs/source-material-status.md) and [docs/architecture.md](docs/architecture.md).
