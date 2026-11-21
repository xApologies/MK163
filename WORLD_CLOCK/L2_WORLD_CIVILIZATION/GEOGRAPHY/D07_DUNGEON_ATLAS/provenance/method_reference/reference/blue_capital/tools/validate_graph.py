"""Validate a proposed spatial graph and its synchronized exports. No remote writes."""
from pathlib import Path
import argparse,csv,json,math,sys
import networkx as nx

def main():
 p=argparse.ArgumentParser();p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();base=args.atlas_dir
 m=json.loads((base/'data/dungeon_graph.json').read_text(encoding='utf-8'));nodes=m['nodes'];edges=m['edges'];by={n['node_id']:n for n in nodes};layers={l['code']:l for l in m['metadata']['layers']};g=nx.Graph();g.add_nodes_from(by)
 failures=[]
 def ck(condition,label):
  if not condition:failures.append(label)
 ck(len(by)==len(nodes),'duplicate node IDs');ck(len({e['edge_id'] for e in edges})==len(edges),'duplicate edge IDs')
 for e in edges:
  ck(e['source'] in by and e['target'] in by,e['edge_id']+' invalid endpoint')
  if e['source'] not in by or e['target'] not in by:continue
  a,b=by[e['source']],by[e['target']];g.add_edge(e['source'],e['target'],edge_id=e['edge_id']);points=e['geometry_xyz_mi']
  ck(points[0]==[a[k] for k in ('x_mi','y_mi','depth_mi')],e['edge_id']+' start geometry')
  ck(points[-1]==[b[k] for k in ('x_mi','y_mi','depth_mi')],e['edge_id']+' end geometry')
  ck(abs(sum(math.dist(u,v) for u,v in zip(points[:-1],points[1:]))-e['modeled_centerline_mi'])<1e-5,e['edge_id']+' length')
  if e['kind']=='lateral_terminal_passage':ck(all(abs(v[2]-a['depth_mi'])<1e-7 for v in points),e['edge_id']+' nonhorizontal terminal arm')
  if e['kind']=='inter_stratum_passage':
   ck(abs('ROYGB'.index(a['code'])-'ROYGB'.index(b['code']))==1,e['edge_id']+' skipped stratum')
   ck(a['network_role']==b['network_role']=='principal',e['edge_id']+' terminal used for descent')
  else:
   ck(a['code']==b['code'],e['edge_id']+' wrong local edge kind')
   l=layers[a['code']];ck(all(l['depth_min_mi']<=v[2]<=l['depth_max_mi'] for v in points),e['edge_id']+' internal edge leaves band')
 ck(g.number_of_edges()==len(edges),'duplicate undirected edges');ck(nx.is_connected(g),'disconnected graph');ck(nx.number_of_selfloops(g)==0,'self-loops')
 core=g.subgraph([n['node_id'] for n in nodes if n['network_role']=='principal']);ck(nx.is_biconnected(core),'principal graph loses biconnectivity')
 for n in nodes:
  l=layers[n['code']];ck(l['depth_min_mi']<=n['depth_mi']<=l['depth_max_mi'],n['node_id']+' invalid depth');ck(g.degree(n['node_id'])==n['degree'],n['node_id']+' wrong degree');ck(set(g.neighbors(n['node_id']))==set(n['neighbors'].split('|')),n['node_id']+' wrong adjacency')
  if n['site_type']=='terminal_chamber_unassigned':ck(n['degree']==1,n['node_id']+' terminal degree')
 for code,l in layers.items():
  cn=[n for n in nodes if n['code']==code and n['network_role']=='principal'];ck(abs(max(n['x_mi'] for n in cn)-min(n['x_mi'] for n in cn)-l['principal_ew_span_mi'])<1e-6,code+' width')
 for file,expected,key in [('nodes.csv',nodes,'node_id'),('edges.csv',edges,'edge_id')]:
  with (base/'data'/file).open(encoding='utf-8-sig',newline='') as f:actual=list(csv.DictReader(f))
  ck(len(actual)==len(expected),file+' count')
  for a,b in zip(actual,expected):
   for col,v in b.items():
    if col=='geometry_xyz_mi':ck(json.loads(a[col])==v,file+' geometry mismatch')
    else:ck(a.get(col)==str(v),file+' '+b[key]+' '+col+' mismatch')
 gm=nx.read_graphml(base/'data/dungeon_graph.graphml');ck(set(gm.nodes())==set(g.nodes()),'GraphML nodes');ck({frozenset(e) for e in gm.edges()}=={frozenset(e) for e in g.edges()},'GraphML edges')
 ck(set(by['R001'][k] for k in ['x_mi','y_mi','depth_mi'])=={0.},'entrance origin')
 result={'status':'FAIL' if failures else 'PASS','nodes':len(nodes),'edges':len(edges),'independent_cycles':len(edges)-len(nodes)+1,'terminal_tips':sum(n['degree']==1 for n in nodes),'failures':failures}
 print(json.dumps(result,indent=2));return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
