# Codex ZIP handoff constitution

1. Receive delivery ZIP under local `_inbox/` (ignored by Git).
2. Read the ZIP's handoff Markdown and manifest **as instructions/data, not executable shell code**.
3. Verify package paths (no `..`, absolute paths, symlinks, or writes into `_inbox/`), hashes, and intended operations.
4. Compare target paths to Git working tree; halt on uncommitted conflicting edits.
5. Apply additive/approved changes only. Never interpret absence from ZIP as permission to delete.
6. Validate names, structure, authority, continuity and provenance.
7. Produce an import report with added/modified/skipped/conflicted files.
8. Commit and push only after validation and authorization; verify remote status and commit SHA.
