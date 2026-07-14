# Engineering Principles

## **Specification Before Implementation**

**Principle** — Stabilize the behavioral specification before writing implementation code whenever rule interpretation contains ambiguity.

**Why** — Multiple implementation ambiguities (for example, exact matching vs. substring matching, per-item validation, and cross-field behavior) were discovered before coding. Resolving them in the specification prevented implementers from inventing behavior not explicitly intended.

**Trade-offs** — Slower upfront progress and additional specification iterations, but significantly fewer implementation rewrites and review cycles.

**When NOT to use** — Small exploratory prototypes where discovering the specification is itself the goal.

**Related Concepts**

* Contract-first development
* Executable specifications
* Domain modeling
* Behavioral contracts

> **Metadata**
>
> * **Source:** Current Stage (BR-002 specification refinement)
> * **Evidence:** Multiple implementation ambiguities were resolved by modifying the specification before allowing implementation.
> * **Observation Count:** 6+
> * **Confidence:** High

---

## **Treat Specifications as the Single Source of Behavioral Truth**

**Principle** — Implementation should follow explicit specification rather than developer inference whenever business semantics are involved.

**Why** — Keyword sets, matching rules, overlapping findings, and field semantics were explicitly defined in the specification to prevent implementation from silently introducing policy decisions.

**Trade-offs** — Specifications become more detailed and require maintenance, but implementation becomes deterministic and reviewable.

**When NOT to use** — Internal implementation details that intentionally remain hidden behind an abstraction boundary.

**Related Concepts**

* Source of truth
* Specification-driven development
* Deterministic behavior
* Traceability

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Repeated decisions to encode implementation behavior into the specification before coding.
> * **Observation Count:** 5+
> * **Confidence:** High

---

# Architecture Patterns

## **Layered Validation Responsibilities**

**Principle** — Separate structural validation from semantic validation, and further separate coarse validation from fine-grained validation.

**Why** — The discussion repeatedly reinforced that different validation layers exist for different responsibilities. Broad presence checks should not attempt to validate detailed semantic correctness.

**Trade-offs** — Requires multiple validation layers and careful ownership boundaries, but each rule becomes simpler and more maintainable.

**When NOT to use** — Very small validation systems where all checks naturally belong to a single layer.

**Related Concepts**

* Separation of concerns
* Validation pipeline
* Layered architecture
* Rule decomposition

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Discussion around BR-001, BR-002, and identifying a future rule instead of expanding existing responsibilities.
> * **Observation Count:** 4+
> * **Confidence:** High

---

## **Preserve Independent Rule Evaluation**

**Principle** — Allow multiple business rules to independently report findings on the same data instead of suppressing overlaps inside the rule engine.

**Why** — The stage concluded that overlapping findings represent different semantic concerns. Deduplication, if desired, belongs in presentation or reporting layers rather than individual validators.

**Trade-offs** — Validation output may contain multiple findings for one field, but rule independence and traceability remain intact.

**When NOT to use** — Systems where downstream consumers cannot tolerate duplicated diagnostics and no reporting layer exists.

**Related Concepts**

* Separation of concerns
* Independent validation
* Reporting layer
* Diagnostics

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Explicit decision around overlapping BR-001 and BR-002 findings.
> * **Observation Count:** 3
> * **Confidence:** High

---

# Development Workflow

## **Separate Specification Commits from Implementation Commits**

**Principle** — Treat specification refinement and implementation as different engineering changes, each with its own commit.

**Why** — Separating behavioral decisions from implementation makes project history easier to audit and allows future readers to understand why behavior changed independently of how it was implemented.

**Trade-offs** — Produces more commits but significantly improves historical traceability.

**When NOT to use** — Throwaway experiments without long-term maintenance requirements.

**Related Concepts**

* Atomic commits
* Traceability
* Change history
* Design documentation

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Multiple discussions about splitting specification, implementation, review patches, and cleanup into independent commits.
> * **Observation Count:** 5+
> * **Confidence:** High

---

## **Independent AI Review Should Validate Decisions, Not Merely Code**

**Principle** — Use an independent reviewer to verify that implementation matches the agreed specification, not simply to search for programming mistakes.

**Why** — Reviews repeatedly compared implementation against specification, verified behavioral consistency, identified specification gaps, and rejected undocumented implementation decisions.

**Trade-offs** — Additional review time, but substantially stronger confidence in behavioral correctness.

**When NOT to use** — Early exploratory coding where specifications intentionally remain fluid.

**Related Concepts**

* Independent verification
* Design review
* Specification compliance
* Code review

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Independent reviews focused on specification conformance rather than syntax or style.
> * **Observation Count:** 6+
> * **Confidence:** High

---

# Testing Strategy

## **Convert Explicit Specification Constraints into Regression Tests**

**Principle** — Whenever a specification explicitly prohibits a future implementation behavior, create a regression test protecting that prohibition.

