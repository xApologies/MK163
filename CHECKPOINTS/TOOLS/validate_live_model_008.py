#!/usr/bin/env python3
"""Read-only 008 package, preservation and reverse-diff validation.

Use --report only for a new external receipt. Existing reports are never replaced.
--verify-remote compares HEAD to fetched origin/main and the live origin ref.
"""
import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import sys
import urllib.parse
import zipfile
from decimal import Decimal
from pathlib import Path, PurePosixPath, PureWindowsPath

SOURCE = "PROVENANCE/WORKSHOP/LIVE_MODEL_008/"
RECEIPT = "CHECKPOINTS/LIVE_MODEL_008_MANIFEST.json"
MAX_BYTES = 100 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def safe(name):
    p = PurePosixPath(name)
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"{s}{i}" for s in ("COM", "LPT") for i in range(1, 10)}
    return (bool(name) and not p.is_absolute() and not PureWindowsPath(name).drive
            and "\\" not in name and ":" not in name and str(p) == name
            and all(c not in (".", "..") and c.casefold() not in (".git", "_inbox")
                    and c == c.rstrip(" .") and c.split(".")[0].upper() not in reserved for c in p.parts))


def zip_safety(z):
    names = z.namelist()
    require(len(names) == len({n.casefold() for n in names}), "ZIP duplicate/case collision")
    require(z.testzip() is None, "ZIP CRC failure")
    for i in z.infolist():
        require(safe(i.filename) and not i.is_dir(), "Unsafe ZIP member: " + i.filename)
        require(not stat.S_ISLNK(i.external_attr >> 16), "ZIP symlink: " + i.filename)
        require(not i.flag_bits & 1 and i.file_size < MAX_BYTES, "Encrypted/oversize ZIP member")


def zip_manifest(z, name, key):
    m = json.loads(z.read(name))
    records = m[key]
    require(len(records) == len({r["path"].casefold() for r in records}), "Duplicate manifest entries")
    require(set(z.namelist()) == {name} | {r["path"] for r in records}, "Unmanifested/missing file")
    for r in records:
        b = z.read(r["path"])
        require(len(b) == r["bytes"] and sha(b) == r["sha256"], "Hash/size mismatch: " + r["path"])
    return m


def validate_package(archive):
    with zipfile.ZipFile(archive) as z:
        zip_safety(z)
        m = zip_manifest(z, "MANIFEST.json", "files")
        require(m["target"] == "xApologies/MK163", "Unexpected target")
        require(m["package"] == "MK163_LIVE_MODEL_008_EXHAUSTIVE_CODEX", "Wrong checkpoint")
        require(m["verified_baseline_commit"] == "efdec25d50767ce3d0690fdeb479c257cacca0e9", "Wrong 007 baseline")
        require(len(m["files"]) == 13 and len(z.namelist()) == 14, "Wrong member count")
        require(not any(n.lower().endswith(".zip") for n in z.namelist()), "Unexpected nested checkpoint archive")
        png = z.read("VISUAL_REFERENCE/SHAPING_ENERGY_MONTAGE.png")
        require(sha(png) == "99eb08720016ee2d3954e7331f77042cb3bebc3814936f0b194adbdf19af213f", "Wrong source illustration")
        require(png[:8] == b"\x89PNG\r\n\x1a\n", "Invalid PNG signature")
        return {"archive_sha256": sha(archive.read_bytes()), "archive_bytes": archive.stat().st_size,
                "archive_entries": len(z.namelist()), "manifest_records": len(m["files"]),
                "manifest_self_reference": "Manifest hashed by archive/integration receipt, not by itself.",
                "path_safety_crc_hashes_and_sizes": "PASS", "source_visual_sha256": sha(png)}


def normalized(text):
    return text.replace("*", "").replace("`", "").casefold()


