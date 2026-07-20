# Current Project Status

**Last updated:** 2026-07-19  
**Default branch:** `main`  
**Active proposal branch:** *none* — Pilot A merged and provisional

## Accepted baseline

Stage 0 decisions ADR-001 through ADR-005 are accepted:

- JSON is the candidate system of record;
- Markdown is a deterministic review projection;
- runs use immutable per-run directories;
- the first vertical slice uses a draft Engineering Profile and one historical Stage source;
- one provider may later be implemented behind a small provider-neutral interface;
- structural pass/fail is separate from evaluation findings;
- extraction does not assign governance or consolidation states.

The frozen engineering v1.0.1 specification remains historical evidence. Extraction Contract v0.1 and Conversation Profile v0.1 remain drafts.

## Pilot A: ChatGPT export ZIP structural inventory

**Status:** Merged and provisional  
**Merge commit:** `2c92d0cd8138b8ff879134db595337cfe3cc29b5`  
**Final reviewed head:** `4b854486990beeca27dfd6661fe7258065bdbced`  
**Owner exception:** ADR-006

Pilot A implements a bounded read-only structural inventory reader for
ChatGPT data-export ZIP archives. Its scope is:

- deterministic ZIP traversal and member validation;
- `logical_files` shard discovery from `export_manifest.json`;
- `export_files` cross-check;
- fail-closed validation (ManifestError, ShardError, SecurityError,
  ZipIntegrityError, LimitExceededError);
- deterministic JSON output to stdout;
- admission-order instrumentation proving security checks precede reads;
- synthetic fixture tests (82 passing on Python 3.11/3.12).

**Pilot A is the only authorized bounded exception** to the general
prohibition on implementation (see Hard holds below). No further
implementation beyond Pilot A is authorized.

## Source fixture blocker — G1-A source selection recorded, G1-B exact-source admission gate open

The repository contains historical extraction outputs, not their complete bounded Stage transcripts.

**G1-A complete (2026-07-20):** Source selection record for `engineering-stage-01` (Stage 1) is established in `docs/admissions/g1-source-fixture-admission.md`:

* ✅ Source identity, provenance, and bounded scope documented
* ✅ Provisional sensitive-data assessment recorded (pending direct source inspection)
* ✅ Private handling rules defined (source stays outside repository)
* ✅ Historical outputs confirmed as comparison evidence only

**G1-B still required** before any extraction run:

* ⏳ Direct inspection of the actual source artifact by the Owner/source provider
* ⏳ Final sensitive-data determination (`cleared` or `redacted_derivative`)
* ⏳ Relation determination (`original` vs `redacted_derivative`)
* ⏳ SHA-256 digest of the exact admitted artifact recorded in the admission record

The source fixture blocker persists until G1-B is closed.

## Validation required before approval (post-Pilot-A)

Before a future extraction proposal can be approved for implementation:

- independent review of Profile/Contract responsibility separation;
- JSON Schema syntax and representative positive/negative instances;
- candidate enum coverage against historical outputs;
- authority-leakage review;
- manifest path, digest, sensitive-source, and namespaced-provider invariants;
- confirmation that no schema field encodes maturity, canonical identity,
  approval, promotion, or KB state.

## Hard holds

Do not yet:

- implement a provider adapter, parser (beyond Pilot A's bounded structural
  ZIP inventory), renderer, validator (beyond Pilot A), or CLI (beyond
  Pilot A's `extractor_agent.inventory`);
- run a model on historical or private source data;
- freeze the Extraction Contract or any Profile;
- promote historical outputs to golden expectations;
- add consolidation, identity, maturity, approval, promotion, or KB-write
  behavior;
- build multi-provider orchestration;
- merge the proposal without independent review and owner authorization.
