# Checkpoint 020 accumulated historical-ledger repair

**Scope: historical provenance fix only.** Baseline 9062336207f55413f1c753f1214653b4fac8ac2b, existing MK163 main matching freshly fetched origin/main. No new repository or complete 020 re-integration.

The repaired ZIP preserves all 41 previous archive entries byte-for-byte and adds exactly three: original 018 Markdown ledger, original 018 CSV ledger and HISTORICAL_LEDGER_REPAIR_NOTE.md. No archived entry is deleted/modified. All 44 members are mapped without duplicating the 41 already installed.

| Original 018 artifact | Bytes | SHA-256 |
|---|---:|---|
| DAILY_LEDGER_DAY_000_116.md |10660|85b169f49a2fc5149f09786656ef0d74a69b1f4e36e4fd903f77cb0645dc9cc4|
| DAILY_LEDGER_DAY_000_116.csv |8264|687fcf95130f63d5718ec433789edc64f2ca957a1dcd7db2e31154ba5c6e5d94|

Both exact hashes match the previously recorded missing originals. Each ledger contains 117 days (0–116), and Markdown/CSV rows agree. All four preserved manifests validate: 017 19/19, 018 26/26, 019 30/30, 020 40/40 = 115 declared hashes. The original outer manifests were not regenerated: the restored files are covered by 018; the new repair note is hashed in the additive repair map. Every one of 44 archive entries has a mapped SHA-256.

The two-file historical provenance gap is **RESOLVED**. Active instructions/open-questions/source registry gain only this scoped resolution. Earlier 020 source map, reports and validation receipts remain byte-identical historical snapshots; their original missing-file findings are not rewritten. Restored ledgers stay in historical 018 provenance, never replacing the current 020 Day 0–167 ledger.

All World Clock, books, continuity, images, prior checkpoint/workshop files and canonical decisions remain unchanged. Calendar total/week alignment, other missing-source references, Nyx rough-age/rental-deck placement questions, and design OPENs are not resolved by recovery of these bytes. No claim of complete literal transcript recovery or universal source completeness is made.

The requested accumulated repair is validated before commit; final remote success/SHA is reported only after a fresh fetch and file-hash audit.

Change scope: **7 files added, 4 metadata files modified, 0 deleted**. All **742** other previously tracked files remain byte-identical. The three modified Markdown records retain their complete prior bytes; the source registry retains every prior entry. No `_inbox` contents are staged.

Validation: [machine-readable results](VALIDATION.json); [read-only repair validator](../TOOLS/validate_checkpoint_020_repair.py). Run `python -B -X utf8 CHECKPOINTS/TOOLS/validate_checkpoint_020_repair.py --root . --archive-dir _inbox` from the repository. Local ZIPs are optional; installed sources, manifests, ledger agreement and preservation checks also run without them.
