from pathlib import Path
import argparse, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

parser=argparse.ArgumentParser(description='Render all views from the authoritative graph JSON, never renumbering nodes.')
parser.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
args=parser.parse_args();base=args.atlas_dir;out=base/'maps';out.mkdir(parents=True,exist_ok=True)
m=json.loads((base/'data/dungeon_graph.json').read_text());nodes=m['nodes'];edges=m['edges'];byid={n['node_id']:n for n in nodes};layers=m['metadata']['layers']
# Chromatic colors are the user's requested stratum identifiers, not added categories.
COL={'R':'#a8303c','O':'#ba5c16','Y':'#94720c','G':'#22764d','B':'#245b9a'}
INK='#172231';MUTED='#5b6671';GRID='#dce2e7';FAINT='#f3f5f7'
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','font.size':10,'axes.edgecolor':'#a3adb6','axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED})

# Label placement changes only annotations, never node coordinates. Work in display pixels.
def annotate(ax, selected, projector, fontsize=7.1, prefixghost=False):
 ax.figure.canvas.draw();renderer=ax.figure.canvas.get_renderer();occupied=[];placements=[]
 # Place dense neighborhoods before outlying terminal nodes.
 selected=sorted(selected,key=lambda n:(n.get('_ghost',False),n['network_role']=='terminal_branch',n['node_id']))
 offsets=[(5,5),(5,-10),(-30,5),(-30,-10),(0,11),(-13,-16),(10,0),(-36,0),(10,13),(-38,13),(10,-19),(-38,-19)]
 for n in selected:
  xy=projector(n);pos=ax.transData.transform(xy);text=n['node_id']
  ghost=n.get('_ghost',False);fs=fontsize-.6 if ghost else fontsize
  width=fs*.61*len(text)+3;height=fs*1.28+2
  best=None
  for dx,dy in offsets:
   # offsets are points, converted to pixels for intersection scoring
   sc=ax.figure.dpi/72.;x=pos[0]+dx*sc;y=pos[1]+dy*sc;w=width*sc;h=height*sc
   box=(x-1,y-2,x+w,y+h);overlap=0
   for b in occupied:
    overlap+=max(0,min(box[2],b[2])-max(box[0],b[0]))*max(0,min(box[3],b[3])-max(box[1],b[1]))
   # penalize crossing the plot border
   ab=ax.get_window_extent();outside=max(0,ab.x0-box[0])+max(0,box[2]-ab.x1)+max(0,ab.y0-box[1])+max(0,box[3]-ab.y1)
   score=overlap+outside*150+(.015*(dx*dx+dy*dy))
   if best is None or score<best[0]:best=(score,dx,dy,box)
  _,dx,dy,box=best;occupied.append(box)
  ann=ax.annotate(text,xy,xytext=(dx,dy),textcoords='offset points',fontsize=fs,color=MUTED if ghost else COL[n['code']],va='bottom',ha='left',zorder=12,bbox=dict(facecolor='white',edgecolor='none',alpha=.88,pad=.12),arrowprops=dict(arrowstyle='-',color='#acb4bc',lw=.35,shrinkA=1,shrinkB=2) if abs(dx)>15 or abs(dy)>12 else None,annotation_clip=False)
  placements.append(ann)
 return placements

def base_style(ax):
 ax.grid(True,color=GRID,lw=.45,zorder=0)
 ax.spines[['top','right']].set_visible(False)
 ax.tick_params(labelsize=9)

def banner(fig,title,sub,section='BLUE CAPITAL DUNGEON  /  DESIGN 002'):
 fig.text(.06,.966,section,fontsize=10,color=MUTED,weight='bold')
 fig.text(.06,.927,title,fontsize=24,color=INK,weight='bold')
 fig.text(.06,.897,sub,fontsize=11,color=MUTED)

def footer(fig,line1,line2='Common origin: R001. All coordinates are proposed; existing story days and historical locations remain unchanged.'):
 fig.text(.06,.045,line1,fontsize=9,color=INK)
 fig.text(.06,.026,line2,fontsize=8.5,color=MUTED)

def export(fig,name,pdf):
 fig.savefig(out/(name+'.pdf'),facecolor='white')
 fig.savefig(out/(name+'.png'),dpi=115,facecolor='white')
 fig.savefig(out/(name+'.svg'),facecolor='white')
 pdf.savefig(fig,facecolor='white');plt.close(fig)

