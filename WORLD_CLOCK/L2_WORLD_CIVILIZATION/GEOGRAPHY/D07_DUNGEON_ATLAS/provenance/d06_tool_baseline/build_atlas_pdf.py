"""Build the two-page atlas guide and prepend it to the original-style map set.

Adapted presentation: verified D05 (via D04/D03/D02) and original D01 Blue Capital Atlas 002. Facts are read
from the authoritative graph; this tool does not change any node or passage.
"""
from pathlib import Path
import argparse
import hashlib
import json
from collections import Counter
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--atlas-dir', type=Path, default=Path(__file__).resolve().parents[1])
base=parser.parse_args().atlas_dir
model=json.loads((base/'data/dungeon_graph.json').read_text())
meta=model['metadata']; metrics=meta['metrics']; layers=meta['layers']; nodes=model['nodes']; edges=model['edges']
byid={n['node_id']:n for n in nodes}
dungeon_id=meta['dungeon_id'];edition=meta['revision'].rsplit('_',1)[-1]
max_depth=max(l['depth_max_mi'] for l in layers)
last_stratum=layers[-1]['stratum']
fontroot=Path('/usr/share/fonts/truetype/dejavu')
if (fontroot/'DejaVuSans.ttf').exists():
    pdfmetrics.registerFont(TTFont('AtlasSans',str(fontroot/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('AtlasBold',str(fontroot/'DejaVuSans-Bold.ttf')))
else:
    # Standard built-ins keep the guide portable when DejaVu is unavailable.
    from reportlab.pdfbase.pdfmetrics import Font
    pdfmetrics.registerFont(Font('AtlasSans','Helvetica','WinAnsiEncoding'))
    pdfmetrics.registerFont(Font('AtlasBold','Helvetica-Bold','WinAnsiEncoding'))
INK=HexColor('#172231'); MUTED=HexColor('#5b6671'); RULE=HexColor('#dce2e7')
W,H=landscape(A3); M=60; TW=W-2*M
style=ParagraphStyle('body',fontName='AtlasSans',fontSize=12,leading=18,textColor=INK)
small=ParagraphStyle('small',parent=style,fontSize=10.5,leading=16,textColor=MUTED)
heading=ParagraphStyle('heading',parent=style,fontName='AtlasBold',fontSize=17,leading=23,spaceAfter=12)
stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(W,H),invariant=1)
c.setTitle(f"MK163 {meta['dungeon_id']} / Blue Domain / Atlas {edition}")
c.setAuthor('MK163 worldbuilding')

def para(text,y,sty=style):
    p=Paragraph(text,sty); _,height=p.wrap(TW,H); p.drawOn(c,M,y-height); return y-height-14

def footer(page):
    c.setStrokeColor(RULE); c.line(M,48,W-M,48)
    c.setFont('AtlasSans',8);c.setFillColor(MUTED)
    c.drawString(M,32,f"{meta['dungeon_id']} / BLUE DOMAIN / PHASE 2 GEOMETRY / ATLAS {edition} / {meta.get('date','2026-11-18')}")
    c.drawRightString(W-M,32,str(page))

def eyebrow(text):
    c.setFillColor(MUTED); c.setFont('AtlasBold',10); c.drawString(M,H-62,text)

def title(lines):
    c.setFillColor(INK);c.setFont('AtlasBold',28)
    y=H-106
    for line in lines:c.drawString(M,y,line);y-=36
    return y-5

eyebrow(f'MK163 / BLUE DOMAIN / {dungeon_id} / PHASE 2 GEOMETRY')
y=title([f'{dungeon_id} - {last_stratum} dungeon / Blue Domain','An extensive, aligned route network.'])
y=para(f"<b>{len(nodes)} nodes. {len(edges)} passages. {len(layers)} strata. One underlying three-dimensional graph.</b>",y)
y=para(f'{dungeon_id} is a {last_stratum}-ending dungeon within the Blue political Domain. This atlas uses the preserved Dungeon Mapping Method 001 and the original D01 renderer and viewer as its foundation. The east-west elevation, north-south elevation, {len(layers)} stratum plans and common-scale overlay all read the same fixed {dungeon_id} geometry. Node and passage identities remain consistent across every product.',y)
headers=['STRATUM','NODE IDS','NODES','DEPTH / MILES','PRINCIPAL WIDTH','INTERNAL LINKS']
rows=[headers]+[[l['stratum'],l['node_range'].replace('–','-'),str(l['node_count']),f"{l['depth_min_mi']:g} - {l['depth_max_mi']:g}",f"{l['principal_ew_span_mi']:g} mi",str(l['internal_edges'])] for l in layers]
widths=[115,150,85,170,200,TW-720]
t=Table(rows,colWidths=widths,rowHeights=[38]+[37]*len(layers))
t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'AtlasBold'),('FONTNAME',(0,1),(-1,-1),'AtlasSans'),('FONTSIZE',(0,0),(-1,0),9.5),('FONTSIZE',(0,1),(-1,-1),12),('BACKGROUND',(0,0),(-1,0),HexColor('#e7edf2')),('TEXTCOLOR',(0,0),(-1,-1),INK),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,-1),.5,RULE)]))
_,th=t.wrap(TW,H); t.drawOn(c,M,y-th);y-=th+24
counts=Counter(tuple([byid[e['source']]['stratum'],byid[e['target']]['stratum']]) for e in edges if e['kind']=='inter_stratum_passage')
connections=[]
for a,b in zip(layers,layers[1:]):
    number=counts[(a['stratum'],b['stratum'])]+counts[(b['stratum'],a['stratum'])]
    connections.append(f"{a['stratum']}-{b['stratum']} {number}")
