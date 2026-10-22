#!/usr/bin/env python3
"""Read-only 009 package, preservation and reverse-diff validation.

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

SOURCE = "PROVENANCE/WORKSHOP/LIVE_MODEL_009/"
RECEIPT = "CHECKPOINTS/LIVE_MODEL_009_MANIFEST.json"
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
        require(m["checkpoint"] == "LIVE_MODEL_009" and m["target"] == "xApologies/MK163", "Unexpected package")
        require(m["observed_baseline_sha"] == "dbc78f7bee9781da4447ccb6bdb7baf8cc198288", "Wrong observed baseline")
        require(len(m["files"]) == 5 and len(z.namelist()) == 6, "Wrong package count")
        return {"archive_sha256": sha(archive.read_bytes()), "archive_bytes": archive.stat().st_size,
                "archive_entries": len(z.namelist()), "manifest_records": len(m["files"]),
                "manifest_self_reference": "Manifest is hashed by inventory/receipt and whole archive, not itself.",
                "path_safety_crc_hashes_and_sizes": "PASS"}


def normalized(text):
    return text.replace("*", "").replace("`", "").casefold()


def validate_semantics(root):
    m = json.loads((root / "PROVENANCE/LIVE_MODEL_009_REVERSE_DIFF.json").read_text(encoding="utf-8"))
    supplied = (root / SOURCE / "AUDIT/REVERSE_DIFF_TARGETS.md").read_text(encoding="utf-8")
    rows = [l for l in supplied.splitlines() if l.startswith("| ")][1:]
    require(len(rows) == len(m["rows"]) == len(m["decisions"]) == 8, "Coverage count")
    for i,(e,row) in enumerate(zip(m["rows"],rows),1):
        require(e["id"] == f"LM009-R{i:02}", "Target ID")
        require(list(e["supplied_row"].values()) == [c.strip() for c in row.strip("|").split("|")], "Supplied row changed")
        require(e["before_semantic_assessment"] and not e["destructive_conflict"], "Missing review or destructive conflict")
        text = "\n".join((root/p).read_text(encoding="utf-8").split("## Record before Live Model 009")[0] for p in e["after_owner_paths"])
        for token in e["after_required_fragments"]:
            require(normalized(token) in normalized(text), e["id"]+": "+token)
    for i,e in enumerate(m["decisions"],1):
        require(e["id"] == f"LM009-D{i:02}", "Decision ID")
        text = "\n".join((root/p).read_text(encoding="utf-8").split("## Record before Live Model 009")[0] for p in e["owners"])
        for token in e["fragments"]:
            require(normalized(token) in normalized(text), e["id"]+": "+token)
    for path in m["protected_byte_identical_paths"]:
        require((root/path).read_bytes() == git(root,"show",m["baseline_commit"]+":"+path), "Unrelated owner changed: "+path)
    rx = re.compile(m["search_scope"]["pattern"],re.I)
    paths = sorted({p for d in m["search_scope"]["roots"] for p in (root/d).rglob("*.md")} | {root/p for p in m["search_scope"]["extra_paths"]})
    actual={};scanned=0
    for p in paths:
        if any(x in p.parts for x in m["search_scope"]["excluded_source_directories"]):continue
        scanned+=1;rel=p.relative_to(root).as_posix();hits=[]
        for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
            if rx.search(line):hits.append((n,sha(line.encode()),rx.findall(line)))
        if hits:actual[rel]=hits
    require(scanned == m["search_scope"]["scanned_markdown_files"], "Search scope changed")
    require(set(actual) == {e["path"] for e in m["surviving_mentions"]}, "Unreviewed matching file")
    for e in m["surviving_mentions"]:
        require(sha((root/e["path"]).read_bytes()) == e["sha256"], "Reviewed owner changed: "+e["path"])
        require(actual[e["path"]] == [(h["line"],h["line_sha256"],h["matched_terms"]) for h in e["matches"]], "Unreviewed search mention")
        require(all(h["classification"] and h["reason"] for h in e["matches"]), "Unclassified mention")
    require(not m["unresolved_active_special_card_mentions"], "Active special Card conflict")
    for path in ["BOOKS/RED/ARCS/ARC_004", "BOOKS/RED/ARCS/ARC_005"]:
        require(not (root/path).exists(), "Unapproved later arc created")
    return {"supplied_target_rows":8,"author_decisions":8,"status_guards":"PASS",
            "scanned_markdown_files":scanned,"matching_files_reviewed":len(actual),
            "surviving_mentions_classified":sum(len(x) for x in actual.values()),
            "protected_owner_paths_byte_identical":len(m["protected_byte_identical_paths"]),
            "active_special_card_mechanics":"RETIRED", "armor_green_conflict":"CLOSED_BY_RETIREMENT_NEITHER_SELECTED",
            "remaining_open":m["remaining_open"],
            "limitation":"Mechanical checks lock the reviewed dispositions/content and byte preservation; they do not independently prove every semantic judgment or authenticate an unseen conversation."}


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
            current = text.split("## Record before Live Model 009")[0]
            for match in re.finditer(r"\b(?:Kira|Kirin|Kyria|Rayon|Aethren|mage|magi|Nix)\b", current, re.I):
                spelling.append([path, match.group()])
    require(not spelling, "Active naming regressions: " + repr(spelling))
    tracked = git(root, "ls-files", "-z").decode().split("\0")[:-1]
    require(not any(p.casefold().startswith("_inbox/") for p in tracked), "Inbox tracked")
    require(subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "_inbox/MK163_LIVE_MODEL_009_BLACK_CARD_RETIREMENT_CODEX.zip"]).returncode == 0, "Inbox not ignored")
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
        "WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md",
        "WORLD_CLOCK/L4_NARRATIVE_REALIZATION/SERIES_STRUCTURE.md",
        "PROVENANCE/OPEN_QUESTIONS_CURRENT.md",
        "PROVENANCE/LIVE_MODEL_008_BLACK_CARD_CHRONOLOGY_CONFLICT.md",
        "WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/SIX_BLACK_BONDS.md",
        "WORLD_CLOCK/L1_FANTASY/TRANSDUCTION_LIFECYCLE.md",
        SOURCE + "CANON_DELTA/ACTIVE_AUTHOR_DECISION.md",
        "PROVENANCE/WORKSHOP/LIVE_MODEL_008/VISUAL_REFERENCE/SHAPING_ENERGY_MONTAGE.png",
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
    result = {"checkpoint": "LIVE_MODEL_009", "status": "FAIL"}
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
