# Engineering Knowledge Extraction

Stage Source Current Chat Session
Specification Engineering Knowledge Extraction Specification v1.0.1 

---

# Engineering Principles

## 1. Specification Must Eliminate Multiple Reasonable Interpretations

Principle

A specification is not complete until independent reviewers converge on the same implementation interpretation without requiring additional discussion.

Why

During BR-005 review, two valid engineering interpretations emerged from the phrase appears in. Neither implementation was objectively incorrect—the ambiguity existed in the specification itself. The resolution was to strengthen the specification rather than change a correct implementation.

Trade-offs

 Gains

   Predictable implementation
   Consistent multi-reviewer outcomes
   Lower implementation risk

 Sacrifices

   More verbose specifications
   Higher specification-writing effort

When NOT to use

Prototype work or exploratory research where implementation freedom is intentional.

Related Concepts

 Specification-as-contract
 Determinism
 Contract-first development
 Ambiguity elimination

 Metadata (Audit Only)

  Source Current Stage
  Evidence Multiple BR-005 review cycles resolving appears in ambiguity via spec refinement.
  Observation Count 6
  Confidence High

---

## 2. Correct Problems at the Layer Where They Originate

Principle

When implementation differences arise from ambiguous requirements, fix the specification rather than forcing implementations to converge by convention.

Why

The BR-005 delimiter discussion demonstrated that the implementation followed one reasonable interpretation of the specification. The real defect was that the specification failed to define delimiter semantics.

Trade-offs

Gains

 Stable architecture
 Cleaner implementation
 Better long-term maintainability

Sacrifices

 Additional specification iterations
 Delayed implementation

When NOT to use

Implementation bugs that clearly violate an already precise specification.

Related Concepts

 Root-cause analysis
 Specification ownership
 Architecture governance

 Metadata

  Source Current Stage
  Evidence BR-005 delimiter discussion and subsequent spec patch.
  Observation Count 4
  Confidence High

---

## 3. Determinism Includes Input Normalization

Principle

Deterministic validation requires explicit normalization rules, not merely deterministic comparison logic.

Why

Even when comparison used exact matching, different delimiter characters (half-widthfull-width punctuation) produced inconsistent outcomes until normalization behavior was formally specified.

Trade-offs

Gains

 Cross-platform consistency
 Language-independent behavior
 Reduced hidden assumptions

Sacrifices

 Slightly larger specifications
 Additional normalization logic

When NOT to use

Free-text semantic search systems.

Related Concepts

 Canonicalization
 Input normalization
 Exact matching
 Internationalization

 Metadata

  Source Current Stage
  Evidence Full-width pipe (`｜`) discussion.
  Observation Count 4
  Confidence High

---

# Architecture Patterns

## 4. Architecture Governance Should Govern Evolution Rather Than Runtime

Principle

Governance documents should define how architecture evolves instead of becoming another runtime architecture layer.

Why

A significant portion of this stage refined governance boundaries, explicitly separating governance from runtime components.

Trade-offs

Gains

 Cleaner architecture
 Better long-term maintainability
 Clear decision ownership

Sacrifices

 Additional documentation
 Governance overhead

When NOT to use

Very small throwaway projects.

Related Concepts

 Meta-architecture
 ADR
 Decision hierarchy
 Architecture governance

 Metadata

  Source Current Stage
  Evidence Governance document refinement.
  Observation Count 5
  Confidence High

---

## 5. Defensive Validation Rules Are Valuable Even When Rarely Triggered

Principle

A validation rule may exist primarily as regression protection rather than expecting frequent failures.

Why

The discussion concluded that BR-005 passing almost all production data is acceptable because its role is protecting against future extractor regressions.

Trade-offs

Gains

 Future-proofing
 Regression detection

Sacrifices

 Lower visible runtime impact
 Additional maintenance

When NOT to use

Performance-critical validation pipelines where every rule must justify runtime cost.

Related Concepts

 Defensive programming
 Regression prevention
 Validation layers

 Metadata

  Source Current Stage
  Evidence BR-005 effectiveness discussion.
  Observation Count 3
  Confidence Medium

---

# Development Workflow

## 6. Separate Specification Review From Implementation Review

Principle

Do not mix specification correctness with implementation correctness in a single review cycle.

Why

The workflow consistently distinguished

Specification Review → Specification Patch → Implementation → Implementation Review.

