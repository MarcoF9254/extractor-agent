# extractor-agent

A governance-first agent for extracting reusable knowledge from conversations, project stages, and other bounded evidence sources.

## Repository status

Stage 0 architecture is approved. The first vertical-slice contract pack is under draft review. No provider implementation, runtime CLI, production run, or permanent knowledge-base write path is authorized.

| Area | Authority status |
|---|---|
| `docs/architecture.md` | Accepted Stage 0 system and authority boundary |
| `docs/decisions.md` | Accepted ADR-001 through ADR-005 |
| `specs/baselines/` | Immutable historical baseline used for Stage 1–7 observational runs |
| `specs/drafts/` | Proposed contracts; not frozen or runtime authority |
| `profiles/drafts/` | Proposed domain profiles; not frozen or runtime authority |
| `schemas/drafts/` | Proposed evaluation schemas; structural validity would not confer knowledge authority |
| `tests/fixtures/stage-outputs/` | Historical outputs retained as observational comparison evidence, not golden truth |
| `src/` | Implementation held until the contract pack is reviewed and authorized |

## Boundary

Extraction operates on one bounded source and produces grounded candidate knowledge.

Cross-source consolidation, maturity assessment, canonical identity, approval, promotion, conflict resolution, deprecation, publication, and permanent knowledge-base mutation are downstream concerns and must not be performed during extraction.

JSON is the candidate system of record. Markdown is a deterministic review projection and cannot become an independently edited source of truth.

## Current milestone

The specification-only vertical-slice pack defines:

1. a draft Engineering Profile;
2. a draft candidate knowledge schema;
3. a draft immutable run manifest and sensitive-source record;
4. separate structural and evaluation finding schemas;
5. the evaluation-only artifact boundary.

The historical `stage-01.md` through `stage-07.md` files are extraction outputs, not the original bounded Stage sources. A real vertical-slice run requires a separately supplied Stage transcript that passes the sensitive-data selection gate.

See [docs/architecture.md](docs/architecture.md), [docs/current-status.md](docs/current-status.md), and [specs/drafts/artifact-contracts-v0.1.md](specs/drafts/artifact-contracts-v0.1.md).
