# Architecture

**Status:** Pre-decision scaffold

No runtime architecture has been approved.

## Current conceptual boundary

```text
Bounded source + approved profile + approved contract
                         |
                         v
                    Extraction
                         |
                         v
              Grounded candidate items
```

The extraction component must not perform cross-source consolidation, maturity assignment, canonical identity resolution, promotion, or publication approval.

## Decisions required before implementation

- Input envelope and source provenance
- Output schema and validation behavior
- Provider/model boundary
- Determinism and retry policy
- Evidence pointers and audit representation
- Human-review handoff
- Storage boundary for runs and approved artifacts
- Threat model for private or sensitive conversations
