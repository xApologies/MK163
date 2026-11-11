# Pouch 015 · source inventory and history

All 77 unique nonarchive members from ten nested ZIPs are mapped by exact SHA-256 in [SOURCE_INVENTORY](SOURCE_INVENTORY.json). Twenty Orange 006 members already present are reused; 57 new source leaves from checkpoints 007–015 are retained verbatim here. The 768-row table and all other 014 CSV/JSON tables have a single exact source copy. Older 007–013 schedules are historical and do not compete with the active 014 charging rule.

Nested ZIP containers are not added as duplicate cumulative archives. Their complete archive graph, original names, sizes and hashes are recorded; the original outer ZIP remains read-only in the ignored local inbox. This preserves every supplied payload leaf without importing older Orange canon again. Original relative archive/file references in historical handoffs resolve through the inventory, not as new execution permission.

Checkpoint 014’s manifest lists eight local members but omits the nested 013 ZIP. Its full archive is hash-verified by pouch 015; the nested 013 ZIP passes CRC, has a recorded independent SHA-256 and its five declared hashes pass. This limitation is explicit, not a fabricated ninth manifest entry.

The source is a cumulative decision-record package, not a literal complete chat transcript. [Integration/audit](../../../CHECKPOINTS/DIPLOMATIC_POUCH_015/INTEGRATION_REPORT.md) · [Requested handoff](015/executable.fd).
