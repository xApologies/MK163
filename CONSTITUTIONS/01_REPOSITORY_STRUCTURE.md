# Repository structure constitution

Top-level tracked directories: `CONSTITUTIONS`, `WORLD_CLOCK`, `BOOKS`, `CONTINUITY`, `PROVENANCE`, `CHECKPOINTS`. Root files: `README.md`, `AGENTS.md`, `.gitignore`. `_inbox/` exists locally and is Git-ignored. No second nested Git repository. Keep canonical facts in one location; reference them elsewhere by stable IDs or paths. Do not create parallel V2/V3 canon folders. Preserve history with Git and provenance records.

## Live-model delivery additions
`.gitattributes` is an allowed root configuration file for preserving original source bytes across platforms. Topic-specific records and source originals live within the existing World Clock and PROVENANCE directories; no additional Git repository or competing top-level framework is created. Delivery tools live under CHECKPOINTS/TOOLS. Templates live under CONSTITUTIONS/TEMPLATES and are not instantiated book arcs.
