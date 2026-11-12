# Banking — local handwritten accounts vs kingdom-wide maege glass network

**Protected substrate spelling: `maege glass` (M-A-E-G-E).** This is the existing Genesis-interactive material, not a newly invented `Mage Glass` or separate class. Historical documents may contain older mistaken spellings; do not duplicate materials or rewrite source quotations.

## Two coexisting service tiers
- **Local bank (Kaira's original):** handwritten notebook account record; basic fixed-manifold bank identification card; physical vault/Genesis crystal custody. Economical local service. Its prior canon remains true; it is NOT retroactively replaced.
- **Kingdom-wide bank:** branches in major cities, expensive connected sigil infrastructure; charges one-time account opening and manufactured ledger cost, monthly service fee, optional custody/lockbox charges. Amounts OPEN. Supports traveling Alchemists, merchants, nobles, Kaira at Blackstone. Bank name OPEN.

## Clerk-facing bank-owned account ledger
A manufactured **maege glass ledger tablet** is already flashed with standard interactive layout but initially unassigned. Bank activates it to one account via basement sigil. It is stored in branch archive; Kaira holds **identification card**, not necessarily the bank-owned ledger.

Interface: account reference **top left**; three dots **top right**: Red = eln/ahm currency transaction history; Orange = Genesis crystal inventories; Yellow = optional lockbox info. Main display entirely switches views. Orange first presents seven squares: Red, Orange, Yellow / Green, Blue, Violet / White; selecting a basin **replaces the entire main display** with its scrollable ledger, not stacked subpanels. Currency and each crystal ledger consist of ordered `+` deposits and `−` withdrawals; signed quantities and running totals, with scrolling history. Crystal inventory uses measured mass (e.g. illustrative 637.8 grams); exact official mass unit/grade OPEN. Currency uses **eln and ahm**, exact exchange ratio OPEN; never canonize 100:1 without user approval.

Lower reserved portion of tablet projects a temporary **ER foam tactile numeric keyboard** only when a row is active: firm, slightly yielding hard-rubber-like touch; stabilized localized projected tactile surface. No need for alphabetic input unless later selected. Clerk enters signed amount; tablet updates via local block. Account authentication/permissions handled by bank infrastructure; account number alone not enough.

## Basement network
- **Three large maege glass data blocks per branch**, each seated on its own sigil anchor in a secure basement; all three share coordinated sigil array. Redundancy; exact quorum/recovery protocol OPEN (two-of-three was suggested, NOT author-approved).
- A smaller **ledger activation pedestal anchor** accepts premanufactured unassigned tablet. Activation flashes/assigns account identity, registers account with local blocks, links tablet's permitted interaction to block; tablet then goes to archive.
- Desk/counter sigils link retrieved ledger to **local** blocks; account transaction entered in ledger -> local block authoritative update -> synchronized network of corresponding blocks at other branches. Ledger does **not** independently synchronize with distant cities; not a self-contained authoritative bank database.
- User proposes engineered **Genesis-field relational/entangled coupling** between remote blocks for information propagation. This is **fictional AERA/MK163 transport**, not ordinary quantum entanglement (which alone cannot signal). Exact mathematical implementation, latency, authorization, transaction ordering, conflict handling and failure recovery OPEN; do not claim derivation completed or physically proven. Existing AERA Rainbow Road may be relevant but do not equate without derivation.

## Example: Kaira withdraws a Green crystal
Kaira presents existing identification card on counter sigil; clerk verifies registered credential, retrieves archived account ledger; crystal is physically retrieved/weighed (illustrative 637.8 g); clerk selects Orange then Green, chooses a `−` row, enters measured mass on ER foam numeric keypad, confirms. Local block records withdrawal, other blocks update, clerk hands Kaira physical crystal. No crystals magically transported; bank must reconcile actual custody. She had **zero of her original three Green crystals still banked after Day 137**, so don't recreate those as available inventory. Other bank-held crystals may exist, exact types/masses OPEN.

## Mathematical interface model (design-level, not transport closure)
An account ledger has ordered transactions `t_i=(account, asset, sign, quantity, sequence)`. For a single asset, balance `B_n = B_0 + Σ_{i=1}^n sign_i * quantity_i`. Separate ledgers for each crystal basin and currency. Distributed state `S_{k+1}=U(S_k,t)` after authorized acceptance. Replica convergence is an intended invariant, not an already-derived Genesis transport equation.
