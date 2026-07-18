# First Vertical-Slice Artifact Contracts

**Version:** 0.1  
**Status:** Draft — evaluation-only, not runtime authority  
**Applies to:** First Engineering Profile vertical slice

## Purpose

Define the machine-readable artifacts needed to perform one reproducible, source-bounded evaluation run without introducing consolidation or governance authority.

The schemas under `schemas/drafts/` are proposals. Schema validity means only that an artifact conforms structurally to its declared draft contract.

## Contract set

| Artifact | Draft schema | Role |
|---|---|---|
| Candidate knowledge | `candidate-knowledge.schema.json` | System-of-record extraction result |
| Run manifest | `run-manifest.schema.json` | Immutable provenance and artifact membership record |
| Structural findings | `structural-findings.schema.json` | Machine-checkable conformance result |
| Evaluation findings | `evaluation-findings.schema.json` | Separate grounding/quality review evidence |
| Markdown projection | No independent schema | Deterministic human-readable projection from candidate JSON |

## Candidate identity boundary

`candidate_id` is a run-local handle only. It supports findings and projection references inside one run.

It is not:

- a canonical signature;
- a permanent knowledge identifier;
- evidence that two candidates across runs are identical;
- an approval, maturity, or promotion state.

Candidate IDs must be unique within one artifact. JSON Schema cannot enforce cross-item field uniqueness, so the structural validator must enforce it.

## Candidate artifact rules

- JSON is the system of record.
- The artifact may contain zero items; an empty grounded extraction is valid.
- Knowledge type must come from the selected Profile's closed enum. The v0.1 schema carries the Engineering Profile v0.1 enum for this vertical slice.
- `normalized_statement` is stylistic normalization within one source, not canonicalization.
- `candidate_concepts` are local unresolved tags, limited to five.
- Confidence measures source support, not objective truth.
- No maturity, canonical identity, cross-source link, approval, version, conflict, promotion, or deprecation field is permitted.
- Markdown must be regenerated from JSON and must never be independently authoritative.

## Immutable run layout

For v0.1 evaluation runs, the specified layout is:

```text
data/runs/<run_id>/
├── manifest.json
├── input/
│   ├── source.txt
│   ├── contract.md
│   └── profile.md
├── raw/
│   ├── model-response.txt
│   └── provider-metadata.json        # optional
├── candidate/
│   ├── items.json
│   └── items.md
└── validation/
    ├── structural-findings.json
    └── evaluation-findings.json
```

After a completed run is admitted, files inside its run directory are immutable. Corrections require a new run ID. A future index or latest pointer is derived and cannot replace or rewrite a run.

Every artifact named by the manifest must carry a SHA-256 digest. The manifest itself is the run membership record and must not list artifacts outside its own run directory.

## Sensitive-source selection gate

The sensitive-data check is recorded at:

```text
manifest.json → source.sensitive_data_check
```

Allowed admitted outcomes:

- `cleared`: the selected source is the unchanged original;
- `redacted_derivative`: the selected source is a recorded derivative of the preserved original.

A blocked source does not qualify for a run manifest and must not be invoked.

The record must include checker identity/role, check time, outcome, and notes. A redacted derivative must include its own path and SHA-256 while the original path and SHA-256 remain recorded. The original must never be silently overwritten.

This is a selection and provenance gate, not a claim that the system provides automated privacy detection.

## Provider boundary

The manifest records the provider, model, interface version, prompt/configuration digest, and invocation parameters needed for comparison.

Provider-specific metadata is allowed only as a separate optional artifact under `raw/provider-metadata.json`. Its manifest entry must include a provider namespace, path, and SHA-256.

Provider-specific fields must not appear in candidate knowledge, structural findings, or evaluation findings.

This contract does not authorize routing, fallback, multiple providers, or production credentials.

## Structural findings

Structural status is one of:

- `pass`: no structural findings;
- `fail`: one or more schema/invariant findings;
- `error`: validation could not execute.

Structural validation covers schema conformance and deterministic invariants, including:

- candidate ID uniqueness;
- artifact paths remaining within the run;
- manifest membership and digest presence;
- allowed closed enums;
- conditional sensitive-data fields;
- Markdown projection provenance.

It does not assess grounding quality, objective truth, maturity, identity, or approval.

## Evaluation findings

Evaluation uses `completed` or `not_performed`, not pass/fail and not approved/rejected.

Findings may address:

- grounding;
- exclusion violations;
- cross-context reusability;
- over-specificity;
- evidence quality;
- confidence calibration;
- profile-type fit.

Each finding is review evidence with level `observation` or `concern`. It cannot mutate candidate JSON or assign governance status.

## Projection rule

`candidate/items.md` must be a deterministic projection of `candidate/items.json`. The manifest records both digests and identifies the JSON source path for the projection.

A projection mismatch is a structural failure. Human edits to the Markdown do not update the JSON and are not accepted as a corrected run.

## First-run holds

This draft does not authorize:

- provider or CLI implementation;
- a real-data run;
- use of any historical source before its sensitive-data record exists;
- freezing the Extraction Contract or Engineering Profile;
- treating historical outputs as golden expected results;
- consolidation, identity, maturity, approval, promotion, or KB writes.

---

End of Artifact Contracts (Draft)
