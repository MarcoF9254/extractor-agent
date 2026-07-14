# Current Project Status

**Last updated:** 2026-07-14  
**Default branch:** `main`  
**Active proposal branch:** `agent/record-stage-0-decisions`

## Current state

Stage 0 architecture decisions D-EA-001 through D-EA-005 were approved after independent review and are recorded as ADR-001 through ADR-005.

Accepted baseline:

- JSON is the candidate system of record;
- Markdown is a deterministic review projection;
- runs use immutable per-run directories;
- the first vertical slice uses a draft Engineering Profile and one historical Stage;
- one provider is implemented behind a small provider-neutral interface;
- structural pass/fail is separate from evaluation findings;
- extraction does not assign governance or consolidation states.

The historical engineering baseline remains frozen evidence. The Extraction Contract v0.1 and Conversation Profile v0.1 remain drafts.

## Review follow-ups

Both non-blocking Stage 0 observations are addressed:

1. `docs/architecture.md` is synchronized with the accepted ADRs.
2. Historical Stage selection now requires a recorded sensitive-data check before use.

## Next scoped milestone

Prepare the first vertical-slice specifications:

1. derive `profiles/drafts/engineering-profile-v0.1.md`;
2. select one representative Stage fixture after the sensitive-data check;
3. define the candidate JSON schema;
4. define the run manifest and immutable artifact contract;
5. define structural and evaluation finding contracts.

This milestone is specification-only until those artifacts are reviewed.

## Hard holds

Do not yet:

- implement a provider adapter or runtime CLI;
- freeze the draft contract or either profile;
- treat historical outputs as exact golden results;
- add consolidation, identity, maturity, promotion, or KB-write behavior;
- build multi-provider orchestration;
- use a historical Stage source without the recorded sensitive-data check.
