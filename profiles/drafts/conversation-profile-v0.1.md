# Conversation Profile

**Extends:** Extraction Contract v0.1
**Version:** 0.1
**Status:** Draft — untested, pending first real run

---

## Relationship to Contract

This Profile supplies only the three things the Contract reserves for Profiles:

1. Extraction Target
2. Knowledge Type (closed enum)
3. Exclude additions

Everything else — Grounding Requirement, Item Format, Quality Filter, Deduplication, Output Rules, Out-of-Scope list — is inherited unchanged from the Contract. Do not restate or modify them here.

---

## Extraction Target

Distill durable knowledge that emerged from this exploratory conversation — knowledge that could plausibly inform thinking or decisions in a **different** conversation, on a **different** topic, later.

This conversation may cover any domain: AI architecture, systems thinking, philosophy, business, or anything else. The target is not the topic — it is the reasoning that would still hold if the topic changed.

Do not extract a summary of what was discussed. Extract what would still be worth knowing after the specific topic is forgotten.

---

## Knowledge Type (Closed Enum)

Each item must carry exactly one of these. If none fit cleanly, discard the item rather than force-fitting it.

| Type | Use when the item is... |
|---|---|
| **Principle** | A general rule that held true across the reasoning, stated prescriptively ("X should/should not..."). |
| **Mental Model** | A way of framing or structuring a problem, not a rule — a lens rather than an instruction. |
| **Framework** | A repeatable multi-step structure for making a decision or analysis (has parts/stages). |
| **Hypothesis** | A claim proposed but not settled within this conversation — flagged as uncertain by the conversation itself. |
| **Observation** | A pattern or fact noticed and reasoned about, without being generalized into a rule. |
| **Open Question** | A question that was raised and left genuinely unresolved — not rhetorical. |
| **Pitfall** | A failure mode or trap identified — something to avoid, with a reason why it goes wrong. |
| **Counterargument** | An objection or opposing view that was seriously engaged with, not just mentioned in passing. |

If an item could fit two types, choose the one closer to how it was actually treated in the conversation (e.g. if it was floated as uncertain, it's a Hypothesis even if it sounds like a Principle).

---

## Exclude (in addition to Contract-level exclusions)

Do **NOT** extract:

- casual small talk, greetings, logistics ("remind me to...", scheduling)
- purely emotional or venting exchanges without a generalizable insight
- factual trivia that was simply stated and accepted, not reasoned through or contested
- test/debug exchanges about the tool itself (e.g. testing this very extraction process)
- restatements of things the person already knew and just confirmed

---

## Notes for First Run

This Profile has not been run against a real conversation yet. Things to watch for and report back on, per the Contract's Freeze Policy:

- Does the Knowledge Type enum actually cover what comes up, or does content keep landing in "none of these fit"?
- Does Principle vs Mental Model, or Hypothesis vs Open Question, cause visible miscategorization?
- Is the Grounding Requirement (inherited from Contract) too strict for non-decision-based reasoning, or does it work as intended?

Do not revise this Profile speculatively before running it once. Collect real friction first.

---

End of Profile (Draft)