def validate_semantics(root):
    m = json.loads((root / "PROVENANCE/LIVE_MODEL_008_REVERSE_DIFF.json").read_text(encoding="utf-8"))
    supplied = (root / SOURCE / "AUDIT/DECISION_MATRIX.md").read_text(encoding="utf-8")
    original_rows = [line for line in supplied.splitlines() if line.startswith("| ")][1:]
    require(len(m["rows"]) == len(original_rows) == 32, "Decision-matrix coverage count")
    covered_sources = set()
    for i, (e, row) in enumerate(zip(m["rows"], original_rows), 1):
        cols = [x.strip() for x in row.strip("|").split("|")]
        require(e["id"] == f"LM008-R{i:02}", "Unstable row ID")
        require(list(e["supplied_row"].values()) == cols, "Supplied matrix row changed")
        require(e["before_semantic_assessment"] and e["disposition"], "Missing semantic disposition")
        require(not e["unresolved_destructive_conflict"], "Unresolved destructive conflict")
        text = "\n".join((root / p).read_text(encoding="utf-8").split("## Record before Live Model 008")[0]
                         for p in e["after_owner_paths"])
        for token in e["after_required_fragments"]:
            require(normalized(token) in normalized(text), e["id"] + ": missing current scope: " + token)
        for p in e["author_source_files"]:
            require((root / p).is_file(), "Missing semantic source")
            covered_sources.add(p)
    all_workshop = {p.relative_to(root).as_posix() for p in (root / SOURCE / "WORKSHOP").glob("*.md")}
    require(covered_sources == all_workshop and len(all_workshop) == 5, "Uncovered workshop record")
    require(m["rows"][30]["retained_open_conflict"], "Armor/Green conflict not retained")
    conflict = (root / "PROVENANCE/LIVE_MODEL_008_BLACK_CARD_CHRONOLOGY_CONFLICT.md").read_text(encoding="utf-8")
    require("Status: OPEN" in conflict and "mushroom" in conflict, "Missing explicit event conflict")
    require(not (root / "BOOKS/RED/ARCS/ARC_004").exists() and not (root / "BOOKS/RED/ARCS/ARC_005").exists(), "Unapproved later arc outline")
    require("Conceive → Shape → Hold → Resolve → Manifest → Release" in (root / "WORLD_CLOCK/L1_FANTASY/TRANSDUCTION_LIFECYCLE.md").read_text(encoding="utf-8"), "Lifecycle changed")
    return {"rows_rechecked": len(m["rows"]), "complete_workshop_records_covered": len(all_workshop),
            "status_guard_regressions": "PASS", "armor_green_chronology_conflict": "OPEN_RETAINED",
            "limitation": "Checks support the documented semantic review; they do not prove fictional physical feasibility or authenticate an unavailable raw chat."}


def validate_installed(root, archive, baseline_snapshot=None):
    root = root.resolve()
    m = json.loads((root / RECEIPT).read_text(encoding="utf-8"))
    require(m["archive_sha256"] == sha(archive.read_bytes()), "Wrong delivery archive")
    require(git(root, "cat-file", "-t", m["baseline_commit"]).strip() == b"commit", "Baseline is not a commit")
    require(git(root, "rev-parse", m["baseline_commit"] + "^{tree}").decode().strip() == m["baseline_tree"], "Baseline tree mismatch")
    baseline_paths = set(git(root, "ls-tree", "-r", "--name-only", "-z", m["baseline_commit"]).decode().split("\0")[:-1])
    records = m["files"]
    require(len(records) == len({e["path"].casefold() for e in records}), "Installed path collision")
    require({e["path"] for e in records if e["before_sha256"]} == baseline_paths, "Missing baseline preservation row")
    changed_texts = {}
    unchanged = modified = history = 0
    for e in records:
        p = root / e["path"]
        require(safe(e["path"]) and p.is_file() and p.resolve().is_relative_to(root), "Unsafe/absent installed file")
        require(not any(q.is_symlink() or getattr(q, "is_junction", lambda: False)() for q in [p, *p.parents] if q.is_relative_to(root)), "Reparse path")
        data = p.read_bytes()
        require(len(data) < MAX_BYTES, "Oversize installed file")
        if e["after_sha256"] is None:
            require(e["path"] == RECEIPT, "Unexpected unhashed file")
        else:
            require(sha(data) == e["after_sha256"] and len(data) == e["after_bytes"], "Installed receipt mismatch: " + e["path"])
        if e["before_sha256"]:
            before = git(root, "show", m["baseline_commit"] + ":" + e["path"])
            require(sha(before) == e["before_sha256"], "Baseline bytes disagree")
            if before == data:
                unchanged += 1
            else:
                modified += 1
                if e["path"] == "PROVENANCE/SOURCE_REGISTRY.json":
                    a, b = json.loads(before), json.loads(data)
                    for k, v in a.items():
                        require(b[k][:len(v)] == v if isinstance(v, list) else b[k] == v, "Lost registry values: " + k)
                else:
                    require(before in data, "Prior content lost: " + e["path"])
            if e["path"].startswith(("CHECKPOINTS/", "PROVENANCE/WORKSHOP/")):
                require(data == before, "Prior history modified: " + e["path"])
                history += 1
        if e["operation"] != "unchanged" and e["path"].endswith(".md"):
            changed_texts[e["path"]] = data.decode("utf-8")
    with zipfile.ZipFile(archive) as z:
        require({e["archive_path"] for e in m["source_mapping"]} == set(z.namelist()), "Source not mapped")
        for e in m["source_mapping"]:
            require((root / e["repository_path"]).read_bytes() == z.read(e["archive_path"]), "Source bytes changed")
    broken = []
    for path, text in changed_texts.items():
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            target = urllib.parse.unquote(target.split("#")[0].strip("<>"))
            if not (root / path).parent.joinpath(target).exists():
                broken.append([path, target])
    require(not broken, "Broken local links: " + repr(broken))
    spelling = []
    for path, text in changed_texts.items():
        if path.startswith(("BOOKS/", "WORLD_CLOCK/")):
            current = text.split("## Record before Live Model 008")[0]
            for match in re.finditer(r"\b(?:Kira|Kirin|Kyria|Rayon|Aethren|mage|magi|Nix)\b", current, re.I):
                spelling.append([path, match.group()])
    require(not spelling, "Active naming regressions: " + repr(spelling))
    tracked = git(root, "ls-files", "-z").decode().split("\0")[:-1]
    require(not any(p.casefold().startswith("_inbox/") for p in tracked), "Inbox tracked")
    require(subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "_inbox/MK163_LIVE_MODEL_008_EXHAUSTIVE_CODEX.zip"]).returncode == 0, "Inbox not ignored")
    git(root, "diff", "--check")
    git(root, "diff", "--cached", "--check")
    inbox_result = "Not requested"
    if baseline_snapshot:
        snap = json.loads(baseline_snapshot.read_text(encoding="utf-8"))
        now = {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in (root / "_inbox").rglob("*") if p.is_file()}
        require(now == snap["inbox"], "Inbox files changed")
        inbox_result = {"status": "PASS", "files_byte_identical": len(now)}
    return {
        "installed_files": len(records), "prior_files_preserved": len(baseline_paths),
        "baseline_files_byte_identical": unchanged, "baseline_files_expanded": modified,
        "prior_workshop_and_checkpoint_files_byte_identical": history,
        "source_members_exact": len(m["source_mapping"]),
        "local_links": "PASS", "active_naming": "PASS", "diff_whitespace": "PASS",
        "safe_paths_case_and_sizes": "PASS", "inbox_ignored_untracked": "PASS",
        "inbox_snapshot": inbox_result,
        "reverse_semantic_diff_regressions": validate_semantics(root),
    }


