# G1 Source Fixture Admission

**Status:** Proposal — Draft PR under review; G1-A source-selection record complete, G1-B exact-source admission gate closed
**Admission ID:** G1
**Created:** 2026-07-20
**Last patched:** 2026-07-20 (G1-B gate closed: all four requirements satisfied)
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

## 3b. Admission Framework — G1-A and G1-B

This admission record distinguishes two phases:

| Phase | What it establishes | Status |
|---|---|---|
| **G1-A — Source selection / admission candidate** | Source identity (`engineering-stage-01`), provenance, bounded scope, private handling rules, historical-output status | ✅ Complete in this record |
| **G1-B — Exact source admission gate** | Direct inspection of actual source artifact, final sensitive-data determination, `original` vs `redacted_derivative` decision, SHA-256 binding of exact admitted bytes **before execution** | ✅ Complete — all four G1-B requirements satisfied in this record |

**The source is fully admitted.** G1-A established *what* source was selected and *why*; G1-B now establishes *exactly which bytes* will be used and that they pass the sensitivity gate. Execution authority is a separate gate governed by the project's implementation and review framework (see §10 Explicit Exclusions).

---

## 4. Sensitive-Data Assessment

**Status:** ✅ Complete — Owner/source-provider direct inspection confirmed; source cleared for private evaluation

| Field | Value |
|---|---|
| **outcome** | `cleared_for_private_evaluation` |
| **checked_at** | 2026-07-20 |
| **checked_by** | Owner/source-provider direct inspection |
| **inspection_scope** | Original Stage 1 transcript (`engineering-stage-01`) — full content reviewed |
| **historical_scope** | Historical extraction output `tests/fixtures/stage-outputs/stage-01.md` |
| **notes** | The Owner/source-provider directly inspected the original Stage 1 transcript. The transcript contains engineering knowledge discussion only (principles, patterns, workflows, practices, pitfalls). No personal data, credentials, or confidential material is present. The source is cleared for private evaluation use. The original transcript remains outside the repository in the private external source store. |

**G1-B complete for sensitive-data:** Direct inspection performed by the Owner/source-provider. No restricted content found. Final outcome recorded as `cleared_for_private_evaluation`. The source is cleared for admission but execution is a separate gate (see §10).

---

## 5. Evaluation Source Determination

**Status:** ✅ Complete — relation determined

| Field | Value |
|---|---|
| **relation** | `original` |
| **decision** | The evaluation source is the original private Stage 1 ChatGPT transcript. The Owner/source-provider directly inspected the transcript and confirmed no restricted content exists (`cleared_for_private_evaluation`). No redacted derivative is required. The original transcript is held in the private external source store, not in this repository. |

**G1-B complete for relation:** Relation established as `original`. The source artifact is the original transcript; no redacted derivative is required. The original remains externally stored.

---

## 6. Deterministic Digest / Immutable Source Identity

**Status:** SHA-256 digest recorded in this admission record; source artifact held in private external source store

| Field | Value |
|---|---|
| **Digest algorithm** | SHA-256 |
| **Current digest** | `7184dcc452e948bac8e11ea2e494c18b84d201c678391530753469e13e311c72` |
| **Source location** | Private external source store (not in this repository) |
| **Binding requirement** | The SHA-256 digest of the exact admitted source artifact **must be recorded in this admission record before any extraction run executes**. The digest is not deferred to run time. The run manifest will redundantly record the digest of the source copy placed in `data/runs/<run_id>/input/`, but that is a consistency check, not the primary binding. |
| **Primary binding** | This admission record, patched with the SHA-256 of the exact source artifact, becomes the immutable identity anchor. A run manifest referencing a different byte-level source would not satisfy this admission. |

**G1-B complete — all four requirements satisfied:** SHA-256 digest computed and recorded (`7184dcc452e948bac8e11ea2e494c18b84d201c678391530753469e13e311c72`). Direct source inspection by Owner/source-provider confirmed. Final sensitive-data determination: `cleared_for_private_evaluation`. Relation: `original`. The source artifact is held in the private external source store. Execution is a separate gate — not authorized by this admission (see §10).

---

## 7. Handling and Location Rules

1. **The original source transcript is private and must not be committed to this repository.**
2. The source artifact is held in a private external source store, not in this repository. Only its SHA-256 digest (`7184dcc452e948bac8e11ea2e494c18b84d201c678391530753469e13e311c72`) is recorded here to bind the logical source ID to the exact bytes.
3. Only the following safe metadata is recorded in this admission record:
   - source_id and provenance description;
   - sensitive-data assessment outcome;
   - digest algorithm specification;
   - SHA-256 digest of the exact source artifact;
   - source location (private external store);
   - handling rules (this section).
4. When a run is performed, the source transcript must be placed at `data/runs/<run_id>/input/source.txt` (per the run layout specified in `specs/drafts/artifact-contracts-v0.1.md`) and its SHA-256 must be recorded in the run manifest.
5. No copy of the source transcript may exist outside the run directory tree after completion unless separately governed by an explicit retention/access policy.
6. If a redacted derivative is later required, it must be created from the preserved original, documented in a new admission record, and the original must never be silently overwritten.

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

This admission record satisfies the **G1-A source-selection/evidence requirements** stated in `docs/current-status.md` ("Source fixture blocker") and `docs/architecture.md` (§ Input assembler). The **G1-B exact-source admission gate is closed** — all four requirements satisfied.

| Requirement | G1-A status | G1-B outstanding |
|---|---|---|
| Source identity, provenance, and bounded scope recorded | ✅ Sections 1–3 | — |
| Sensitive-data selection check | ✅ `cleared_for_private_evaluation` — Owner direct inspection (Section 4) | — |
| Original preserved or redacted derivative recorded | ✅ Relation: `original`; handling rules defined (Sections 5, 7); original preserved outside repo | — |
| Deterministic digest / immutable identity | ✅ `7184dcc452e948bac8e11ea2e494c18b84d201c678391530753469e13e311c72` recorded (Section 6); source held in private external store | — |
| Historical output remains comparison evidence | ✅ Section 8 | — |

**The source fixture blocker in `docs/current-status.md` is resolved for admission.** The G1 source is fully admitted (G1-A selection record + G1-B exact-source gate). Execution is a separate gate — no extraction run is authorized by this admission (see §10).

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
