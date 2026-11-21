"""Configured initial-build generator, retained from corrected D02 and original D01.
Each dungeon uses its own frozen specification; construction algorithms are unchanged.

Method: best-candidate placement, Delaunay pruning with biconnected cores,
constant-depth terminal chains, distributed adjacent-stratum matching and
four-vertex natural passage centerlines. Never run to redraw an established
atlas: use the saved JSON and render_atlas.py/build_viewer.py instead.
"""
from pathlib import Path
import json, csv, math, hashlib, zipfile, shutil
import numpy as np
import networkx as nx
from scipy.spatial import Delaunay

import argparse
parser=argparse.ArgumentParser(description='Reproduce the initial proposal in a NEW directory. Never run over an edited live graph.')
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--spec',type=Path,required=True,help='Frozen specification; only for initial build in a fresh directory.')
args=parser.parse_args()
GEO=args.output
if (GEO/'data/dungeon_graph.json').exists():
 raise SystemExit('Refusing to overwrite an existing graph. Choose a new --output directory.')
DATA=GEO/'data'; MAPS=GEO/'maps'; TOOLS=GEO/'tools'
for p in [DATA,MAPS,TOOLS]:p.mkdir(parents=True,exist_ok=True)
spec_path=args.spec.resolve()
spec=json.loads(spec_path.read_text(encoding='utf-8'))
parameter_path=spec_path.parent/spec['generation_parameters_file']
params=json.loads(parameter_path.read_text(encoding='utf-8'))
seed=spec['seed']
assert isinstance(seed,int), 'Seed must be a fixed integer.'
rng=np.random.default_rng(seed)
specs=[tuple(l[k] for k in ['stratum','code','depth_min_mi','depth_max_mi','principal_ew_span_mi','provisional_ns_span_mi','core_node_count','terminal_node_count','terminal_branch_count']) for l in spec['layers']]
codes=[s[1] for s in specs]
portals=[l['links_to_next_layer'] for l in spec['layers'][:-1]]
assert specs and specs[0][2]==0 and len(set(codes))==len(codes)
assert all(s[3]>s[2] and s[4]>0 and s[5]>0 and s[6]>=4 and s[7]>=s[8]>=1 and s[8]<=s[6] for s in specs)
assert all(a[3]==b[2] for a,b in zip(specs,specs[1:])), 'Stratum bands must be contiguous.'
assert all(isinstance(k,int) and 2<=k<=min(specs[i][6],specs[i+1][6]) for i,k in enumerate(portals))
assert spec['topology_policy']['principal_core_biconnected'] is True
assert spec['topology_policy']['each_stratum_core_biconnected'] is True
assert spec['topology_policy']['terminal_arms_constant_depth'] is True
assert spec['topology_policy']['allow_parallel_passages_between_same_nodes'] is False
assert not spec['known_site_constraints'], 'Protected anchors require explicit handling; never silently ignore them.'
assert params['coordinate_decimal_places']==6, 'This code version uses six-decimal coordinate storage.'
# Retain the exact input bytes beside every fresh reproduction.
(GEO/'config').mkdir(parents=True,exist_ok=True)
for source in [spec_path,parameter_path]:
 target=GEO/'config'/source.name
 if source!=target.resolve(): shutil.copy2(source,target)

