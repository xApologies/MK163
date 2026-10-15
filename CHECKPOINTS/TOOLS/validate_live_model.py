#!/usr/bin/env python3
"""Validate MK163 live-model payload or installed repository without modifying either."""
from pathlib import Path, PurePosixPath
import argparse, json, hashlib, re, sys

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def safe(s):
    p=PurePosixPath(s)
    return bool(s) and not p.is_absolute() and not any(x in ('..','.git','_inbox') for x in p.parts) and ':' not in s and '\\' not in s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True,type=Path);ap.add_argument('--manifest',required=True,type=Path);ap.add_argument('--structural-only',action='store_true');ap.add_argument('--report',type=Path);a=ap.parse_args()
    root=a.root.resolve();m=json.loads(a.manifest.read_text(encoding='utf-8'));errors=[];count=0
    seen=set()
    for f in m['files']:
        rel=f['path']
        if not safe(rel):errors.append('Unsafe path '+rel);continue
        if rel.casefold() in seen:errors.append('Case collision '+rel)
        seen.add(rel.casefold());p=root/rel
        if not p.is_file() or p.is_symlink():errors.append('Absent/not regular '+rel);continue
        if root not in p.resolve().parents:errors.append('Escaping path '+rel);continue
        count+=1
        if p.stat().st_size>=100*1024*1024:errors.append('Over ordinary GitHub file limit '+rel)
        if not a.structural_only and (p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256']):errors.append('Payload hash mismatch '+rel)
    cov=json.loads((root/'PROVENANCE/WORKSHOP/COVERAGE.json').read_text(encoding='utf-8'))
    evidence=[json.loads(x) for x in (root/'PROVENANCE/WORKSHOP/AUTHOR_SOURCE_RECORDS.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    journal=(root/'PROVENANCE/WORKSHOP/AUTHOR_EVIDENCE_JOURNAL.md').read_text(encoding='utf-8')
    if len(evidence)!=m['counts']['author_evidence_passages']:errors.append('Evidence count mismatch')
    for e in evidence:
        if e['text'] not in journal:errors.append('Evidence passage absent from journal '+e['id'])
    for t in cov['topics']:
        p=root/t['path']
        if not p.is_file():errors.append('Missing topic '+t['path']);continue
        text=p.read_text(encoding='utf-8')
        for id in t['author_records']:
            e=next(x for x in evidence if x['id']==id)
            quoted='\n'.join('> '+ln if ln else '>' for ln in e['text'].splitlines())
            if quoted not in text:errors.append('Evidence absent from topic '+id+' '+t['path'])
    for s in json.loads((root/'PROVENANCE/SOURCE_DOCUMENTS/ATTACHMENT_MANIFEST.json').read_text(encoding='utf-8')):
        p=root/s['path']
        if not p.is_file() or sha(p)!=s['sha256']:errors.append('Original source not preserved '+s['id'])
    for s in json.loads((root/'PROVENANCE/PROPHECY_SOURCE_MANIFEST.json').read_text(encoding='utf-8')):
        p=root/s['path']
        if not p.is_file():errors.append('Missing prophecy '+s['path']);continue
        b=p.read_bytes();gitsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if gitsha!=s['git_blob_sha']:errors.append('Prophecy source changed '+s['path'])
    api=json.loads((root/'WORLD_CLOCK/L0_MATHEMATICS/SOURCE_API_4_3/EXTRACTION_MANIFEST.json').read_text(encoding='utf-8'))
    for e in api:
        if 'exact_byte_parts' in e:
            total=hashlib.sha256();size=0
            for part in e['exact_byte_parts']:
                p=root/part['path']
                if not p.is_file():errors.append('Missing API part '+part['path']);continue
                if sha(p)!=part['sha256']:errors.append('Changed API part '+part['path'])
                with p.open('rb') as f:
                    for b in iter(lambda:f.read(1024*1024),b''):total.update(b);size+=len(b)
            if total.hexdigest()!=e['sha256'] or size!=e['original_bytes']:errors.append('API recombination fails '+e['member'])
        elif not (root/e['path']).is_file() or sha(root/e['path'])!=e['sha256']:errors.append('Changed API source '+e['member'])
    for c in json.loads((root/'PROVENANCE/WORKSHOP/ACCEPTANCE_CHECKS.json').read_text(encoding='utf-8')):
        text=(root/c['path']).read_text(encoding='utf-8').casefold()
        for token in c['required_case_insensitive_fragments']:
            if token.casefold() not in text:errors.append('Content check '+c['id']+': '+token)
    result={'delivery':m['delivery'],'validated_root':str(root),'status':'PASS' if not errors else 'FAIL','payload_files_found':count,'topic_records':len(cov['topics']),'author_evidence_passages':len(evidence),'source_preservation_checked':True,'prophecy_git_blobs_checked':True,'api_parts_recombined_hash_checked':True,'errors':errors,'note':'Mechanical integrity and declared coverage checks; not an independent proof of all fictional or mathematical claims.'}
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2));return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