y=para(f"{metrics['interstratum_edges']} additional passages join neighboring strata: {'; '.join(connections)}. Internal links plus boundary links total {len(edges)}.",y)
y=para(f"{metrics['terminal_tips']} lateral terminal arms contain {metrics['terminal_arm_nodes']} nodes. Each arm stays at its attachment depth. The connected graph has {metrics['independent_cycles']} independent cycles: E - V + 1 = {len(edges)} - {len(nodes)} + 1. This is a count of independent loops, not all possible itineraries.",y)
y=para(f'Scope: the depth bands and {max_depth:g}-mile maximum are author-selected. Horizontal spans, exact coordinates and passage geometry are computational design proposals. This structural atlas does not assign environmental regions, travel times, tournament markers, historical sites or story dates.',y,small)
assert y>65,('Guide page1 overflow',y)
footer(1);c.showPage()

eyebrow('HOW TO READ THE ATLAS')
y=title(['Fixed places. Different projections.'])
y=para('<b>A node retains its identity when the viewpoint changes.</b>',y)
example=byid.get('Y023',nodes[len(nodes)//2]); identity=example['node_id']; alias=example['west_to_east_index']
y=para(f"{identity} refers to the same {dungeon_id} location in the elevation, stratum plan, data table and explorer. Its west-to-east sorting alias is {alias}; that is a display-order index, not a second node. Use the global reference {meta['dungeon_id']}-{identity} when comparing dungeons. Existing IDs are never recycled or renumbered for a new view.",y)
y=para(f"This node's proposed coordinates are x = {example['x_mi']:.6f} miles, y = {example['y_mi']:.6f} miles, depth = {example['depth_mi']:.6f} miles. Its actual neighbors are {', '.join(example['neighbors'].split('|'))}. The graph and explorer expose every connection.",y)
y=para('Coordinate and symbol key',y,heading)
y=para('R001 is the surface entrance at (0, 0, 0). East is positive x, north is positive y, and depth increases downward. Plans use equal horizontal units with local zoom; the final overlay and the explorer common-scale mode compare the actual horizontal extents. Elevations enlarge the vertical display scale for readability.',y)
y=para('Solid lines represent principal natural passages; dashed lines represent lateral terminal arms; dotted gray lines join adjacent strata. Hollow squares mark terminal tips, a star marks the entrance, and hollow gray diamonds show neighboring-stratum endpoints on plan pages. Crossed lines are not junctions unless they share a numbered node.',y)
y=para('What remains open',y,heading)
y=para('These are major-route centerlines, not measured cave walls, widths or headroom. A connected edge does not establish walking access, safe climbing, rope anchors, water crossings or clearance. Passage length is computed from its stored 3D polyline; it is not a travel-time estimate. Environmental regions, current conditions and expedition records remain separate future overlays.',y)
y=para('Principal width guides describe the main network span, not walls. Lateral arms can extend beyond those guides. Ordinary field changes do not regenerate the graph. Future edits must preserve permanent IDs and update the shared model and its derived exports together.',y)
y=para(f'Reference method: provenance/method_reference/DUNGEON_MAPPING_STANDARD.md, especially sections 06-18 and 30. Companion files: data/dungeon_graph.json, synchronized CSV/GraphML exports, maps/ and DUNGEON_EXPLORER.html. The viewer works offline and supports local IDs, width aliases and {dungeon_id}-prefixed node searches.',y,small)
assert y>65,('Guide page2 overflow',y)
footer(2);c.save();stream.seek(0)
writer=PdfWriter();writer.append(PdfReader(stream));writer.append(PdfReader(base/'maps/NETWORK_MAPS.pdf'))
writer.add_metadata({'/Title':f"MK163 {meta['dungeon_id']} / Blue Domain / Atlas {edition}",'/Author':'MK163 worldbuilding','/Subject':'Phase 2: fixed 3D graph and consistent projections'})
target=base/f'MK163_{dungeon_id}_ATLAS_{edition}.pdf'
with target.open('wb') as f:writer.write(f)
assert len(PdfReader(target).pages)==len(layers)+5
print(target)
