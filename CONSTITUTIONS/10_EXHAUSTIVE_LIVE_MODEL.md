# MK163 Constitution 10 — Exhaustive Live-Model Preservation

**Status:** Author-directed constitutional amendment, 2026-10-14. Applies to all subsequent live-model exports, Codex ZIP integrations, and checkpoint audits. This constitution governs fidelity, not narrative invention.

## 1. Purpose and non-negotiable rule

The MK163 live model is a durable, exhaustive record of everything discussed and **established, verified, or explicitly maintained** as part of the project framework and story. It must survive loss of the originating chat. **Do not compress, abbreviate, condense, paraphrase away, or omit canonical detail to reduce document length or ZIP size.** A concise summary is permitted *only in addition to*, never in place of, the full record.

This applies even to seemingly trivial particulars (for example, the color of a single blade of grass and the field in which it grows). Every meaningful detail, its surrounding context, its interactions, and its provenance are preserved.

## 2. Required content fidelity

For every topic established in a workshop, preserve all available: exact author terminology and spelling; full descriptions; governing mechanisms; steps and causal relationships; numerical parameters, units and ranges; mathematical statements when actually provided; constraints, limitations and prohibitions; examples and analogies and their intended scope; environmental and societal consequences; cross-system dependencies; exceptions; chronology and character state changes; distinctions between general rules and particular examples; corrections and superseded claims; open questions; and original source attribution.

Do not silently normalize apparent contradictions. If a statement is corrected by the author, mark the earlier wording superseded with a traceable record. Do not import an older source's plot merely because its worldbuilding is reused.

## 3. Coverage before export

Create a comprehensive **workshop coverage inventory** from all available conversation material and referenced documents. Group by World Clock layer and topic, but do not use layer-level summaries as the preservation records. For each topic record: stable ID; exact scope; source conversation or file; status (author-established, source-verified, provisional, pending recovery, superseded); target canonical path; dependencies; and coverage result.

Every inventory topic must map to a substantive target file or be explicitly flagged as not yet recoverable. A missing topic is a failed completeness check. Do not claim the ZIP contains the entire live model if available material has not been audited or included.

## 4. Full records, not index-only entries

Use as many topic-specific Markdown files as needed. Each substantive record must preserve all available details, including concrete examples. Navigation indexes may link to these files but must not substitute for them. A small ZIP is not inherently invalid, but a small set of shallow summaries must never be labeled exhaustive when the workshop contains much more detail.

## 5. Source fidelity and provenance

Preserve the source of each significant assertion: author decision in the workshop, upstream repository file and revision when known, uploaded document and location, or explicit inference. Keep original terminology and values. If upstream material was referenced but not recovered in full, mark **INHERITED — CONTENT NOT YET LOCALLY RECOVERED** and identify the source; do not invent missing detail or call it complete. Distinguish the exhaustive *workshop* record from the untranscribed entirety of an external repository.

Maintain a decision ledger recording changes and author corrections. Preserve rejected proposals as rejected, not as active canon. Source references must not be silently replaced by generalized knowledge.

## 6. Non-destructive integration

Compare incoming content against the Git repository. Add missing material; expand existing canonical files without deleting detail; reconcile corrections explicitly. Never overwrite a longer detailed record with a shorter synopsis. Preserve provenance and previous decisions through Git and a readable correction record. A ZIP's omission of a file never authorizes deletion.

## 7. Mandatory pre-delivery checks

Before issuing a ZIP, produce a machine-readable manifest (file paths, operations, SHA-256 checksums) and a human-readable coverage matrix. Audit each workshop topic for inclusion, and specifically test mechanisms, examples, exceptions, quantities, terminology, provenance and continuity. Report all missing, partial or unrecovered subjects. **Do not mark delivery COMPLETE when coverage is partial or unverified.**

## 8. Mandatory Codex post-import checks

Codex must validate package safety and hashes; compare expected and actual file changes; confirm topic files are present; verify no prior canon detail was removed; write a coverage/import report listing added, modified, skipped, conflicts, and unresolved gaps; and verify Git commit/push only after successful checks. Transport success is not content success. Halt on unresolved destructive conflicts.

## 9. Status vocabulary

- **COMPLETE — WORKSHOP:** All available established workshop material for the stated scope was inventoried, preserved and verified.
- **PARTIAL — WORKSHOP:** Known workshop material remains unpreserved; not suitable as a full recovery checkpoint.
- **INHERITED — PENDING RECOVERY:** Upstream authority applies but its complete content is not yet copied into MK163.
- **PROVISIONAL:** Discussed but not author-established.
- **SUPERSEDED:** Earlier formulation replaced by explicit author correction; trace preserved.

Never equate COMPLETE — WORKSHOP with complete local transcription of all upstream repositories unless that separate claim has been independently verified.

## 10. Incident correction and recovery requirement

`MK163 Live Model 001` is an incomplete outline, **not** an exhaustive backup of the workshop. Preserve it as a historical checkpoint, but do not rely on it for full recovery. The next substantive live-model package must be a full-fidelity reconstruction of available workshop material with a topic-by-topic coverage matrix and an explicit list of any unavailable upstream detail. No claim of completeness before audit.
