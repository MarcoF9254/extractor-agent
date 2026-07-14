# Current Project Status

**Last updated:** 2026-07-14  
**Default branch:** `main`  
**Active proposal branch:** `agent/stage-0-architecture-baseline`

## Current state

The repository is initialized with:

- a frozen historical engineering extraction baseline;
- a draft domain-agnostic Extraction Contract v0.1;
- a draft Conversation Profile v0.1;
- observational Stage 1–7 output fixtures;
- a pre-decision architecture scaffold.

No runtime architecture, candidate JSON schema, provider, or production deployment has been approved.

## Active work

Stage 0 proposes governance and the minimum architecture/authority decisions required before implementation.

Decision packet: `docs/stage-0-architecture-review.md`

Pending decisions:

- D-EA-001 — system-of-record output;
- D-EA-002 — immutable run layout;
- D-EA-003 — first vertical slice;
- D-EA-004 — provider boundary;
- D-EA-005 — evaluation status semantics.

## Hard holds

Do not begin runtime implementation until the pending Stage 0 decisions are dispositioned.

Do not:

- treat historical fixtures as canonical or exact golden outputs;
- freeze the draft contract or conversation profile without required real runs;
- assign maturity or canonical identity during extraction;
- add a permanent knowledge-base write path;
- select a multi-provider framework without evidence that one provider adapter is insufficient.

## Recommended next action

Review the Stage 0 decision packet, obtain independent architecture review, then record owner dispositions. After approval, derive the Engineering Profile and define the candidate/run contracts.
