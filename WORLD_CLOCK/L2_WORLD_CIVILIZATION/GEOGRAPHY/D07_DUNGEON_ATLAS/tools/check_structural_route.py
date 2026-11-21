#!/usr/bin/env python3
"""Check a deepest-node objective and same-path return using actual configured edges.

This is a topology/distance regression, not an authored expedition. It adds
no environmental classifications, encounters, travel durations or story days.
"""
from pathlib import Path
import argparse
import hashlib
import json
import networkx as nx

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
p.add_argument('--output',type=Path)
a=p.parse_args(); base=a.atlas_dir.resolve()
source=base/'data/dungeon_graph.json'
model=json.loads(source.read_text()); by={n['node_id']:n for n in model['nodes']}
g=nx.Graph()
for n in by:g.add_node(n)
for e in model['edges']:g.add_edge(e['source'],e['target'],**e,weight=e['modeled_centerline_mi'])
start=next(n['node_id'] for n in model['nodes'] if n['site_type']=='surface_entrance')
target=max(model['nodes'],key=lambda n:(n['depth_mi'],n['node_id']))['node_id']
path=nx.shortest_path(g,start,target,weight='weight');return_path=list(reversed(path))
passages=[g[u][v]['edge_id'] for u,v in zip(path,path[1:])]
length=round(sum(g[u][v]['weight'] for u,v in zip(path,path[1:])),6)
assert all(g.has_edge(u,v) for u,v in zip(return_path,return_path[1:]))
assert set(by[n]['code'] for n in path)==set(l['code'] for l in model['metadata']['layers'])
result={'status':'PASS','dungeon_id':model['metadata']['dungeon_id'],
 'graph_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'scope':'Topology and modeled centerline-distance test only; not a selected expedition or tournament marker.',
 'objective':'Deepest modeled node, distinct from first entry into '+model['metadata']['layers'][-1]['stratum']+' or a future marker.',
 'start':start,'target':target,'target_depth_mi':by[target]['depth_mi'],
 'descent_node_sequence':path,'descent_edge_sequence':passages,
 'return_node_sequence':return_path,'return_edge_sequence':list(reversed(passages)),
 'one_way_modeled_centerline_mi':length,'round_trip_modeled_centerline_mi':round(length*2,6),
 'return_connectivity_verified':True,'all_strata_visited':True,
 'traversal_method':'OPEN','environmental_conditions':'PENDING','difficulty':'OPEN',
 'elapsed_days':'OPEN','encounters':'UNASSIGNED','story_event_created':False}
out=a.output or base/'validation/STRUCTURAL_ROUTE_TEST.json'
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
