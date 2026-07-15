# Architecture Decision Records

This file records accepted architecture decisions only. Proposals and pending decisions belong in review packets until the owner explicitly approves them.

## ADR-001: Machine-readable candidate artifact with rendered review projection

**Status:** Accepted  
**Approved:** 2026-07-14  
**Source decision:** D-EA-001

### Context

Extraction output must support deterministic validation and automation while remaining practical for human review. Independently editable JSON and Markdown would create competing sources of truth.

### Decision

Use JSON as the system-of-record candidate artifact and generate Markdown as a deterministic review projection.

The Markdown projection must not carry independent authority or be edited as a substitute for changing the JSON artifact or its generating inputs.

### Consequences

A renderer and projection tests are required. Human review remains readable, while structural validation and downstream automation operate on one authoritative representation.

## ADR-002: Immutable per-run artifact directories

**Status:** Accepted  
**Approved:** 2026-07-14  
**Source decision:** D-EA-002

### Context

Overwriting a latest-output directory would weaken provenance, replayability, and comparison across model or contract changes. Database-first storage would add infrastructure before the artifact contract is known.

### Decision

Store each extraction execution in an immutable `data/runs/<run_id>/` directory. A separate index or latest pointer may be derived later but must not replace immutable runs.

The first contract design should cover the run manifest, captured inputs, raw model response, candidate JSON, rendered Markdown, and validation findings.

### Consequences

Storage use increases and cleanup/retention policy will be required before production. In return, every run can be audited, compared, and reproduced without rewriting evidence.

## ADR-003: Engineering historical-Stage vertical slice first

**Status:** Accepted  
**Approved:** 2026-07-14  
**Source decision:** D-EA-003

### Context

The repository has seven historical engineering extraction outputs but no approved Engineering Profile. Starting both conversation and engineering profiles would widen the evaluation surface prematurely.

### Decision

The first vertical slice will derive a draft Engineering Profile from the draft contract and frozen historical baseline, then run against one representative historical Stage.

Before selecting or copying the Stage source into a run, record a sensitive-data check confirming that it contains no personal, confidential, credential, or otherwise restricted material. If it does, redact through an explicitly recorded derived source or select another fixture; do not silently modify the original evidence.

### Consequences

Historical output provides comparison evidence but is not an exact golden result. The Conversation Profile remains draft and out of the first implementation slice.

## ADR-004: Provider-neutral boundary with one initial provider

**Status:** Accepted  
**Approved:** 2026-07-14  
**Source decision:** D-EA-004

### Context

Hard-coding provider semantics into extraction contracts would create coupling. A general multi-provider orchestration framework would be speculative before a second provider creates real pressure.

### Decision

Define a small provider-neutral invocation interface and implement one provider first. Persist provider, model, prompt/configuration, and relevant invocation parameters in the run manifest.

Do not build general orchestration, routing, or fallback behavior without evidence from an additional provider or production requirement.

### Consequences

The first provider adapter remains replaceable without forcing premature abstraction. Some provider-specific metadata may be retained in a namespaced raw section rather than leaking into candidate knowledge fields.

## ADR-005: Separate structural status from evaluation findings

**Status:** Accepted  
**Approved:** 2026-07-14  
**Source decision:** D-EA-005

### Context

A single pass/fail result would collapse machine-checkable artifact integrity and judgment-based grounding quality. Using approved/rejected knowledge states during extraction would leak governance authority into a source-bounded stage.

### Decision

Use structural pass/fail for machine-checkable contract conformance and record grounding, exclusion, and quality concerns as separate evaluation findings.

Extraction must not assign approved, canonical, mature, promoted, deprecated, or equivalent governance states.

### Consequences

Consumers can distinguish unusable artifacts from structurally valid candidates that still need semantic evaluation. Promotion remains downstream and owner-governed.