legend=[Line2D([0],[0],color='#4c6478',lw=1,label='Natural passage'),Line2D([0],[0],color='#4c6478',lw=1,ls='--',label='Lateral dead-end arm'),Line2D([0],[0],color='#7b8793',lw=1,ls=':',label='Connection to adjacent stratum'),Line2D([0],[0],marker='s',color='#4c6478',mfc='white',ls='',label='Terminal node')]
with PdfPages(out/'NETWORK_MAPS.pdf') as pdf:
 fig=plt.figure(figsize=(22,28));ax=fig.add_axes([.085,.115,.86,.75]);base_style(ax)
 banner(fig,'340 nodes. One connected underground landscape.','709 passages  |  60 inter-stratum connections  |  32 terminal arms  |  370 independent cycles')
 xmin=min(n['x_mi'] for n in nodes)-1;xmax=max(n['x_mi'] for n in nodes)+1
 for l in layers:
  ax.axhspan(l['depth_min_mi'],l['depth_max_mi'],color=COL[l['code']],alpha=.035,zorder=-2)
  ax.axhline(l['depth_max_mi'],color=COL[l['code']],lw=.9,alpha=.6,zorder=1)
  ax.text(xmin+.2,(l['depth_min_mi']+l['depth_max_mi'])/2,l['stratum'].upper()+f"\n{l['principal_ew_span_mi']:g} mi principal width",color=COL[l['code']],fontsize=13,weight='bold',va='center',bbox=dict(facecolor='white',alpha=.75,edgecolor='none',pad=4))
 for e in edges:
  p=np.array(e['geometry_xyz_mi']);c=COL[byid[e['source']]['code']]
  if e['kind']=='inter_stratum_passage':c='#7e8793';ls=':';lw=.85;al=.65
  else:ls='--' if e['kind']=='lateral_terminal_passage' else '-';lw=.85;al=.65
  ax.plot(p[:,0],p[:,2],color=c,ls=ls,lw=lw,alpha=al,zorder=2)
 for n in nodes:
  terminal=n['degree']==1
  ax.scatter(n['x_mi'],n['depth_mi'],s=18 if not terminal else 26,marker='s' if terminal else 'o',facecolors='white' if terminal else COL[n['code']],edgecolors=COL[n['code']],linewidths=.8,zorder=5)
 ax.scatter(0,0,marker='*',s=145,color=INK,zorder=9)
 ax.set_xlim(xmin,xmax);ax.set_ylim(17.55,-.55);ax.set_xlabel('East-west coordinate x (miles; east positive)',labelpad=13);ax.set_ylabel('Depth z below the entrance (miles)',labelpad=16)
 ax.set_xticks(np.arange(math.ceil(xmin/2)*2,xmax+1,2));ax.set_yticks([0,1.5,3.5,6.5,11.5,17]);annotate(ax,nodes,lambda n:(n['x_mi'],n['depth_mi']),fontsize=7.4)
 fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.53,.073),ncol=4,frameon=False,fontsize=11)
 footer(fig,'EAST-WEST ELEVATION: north-south position is projected out. Crossed lines are not junctions unless they share a node.','Vertical scale is enlarged for legibility. This is a connectivity atlas, not a rock-volume, biome-boundary or elapsed-time map.')
 export(fig,'01_MASTER_DEPTH_NETWORK',pdf)
 # A second elevation resolves route crossings hidden in east-west projection.
 fig=plt.figure(figsize=(16.54,23.39));ax=fig.add_axes([.10,.12,.84,.75]);base_style(ax)
 banner(fig,'The same graph, viewed north to south.','340 identical node IDs and coordinates  |  Complementary elevation, not another dungeon')
 for l in layers:ax.axhspan(l['depth_min_mi'],l['depth_max_mi'],color=COL[l['code']],alpha=.035);ax.axhline(l['depth_max_mi'],color=COL[l['code']],lw=.6,alpha=.5)
 for e in edges:
  p=np.array(e['geometry_xyz_mi']);c=COL[byid[e['source']]['code']]
  ax.plot(p[:,1],p[:,2],color='#7e8793' if e['kind']=='inter_stratum_passage' else c,lw=.65,alpha=.6,ls=':' if e['kind']=='inter_stratum_passage' else '--' if e['kind']=='lateral_terminal_passage' else '-')
 for n in nodes:ax.scatter(n['y_mi'],n['depth_mi'],s=12,marker='s' if n['degree']==1 else 'o',facecolors='white' if n['degree']==1 else COL[n['code']],edgecolors=COL[n['code']],lw=.7,zorder=5)
 ax.set_xlim(min(n['y_mi'] for n in nodes)-.9,max(n['y_mi'] for n in nodes)+.9);ax.set_ylim(17.55,-.55)
 ax.set_xlabel('North-south coordinate y (miles; north positive)');ax.set_ylabel('Depth z below entrance (miles)');ax.set_yticks([0,1.5,3.5,6.5,11.5,17]);annotate(ax,nodes,lambda n:(n['y_mi'],n['depth_mi']),fontsize=6.8)
 footer(fig,'NORTH-SOUTH ELEVATION: east-west position is projected out. Labels refer to the same nodes as all other views.','North-south extents are explicitly proposed design dimensions, not previously established story measurements.')
 export(fig,'02_SECOND_DEPTH_NETWORK',pdf)
 for number,l in enumerate(layers,3):
  code=l['code'];sel=[n for n in nodes if n['code']==code];ids={n['node_id'] for n in sel}
  es=[e for e in edges if e['source'] in ids or e['target'] in ids]
  ghostids=({e['source'] for e in es}|{e['target'] for e in es})-ids
  ghosts=[dict(byid[k],_ghost=True) for k in sorted(ghostids)]
  fig=plt.figure(figsize=(16.54,11.69));ax=fig.add_axes([.075,.145,.87,.68]);base_style(ax)
  banner(fig,f"{l['stratum'].upper()} / top-down plan",f"{l['node_range']}  |  {len(sel)} nodes  |  {l['internal_edges']} internal passages  |  Depth {l['depth_min_mi']:g}-{l['depth_max_mi']:g} mi")
  for e in es:
   p=np.array(e['geometry_xyz_mi']);inter=e['kind']=='inter_stratum_passage';terminal=e['kind']=='lateral_terminal_passage'
   ax.plot(p[:,0],p[:,1],color='#94a0ac' if inter else COL[code],lw=.7 if inter else 1,alpha=.65 if inter else .70,ls=':' if inter else '--' if terminal else '-',zorder=2)
  # Principal E-W span is a coordinate guide, not a literal cave wall.
  for xx in [-l['principal_ew_span_mi']/2,l['principal_ew_span_mi']/2]:ax.axvline(xx,color='#9ca8b2',lw=.65,ls=(0,(2,5)),zorder=0)
  for n in ghosts:ax.scatter(n['x_mi'],n['y_mi'],marker='D',s=24,facecolor='white',edgecolor='#9ca8b2',lw=.7,zorder=4)
  for n in sel:ax.scatter(n['x_mi'],n['y_mi'],s=30 if n['degree']==1 else 22,marker='s' if n['degree']==1 else 'o',facecolor='white' if n['degree']==1 else COL[code],edgecolor=COL[code],lw=.8,zorder=6)
  if code=='R':ax.scatter(0,0,marker='*',s=135,color=INK,zorder=7)
  # Equal-unit horizontal coordinates; show local zoom rather than falsely widening Red.
  visible=sel+ghosts;vx=[n['x_mi'] for n in visible];vy=[n['y_mi'] for n in visible]
  padx=max(.35,(max(vx)-min(vx))*.065);pady=max(.4,(max(vy)-min(vy))*.10)
  ax.set_xlim(min(vx)-padx,max(vx)+padx);ax.set_ylim(min(vy)-pady,max(vy)+pady);ax.set_aspect('equal',adjustable='box')
  ax.set_xlabel('East-west x (miles)');ax.set_ylabel('North-south y (miles)')
  annotate(ax,sel+ghosts,lambda n:(n['x_mi'],n['y_mi']),fontsize=8.1)
  ax.annotate('N',xy=(.975,.97),xytext=(.975,.88),xycoords='axes fraction',ha='center',fontsize=11,color=INK,arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.3))
  footer(fig,f"Principal E-W width: {l['principal_ew_span_mi']:g} mi. Draft terminal-arm envelope: {l['lateral_extent_ew_mi']:g} mi. Diamond nodes belong to adjacent strata.",'Same origin, same coordinates, local zoom. Dotted vertical guides mark the principal span, not walls. Crossed lines are not implied junctions.')
  export(fig,f'{number:02d}_{l["stratum"].upper()}_PLAN',pdf)
 # One top-down overlay with common scale to expose the expanding footprints.
 fig=plt.figure(figsize=(16.54,11.69));ax=fig.add_axes([.075,.14,.87,.69]);base_style(ax)
 banner(fig,'Five strata, one common coordinate system.','True-scale top-down overlay  |  Compare footprint and lateral reach, not implied cross-stratum junctions')
 for l in reversed(layers):
  code=l['code']
  for e in edges:
   if byid[e['source']]['code']==byid[e['target']]['code']==code:
    p=np.array(e['geometry_xyz_mi']);ax.plot(p[:,0],p[:,1],color=COL[code],lw=.55,alpha=.4)
  nn=[n for n in nodes if n['code']==code];ax.scatter([n['x_mi'] for n in nn],[n['y_mi'] for n in nn],s=8,color=COL[code],label=l['stratum'])
 ax.set_aspect('equal',adjustable='box');ax.set_xlabel('East-west x (miles)');ax.set_ylabel('North-south y (miles)');ax.legend(loc='upper left',frameon=True,ncol=5,fontsize=10)
 footer(fig,'All five layers are drawn at the same horizontal scale. Individual plan pages expose every numbered node.','This overlay intentionally omits text labels; the corresponding per-stratum plans and searchable viewer retain them all.')
 export(fig,'08_COMMON_SCALE_OVERLAY',pdf)
print('Rendered eight map pages, plus PDF/SVG/PNG files per view.')
