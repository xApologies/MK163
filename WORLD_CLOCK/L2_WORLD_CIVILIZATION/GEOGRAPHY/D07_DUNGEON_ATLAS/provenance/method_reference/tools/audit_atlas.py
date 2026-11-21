#!/usr/bin/env python3
"""Read-only structural audit of atlas topology, exports and saved environment overlays."""
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path
from collections import Counter
import networkx as nx

def csv_rows(p: Path):
    with p.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def audit(base: Path) -> dict:
    failures=[];warnings=[];checks=[]
    def check(ok,label):
        checks.append({'check':label,'passed':bool(ok)})
        if not ok:failures.append(label)
    file=base/'data/dungeon_graph.json'
    model=json.loads(file.read_text(encoding='utf-8'));ns=model['nodes'];es=model['edges']
    by={n['node_id']:n for n in ns};eb={e['edge_id']:e for e in es}
    layers=model['metadata']['layers'];order={l['code']:i for i,l in enumerate(layers)};lb={l['code']:l for l in layers}
    check(len(by)==len(ns),'unique node IDs');check(len(eb)==len(es),'unique edge IDs')
    g=nx.Graph();g.add_nodes_from(by)
    for n in ns:
        check(n['code'] in lb,n['node_id']+' stratum exists')
        check(all(isinstance(n[k],(int,float)) and math.isfinite(n[k]) for k in ('x_mi','y_mi','depth_mi')),n['node_id']+' finite coordinates')
        if n['code'] in lb:
            l=lb[n['code']];check(l['depth_min_mi']<=n['depth_mi']<=l['depth_max_mi'],n['node_id']+' inside depth band')
    for e in es:
        ok=e['source'] in by and e['target'] in by
        check(ok,e['edge_id']+' valid endpoints')
        if not ok:continue
        a,b=by[e['source']],by[e['target']];points=e['geometry_xyz_mi'];g.add_edge(e['source'],e['target'],**e)
        check(e['source']!=e['target'],e['edge_id']+' no self loop')
        check(len(points)>=2 and all(len(v)==3 and all(math.isfinite(c) for c in v) for v in points),e['edge_id']+' finite 3D polyline')
        check(points[0]==[a[k] for k in ('x_mi','y_mi','depth_mi')] and points[-1]==[b[k] for k in ('x_mi','y_mi','depth_mi')],e['edge_id']+' polyline endpoints')
        measured=sum(math.dist(u,v) for u,v in zip(points,points[1:]))
        check(abs(measured-e['modeled_centerline_mi'])<1e-5,e['edge_id']+' measured centerline')
        check(e['modeled_centerline_mi']>0 and e['modeled_centerline_mi']+1e-6>=e['straight_line_mi'],e['edge_id']+' positive length and chord bound')
        if e['kind']=='inter_stratum_passage':
            check(abs(order[a['code']]-order[b['code']])==1,e['edge_id']+' adjacent strata')
            check(a['network_role']==b['network_role']=='principal',e['edge_id']+' principal cross-layer endpoints')
        else:
            check(a['code']==b['code'],e['edge_id']+' local same stratum')
            l=lb[a['code']];check(all(l['depth_min_mi']<=pt[2]<=l['depth_max_mi'] for pt in points),e['edge_id']+' whole local polyline inside band')
        if e['kind']=='lateral_terminal_passage':
            check(all(abs(pt[2]-a['depth_mi'])<1e-7 for pt in points),e['edge_id']+' terminal depth constant')
    check(g.number_of_edges()==len(es),'no duplicate undirected edges')
    check(nx.is_connected(g),'whole graph connected')
    core=g.subgraph(n['node_id'] for n in ns if n['network_role']=='principal')
    check(nx.is_biconnected(core),'principal network biconnected (reference policy)')
    for n in ns:
        check(n['degree']==g.degree(n['node_id']),n['node_id']+' degree synchronized')
        check(set(n['neighbors'].split('|'))==set(g.neighbors(n['node_id'])),n['node_id']+' neighbors synchronized')
    for filename,expected,key in [('nodes.csv',ns,'node_id'),('edges.csv',es,'edge_id')]:
        actual=csv_rows(base/'data'/filename)
        ok=len(actual)==len(expected)
        if ok:
            for a,b in zip(actual,expected):
                for k,v in b.items():
                    av=json.loads(a[k]) if k=='geometry_xyz_mi' else a.get(k)
                    if av!=(v if k=='geometry_xyz_mi' else str(v)):ok=False
        check(ok,filename+' matches JSON values and order')
    envn_file=base/'data/environment_nodes_003.csv';enve_file=base/'data/environment_passages_003.csv'
    env_summary={}
    if envn_file.exists() and enve_file.exists():
        envn=csv_rows(envn_file);enve=csv_rows(enve_file)
        check(len(envn)==len(ns) and {r['node_id'] for r in envn}==set(by),'environment node coverage and uniqueness')
        check(len(enve)==len(es) and {r['edge_id'] for r in enve}==set(eb),'environment edge coverage and uniqueness')
        for r in envn:
            n=by[r['node_id']]
            check(all(abs(float(r[k])-n[k])<1e-9 for k in ('x_mi','y_mi','depth_mi')),r['node_id']+' environment coordinates synchronized')
            check('ELDRIS_DERIVED_ONLY' in r['genesis_dust'],r['node_id']+' dust source rule')
            check(r['historical_registry']=='ACCORD_REGISTRY_OWNED_NOT_ASSIGNED',r['node_id']+' no invented history')
            if n['site_type']=='surface_entrance' and 'forest' in r['genesis_flora']:
                warnings.append(r['node_id']+': provisional forest overlay overlaps the entrance; retain as review item, not automatic accepted vegetation.')
        for r in enve:
            e=eb[r['edge_id']]
            check(r['source']==e['source'] and r['target']==e['target'],r['edge_id']+' environment endpoints synchronized')
            check(r['difficulty'] in {'low','medium','hard'},r['edge_id']+' allowed difficulty')
        regions=csv_rows(base/'data/environment_regions_003.csv');water=csv_rows(base/'data/environment_waterways_003.csv')
        for r in regions:
            ids=r['nodes'].split('|');valid=set(ids)<=set(by)
            check(valid and len(set(ids))==int(r['node_count']),r['region_id']+' valid region membership')
            if valid:check(nx.is_connected(g.subgraph(ids)),r['region_id']+' connected induced region')
        for r in water:
            ids=r['nodes'].split('|');valid=set(ids)<=set(by)
            check(valid,r['feature_id']+' valid water nodes')
            if valid:check(nx.is_connected(g.subgraph(ids)),r['feature_id']+' connected water nodes')
            passages=r['passage_ids'].split('|') if r['passage_ids'] else []
            if passages:
                check(len(passages)==len(ids)-1,r['feature_id']+' water path edge count')
                for u,v,eid in zip(ids,ids[1:],passages):
                    check(eid in eb and {eb[eid]['source'],eb[eid]['target']}=={u,v},r['feature_id']+' ordered passage '+eid)
        summary=json.loads((base/'data/environment_summary_003.json').read_text())
        check(summary['source_graph_sha256']==hashlib.sha256(file.read_bytes()).hexdigest(),'environment points at exact graph hash')
        env_summary={'node_rows':len(envn),'passage_rows':len(enve),'regions':len(regions),'water_features':len(water),'difficulties':dict(Counter(r['difficulty'] for r in enve))}
        warnings.append('Environmental generator and exact difficulty thresholds are not included in checkpoint004; audit checks saved results, not a recovered generation algorithm.')
    c=nx.number_connected_components(g)
    return {'status':'FAIL' if failures else 'PASS_WITH_REVIEW_ITEMS' if warnings else 'PASS','graph_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
            'metrics':{'nodes':len(ns),'edges':len(es),'components':c,'independent_cycles':len(es)-len(ns)+c,'principal_nodes':len(core),'terminal_tips':sum(g.degree(n)==1 for n in g)},
            'environment':env_summary,'check_count':len(checks),'failure_count':len(failures),'failures':failures,'review_items':warnings,
            'scope':'Structural and cross-file checks only; not geological realism, travel feasibility, historical accuracy, hydrologic flow, or ecology validation.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--atlas-dir',required=True,type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        result=audit(a.atlas_dir)
    except (OSError,KeyError,ValueError,nx.NetworkXException) as exc:
        result={'status':'FAIL','error':str(exc),'scope':'Input/schema failure'}
    text=json.dumps(result,indent=2)+'\n'
    if a.output:
        if a.output.exists():p.error('Audit output exists. Select a new filename.')
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
    print(text);return 1 if result['status']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
