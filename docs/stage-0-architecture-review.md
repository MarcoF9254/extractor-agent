# Stage 0 Architecture and Authority Review

**Status:** Draft decision packet  
**Reference repository:** `MarcoF9254/monthly-agent`  
**Scope:** Documentation and owner-gated architecture only; no runtime implementation

## 1. Problem

The repository contains a frozen historical engineering extraction baseline, a draft domain-agnostic contract, a draft conversation profile, and seven observed Stage outputs. It does not yet have an approved runtime architecture, machine-readable output contract, run artifact contract, or first vertical-slice definition.

The immediate goal is therefore not to choose a model or build an orchestration framework. It is to stabilize the minimum boundaries needed for a reproducible extraction run.

## 2. Cross-repository reference

### Patterns suitable for reuse from monthly-agent

- governance as a meta-layer;
- architecture → specification → implementation → validation sequencing;
- evidence/authority separation;
- explicit uncertainty instead of inference;
- structural validation separated from semantic QA;
- immutable, auditable run artifacts;
- narrow, independently testable components;
- accepted ADRs separated from proposals;
- owner approval for authority-bearing decisions.

### Patterns that must not be copied directly

- activity-record schema and business-rule registry;
- participant-facing severity assumptions;
- newsletter publication workflow;
- per-record activity identity semantics;
- source-specific directory and field conventions;
- the assumption that QA approval makes an artifact publication-ready.

Knowledge extraction has an additional downstream boundary: a valid extraction remains a candidate. It does not gain maturity, canonical identity, or permanent-KB authority.

## 3. Proposed minimal pipeline

```text
Bounded source
    + approved contract
    + approved profile
          ↓
     Extractor adapter
          ↓
 Candidate artifact (JSON)
          ↓
 Structural validation
          ↓
 Rendered review projection (Markdown)
          ↓
 Human/agent evaluation evidence
```

Not shown because they are explicitly downstream: consolidation, identity resolution, maturity assessment, conflict resolution, promotion, publication, and KB mutation.

## 4. Proposed responsibility boundaries

| Component | Responsibility | Must not do |
|---|---|---|
| Input assembler | Package one bounded source plus provenance and selected authority documents | Add outside knowledge or query the KB |
| Extractor adapter | Invoke a configured model and capture raw response and invocation metadata | Consolidate across sources |
| Candidate parser | Convert model response into the approved candidate schema | Repair unsupported knowledge silently |
| Structural validator | Check schema, enums, required fields, and artifact integrity | Judge objective truth or canonical identity |
| Evaluation layer | Record grounding/exclusion/quality findings against source evidence | Promote candidates |
| Renderer | Produce human-readable Markdown from the machine artifact | Become a second source of truth |
| Run writer | Persist immutable inputs, outputs, findings, and hashes | Rewrite prior runs |

## 5. Pending owner decisions

### D-EA-001 — System-of-record output

**DECISION PENDING — Requires Owner Approval**

Options:

1. Markdown only.
2. JSON only.
3. JSON system artifact plus deterministic Markdown projection.

**Recommendation:** Option 3.

**Trade-off:** Two representations require renderer tests, but JSON supports validation and automation while Markdown remains reviewable. Markdown must be derived, never independently edited as authority.

### D-EA-002 — Run artifact layout

**DECISION PENDING — Requires Owner Approval**

Options:

1. Overwrite a single latest-output directory.
2. Immutable run directories with a separate latest pointer or index.
3. Database-first storage.

**Recommendation:** Option 2 for the first vertical slice.

Proposed shape:

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

**Trade-off:** More files per run, but strong provenance, replayability, and non-destructive comparison.

### D-EA-003 — First vertical slice

**DECISION PENDING — Requires Owner Approval**

Options:

1. Conversation Profile against a new general conversation.
2. Engineering extraction against one historical Stage.
3. Build both profiles and test both immediately.

**Recommendation:** Option 2, using one representative historical Stage and deriving a draft Engineering Profile from the frozen baseline.

**Reason:** Existing Stage evidence makes regression comparison possible. Option 3 widens the authority and evaluation surface too early.

### D-EA-004 — Model/provider boundary

**DECISION PENDING — Requires Owner Approval**

Options:

1. Hard-code one provider SDK.
2. Define a small provider-neutral invocation interface and implement one provider first.
3. Build a general multi-provider orchestration layer immediately.

**Recommendation:** Option 2.

The first implementation should support one real provider but persist provider/model/prompt parameters in the run manifest. Avoid an orchestration framework until a second provider creates demonstrated pressure.

### D-EA-005 — Evaluation status semantics

**DECISION PENDING — Requires Owner Approval**

Options:

1. A single pass/fail result.
2. Structural pass/fail plus separate evaluation findings.
3. Approved/rejected knowledge states during extraction.

**Recommendation:** Option 2.

Extraction can fail structurally or carry grounding/quality findings. It must not assign governance states such as approved, canonical, or mature.

## 6. Proposed first delivery sequence

1. Owner reviews D-EA-001 through D-EA-005.
2. Derive `profiles/drafts/engineering-profile-v0.1.md` from the draft contract and frozen historical baseline.
3. Define the candidate JSON schema and run manifest contract.
4. Select one Stage fixture and record expected evaluation questions, not a forced golden output.
5. Implement a local CLI vertical slice with one provider.
6. Compare its artifact with the historical output and record defects.
7. Review contract/profile friction before freezing either document.

## 7. Risks

- **Premature schema lock-in:** a schema can encode unresolved consolidation concepts.
- **False goldens:** historical Stage outputs contain useful evidence and defects; exact-text equality would preserve mistakes.
- **Renderer drift:** separately editable JSON and Markdown create two competing truths.
- **Provider leakage:** SDK-specific fields can contaminate the domain contract.
- **Authority collapse:** calling candidates approved knowledge would merge extraction and governance.
- **Sensitive-source exposure:** future private conversations require explicit retention, redaction, and access controls before production use.

## 8. Completion criteria for Stage 0

Stage 0 completes only when:

- D-EA-001 through D-EA-005 have explicit owner dispositions;
- governance and ADR document responsibilities are accepted;
- the first vertical slice and its evidence source are selected;
- no pending decision is accidentally recorded as accepted architecture.
