# Dungeon Mapping Method — 001

**Start with [DUNGEON_MAPPING_STANDARD.md](DUNGEON_MAPPING_STANDARD.md).** It is the exhaustive instruction file requested for creating future dungeon atlases using the Blue Capital method.

This is a **standalone method and reference package**, not a new cumulative story checkpoint. The existing Violet cumulative 004 ZIP and its selected first trial are unchanged.

## What is included

- A 32-section manual with schemas, worked examples, adaptation instructions, quality gates, and source boundaries.
- The actual original generator, renderer, viewer builder, and validator, preserved under `reference/blue_capital/tools/`.
- The actual 340-node / 709-passage graph and environmental companion as regression fixtures.
- The author-locked R001-to-B041 trial, a machine-readable route template, and a route-report tool.
- New-city planning templates, empty table headers, tested dependency versions, reproduction/audit tools, and Codex work orders.
- A complete delivery manifest and preservation/source audits.

The original generator **reproduced all eight graph outputs byte-for-byte** during this task. Its map renderer and viewer also ran successfully. The original environmental generation script was not in checkpoint 004; that gap is explicitly documented rather than reconstructed as fact.

## Quick use

```bash
python tools/verify_package.py
python tools/audit_atlas.py --atlas-dir reference/blue_capital
python tools/reproduce_reference.py --output ../blue_capital_reproduction --render --viewer
```

Install `requirements-tested.txt` first when the dependencies are not available. Use a fresh output path. The reference generator is intentionally Blue-specific: for a new city, follow manual section 30 and `CODEX_NEW_DUNGEON_WORK_ORDER.md` rather than running it unchanged and relabeling the output.

## Authority and integration

`INTEGRATION_FOR_CODEX.md` explains where to store this method without overwriting local geography or duplicating framework canon. All reference payloads are copies, not new competing live owners. The included templates do not create new story events or a future city by themselves.

No GitHub repository changes are part of this delivery.
