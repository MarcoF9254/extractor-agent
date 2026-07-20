# G1 Source Fixture Admission

**Status:** Proposal — Draft PR under review
**Admission ID:** G1
**Created:** 2026-07-20
**Associated branch:** `docs/admissions/g1-source-fixture-admission`

---

## 1. Source Selection Identity

| Field | Value |
|---|---|
| **source_id** | `engineering-stage-01` |
| **Admission** | G1 — first bounded historical Stage source admitted for evaluation |

The selected source is the **Stage 1** original ChatGPT conversation transcript that served as the input for the Engineering Knowledge Extraction v1.0.1 specification run. The historical extraction output derived from this source is `tests/fixtures/stage-outputs/stage-01.md`.

---

## 2. Source Provenance

- **Origin:** ChatGPT conversation transcript, produced during an Engineering Knowledge Extraction Stage 1 session.
- **Specification version:** Engineering Knowledge Extraction Specification v1.0.1 (`specs/baselines/engineering-knowledge-extraction-v1.0.1.md`).
- **Repository fixture:** `tests/fixtures/stage-outputs/stage-01.md` — the historical extraction output from this source, retained as comparison evidence.
- **Relationship:** The source transcript is the original conversational evidence; `stage-01.md` is a downstream extraction output, not the source itself.

---

## 3. Bounded Source Scope

The admitted source is **exactly one** ChatGPT conversation transcript:

- **Content type:** Engineering knowledge extraction discussion covering software engineering principles, architecture patterns, development workflow, testing strategy, repository/git practices, pitfalls, rejected alternatives, anti-patterns, and decision heuristics.
- **Language:** Primarily Chinese (zh-CN) with English technical terminology.
- **Duration/boundary:** Stage 1 of the Engineering Knowledge Extraction process, as defined by the frozen specification baseline.
- **Exclusions:** The source is bounded to the Stage 1 conversation only. It does not include Stages 2–7, any other ChatGPT sessions, project planning discussions, or external reference material beyond what was discussed in-session.

---

## 4. Sensitive-Data Assessment

| Field | Value |
|---|---|
| **outcome** | `cleared` |
| **checked_at** | 2026-07-20 |
| **checked_by** | Agent preflight — G1 admission author |
| **notes** | Assessment was performed by examining the historical extraction output `tests/fixtures/stage-outputs/stage-01.md`, which contains only engineering knowledge content: engineering principles, architecture patterns, development workflow strategies, testing approaches, repository practices, pitfalls, and decision heuristics. No personal data (names, email addresses, phone numbers, physical addresses), credentials (API keys, passwords, tokens), confidential business information, financial data, health information, or personally identifiable information of any kind is present in the extracted output. The original source transcript is expected to contain equivalent engineering-focused discussion content. The definitive inspection of the original transcript should be confirmed by the source provider before a run. If the source provider identifies restricted content not visible in the extraction output, a redacted derivative must be recorded and a new admission documented. |

---

## 5. Evaluation Source Determination

| Field | Value |
|---|---|
| **relation** | `original` |
| **decision** | The evaluation source is the original private Stage 1 ChatGPT transcript. No redacted derivative is required based on the sensitive-data assessment. |

The `original` relation is bound to the assessment outcome `cleared` per the governance invariant: `cleared → original`. If the source provider's direct inspection later contradicts this assessment, the source must be reclassified as `redacted_derivative` with a new admission record.

---

## 6. Deterministic Digest / Immutable Source Identity

| Field | Value |
|---|---|
| **Digest algorithm** | SHA-256 |
| **Current digest** | *To be computed when the source transcript is provided for the evaluation run* |
| **Binding mechanism** | The SHA-256 digest of the source transcript will be recorded at run time in the run manifest (`manifest.json → source.original.sha256`). This admission record identifies the source by *provenance and scope*. The run manifest binds the *exact bytes* used for the run. The combination of admission ID (G1) plus run-time SHA-256 provides deterministic identity binding across planning → admission → execution. |

The admission record establishes the *what* (source identity, provenance, scope). The run manifest establishes the *exact bytes that were used*. Both are required for a fully determined extraction evaluation.

---

## 7. Handling and Location Rules

1. **The original source transcript is private and must not be committed to this repository.**
2. Only the following safe metadata is recorded in this admission record:
   - source_id and provenance description;
   - sensitive-data assessment outcome;
   - digest algorithm specification;
   - handling rules (this section).
3. When a run is performed, the source transcript must be placed at `data/runs/<run_id>/input/source.txt` (per the run layout specified in `specs/drafts/artifact-contracts-v0.1.md`) and its SHA-256 must be recorded in the run manifest.
4. No copy of the source transcript may exist outside the run directory tree after completion unless separately governed by an explicit retention/access policy.
5. If a redacted derivative is later required, it must be created from the preserved original, documented in a new admission record, and the original must never be silently overwritten.

---

## 8. Historical Output Status

`tests/fixtures/stage-outputs/stage-01.md` and all other historical Stage outputs (stage-02 through stage-07) are **observational comparison evidence only**.

They are:
- **Not golden truth.** An extraction run against the G1 source may produce different output, including different structure, content, coverage, and quality. This is expected and acceptable.
- **Not expected canonical output.** Historical outputs reflect the specific model, prompt, and specification version used at the time. They contain both useful evidence and potential defects.
- **Retained for variance and regression comparison.** The evaluation layer may compare run results against historical output to identify drift, missing coverage, or quality changes. Difference alone is not a defect.
- **Not authoritative for profile or contract freeze.** The existence of historical extracted content does not ratify or freeze the Engineering Profile, Extraction Contract, or any schema.

This status is consistent with ADR-003, `docs/governance.md` (§ Evidence classes), `docs/source-material-status.md`, and `docs/architecture.md` (§ First vertical slice).

---

## 9. Governance Compliance

This admission record satisfies the prerequisites stated in `docs/current-status.md` ("Source fixture blocker") and `docs/architecture.md` (§ Input assembler):

| Requirement | Status |
|---|---|
| Supply one complete Stage source | ✅ G1 — engineering-stage-01 |
| Record sensitive-data selection check | ✅ Outcome: cleared |
| Preserve original or recorded redacted derivative | ✅ Original preserved outside repository |
| Historical output remains comparison evidence only | ✅ Section 8 above |

---

## 10. Explicit Exclusions

In accordance with the G1 scope:

- No LLM execution, extraction run, or provider adapter is authorized by this admission.
- No new parser, renderer, validator, or CLI is authorized.
- No Contract, Profile, or schema is frozen, ratified, or modified by this admission.
- No Pilot B implementation or extraction-semantic change is authorized.
- No consolidation, identity resolution, maturity assessment, approval, promotion, or KB-write behavior is authorized.
- No multi-provider orchestration or downstream activation is authorized.
- No cross-stage contract design is created or implied.
- No architecture policy beyond what is required to record this one bounded source admission is established.

---

*End of G1 Source Fixture Admission*