This prevented implementation changes from compensating for specification defects.

Trade-offs

Gains

 Cleaner reviews
 Reduced scope creep
 Better traceability

Sacrifices

 More review iterations

When NOT to use

Tiny personal scripts.

Related Concepts

 Stage gates
 Design review
 Contract-first

 Metadata

  Source Current Stage
  Evidence Entire BR-005 review workflow.
  Observation Count 7
  Confidence High

---

## 7. Living Handoff Documents Improve AI Collaboration

Principle

Maintain a concise, continuously updated project status dashboard specifically for AI handoff rather than treating README as operational state.

Why

The stage refined `current-status` several times to eliminate stale information and improve future AI continuity.

Trade-offs

Gains

 Faster onboarding
 Reduced context rebuilding

Sacrifices

 Manual synchronization effort

When NOT to use

Very short-lived projects.

Related Concepts

 AI memory
 Operational dashboard
 Project continuity

 Metadata

  Source Current Stage
  Evidence Multiple revisions of current-status dashboard.
  Observation Count 5
  Confidence High

---

# AI Collaboration Patterns

## 8. Independent AI Reviews Reveal Specification Weakness Better Than Consensus

Principle

Allow multiple reviewers to independently interpret the same specification before reconciling differences.

Why

The disagreement between reviewers exposed specification ambiguity that neither reviewer alone could have conclusively identified.

Trade-offs

Gains

 Better specifications
 Hidden assumptions surfaced

Sacrifices

 More review time
 More reconciliation work

When NOT to use

Routine maintenance tasks.

Related Concepts

 Independent verification
 Multi-agent review
 Consensus building

 Metadata

  Source Current Stage
  Evidence GPT vs Claude discussion around BR-005.
  Observation Count 6
  Confidence High

---

# Decision Frameworks

## 9. Downgrade Issues When New Evidence Changes Their Nature

Principle

Engineering reviews should allow issue severity to decrease when later evidence demonstrates that the original concern belonged to another layer.

Why

Several initially classified Blocking issues were later downgraded after determining that the true problem existed in the specification rather than the implementation.

Trade-offs

Gains

 More objective reviews
 Better engineering culture

Sacrifices

 Requires willingness to revise previous conclusions

When NOT to use

Safety-critical certification where review states are immutable.

Related Concepts

 Evidence-based review
 Severity calibration
 Root-cause correction

 Metadata

  Source Current Stage
  Evidence Reclassification of BR-005 implementation findings.
  Observation Count 4
  Confidence High

---

# Rejected Decisions

### Reject Fix Correct Implementations to Compensate for Ambiguous Specifications

Why rejected

The ambiguity originated in the specification.

Would become valid when

The implementation clearly violates an unambiguous specification.

---

### Reject Semantic Validation for Source References

Why rejected

Semantic interpretation violates deterministic business-rule architecture.

Would become valid when

A future QA layer explicitly introduces semantic verification outside deterministic validators.

---

# Anti-patterns

### Encoding Engineering Decisions Inside Implementation Only

Why harmful

Hidden assumptions become invisible to future implementers and reviewers.

---

### Treating Dashboards as Automatically Accurate

Why harmful

Operational dashboards quickly become stale unless their maintenance policy is explicitly defined.

---

# Decision Heuristics

### Heuristic 1 — Specification vs Implementation

```text
Reviewer disagreement
        ↓
Locate disagreement source
        ↓
Specification ambiguity
        ↓
YES → Patch specification
NO
        ↓
Patch implementation
```

---

### Heuristic 2 — Issue Classification

```text
Potential defect
      ↓
Violates current specification
      ↓
Yes → Implementation issue
      ↓
No
      ↓
Specification ambiguous
      ↓
Yes → Specification issue
      ↓
Clarify specification first
```

---

### Heuristic 3 — Multi-AI Review

```text
Independent reviews
        ↓
Identify disagreements
        ↓
Determine whether disagreement
comes from reviewer judgment
or specification wording
        ↓
If wording →
Improve specification
rather than forcing reviewer consensus
```

---

這一輪抽取共保留了 9 個長期可重用 Knowledge Items、2 個 Rejected Decisions、2 個 Anti-patterns、以及 3 個 Decision Heuristics。所有項目均依據本 Stage 的實際討論、決策、分歧與修正過程整理，符合 v1.0.1 的 Grounding Requirement。
