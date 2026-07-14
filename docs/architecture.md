# Architecture

**Status:** Accepted Stage 0 baseline  
**Decision record:** `docs/decisions.md`

## Purpose

`extractor-agent` performs one source-bounded extraction and produces grounded candidate knowledge with reproducible evidence. It does not consolidate across sources or mutate a permanent knowledge base.

## System boundary

```text
Bounded source
    + approved contract
    + approved profile
          ↓
     Input assembler
          ↓
     Provider adapter
          ↓
    Raw model response
          ↓
     Candidate parser
          ↓
 Candidate JSON artifact
          ↓
 Structural validation
          ↓
 Evaluation findings
          ↓
 Markdown review projection
```

Downstream and explicitly outside this architecture baseline:

- cross-source deduplication and consolidation;
- canonical identity resolution;
- maturity assessment;
- conflict resolution;
- approval, promotion, versioning, and deprecation;
- publication to or mutation of a permanent knowledge base.

## Components

### Input assembler

Packages exactly one bounded source with provenance plus the selected approved contract and profile.

It must not query a knowledge base, add outside knowledge, or combine independent sources into one implicit extraction scope.

Before the first historical Stage fixture is used, selection must include a recorded sensitive-data check. Restricted content requires an explicitly recorded redacted derivative or a different fixture; original evidence must not be silently rewritten.

### Provider adapter

Exposes a small provider-neutral invocation interface. The first implementation supports one provider only.

Provider, model, prompt/configuration, and relevant invocation parameters are captured in the run manifest. Provider-specific raw metadata may be namespaced but must not leak into candidate knowledge fields.

### Candidate parser

Converts the raw model response into the approved candidate JSON schema.

It reports parse/conformance failures and must not silently repair unsupported knowledge, invent evidence, or perform cross-source identity matching.

### Structural validator

Checks machine-readable invariants such as required fields, closed enums, artifact integrity, and contract versions. Its result is structural pass/fail.

It does not judge objective truth, maturity, canonical identity, or promotion status.

### Evaluation layer

Records source-grounding, exclusion, and reusable-quality findings separately from structural validity.

Evaluation findings are review evidence. They do not approve, reject, canonize, or promote permanent knowledge.

### Renderer

Produces a deterministic Markdown review projection from the candidate JSON system artifact.

The projection is not independently authoritative and must not become a second editable source of truth.

### Run writer

Persists an immutable per-run tree under `data/runs/<run_id>/`.

The run contract will cover:

```text
data/runs/<run_id>/
├── manifest.json
├── input/
│   ├── source.txt
│   ├── contract.md
│   └── profile.md
├── raw/
│   └── model-response.txt
├── candidate/
│   ├── items.json
│   └── items.md
└── validation/
    ├── structural-findings.json
    └── evaluation-findings.json
```

Exact filenames and schemas remain specification work. The architectural requirements are immutability, provenance, replayability, and separation of source, raw response, candidates, projections, and findings.

## Authority model

| Artifact | Authority |
|---|---|
| Frozen baseline | Immutable historical contract/evidence within its declared scope |
| Approved contract/profile | Runtime behavioral authority |
| Source and raw response | Immutable run evidence |
| Candidate JSON | System-of-record extraction result, but candidate only |
| Markdown projection | Derived human-review view |
| Structural/evaluation findings | Validation and review evidence |
| ADR | Accepted architecture authority |
| Permanent knowledge record | Outside extraction-agent scope |

Format acceptance does not confer knowledge authority.

## First vertical slice

The first vertical slice will:

1. derive a draft Engineering Profile from the draft contract and frozen historical engineering baseline;
2. select one representative historical Stage only after a recorded sensitive-data check;
3. define the candidate JSON and run manifest contracts;
4. implement one provider through the provider-neutral interface;
5. persist one immutable run;
6. compare the new result with the historical fixture as observational evidence, not exact golden truth;
7. record contract/profile friction before either draft is frozen.

## Change constraints

- Specification precedes runtime implementation.
- Frozen baselines are not edited to make implementation pass.
- Historical outputs are not exact goldens unless separately approved.
- JSON is the candidate system of record; Markdown is derived.
- A run is immutable after completion.
- Extraction never assigns governance or consolidation states.
- Multi-provider orchestration requires demonstrated need.
