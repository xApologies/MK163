# D07 execution guide

Run these commands from the extracted `MK163_D07_ATLAS_001` directory. Python and the packages in `requirements-tested.txt` are required for rebuilding; opening the finished PDF or HTML does not require Python.

## Read and validate the existing atlas

Verify every delivered payload file against the complete manifest:

```bash
python3 tools/verify_package.py --atlas-dir .
```

The saved `data/dungeon_graph.json` is authoritative. Validate it and all synchronized graph exports:

```bash
python3 tools/validate_graph.py --atlas-dir .
```

This checks the selected specification, node/edge identities, topology, geometry, lengths, branch policy, inter-stratum links, and derived exports. Read the resulting report for actual outcomes and scope.

## Rebuild displays without rebuilding geography

```bash
python3 tools/rebuild_views.py --atlas-dir .
```

The wrapper validates the saved graph, rebuilds its maps and offline explorer, and assembles the atlas PDF. It verifies that rendering has not changed the authoritative graph. It does not invoke the initial generator or add new geography.

The individual display commands are:

```bash
python3 tools/render_atlas.py --atlas-dir .
python3 tools/build_viewer.py --atlas-dir .
python3 tools/build_atlas_pdf.py --atlas-dir .
```

The renderer writes nine PNG/SVG/PDF views and `maps/NETWORK_MAPS.pdf`. The viewer builder writes `DUNGEON_EXPLORER.html`. The PDF assembler writes `MK163_D07_ATLAS_001.pdf` with two guides followed by the nine map pages.

## Reproduce initial construction separately

For a reproducibility check, use a fresh destination that does not already contain an atlas:

```bash
python3 tools/reproduce_build.py --atlas-dir . --output ../D07_reproduction
```

This is an isolated reconstruction from the frozen specification, seed, and adapted generator. Compare its graph products to the saved authoritative outputs. It is not a routine edit or display operation.

The lower-level initial-construction command is:

```bash
python3 tools/generate_dungeon.py --spec config/dungeon_spec.json --output ../D07_fresh_initial_build
```

The generator refuses to overwrite an existing graph. Preserve that guard. Do not delete or rename the live graph just to make regeneration proceed.

## Dependency environment

The tested versions are in `requirements-tested.txt` and `validation/TESTED_ENVIRONMENT.json`. In a separate environment, install the recorded packages before reproduction:

```bash
python3 -m pip install -r requirements-tested.txt
```

Dependency versions and operation order can affect triangulation, random draws, serialization, and typography. A seed alone does not guarantee an identical atlas. The saved graph and exact source files are part of the reproducibility record. PDF bytes may differ between render environments even when the graph and geometry match.

## Edit an established map deliberately

For a selected geographical revision, preserve the current graph and its provenance first. Edit only the intended authoritative records, retain existing IDs, append unused IDs for additions, and update dependent lengths, adjacency, display indexes, and exports together. Validate the edited model before rebuilding views. The display wrapper does not repair stale CSVs or implement a graph-editing workflow.

Environmental work should join new records to the existing D07 node and edge IDs, with a graph revision/hash reference. It should not run the random generator. Label placement, rotation, page layout, and ordinary changing conditions also leave physical geometry unchanged.

## Interpret validation precisely

The independent audit and reproduction reports validate the recorded structural model and file agreement. Render coverage establishes which graph records feed each view. Viewer functional checks establish only the interface behaviors recorded by the corresponding test. Visual-review records describe the rendered pages actually inspected.

These checks do not supply missing environmental conditions, crossing methods, party access, travel times, or actual encounters. An analytical structural route is not a selected expedition.

The packaged viewer logic check can be run with Node.js:

```bash
node tools/check_viewer_logic.js
```

It exercises the embedded viewer logic, view record selection, searches, controls, and unchanged source geometry. This Node-based check does not certify browser layout, mobile rendering, or touch behavior. Consult its actual report at `validation/VIEWER_LOGIC_CHECK.json` for the tested scope.

The optional `tools/check_viewer_browser.py` requires Playwright and a working Chromium executable. Consult the current validation records for whether that optional check was run. It is not required to open the finished atlas or reproduce its graph.

The structural objective-and-return check is:

```bash
python3 tools/check_structural_route.py --atlas-dir .
```

It checks an analytical path from R001 to the deepest modeled Violet node and the same-path return. The report keeps environmental conditions, accessibility and elapsed days open.

## Integration

Use [INTEGRATION_FOR_CODEX.md](INTEGRATION_FOR_CODEX.md) before copying into a live repository. Inspect the current owner paths and preserve D01, D02, D03, D04, D05, and D06. The package itself does not perform a commit, create a pull request, or push a remote branch.
