# Architecture Decision Records

This file records accepted architecture decisions only.

Proposals and pending decisions belong in `docs/stage-0-architecture-review.md` until the owner explicitly approves them.

## Accepted decisions

No extractor-agent runtime or artifact architecture decision has been accepted yet.

## Historical constraints already present in source material

The following are not new ADRs. They are constraints declared by the current draft Extraction Contract and remain non-authoritative until that contract is reviewed and frozen:

- extraction is bounded to one source;
- extraction is stateless;
- extraction emits candidate knowledge only;
- maturity and canonical identity are out of scope;
- cross-source consolidation is downstream;
- profiles supply the extraction target, closed knowledge-type enum, and additional exclusions.

When the relevant contract is approved, architecture ADRs may reference it without duplicating its normative text.
