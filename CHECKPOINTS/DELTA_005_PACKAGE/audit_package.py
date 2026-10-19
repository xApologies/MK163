#!/usr/bin/env python3
"""MK163 Delta 005 safe package audit. Does not modify the target repository."""
import argparse, hashlib, json, pathlib, sys, zipfile
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zip_path")
    ap.add_argument("--repo",default=None,help="optional local MK163 checkout for existence checks")
    a=ap.parse_args()
    bad=[]
    with zipfile.ZipFile(a.zip_path) as z:
        names=z.namelist()
        if z.testzip(): bad.append("CRC check failed")
        if len(names)!=len(set(n.lower() for n in names)):bad.append("case-insensitive collision")
        for n in names:
            p=pathlib.PurePosixPath(n)
            if n.startswith("/") or "\\" in n or ".." in p.parts:bad.append("unsafe path "+n)
            if (z.getinfo(n).external_attr>>16)&0o170000==0o120000:bad.append("symlink "+n)
        manifest=json.loads(z.read("MANIFEST.json"))
        for f in manifest["files"]:
            n=f["path"]
            if n not in names:bad.append("missing "+n);continue
            data=z.read(n)
            if len(data)!=f["bytes"]:bad.append("size "+n)
            if hashlib.sha256(data).hexdigest()!=f["sha256"]:bad.append("hash "+n)
        expected=["execution.md","executable.me","BASELINE_REPOSITORY_AUDIT.json","README.md"]
        for n in expected:
            if n not in names:bad.append("missing "+n)
        if a.repo:
            repo=pathlib.Path(a.repo)
            if not (repo/"AGENTS.md").exists():bad.append("repo missing AGENTS.md")
            print("Local repo exists:",repo.is_dir())
        print("ZIP entries:",len(names))
        print("Payload files:",len(manifest["files"]))
        print("Manifest status:",manifest.get("status"))
        print("Compressed bytes:",pathlib.Path(a.zip_path).stat().st_size)
        print("Uncompressed bytes:",sum(x.file_size for x in z.infolist()))
    if bad:
        for x in bad:print("FAIL:",x,file=sys.stderr)
        sys.exit(1)
    print("PASS: package structure, CRC and manifest hashes. This is NOT a semantic completeness audit.")
if __name__=="__main__":main()
