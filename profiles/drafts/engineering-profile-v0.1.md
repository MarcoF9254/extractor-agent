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

### Contract escape hatch / self-check

If any Profile-local instruction, exclusion, or Knowledge-Type assignment would produce an item that violates the Contract's grounding requirement (`normalized_statement` must be directly supported by source evidence), quality filter (any required answer to the Contract's four questions is No), or downstream exclusions, the **Contract prevails**. The Profile is an extension, not an override.

Before outputting each candidate, verify that no Profile-local decision (type assignment, exclusion application, scope narrowing) has silently evaded a Contract constraint that would have blocked the item if the Contract alone were evaluated. This is a self-check; it does not modify the Contract or create new Contract obligations.

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
5. **Knowledge Type cannot rescue a failed item.** Does this item pass all four Contract quality questions **independent of** which Knowledge Type is assigned? If a question fails for the item as a candidate, assigning a different or permissive type does not fix it. The Knowledge Type is a classification of a passing item, not a quality pass itself.

If any required answer is No, discard the item.

## First-Run Evaluation Notes

The first run must record evidence about:

- whether the nine types are distinguishable in practice;
- whether Testing Strategy and Development Workflow overlap excessively;
- whether Repository & Git Practice deserves a separate type;
- whether Pitfall and Rejected Alternative are consistently separated;
- whether the Contract's common item skeleton can represent the historical baseline's "When NOT to use" content through Trade-offs / Limitations;
- whether the profile produces useful items without recreating historical section headings as padding.

### Observation / Open Question enum-pressure notes

The historical Stage 1 output contains items that are descriptive observations or open questions rather than prescriptive engineering knowledge. The 9-type closed enum was designed before bounded-source run evidence against a real Stage transcript. This evaluation note records the following open questions for the first-run evidence:

- Does the 9-type enum force an item into a type it does not fit, producing a plausible-sounding but inaccurate knowledge item?
- If so, is the right response to discard the item (the item fails the quality gate), or does the enum need revision?
- Would adding an Observation or Open Question type improve coverage of genuine source content that is neither prescriptive nor a pitfall nor a rejected alternative — or would it create a dumping ground for items that failed the quality filter?
- Can the existing Rejected Alternative type accommodate open questions that were seriously considered and remain unresolved, or does that stretch the type's semantics?

These questions are recorded for evaluation evidence only. They do not change the 9-type enum. The enum may be revised only from bounded-source run evidence per the rule below.

Do not revise the enum merely because a historical output used a different heading. Revise only from bounded-source run evidence.

---

End of Engineering Profile (Draft)