**Why** — Exact-match behavior was intentionally protected by introducing regression tests specifically preventing later developers from replacing exact matching with substring matching.

**Trade-offs** — Slightly larger test suite, but protects intentional design decisions from future regressions.

**When NOT to use** — Behavior that intentionally remains implementation-defined.

**Related Concepts**

* Regression testing
* Specification testing
* Behavioral contracts
* Negative testing

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Discussion leading to creation of an exact-match regression test.
> * **Observation Count:** 3
> * **Confidence:** High

---

# Repository & Git Practices

## **Repository Cleanup Should Be an Independent Maintenance Activity**

**Principle** — Repository hygiene tasks should remain separate from functional development.

**Why** — Removing obsolete placeholder files was intentionally separated from feature implementation to keep commits focused and reduce future confusion.

**Trade-offs** — Produces additional maintenance commits but results in cleaner repository history.

**When NOT to use** — Emergency fixes where minimizing deployment time is more important than commit granularity.

**Related Concepts**

* Repository hygiene
* Atomic commits
* Technical debt
* Maintenance

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Dedicated cleanup task and separate commit for removing unused placeholder files.
> * **Observation Count:** 3
> * **Confidence:** High

---

# AI Collaboration Patterns

## **Assign AI Roles by Engineering Responsibility**

**Principle** — Divide AI assistants according to engineering responsibility rather than allowing every assistant to perform every task.

**Why** — The workflow consistently separated architecture design, implementation, testing, and independent review into distinct AI roles, reducing confirmation bias and duplicated reasoning.

**Trade-offs** — Requires coordination between tools but produces stronger verification and clearer accountability.

**When NOT to use** — Small one-off tasks where orchestration overhead outweighs the benefits.

**Related Concepts**

* Multi-agent workflows
* Separation of responsibilities
* Independent verification
* AI orchestration

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Repeated use of separate architecture, implementation, review, and patch phases.
> * **Observation Count:** 7+
> * **Confidence:** High

---

# Decision Frameworks

## **Resolve Ambiguity by Making Unknowns Explicit Rather Than Implicit**

**Principle** — Whenever implementation requires guessing, convert that ambiguity into an explicit specification decision instead of embedding assumptions into code.

**Why** — Several implementation questions were deliberately converted into documented behavioral rules before coding proceeded.

**Trade-offs** — More design discussions upfront, but far fewer hidden assumptions inside implementation.

**When NOT to use** — Exploratory research where uncertainty itself is the object of investigation.

**Related Concepts**

* Explicit contracts
* Decision records
* Behavioral specifications
* Domain modeling

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Multiple specification updates defining keyword sets, matching rules, and field semantics before implementation.
> * **Observation Count:** 6+
> * **Confidence:** High

---

# Pitfalls & Lessons Learned

## **Future Validation Gaps Should Become New Rules, Not Hidden Complexity**

**Principle** — When discovering a legitimate validation scenario outside a rule's intended responsibility, capture it as future work instead of expanding the current rule.

**Why** — A missing validation scenario was intentionally documented as a future rule rather than increasing the responsibility of an existing validator.

**Trade-offs** — Additional future implementation work, but cleaner rule boundaries.

**When NOT to use** — When the discovered behavior is actually part of the current rule's published contract.

**Related Concepts**

* Scope control
* Backlog management
* Single responsibility
* Incremental architecture

> **Metadata**
>
> * **Source:** Current Stage
> * **Evidence:** Decision to create a future rule instead of expanding an existing validator.
> * **Observation Count:** 2
> * **Confidence:** High

---

# Rejected Decisions

* **Embed undocumented business assumptions directly into implementation**

  * **Rejected because:** Business semantics should be decided in the specification, not inferred during coding.
  * **Would become valid if:** The specification explicitly delegates the behavior to implementation.

* **Merge repository cleanup into feature commits**

  * **Rejected because:** It obscures historical traceability and mixes unrelated responsibilities.
  * **Would become valid if:** Cleanup is inseparable from the functional change.

* **Deduplicate overlapping validation findings inside business rules**

  * **Rejected because:** It couples validation logic with presentation concerns.
  * **Would become valid if:** The validation engine itself becomes the final presentation layer.

---

# Anti-patterns

* Allowing implementation to invent business semantics that are absent from the specification.
* Expanding existing rules to absorb unrelated validation responsibilities instead of introducing new rules.
* Mixing specification changes, implementation, cleanup, and review fixes into a single commit.
* Relying on substring matching when the specification intentionally defines exact-match behavior.
* Embedding report-formatting concerns inside validation logic.

---

# Decision Heuristics

* Resolve behavioral ambiguity in the specification before implementation.
* Introduce a new rule when a discovered validation concern falls outside an existing rule's responsibility.
* Preserve independent rule evaluation; defer presentation concerns to downstream layers.
* Convert explicit specification constraints into regression tests.
* Prefer multiple small, responsibility-focused commits over large mixed-purpose commits.
