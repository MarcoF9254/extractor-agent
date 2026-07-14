# Engineering Knowledge Extraction — Stage 3

---

# Engineering Principles

### EP-001 — Specification is the implementation contract

**Knowledge**

Treat the specification as the authoritative contract. Review and stabilize the specification before implementation. Implementation should conform to the finalized specification rather than evolving it during coding.

**Evidence**

Repeated throughout BR-003 and BR-004 workflow where specification reviews preceded implementation and implementation reviews were judged against the finalized specification.

**Confidence**

High

---

### EP-002 — Determinism is preferred over heuristic intelligence

**Knowledge**

When business validation requires predictable behavior, prefer deterministic rules (closed lists, exact matching, explicit workflow stages) over fuzzy matching, regex inference, NLP, or heuristic interpretation.

**Evidence**

Repeated discussion around BR-003 registration period matching and BR-004 workflow validation.

**Confidence**

High

---

### EP-003 — Business validators report, never repair

**Knowledge**

Business Rule validators should detect and report violations only. They should not mutate records, infer missing information, or silently correct data.

**Evidence**

Repeated architectural discussions defining validators as reporting components within the pipeline.

**Confidence**

High

---

### EP-004 — Validation logic should be executable from the specification

**Knowledge**

A specification should contain enough deterministic detail that two independent implementers produce equivalent validator behavior without inventing additional business logic.

**Evidence**

Repeated Claude reviews requiring specification clarification before implementation.

**Confidence**

High

---

# Architecture Patterns

### AP-001 — Specification-first development

**Pattern**

```
Specification
    ↓
Review
    ↓
Patch
    ↓
Implementation
```

Implementation begins only after specification reaches a deterministic state.

**Confidence**

High

---

### AP-002 — Execution scope is part of business rule design

**Pattern**

Business rules may only be valid within a specific workflow stage.

Example:

* Pre-QA
* Post-QA
* Pre-Publish

Execution scope should therefore be documented explicitly as part of the rule specification.

**Evidence**

BR-004 introduced an explicit Validation Scope section after review identified ambiguity.

**Confidence**

High

---

### AP-003 — Single-responsibility business rules

**Pattern**

Each Business Rule should validate exactly one business concern and should not alter the behavior of previously implemented rules.

**Confidence**

High

---

### AP-004 — Stable finding contract

**Pattern**

All Business Rules emit findings using a shared output contract rather than rule-specific formats.

Common fields include:

* index
* activity_id
* rule_id
* field
* path
* severity
* message
* recommendation

**Confidence**

High

---

# Development Workflow

### DW-001 — Multi-stage engineering review pipeline

```
Architecture
    ↓
Specification Review
    ↓
Codex Implementation
    ↓
pytest
    ↓
Local Architecture Review
    ↓
Commit
    ↓
Push
    ↓
Independent Commit Review
    ↓
Patch (if required)
```

Each stage has a distinct purpose and should not be skipped.

**Confidence**

High

---

### DW-002 — Separate specification review from implementation review

Specification review focuses on business logic, determinism, ambiguity, and rule completeness.

Implementation review focuses on code correctness, contract compliance, regression safety, and implementation fidelity.

**Confidence**

High

---

### DW-003 — Treat blocking and non-blocking feedback differently

Blocking issues must be resolved before implementation or merge.

Non-blocking observations should be recorded for later maintenance rather than delaying progress.

**Confidence**

High

---

### DW-004 — Prefer small maintenance patches

Cross-cutting improvements (helper extraction, CLI consistency, documentation synchronization) should be implemented as separate maintenance commits instead of being mixed into feature implementation.

**Confidence**

High

---

# Testing Strategy

### TS-001 — Specifications define test cases

Every deterministic branch introduced into a specification should eventually appear as explicit regression tests.

**Confidence**

High

---

### TS-002 — Test both rule logic and integration

Coverage should include:

* direct rule tests
* CLI integration
* regression against previous rules

instead of only unit testing validator functions.

**Confidence**

High

---

### TS-003 — Regression before every commit

Every commit should be gated by the full pytest suite to ensure new rules do not alter existing behavior.

**Confidence**

High

---

# Git & Repository Practices

### GP-001 — One commit, one responsibility

Separate commits for:

* specification refinement
* implementation
* maintenance
* documentation

Avoid combining unrelated changes.

**Confidence**

High

---

### GP-002 — Keep unrelated local changes isolated

When staging commits, explicitly avoid unrelated untracked or work-in-progress files.

**Confidence**

High

---

### GP-003 — Independent review should occur after push

The authoritative review should evaluate the committed Git history rather than an uncommitted working tree.

**Confidence**

High

---

# AI Collaboration Patterns

### AI-001 — Role specialization improves review quality

Assign stable responsibilities:

* Architecture → ChatGPT
* Local implementation → Codex
* Independent commit review → Claude GitHub MCP

This separation reduces confirmation bias and prevents implementation-driven architectural drift.

**Confidence**

High

---

### AI-002 — Use different review stages for different objectives

Different review stages examine different concerns:

* Specification review
* Local implementation review
* Commit-level review

Avoid collapsing them into a single review pass.

**Confidence**

High

---

### AI-003 — Local repository and remote repository serve different purposes

Treat:

* local repository as the implementation source for Codex
* GitHub as the review source for independent reviewers

Avoid mixing these sources of truth.

**Confidence**

High

---

# Pitfalls & Lessons Learned

### PL-001 — Ambiguous specifications force implementers to invent business logic

When a specification omits deterministic decision rules, implementers inevitably introduce subjective heuristics.

The correct solution is to strengthen the specification rather than relying on implementation discretion.

**Confidence**

High

---

### PL-002 — Workflow assumptions must be explicit

Concepts such as "before QA" or "newly extracted" cannot be inferred from a static data snapshot.

Execution stage assumptions should therefore be documented explicitly.

**Confidence**

High

---

### PL-003 — Avoid premature architectural cleanup

Repeated helper duplication is acceptable temporarily if immediate refactoring would increase delivery risk.

Schedule such work as dedicated maintenance instead.

**Confidence**

High

---

# Rejected Decisions

### RD-001

**Rejected**

Implement fuzzy or heuristic matching for registration timing.

**Reason**

Introduces non-deterministic behavior and implementation-specific interpretation.

**Accepted Alternative**

Closed lists, exact matching, and deterministic specification wording.

**Confidence**

High

---

### RD-002

**Rejected**

Allow implementation to decide ambiguous business behavior.

**Reason**

Different implementers would produce inconsistent validators.

**Accepted Alternative**

Clarify specifications until implementation becomes deterministic.

**Confidence**

High

---

# Anti-patterns

### APT-001 — Specification drift

Changing implementation without first updating the specification.

**Confidence**

High

---

### APT-002 — Mixing maintenance with feature delivery

Combining helper refactors, documentation cleanup, and new business logic into one commit increases review complexity and regression risk.

**Confidence**

High

---

### APT-003 — Treating independent review as optional

Skipping independent post-commit review removes an important defense against implementation bias.

**Confidence**

High

---

# Decision Heuristics

### DH-001

If reviewers can reasonably implement the specification differently, the specification is not yet complete.

**Confidence**

High

---

### DH-002

Resolve specification ambiguity before writing production code.

**Confidence**

High

---

### DH-003

When a rule depends on workflow timing, model the execution stage explicitly instead of assuming it.

**Confidence**

High

---

### DH-004

Prefer incremental convergence over large architectural rewrites.

Small deterministic improvements accumulate into a more stable architecture with lower regression risk.

**Confidence**

High
