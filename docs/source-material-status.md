# Source Material Status

## Authority map

| Material | Repository location | Status | Intended use |
|---|---|---|---|
| Engineering Knowledge Extraction Specification v1.0.1f | `specs/baselines/engineering-knowledge-extraction-v1.0.1.md` | Frozen historical baseline | Reproduce and evaluate the Stage 1–7 extraction runs |
| Extraction Contract v0.1 | `specs/drafts/extraction-contract-v0.1.md` | Draft, not frozen | Candidate domain-agnostic extraction contract |
| Conversation Profile v0.1 | `profiles/drafts/conversation-profile-v0.1.md` | Draft, not frozen | Candidate profile extending the draft contract |
| Stage 1–7 outputs | `tests/fixtures/stage-outputs/` | Observational test evidence | Review variance, defects, and regression behavior |

## Duplicate baseline decision

Two uploaded files both declared Engineering Knowledge Extraction Specification v1.0.1 as frozen. The file carrying the `v1.0.1f` name is retained as the historical baseline because it is the final-form version used in the reviewed Stage runs. The alternate formatting/version is intentionally not duplicated in the repository.

This decision records file placement only. It does not promote the historical engineering specification into the future universal extraction contract.

## Governance rule

File format does not confer authority. Draft, frozen baseline, test evidence, approved contract, and canonical knowledge must remain distinguishable in both repository location and document metadata.
