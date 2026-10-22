#!/usr/bin/env python3
"""Read-only 009B package, preservation and reverse-diff validation.

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

SOURCE = "PROVENANCE/WORKSHOP/LIVE_MODEL_009B/"
RECEIPT = "CHECKPOINTS/LIVE_MODEL_009B_MANIFEST.json"
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


def unique_json(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, "Duplicate JSON key: " + k)
        result[k] = v
    return result


def validate_package(archive):
    with zipfile.ZipFile(archive) as z:
        zip_safety(z)
        m = json.loads(z.read("MANIFEST.json"), object_pairs_hook=unique_json)
        require(m["package"] == "MK163_LIVE_MODEL_009B_AUDITED_CODEX" and m["target_repository"] == "xApologies/MK163", "Unexpected package")
        require(m["baseline_sha"] == "50222dde617803cbdfaa6991d37d210411e4aa80", "Wrong supplied baseline")
        require(len(m["members"]) == m["member_count_excluding_manifest"] == 14, "Wrong manifest count")
        require(set(z.namelist()) == set(m["members"]) | {"MANIFEST.json"}, "Unmanifested/missing file")
        for path, e in m["members"].items():
            data = z.read(path)
            require(len(data) == e["bytes"] and sha(data) == e["sha256"], "Hash/size mismatch: " + path)
        return {"archive_sha256": sha(archive.read_bytes()), "archive_bytes": archive.stat().st_size,
                "archive_entries": len(z.namelist()), "manifest_records": len(m["members"]),
                "manifest_self_reference": "Manifest is hashed by inventory/receipt and whole archive, not itself.",
                "path_safety_crc_hashes_and_sizes": "PASS"}


def normalized(text):
    return text.replace("*", "").replace("`", "").casefold()


def table(root, path):
    lines = (root / path).read_text(encoding="utf-8").splitlines()
    header = [c.strip() for c in next(l for l in lines if l.startswith("| ")).strip("|").split("|")]
    return [dict(zip(header, [c.strip() for c in l.strip("|").split("|")])) for l in lines if l.startswith("| ")][1:]


def current(root, path):
    return (root / path).read_text(encoding="utf-8").split("## Record before Live Model 009B")[0]


def validate_semantics(root):
    m = json.loads((root / "PROVENANCE/LIVE_MODEL_009B_REVERSE_DIFF.json").read_text(encoding="utf-8"))
    rows = table(root, SOURCE + "COVERAGE_MATRIX.md")
    require(len(rows) == len(m["rows"]) == 36, "36-topic coverage missing")
    statuses = {"ALREADY_PRESENT", "ADD", "REVISE", "CONFLICT", "OPEN"}
    for i, (e, supplied) in enumerate(zip(m["rows"], rows), 1):
        require(e["id"] == f"T{i:02}" and e["supplied_row"] == supplied, "Supplied topic changed")
        require(e["status"] in statuses and e["before_semantic_assessment"] and e["resulting_change"] and not e["destructive_conflict"], "Incomplete topic disposition")
        for p, h in e["before_owner_sha256"].items():
            require(sha(git(root, "show", m["baseline_commit"] + ":" + p)) == h, "Before-owner mismatch")
        after = normalized("\n".join(current(root, p) for p in e["after_owner_paths"]))
        for token in e["after_required_fragments"]:
            require(normalized(token) in after, e["id"] + ": " + token)
    supplied_decisions = table(root, SOURCE + "DECISIONS/AUTHOR_DECISIONS_AND_SUPERSESSIONS.md")
    require(len(supplied_decisions) == len(m["decisions"]) == 19, "Decision count")
    covered = set()
    for i, (e, supplied) in enumerate(zip(m["decisions"], supplied_decisions), 1):
        require(e["id"] == f"009B-{i:02}" and e["supplied_row"] == supplied, "Decision changed")
        require(e["topic_ids"] and all(t in {r["id"] for r in m["rows"]} for t in e["topic_ids"]), "Decision not covered")
        covered.update(e["topic_ids"])
        require(all((root / p).is_file() for p in e["owners"]), "Decision owner missing")
    require(len(covered) == 36, "Decision mapping does not cover all topics")
    actual_quotes = []
    for path, prefix, count in [(SOURCE + "PROVENANCE/AUTHOR_EVIDENCE_EXCERPTS.md", "E", 27), (SOURCE + "SOURCE_REGISTER.md", "SR", 6)]:
        found = [(n, sha(line.encode())) for n,line in enumerate((root/path).read_text(encoding="utf-8").splitlines(), 1) if line.startswith("> ")]
        require(len(found) == count, "Quotation count changed")
        for i, (line, h) in enumerate(found, 1):
            actual_quotes.append((f"{prefix}{i:02}", path, line, h))
    require(actual_quotes == [(e["id"], e["path"], e["line"], e["line_sha256"]) for e in m["evidence_excerpts_reviewed"]], "Unreviewed/modified excerpt")
    require(all(e["review"] and e["topic_ids"] for e in m["evidence_excerpts_reviewed"]), "Excerpt review missing")
    for path in m["protected_byte_identical_paths"]:
        require((root/path).read_bytes() == git(root,"show",m["baseline_commit"]+":"+path), "Protected history/owner changed: "+path)
    # Prior detailed bond forms, chronology and correspondences must remain literally present.
    bonds = "WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/SIX_BLACK_BONDS.md"
    require((root/bonds).read_bytes().endswith(git(root,"show",m["baseline_commit"]+":"+bonds)), "Bond chronology altered")
    card = normalized(current(root,"WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md"))
    require("live_model_009 retirement remains active" in card and "cannot independently" in card and "not a new subclass" in card, "Retirement/exclusivity guard lost")
    for p in ["WORLD_CLOCK/L4_NARRATIVE_REALIZATION/SERIES_STRUCTURE.md", "BOOKS/RED/ARCS/ARC_002/ARC.md"]:
        require("retired" in current(root,p) and "Arc V" in current(root,p), "Arc V retirement lost")
    for p in ["BOOKS/RED/ARCS/ARC_004", "BOOKS/RED/ARCS/ARC_005"]:
        require(not (root/p).exists(), "Unapproved later arc created")
    require(not m["literal_transcript_complete"] and not m["unresolved_destructive_conflicts"], "Fidelity/conflict boundary violated")
    return {"supplied_topics":36, "author_decisions":19,"selected_author_excerpts":27,"source_register_quote_occurrences":6,
            "topic_status_counts":{s:sum(e["status"]==s for e in m["rows"]) for s in sorted(statuses)},
            "status_guards":"PASS","protected_owner_and_history_paths_byte_identical":len(m["protected_byte_identical_paths"]),
            "active_special_card_mechanics":"RETIRED","vaelum_identity":"RESOLVED","bond_chronology":"PRESERVED",
            "remaining_open":m["remaining_open"],"literal_transcript_complete":False,"limitation":m["mechanical_validation_limit"]}


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
    actual_paths = set(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")[:-1])
    require(actual_paths == {e["path"] for e in records}, "Uninventoried/missing repository files")
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
        if path.startswith(("BOOKS/", "WORLD_CLOCK/", "CONSTITUTIONS/")) or path in ("AGENTS.md", "PROVENANCE/OPEN_QUESTIONS_CURRENT.md"):
            current = text.split("## Record before Live Model 009B")[0]
            for match in re.finditer(r"\b(?:Kira|Kirito|Kirin|Kyria|Rayon|Aethren|mage|magi|Nix|Daelum|runae|runei)\b", current, re.I):
                spelling.append([path, match.group()])
    require(not spelling, "Active naming regressions: " + repr(spelling))
    tracked = git(root, "ls-files", "-z").decode().split("\0")[:-1]
    require(not any(p.casefold().startswith("_inbox/") for p in tracked), "Inbox tracked")
    require(subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "_inbox/MK163_LIVE_MODEL_009B_TERMINOLOGY_CORRECTED_CODEX.zip"]).returncode == 0, "Inbox not ignored")
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
        SOURCE + "PROVENANCE/AUTHOR_EVIDENCE_EXCERPTS.md",
        "PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md",
        "WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/SIGIL_ENGINEERING.md",
        "WORLD_CLOCK/L2_WORLD_CIVILIZATION/ENVIRONMENT/DUNGEONS.md",
        "BOOKS/RED/ARCS/ARC_002/ARC.md",
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
    result = {"checkpoint": "LIVE_MODEL_009B", "status": "FAIL"}
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