def verify_remote(root):
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    tracking = git(root, "rev-parse", "origin/main").decode().strip()
    live = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/main").decode().split()[0]
    require(commit == tracking == live, "Remote commit mismatch")
    require(git(root, "rev-list", "--left-right", "--count", "HEAD...origin/main").split() == [b"0", b"0"], "Divergence")
    require(not git(root, "status", "--porcelain").strip(), "Working tree not clean")
    samples = [
        "WORLD_CLOCK/L1_FANTASY/TRANSDUCTION_LIFECYCLE.md",
        "WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md",
        "WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/RED_VIOLET_DUNGEON_CITY.md",
        "BOOKS/RED/ARCS/ARC_002/ARC.md",
        "PROVENANCE/LIVE_MODEL_008_BLACK_CARD_CHRONOLOGY_CONFLICT.md",
        SOURCE + "VISUAL_REFERENCE/SHAPING_ENERGY_MONTAGE.png",
    ]
    verified = {}
    for path in samples:
        remote_bytes = git(root, "show", "origin/main:" + path)
        require(remote_bytes == (root / path).read_bytes(), "Fetched remote content mismatch: " + path)
        verified[path] = sha(remote_bytes)
    return {"status": "VERIFIED", "post_commit_sha": commit, "fetched_remote_content_samples": verified, "fetched_origin_main": tracking,
            "live_origin_main": live, "ahead": 0, "behind": 0,
            "working_tree": "clean", "post_publication_reverse_diff": validate_semantics(root)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive", type=Path)
    ap.add_argument("--root", type=Path)
    ap.add_argument("--baseline-snapshot", type=Path, help="External pre-work snapshot including inbox hashes")
    ap.add_argument("--report", type=Path, help="New external JSON receipt; refuses overwrite")
    ap.add_argument("--verify-remote", action="store_true")
    args = ap.parse_args()
    result = {"checkpoint": "LIVE_MODEL_008", "status": "FAIL"}
    try:
        result["package"] = validate_package(args.archive)
        if args.root:
            result["pre_commit_sha"] = json.loads((args.root / RECEIPT).read_text(encoding="utf-8"))["baseline_commit"]
            result["installed"] = validate_installed(args.root, args.archive, args.baseline_snapshot)
        if args.verify_remote:
            require(args.root is not None, "--verify-remote needs --root")
            result["publication"] = verify_remote(args.root)
        result["status"] = "PASS"
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as e:
        result["error"] = str(e)
    if args.report:
        with args.report.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    sys.exit(main())
