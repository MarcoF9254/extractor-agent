# Current Project Status

**Last updated:** 2026-07-17  
**Default branch:** `main`  
**Active proposal branch:** `agent/vertical-slice-contract-pack`

## Accepted baseline

Stage 0 decisions ADR-001 through ADR-005 are accepted:

- JSON is the candidate system of record;
- Markdown is a deterministic review projection;
- runs use immutable per-run directories;
- the first vertical slice uses a draft Engineering Profile and one historical Stage source;
- one provider may later be implemented behind a small provider-neutral interface;
- structural pass/fail is separate from evaluation findings;
- extraction does not assign governance or consolidation states.

The frozen engineering v1.0.1 specification remains historical evidence. Extraction Contract v0.1 and Conversation Profile v0.1 remain drafts.

## Active proposal

The first vertical-slice contract pack proposes:

- `profiles/drafts/engineering-profile-v0.1.md`;
- `specs/drafts/artifact-contracts-v0.1.md`;
- candidate knowledge, run manifest, structural findings, and evaluation findings schemas under `schemas/drafts/`;
- README reconciliation with the accepted Stage 0 baseline.

All new artifacts are draft and evaluation-only. Their presence does not authorize implementation or a run.

## Review follow-ups addressed in the proposal

1. Sensitive-data check location is bound to `manifest.json → source.sensitive_data_check`.
2. Provider-specific metadata is isolated as an optional, namespaced raw artifact.
3. README no longer states that runtime architecture is wholly unapproved.

## Source fixture blocker

The repository contains historical extraction outputs, not their complete bounded Stage transcripts.

Before the first run:

1. supply one complete Stage source;
2. perform and record the sensitive-data selection check;
3. preserve the original or create a recorded redacted derivative;
4. treat the historical output only as comparison evidence.

No specific Stage source has been selected or admitted.

## Validation required before approval

- independent review of Profile/Contract responsibility separation;
- JSON Schema syntax and representative positive/negative instances;
- candidate enum coverage against historical outputs;
- authority-leakage review;
- manifest path, digest, sensitive-source, and namespaced-provider invariants;
- confirmation that no schema field encodes maturity, canonical identity, approval, promotion, or KB state.

## Hard holds

Do not yet:

- implement a provider adapter, parser, renderer, validator, or CLI;
- run a model on historical or private source data;
- freeze the Extraction Contract or any Profile;
- promote historical outputs to golden expectations;
- add consolidation, identity, maturity, approval, promotion, or KB-write behavior;
- build multi-provider orchestration;
- merge the proposal without independent review and owner authorization.