allnodes=[]; rawedges=[]; layerdata=[]
# Spatially spaced, irregular nodes, with more local cycles than a tree.
for li,(name,code,z0,z1,w,ns,ncore,nside,nbranches) in enumerate(specs):
 pts=[]
 if li==0: pts.append([0.,0.])
 # exact adopted east-west span refers to the principal network only
 pts.extend([[-w/2,-.08*ns],[w/2,.13*ns]])
 # Best-candidate placement produces an irregular spread without crowded clumps.
 while len(pts)<ncore:
  candidates=[]
  draws=0
  while len(candidates)<params['candidates_per_new_point']:
   draws+=1
   if draws>params['candidate_draw_limit_per_point']: raise RuntimeError('Candidate-placement retry budget exhausted.')
   x=rng.uniform(-w/2,w/2); y=rng.uniform(-ns/2,ns/2)
   if (x/(w/2))**2+(y/(ns/2))**2 < params['elliptical_acceptance_squared']:
    candidates.append([x,y])
  ca=np.array(candidates); pa=np.array(pts)
  scale=np.array([w,ns])
  ds=(((ca[:,None,:]-pa[None,:,:])/scale)**2).sum(axis=2).min(axis=1)
  pts.append(ca[np.argmax(ds)].tolist())
 xy=np.array(pts)
 # Depth correlated with north-south coordinate, but not a rigid stack or grid.
 f=.10+.80*(xy[:,1]/ns+.5)+rng.uniform(*params['depth_fraction_jitter'],ncore)
 f=np.clip(f,*params['depth_fraction_clamp'])
 zz=z0+(z1-z0)*f
 if li==0: zz[0]=0.
 if li==len(specs)-1: zz[int(np.argmax(zz))]=z1
 local=[]
 for i,(x,y) in enumerate(xy):
  local.append(dict(tmp=f'{code}c{i}',stratum=name,code=code,x_mi=round(float(x),6),y_mi=round(float(y),6),depth_mi=round(float(zz[i]),6),network_role='principal',branch_id='',site_type='junction_or_chamber_unassigned'))
 if li==0: local[0]['site_type']='surface_entrance'
 tri=Delaunay(xy)
 h=nx.Graph(); h.add_nodes_from(range(ncore))
 for a,b,c in tri.simplices:
  h.add_edges_from([(int(a),int(b)),(int(b),int(c)),(int(c),int(a))])
 # Remove longer candidate edges only while preserving vertex-biconnectivity.
 ranked=list(h.edges())
 ranked.sort(key=lambda e:np.linalg.norm((xy[e[0]]-xy[e[1]])/np.array([w,ns]))*(.8+rng.random()*.4),reverse=True)
 target=int(round(params['target_internal_core_edges_per_node']*ncore))
 for a,b in ranked:
  if h.number_of_edges()<=target: break
  if h.degree(a)<=2 or h.degree(b)<=2: continue
  h.remove_edge(a,b)
  if not nx.is_biconnected(h): h.add_edge(a,b)
 assert nx.is_biconnected(h)
 for a,b in h.edges():rawedges.append((local[a]['tmp'],local[b]['tmp'],'principal_passage'))
 # Terminal arms keep their attachment depth; they do not secretly descend.
 side_counts=[nside//nbranches+(1 if k<nside%nbranches else 0) for k in range(nbranches)]
 used=set()
 for j,count in enumerate(side_counts):
  # alternate east and west, varied lateral orientation; not a symmetric outline
  theta=(0 if j%2==0 else np.pi)+rng.uniform(*params['terminal_angle_jitter_radians'])
  direction=np.array([math.cos(theta),math.sin(theta)])
  scores=(xy/np.array([w,ns]))@direction
  attach=next(int(k) for k in np.argsort(scores)[::-1] if int(k) not in used)
  used.add(attach)
  start=xy[attach].copy(); prev=local[attach]['tmp']
  extension=w*rng.uniform(*params['terminal_extension_fraction_of_ew_width'])
  bend=np.array([-direction[1],direction[0]])*rng.uniform(*params['terminal_bend_fraction_of_ew_width'])*w
  bid=f'{code}-T{j+1:02d}'
  for k in range(count):
   t=(k+1)/count
   coord=start+direction*extension*t+bend*math.sin(t*math.pi)
   tmp=f'{code}s{j}_{k}'
   local.append(dict(tmp=tmp,stratum=name,code=code,x_mi=round(float(coord[0]),6),y_mi=round(float(coord[1]),6),depth_mi=round(float(zz[attach]),6),network_role='terminal_branch',branch_id=bid,site_type='terminal_chamber_unassigned' if k==count-1 else 'lateral_junction_unassigned'))
   rawedges.append((prev,tmp,'lateral_terminal_passage')); prev=tmp
 local.sort(key=lambda n:(n['depth_mi'],n['x_mi'],n['y_mi']))
 for i,n in enumerate(local): n['node_id']=f'{code}{i+1:03d}'
 for i,n in enumerate(sorted(local,key=lambda n:(n['x_mi'],n['y_mi'],n['depth_mi']))): n['west_to_east_index']=f'{code}-W{i+1:03d}'
 for i,n in enumerate(sorted(local,key=lambda n:(-n['y_mi'],n['x_mi'],n['depth_mi']))): n['north_to_south_index']=f'{code}-N{i+1:03d}'
 allnodes.extend(local)
 layerdata.append(dict(stratum=name,code=code,depth_min_mi=z0,depth_max_mi=z1,principal_ew_span_mi=w,provisional_ns_span_mi=ns,core_node_count=ncore,terminal_node_count=nside,terminal_branch_count=nbranches))

# Multiple distributed crossings between every adjacent pair of strata.
for li,needed in enumerate(portals):
 upper=[n for n in allnodes if n['code']==specs[li][1] and n['network_role']=='principal']
 lower=[n for n in allnodes if n['code']==specs[li+1][1] and n['network_role']=='principal']
 # Use different endpoints, not one fictional choke point.
 upper=sorted(upper,key=lambda n:n['depth_mi'],reverse=True)[:max(needed+4,int(len(upper)*.60))]
 lower=sorted(lower,key=lambda n:n['depth_mi'])[:max(needed+4,int(len(lower)*.60))]
 pairs=[]
 for a in upper:
  for b in lower:
   d=math.dist([a['x_mi'],a['y_mi'],a['depth_mi']],[b['x_mi'],b['y_mi'],b['depth_mi']])
   pairs.append((d*(.93+.14*rng.random()),a,b))
 pairs.sort(key=lambda p:p[0]); used_a=set(); used_b=set(); chosen=[]
 for _,a,b in pairs:
  if a['tmp'] in used_a or b['tmp'] in used_b: continue
  chosen.append((a,b)); used_a.add(a['tmp']); used_b.add(b['tmp'])
  if len(chosen)==needed: break
 assert len(chosen)==needed
 for a,b in chosen: rawedges.append((a['tmp'],b['tmp'],'inter_stratum_passage'))

bytmp={n['tmp']:n for n in allnodes}; byid={n['node_id']:n for n in allnodes}
graph=nx.Graph()
for i,n in enumerate(allnodes):
 n['global_index']=i+1; n['geography_status']=spec['geography_status'];n['in_world_survey_status']='UNASSIGNED';graph.add_node(n['node_id'])
edges=[]
for i,(at,bt,kind) in enumerate(rawedges):
 a,b=bytmp[at],bytmp[bt]
 p=np.array([a['x_mi'],a['y_mi'],a['depth_mi']]);q=np.array([b['x_mi'],b['y_mi'],b['depth_mi']])
 length=float(np.linalg.norm(q-p));d=q-p
 horizontal=np.array([-d[1],d[0],0.]);hn=np.linalg.norm(horizontal)
 if hn: horizontal/=hn
 amp=length*rng.uniform(*params['polyline_offset_fraction_of_chord'])
 vertices=[p]
 for t,sign in [(1/3,1),(2/3,-.5)]:
  v=p+(q-p)*t+horizontal*amp*sign
  vertices.append(v)
 vertices.append(q)
 coords=[[round(float(v),6) for v in pt] for pt in vertices]
 model_length=sum(math.dist(u,v) for u,v in zip(coords[:-1],coords[1:]))
 e=dict(edge_id=f'E{i+1:04d}',source=a['node_id'],target=b['node_id'],kind=kind,strata=f"{a['stratum']}|{b['stratum']}" if a['stratum']!=b['stratum'] else a['stratum'],straight_line_mi=round(length,6),modeled_centerline_mi=round(model_length,6),depth_change_source_to_target_mi=round(b['depth_mi']-a['depth_mi'],6),geometry_xyz_mi=coords,direction='UNDIRECTED_TOPOLOGY',traversal_method='OPEN',travel_time='OPEN',terrain_detail='OPEN',geography_status=spec['geography_status'])
 edges.append(e);graph.add_edge(e['source'],e['target'],edge_id=e['edge_id'],weight=e['modeled_centerline_mi'],kind=kind)
for n in allnodes:
 n['degree']=graph.degree(n['node_id']);n['neighbors']='|'.join(sorted(graph.neighbors(n['node_id'])));n.pop('tmp')

# Graph integrity tests.
coreids=[n['node_id'] for n in allnodes if n['network_role']=='principal']
core=graph.subgraph(coreids).copy()
leafs=[n for n in allnodes if n['degree']==1]
checks={
 'unique_node_ids':len(byid)==len(allnodes),
 'unique_edge_ids':len({e['edge_id'] for e in edges})==len(edges),
 'one_connected_component':nx.number_connected_components(graph)==1,
 'no_self_loops':nx.number_of_selfloops(graph)==0,
 'no_duplicate_edges':graph.number_of_edges()==len(edges),
 'principal_network_vertex_biconnected':nx.is_biconnected(core),
 'entrance_identity':byid[codes[0]+'001']['site_type']=='surface_entrance',
 'entrance_at_origin':all(byid[codes[0]+'001'][k]==0 for k in ['x_mi','y_mi','depth_mi']),
 'only_configured_strata':set(n['code'] for n in allnodes)==set(codes),
 'deepest_node_matches_spec':max(n['depth_mi'] for n in allnodes)==specs[-1][3],
 'all_stratum_depth_bounds':all(next(s[2] for s in specs if s[1]==n['code'])<=n['depth_mi']<=next(s[3] for s in specs if s[1]==n['code']) for n in allnodes),
 'lateral_arms_constant_depth':all(abs(e['depth_change_source_to_target_mi'])<1e-7 for e in edges if e['kind']=='lateral_terminal_passage'),
 'all_terminal_tips_degree_one':all(n['degree']==1 for n in allnodes if n['site_type']=='terminal_chamber_unassigned'),
 'no_terminal_interstratum_links':all(byid[e['source']]['network_role']==byid[e['target']]['network_role']=='principal' for e in edges if e['kind']=='inter_stratum_passage'),
 'only_adjacent_strata_linked':all(abs(codes.index(byid[e['source']]['code'])-codes.index(byid[e['target']]['code']))==1 for e in edges if e['kind']=='inter_stratum_passage'),
 'polyline_endpoints_match_nodes':all(e['geometry_xyz_mi'][0]==[byid[e['source']][k] for k in ['x_mi','y_mi','depth_mi']] and e['geometry_xyz_mi'][-1]==[byid[e['target']][k] for k in ['x_mi','y_mi','depth_mi']] for e in edges),
 'modeled_lengths_not_shorter_than_chords':all(e['modeled_centerline_mi']+1e-6>=e['straight_line_mi'] for e in edges),
}
for layer in layerdata:
 nodes=[n for n in allnodes if n['code']==layer['code']];cn=[n for n in nodes if n['network_role']=='principal']
 assert abs(max(n['x_mi'] for n in cn)-min(n['x_mi'] for n in cn)-layer['principal_ew_span_mi'])<1e-6
 layer.update(node_count=len(nodes),node_range=f"{nodes[0]['node_id']}–{nodes[-1]['node_id']}",lateral_extent_ew_mi=round(max(n['x_mi'] for n in nodes)-min(n['x_mi'] for n in nodes),3),internal_edges=sum(1 for e in edges if byid[e['source']]['code']==byid[e['target']]['code']==layer['code']),cycle_rank_internal=nx.cycle_basis(graph.subgraph([n['node_id'] for n in nodes])).__len__())
checks['principal_east_west_widths_match']=True
assert all(checks.values()),checks
metrics=dict(nodes=len(allnodes),edges=len(edges),principal_nodes=len(coreids),terminal_arm_nodes=len(allnodes)-len(coreids),terminal_tips=len(leafs),interstratum_edges=sum(1 for e in edges if e['kind']=='inter_stratum_passage'),connected_components=nx.number_connected_components(graph),independent_cycles=len(edges)-len(allnodes)+1,average_degree=round(sum(dict(graph.degree()).values())/len(allnodes),3),maximum_degree=max(dict(graph.degree()).values()),principal_articulation_points=list(nx.articulation_points(core)),entrance_degree=graph.degree(codes[0]+'001'))
meta=dict(
 title=spec['display_name']+' — extensive 3D route-network design',
 dungeon_id=spec['dungeon_id'],revision=spec['revision'],date=spec['build_date'],seed=seed,
 generator_version=spec['generator_version'],phase=spec['phase'],
 status='PROPOSED_SPATIAL_EMBEDDING; approved strata and depth bands preserved',
 coordinate_system={'origin':codes[0]+'001 / surface entrance','x':'east-positive, miles','y':'north-positive, miles','z':'depth-positive, miles','reference':'common origin in every projection; map zoom may differ'},
 geography_notes=[
  'Principal E-W spans: '+','.join(str(s[4]) for s in specs)+' miles; terminal arms extend farther. Horizontal spans are explicit design proposals.',
  'Node counts, coordinates, passage geometry and north-south dimensions are computational design proposals.',
  'Included strata: '+', '.join(s[0] for s in specs)+'. Maximum modeled depth: '+str(specs[-1][3])+' miles.',
  'All links are natural geological connections. Projected crossings are not junctions without a shared node ID.',
  'One saved graph supplies every view. Rendering never samples or rebuilds geometry.',
  'Stable global node key is (dungeon_id,node_id); '+spec['dungeon_id']+'-R001 is a convenient display reference.',
  'Nodes represent major junctions/regions, not measured chamber dimensions.',
  'Environments, survey knowledge, accessibility, directional costs, fatigue and travel days remain OPEN.',
  'No existing atlas, route, marker, chronology or historical-site location is changed.'
 ],
 spec_sha256=hashlib.sha256(spec_path.read_bytes()).hexdigest(),
 generation_parameters_sha256=hashlib.sha256(parameter_path.read_bytes()).hexdigest(),
 metrics=metrics,layers=layerdata)

model=dict(metadata=meta,nodes=allnodes,edges=edges)
(DATA/'dungeon_graph.json').write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n')

def writecsv(name,rows,fields):
 with (DATA/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
nodefields=list(allnodes[0])
writecsv('nodes.csv',allnodes,nodefields)
eflat=[]
for e in edges:
 d=dict(e);d['geometry_xyz_mi']=json.dumps(d['geometry_xyz_mi'],separators=(',',':'));eflat.append(d)
writecsv('edges.csv',eflat,list(eflat[0]))
writecsv('adjacency.csv',[dict(node_id=n['node_id'],neighbors=n['neighbors'],degree=n['degree']) for n in allnodes],['node_id','neighbors','degree'])
writecsv('view_index.csv',[{k:n[k] for k in ['node_id','global_index','stratum','west_to_east_index','north_to_south_index','x_mi','y_mi','depth_mi']} for n in allnodes],['node_id','global_index','stratum','west_to_east_index','north_to_south_index','x_mi','y_mi','depth_mi'])
writecsv('stratum_connections.csv',[{k:e[k] for k in ['edge_id','source','target','strata','modeled_centerline_mi']} for e in edges if e['kind']=='inter_stratum_passage'],['edge_id','source','target','strata','modeled_centerline_mi'])
for n in allnodes:graph.nodes[n['node_id']].update({k:v for k,v in n.items() if isinstance(v,(str,int,float))})
nx.write_graphml(graph,DATA/'dungeon_graph.graphml')
validation=dict(checks=checks,metrics=metrics,layers=layerdata,note='Graph-theory checks validate the proposed model, not travel realism, geological plausibility or finished canon.')
(DATA/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')

print(json.dumps(validation,indent=2))
print('ATLAS_DIRECTORY',GEO)
