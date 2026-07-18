# Engineering Profile

**Extends:** Extraction Contract v0.1  
**Version:** 0.1  
**Status:** Draft — pending review and first bounded-source run  
**Derived from:** Frozen Engineering Knowledge Extraction Specification v1.0.1 and observed Stage 1–7 outputs

## Relationship to Contract

This Profile supplies only the domain authority reserved for Profiles:

1. Extraction Target
2. Knowledge Type closed enum
3. Engineering-specific exclusions

The Contract's grounding requirement, item skeleton, quality filter, in-source deduplication, output rules, and downstream exclusions remain unchanged.

## Extraction Target

Distill durable engineering knowledge that emerged from one bounded engineering conversation or project stage and could guide decisions in a genuinely different software project, programming language, repository, team, or technology stack.

Extract the reusable reasoning behind engineering choices, not the project record. Preserve trade-offs and applicability limits. Project-specific detail may appear only where needed to identify the source evidence grounding an item.

## Knowledge Type — Closed Enum

Every candidate item must use exactly one value:

| Value | Use when the item is |
|---|---|
| **Engineering Principle** | A prescriptive engineering rule or constraint |
| **Architecture Pattern** | A reusable division of responsibilities, boundary, data flow, or system structure |
| **Development Workflow** | A repeatable sequence for planning, implementation, handoff, or change control |
| **Testing Strategy** | A reusable approach to verification, regression control, fixtures, or test scope |
| **Repository & Git Practice** | A reusable repository, branch, commit, review, or release practice |
| **AI Collaboration Pattern** | A reusable allocation of work, evidence, authority, or review among humans and AI systems |
| **Decision Framework** | A repeatable method for comparing alternatives and reaching engineering decisions |
| **Pitfall** | A grounded failure mode or anti-pattern, including why it fails |
| **Rejected Alternative** | A seriously considered option that was rejected, including the rejection conditions and when it could become valid |

If an item fits more than one value, use the type closest to how the source treated it. Do not duplicate one item under multiple types.

## Exclude — In Addition to Contract Exclusions

Do not extract:

- milestone, ticket, PR, branch, commit, or deployment status;
- filenames, identifiers, version numbers, or repository layout unless they ground a reusable practice;
- one-off defects, environment failures, encoding problems, or temporary workarounds without a generalized engineering lesson;
- implementation details that do not expose a reusable boundary, trade-off, or failure mode;
- generic best practices introduced by the extractor but not articulated or applied in the source;
- a list of technologies, tools, models, or libraries without grounded selection reasoning;
- praise, approval, or review outcomes that contain no reusable engineering judgment;
- project policy as if it were universally applicable engineering knowledge.

## Engineering-Specific Quality Questions

After applying the Contract's four required questions, also ask:

1. Does the item preserve an engineering judgment, trade-off, failure mode, or repeatable method actually present in the source?
2. Could another engineering team apply it without knowing the source project's domain?
3. Has project history been removed without removing the evidence pointer?
4. If typed as a Rejected Alternative, are the rejection reason and possible validity conditions both present?

If any required answer is No, discard the item.

## First-Run Evaluation Notes

The first run must record evidence about:

- whether the nine types are distinguishable in practice;
- whether Testing Strategy and Development Workflow overlap excessively;
- whether Repository & Git Practice deserves a separate type;
- whether Pitfall and Rejected Alternative are consistently separated;
- whether the Contract's common item skeleton can represent the historical baseline's “When NOT to use” content through Trade-offs / Limitations;
- whether the profile produces useful items without recreating historical section headings as padding.

Do not revise the enum merely because a historical output used a different heading. Revise only from bounded-source run evidence.

---

End of Engineering Profile (Draft)
