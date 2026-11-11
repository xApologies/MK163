# Checkpoint 020 historical ledger repair

The two original Checkpoint 018 daily ledger artifacts were inadvertently omitted from the inherited 018 directory during cumulative packaging. This archive restores their exact original bytes. No prior archive entry was modified or deleted.

The Day 0–167 ledger at the root remains the current working version; the restored Day 0–116 ledgers are historical provenance, not an instruction to overwrite the current ledger.

## Codex integration
Preserve historical ledgers in checkpoint provenance. Integrate the latest working ledger by scoped reconciliation, not by overwriting or duplicating existing repository files.

## Restored SHA-256
- `MK163_CUMULATIVE_CHECKPOINT_020_2026-11-11/INHERITED_CHECKPOINT_019/INHERITED_CHECKPOINT_018/CALENDAR/DAILY_LEDGER_DAY_000_116.md`: `85b169f49a2fc5149f09786656ef0d74a69b1f4e36e4fd903f77cb0645dc9cc4`
- `MK163_CUMULATIVE_CHECKPOINT_020_2026-11-11/INHERITED_CHECKPOINT_019/INHERITED_CHECKPOINT_018/CALENDAR/DAILY_LEDGER_DAY_000_116.csv`: `687fcf95130f63d5718ec433789edc64f2ca957a1dcd7db2e31154ba5c6e5d94`
