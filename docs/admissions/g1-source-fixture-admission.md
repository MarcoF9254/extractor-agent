# G1 Source Fixture Admission

**Status:** Proposal — Draft PR under review; G1-A source-selection record complete, G1-B exact-source admission gate open
**Admission ID:** G1
**Created:** 2026-07-20
**Last patched:** 2026-07-20
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
| **G1-B — Exact source admission gate** | Direct inspection of actual source artifact, final sensitive-data determination, `original` vs `redacted_derivative` decision, SHA-256 binding of exact admitted bytes **before execution** | ⏳ Outstanding — see Sections 4–6 below |

**The source is not fully admitted for execution until G1-B is closed.** G1-A establishes *what* source was selected and *why*; G1-B establishes *exactly which bytes* will be used and that they pass the sensitivity gate.

---

## 4. Sensitive-Data Assessment

**Status:** Provisional / pending direct source inspection — G1-B gate not yet closed

| Field | Value |
|---|---|
| **outcome** | `pending_source_inspection` |
| **checked_at** | 2026-07-20 |
| **checked_by** | Agent preflight — G1 admission author |
| **scope** | Historical extraction output `tests/fixtures/stage-outputs/stage-01.md` |
| **notes** | Assessment was performed against the historical extraction output only. The extracted content contains only engineering knowledge (principles, patterns, workflows, practices, pitfalls). No personal data, credentials, or confidential material is visible in the extracted output. **The original Stage 1 transcript itself has not been directly inspected.** The definitive sensitive-data determination requires the Owner/source provider to inspect the actual source artifact. If restricted content is found, a redacted derivative must be created and recorded. |

**G1-B requirement:** Direct inspection of the actual source artifact by the Owner/source provider, followed by a final outcome of `cleared` or `redacted_derivative`. Until that inspection is recorded, the sensitive-data gate is not closed.

---

## 5. Evaluation Source Determination

**Status:** Pending — depends on G1-B sensitive-data gate closure

| Field | Value |
|---|---|
| **relation** | *To be determined* — depends on final sensitive-data outcome |
| **decision** | The evaluation source will be the original private Stage 1 ChatGPT transcript **if** the final sensitive-data assessment is `cleared`. If the assessment outcome is `redacted_derivative`, the evaluation source must be a recorded redacted derivative with its own path and SHA-256, while the original is preserved. The `original` / `redacted_derivative` relation cannot be determined until the Owner/source provider directly inspects the actual source artifact. |

**G1-B requirement:** After direct source inspection, record the final relation — either `original` (if cleared) or `redacted_derivative` (if restricted content exists and a derivative is created).

---

## 6. Deterministic Digest / Immutable Source Identity

**Status:** SHA-256 algorithm selected; exact digest requires G1-B gate closure

| Field | Value |
|---|---|
| **Digest algorithm** | SHA-256 |
| **Current digest** | *Not yet computed* — requires Owner/source provider to provide the exact source artifact for hashing |
| **Binding requirement** | The SHA-256 digest of the exact admitted source artifact **must be recorded in this admission record before any extraction run executes**. The digest is not deferred to run time. The run manifest will redundantly record the digest of the source copy placed in `data/runs/<run_id>/input/`, but that is a consistency check, not the primary binding. |
| **Primary binding** | This admission record, patched with the SHA-256 of the exact source artifact, becomes the immutable identity anchor. A run manifest referencing a different byte-level source would not satisfy this admission. |

**G1-B requirement:** Owner/source provider provides the actual source artifact for hashing. SHA-256 is computed and recorded here. The admission record is updated to reflect the exact digest, finalizing the identity binding before any run.

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

This admission record satisfies the **G1-A source-selection/evidence requirements** stated in `docs/current-status.md` ("Source fixture blocker") and `docs/architecture.md` (§ Input assembler). The **G1-B exact-source admission gate** remains open.

| Requirement | G1-A status | G1-B outstanding |
|---|---|---|
| Source identity, provenance, and bounded scope recorded | ✅ Sections 1–3 | — |
| Sensitive-data selection check | ✅ Provisional assessment recorded (Section 4) | ⏳ Direct source inspection by Owner, final outcome (`cleared` or `redacted_derivative`) |
| Original preserved or redacted derivative recorded | ✅ Handling rules defined (Section 7); original preserved outside repo | ⏳ Relation (`original` / `redacted_derivative`) determined after final sensitive-data outcome |
| Deterministic digest / immutable identity | ✅ Algorithm specified (SHA-256) | ⏳ Exact digest computed and recorded in this admission record before execution |
| Historical output remains comparison evidence | ✅ Section 8 | — |

**The source fixture blocker in `docs/current-status.md` is not fully resolved until all G1-B items above are closed.**

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
