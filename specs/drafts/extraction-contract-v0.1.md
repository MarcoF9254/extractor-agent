# Extraction Contract

**Version:** 0.1
**Status:** Draft — pending review, NOT frozen
**Last Updated:** 2026-07-09

---

## Relationship to Profiles

This document defines the **minimal, domain-agnostic contract** that any extraction pass must follow, regardless of source type.

This document does **NOT** define:

- what counts as valid knowledge in a given domain
- the specific Knowledge Type enum
- domain-specific exclusions

Those belong to a **Profile** (e.g. `engineering-profile.md`, `conversation-profile.md`), which extends this contract and supplies domain-specific values only.

**Inherited (Profile cannot change these):**

- Grounding Requirement
- Quality Filter structure
- Output Rules
- Any field reserved for Consolidation or Governance (see "Out of Scope" below)

**Domain-Supplied Content (Profile's actual responsibility — not a fill-in-the-blank):**

- `Extraction Target` statement
- the closed `Knowledge Type` enum
- `Exclude` list additions

A Profile is not a passive configuration of pre-defined options — deciding what counts as valid knowledge in a domain is real authority the Profile holds. But it never gets to touch the inherited behavior above.

If a Profile needs to deviate from the inherited section, that is a signal the Contract itself needs revision — not that the Profile should silently diverge.

---

## Scope

Extraction operates on **exactly one conversation / stage / source**, in isolation.

Extraction is **stateless**:

- It does not read the existing Knowledge Base.
- It does not know what has been extracted before, in this source or any other.
- Its output must be reproducible from the source text alone.

If a rule requires knowledge of anything outside the current source, that rule does not belong in Extraction.

Extraction produces **candidate knowledge only**. It never reads from, writes to, or modifies the permanent Knowledge Base. This is an authority constraint, distinct from statelessness above — statelessness is about what Extraction is *allowed to know*; this is about what Extraction is *allowed to change*.

---

## Grounding Requirement (Hard Constraint)

Every knowledge item **MUST** be traceable to a specific reasoning chain, question, claim, observation, trade-off, or decision **explicitly articulated within this source**.

Do **NOT** include generic knowledge that was not actually surfaced, reasoned through, or applied here — even if it is true, even if it is common knowledge in the domain.

When unsure whether something is grounded, discard it rather than include it.

---

## Knowledge Item Format (Skeleton)

Every item MUST use this shape. Profiles may rename field labels for tone (e.g. "Principle" vs "Core Statement") but MUST NOT remove or reorder the underlying structure.

**Title**

**Knowledge Type** — One value from the Profile's closed enum. Free-text types are not permitted.

**Normalized Statement** — A concise, reusable statement of the knowledge, written as abstractly and context-independently as this single source allows.

> Normalization is a **style constraint**, applied within this source only. It does NOT imply identity matching against any other item — in this source or elsewhere. Two Normalized Statements that happen to say the same thing are still separate, unresolved items until Consolidation determines otherwise. Do not rename this field "Canonical" — that term is reserved for Identity Resolution, which is explicitly out of scope (see below).

**Reasoning** — Why this holds, grounded in what was actually discussed.

**Trade-offs / Limitations** — What is gained, what is sacrificed, where it does not apply.

**Candidate Concepts** — 0–5 concepts this item appears related to, based **only** on this source's own content. Use only when meaningful — do not pad to reach a minimum count. This is a local, unverified tag — not a resolved link to any existing Knowledge Base entry. Do not attempt to match against prior extractions.

> **Metadata (Audit Only)**
>
> - Source: [conversation / stage identifier]
> - Evidence: [1-line pointer to the specific exchange grounding this item]
> - Reinforcement Count: [times this item was reinforced within this source]
> - Confidence: [High / Medium / Low — reflects how strongly *this source* supports the item, not objective truth]
>
> If every item in a batch would receive the same confidence, reconsider the evaluation.

---

## Quality Filter

Before outputting each item, ask:

1. Is this grounded in something actually articulated in this source?
2. Will this plausibly still be useful outside the immediate context that produced it?
3. Could a genuinely different context (project, conversation, domain) reuse this?
4. Is this knowledge, rather than a record of what happened (history, status, narration)?

If any answer is **No**, discard it.

Profiles may append domain-specific filter questions but may not remove the four above.

---

## Deduplication (In-Source Only)

If multiple observations **within this same source** describe the same underlying item, merge them into one stronger item.

Cross-source deduplication is explicitly out of scope (see below).

---

## Output Rules

- Do not summarize the source.
- Do not produce meeting notes or a narrative account.
- Do not explain the conversation.
- Do not include specifics (names, dates, filenames, one-off events) unless they are the evidence pointer for an item.
- Keep Metadata visually separate for audit purposes.
- Skip empty or weak categories rather than padding output.
- Produce a clean, structured chapter — not a transcript summary.

---

## Explicitly Out of Scope (belongs to later phases)

Extraction MUST NOT attempt any of the following. Listed here so future Consolidation / Governance specs know these responsibilities have not been handled yet.

| Responsibility | Why it's excluded here | Belongs to |
|---|---|---|
| Maturity assignment (Raw / Emerging / Validated) | Requires cross-source evidence; a single source cannot establish maturity | Consolidation |
| Identity Resolution / Canonical Signature (e.g. `KT-DET-001`) | Requires knowing whether this item already exists elsewhere — a `resolve()` operation, not a `generate()` operation; breaks statelessness | Consolidation / Identity Registry |
| Related Knowledge Graph Linking (resolved edges to existing KB entries) | Requires querying the KB at extraction time; only Candidate Concepts (self-contained tags) are permitted here | Consolidation |
| Cross-source deduplication / merging | Requires visibility across sources | Consolidation |
| Approve / Version / Deprecate / Conflict Resolution | Requires authority over the permanent record, not just candidate output | Governance |

---

## Future Governance Questions (Not Resolved — Do Not Design Against These Yet)

Recorded here so they are not lost, and so no rule is written to address them without evidence:

- **Extraction Granularity** — Nothing in this Contract constrains how many items a single source should yield. One agent extracting 3 items and another extracting 30 from the same source both currently satisfy this Contract. Whether this needs a norm (and what it should be) should be decided after running real extractions, not now.

These are explicitly **not** in scope for v0.1. Do not let them motivate new fields or rules until there is real extraction output to observe.

---

## Freeze Policy

This contract is a **draft**. It should not be frozen until:

1. At least one Profile (Engineering, Conversation) has been derived from it and reviewed.
2. It has been test-run against at least one real source per Profile.

Only after that cycle should this document move to `Status: Frozen`.

---

End of Contract (Draft)
