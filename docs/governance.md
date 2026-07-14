# Governance

**Status:** Draft for owner review

## Purpose

Governance is a meta-layer over architecture, specifications, implementation, validation, and release. It is not an extraction stage or runtime component.

This document adapts governance patterns proven in `monthly-agent` to the different authority boundary of `extractor-agent`.

## Governing sequence

```text
Architecture
    ↓
Specification
    ↓
Implementation
    ↓
Validation
    ↓
Release
```

Governance constrains every step without becoming part of the runtime pipeline.

## Core principles

1. **Specification precedes implementation.** Ambiguous extraction behavior must be resolved in the contract or profile before code encodes it.
2. **Evidence and authority are separate.** Source material and test runs show what exists; they do not approve policy or canonical knowledge.
3. **Format does not confer authority.** Markdown, JSON, schema validity, or model confidence cannot promote a candidate.
4. **Extraction is stateless and source-bounded.** It receives one bounded source and must not query or mutate a permanent knowledge base.
5. **Candidate output is not canonical knowledge.** Maturity, identity resolution, cross-source merging, approval, versioning, and deprecation are downstream responsibilities.
6. **Frozen baselines are immutable evidence.** Defects found in a frozen baseline are corrected prospectively in a new version, not rewritten silently.
7. **Human approval governs authority changes.** Agents may prepare evidence, options, recommendations, and projections; the owner approves contracts, profiles, architecture decisions, and promotion policy.
8. **Accepted architecture is recorded separately from proposals.** ADRs contain accepted decisions only.

## Evidence classes

| Class | Meaning | May authorize policy? |
|---|---|---|
| Source evidence | A bounded conversation, stage, or document | No |
| Observational evidence | Historical outputs, dry runs, comparisons, defects | No |
| Contractual evidence | Approved contracts, profiles, schemas, and ADRs | Only within their declared scope |
| Authority decision | Explicit owner approval | Yes |

Evidence can justify a recommendation but cannot substitute for approval.

## Document responsibilities

- `docs/architecture.md`: accepted system boundaries and runtime responsibilities.
- `docs/decisions.md`: accepted ADRs only.
- `docs/stage-0-architecture-review.md`: proposals, options, trade-offs, and recommendations.
- `specs/baselines/`: immutable historical baselines.
- `specs/drafts/` and `profiles/drafts/`: proposals with no runtime authority.
- `tests/fixtures/`: observational fixtures unless explicitly promoted to a golden expectation.

## Pending decision convention

Owner-gated proposals must be labelled:

```text
DECISION PENDING — Requires Owner Approval
```

Each pending decision must contain:

- the boundary being decided;
- viable options;
- relevant trade-offs;
- one recommendation;
- consequences of deferral.

## Review workflow

- **Architecture author:** prepares a coherent proposal and evidence map.
- **Independent reviewer:** challenges hidden assumptions, accidental policy, and boundary drift.
- **Owner:** accepts, rejects, or modifies authority-bearing decisions.
- **Implementer:** implements approved specifications.
- **Validator/reviewer:** checks conformance and regression evidence.

The author of an authority-bearing artifact should not be its only reviewer.

## Change rules

- Do not change frozen baselines to make tests pass.
- Do not treat observed Stage outputs as golden truth without an explicit decision.
- Do not add downstream consolidation fields to the extraction contract.
- Keep proposals out of ADRs until approved.
- Preserve raw sources and run artifacts; generate derived views separately.
