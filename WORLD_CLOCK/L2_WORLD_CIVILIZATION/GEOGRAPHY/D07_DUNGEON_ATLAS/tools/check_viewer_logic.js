// Functional checks for the actual embedded viewer JavaScript in a minimal DOM.
// This is not a browser layout or touch-device test. No third-party dependencies.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const base=path.resolve(process.argv[2]||path.join(__dirname,'..'));
const html=fs.readFileSync(path.join(base,'DUNGEON_EXPLORER.html'),'utf8');
const graph=JSON.parse(fs.readFileSync(path.join(base,'data/dungeon_graph.json'),'utf8'));
const layerCodes=graph.metadata.layers.map(l=>l.code);
const lastCode=layerCodes[layerCodes.length-1];
const expectedViews=['xz','yz','3d',...layerCodes,'xy'];
const menu=html.match(/<select id="view"[\s\S]*?<\/select>/)[0];
const menuViews=[...menu.matchAll(/<option value="([^"]+)"/g)].map(m=>m[1]);
assert.deepStrictEqual(menuViews,expectedViews,'View menu must contain only included strata.');
class Element {
  constructor(tag,id=''){this.tagName=tag;this.id=id;this.attrs={};this.children=[];this.style={};this.value='';this.checked=false;this.listeners={};this.textContent='';this._html='';this.classList={add(){},remove(){}};}
  setAttribute(k,v){this.attrs[k]=String(v);}
  getAttribute(k){return this.attrs[k]??null;}
  append(...els){this.children.push(...els);}
  addEventListener(k,v){this.listeners[k]=v;}
  set innerHTML(v){this._html=v;this.children=[];for(const m of v.matchAll(/<([a-z]+)[^>]*\bid="([^"]+)"[^>]*>/g)){this.children.push(new Element(m[1],m[2]));}}
  get innerHTML(){return this._html;}
  querySelector(query){const id=query.startsWith('#')?query.slice(1):null;return walk(this).find(e=>id?e.id===id:e.tagName===query)||null;}
  click(){if(this.onclick)this.onclick({stopPropagation(){}});if(this.listeners.click)this.listeners.click({stopPropagation(){}});}
  getBoundingClientRect(){return {x:0,y:0,left:0,top:0,width:1200,height:850};}
}
function walk(e){return e.children.flatMap(c=>[c,...walk(c)]);}
const elements={};
for(const m of html.split('<script>')[0].matchAll(/<([a-z]+)\b([^>]*\bid="([^"]+)"[^>]*)>/g)){
  const e=elements[m[3]]=new Element(m[1],m[3]);e.checked=/\bchecked\b/.test(m[2]);e.value=(m[2].match(/\bvalue="([^"]*)"/)||[])[1]||'';
}
elements.view.value='xz';
const document={getElementById(id){return elements[id];},createElementNS(ns,tag){return new Element(tag);},createElement(tag){return new Element(tag);}};
const context=vm.createContext({document,window:{addEventListener(){}},setTimeout,console,Math,Set,Map,JSON,Array,Object,String,Number,RegExp});
const script=html.match(/<script>([\s\S]*)<\/script>/)[1];
vm.runInContext(script,context,{timeout:10000,filename:'embedded-viewer.js'});
const run=s=>vm.runInContext(s,context,{timeout:10000});
const before=run('JSON.stringify(MODEL)');
const report=[];
for(const view of expectedViews){
  elements.view.value=view;run('draw(true)');
  const localIds=new Set(graph.nodes.filter(n=>view.length!==1||n.code===view).map(n=>n.node_id));
  const es=graph.edges.filter(e=>localIds.has(e.source)||localIds.has(e.target));
  const expectedIds=new Set([...localIds,...es.flatMap(e=>[e.source,e.target])]);
  const rendered=walk(elements.map),ns=rendered.filter(e=>e.attrs.class==='node'),polylines=rendered.filter(e=>e.tagName==='polyline');
  assert.deepStrictEqual(new Set(ns.map(e=>e.attrs['data-id'])),expectedIds);
  assert.strictEqual(polylines.length,es.length);
  assert.strictEqual(rendered.filter(e=>e.attrs.class==='nodeLabel').length,expectedIds.size);
  for(const e of polylines){assert.strictEqual(e.attrs.points.split(' ').length,4);assert(!/NaN|Infinity/.test(e.attrs.points));}
  report.push({view,node_count:ns.length,edge_count:polylines.length,all_ids_and_geometry_vertex_counts_match:true});
}
const entrance=graph.nodes.find(n=>n.site_type==='surface_entrance');
const example=graph.nodes.filter(n=>n.code===lastCode).reduce((a,b)=>a.depth_mi>=b.depth_mi?a:b);
const searchCases=[[entrance.code+'1',entrance.node_id],[graph.metadata.dungeon_id+'-'+example.node_id,example.node_id],[example.west_to_east_index,example.node_id]];
for(const code of layerCodes){
  const n=graph.nodes.find(n=>n.code===code);
  searchCases.push([code+'1',n.node_id],[graph.metadata.dungeon_id+'-'+n.node_id,n.node_id],[n.west_to_east_index,n.node_id]);
}
for(const [query,id] of searchCases){
  elements.search.value=query;elements.find.click();assert.strictEqual(run('selected'),id);
}
const absentCodes=[...'ROYGBV'].filter(c=>!layerCodes.includes(c));
for(const code of absentCodes){
  for(const query of [code+'001',graph.metadata.dungeon_id+'-'+code+'001',code+'-W001']){
    const oldSelected=run('selected');elements.search.value=query;elements.find.click();
    assert.strictEqual(run('selected'),oldSelected,'An absent stratum must not select a node.');
    assert.strictEqual(elements.note.textContent,'No node matches that ID or width index.');
  }
}
const byId=Object.fromEntries(graph.nodes.map(n=>[n.node_id,n]));
const navigationNode=graph.nodes.find(n=>n.code===lastCode&&n.neighbors.split('|').some(id=>byId[id].code!==lastCode))||example;
elements.view.value=lastCode;elements.search.value=navigationNode.node_id;elements.find.click();
const neighborIds=navigationNode.neighbors.split('|');
const crossIndex=neighborIds.findIndex(id=>byId[id].code!==lastCode);const neighborIndex=crossIndex<0?0:crossIndex;
const neighbor=neighborIds[neighborIndex];elements.selection.querySelector('#neighbors').children[neighborIndex].click();assert.strictEqual(run('selected'),neighbor);
if(byId[neighbor].code!==lastCode)assert.strictEqual(elements.view.value,byId[neighbor].code);
elements.reset.click();elements.view.value='xz';elements.arms.checked=false;run('draw(true)');
assert.strictEqual(walk(elements.map).filter(e=>e.tagName==='polyline').length,graph.edges.filter(e=>e.kind!=='lateral_terminal_passage').length);
assert.strictEqual(walk(elements.map).filter(e=>e.attrs.class==='node').length,graph.nodes.filter(n=>n.network_role==='principal').length);
elements.arms.checked=true;elements.labels.checked=false;run('draw(true)');assert.strictEqual(walk(elements.map).filter(e=>e.attrs.class==='nodeLabel').length,0);
elements.labels.checked=true;elements.reset.click();const box=elements.map.attrs.viewBox;elements.zin.click();assert.notStrictEqual(elements.map.attrs.viewBox,box);
elements.view.value='3d';run('draw(true)');const polyline0=walk(elements.map).find(e=>e.tagName==='polyline').attrs.points;
elements.yaw.value='80';elements.yaw.oninput();assert.notStrictEqual(walk(elements.map).find(e=>e.tagName==='polyline').attrs.points,polyline0);
elements.view.value=lastCode;elements.shared.checked=true;run('draw(true)');assert(walk(elements.map).some(e=>e.tagName==='polyline'));
assert.strictEqual(run('JSON.stringify(MODEL)'),before);
assert(!/<script[^>]+src=|<link[^>]+href=|url\(https?:|fetch\(/i.test(html),'External dependency found');
const result={status:'PASS',test_kind:'actual embedded JavaScript executed in a minimal DOM harness',graph_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(base,'data/dungeon_graph.json'))).digest('hex'),included_layer_codes:layerCodes,last_stratum_code:lastCode,view_menu_matches_included_strata:true,absent_stratum_searches_rejected:absentCodes,views:report,local_width_alias_and_global_search:true,searched_layer_codes:layerCodes,deepest_node_search:example.node_id,neighbor_navigation:true,visibility_controls:true,zoom_rotation_and_common_scale_controls:true,source_geometry_unchanged:true,self_contained_no_external_dependencies:true,limitations:['Full browser layout and touch-device tests were not performed in this build. This minimal-DOM harness verifies logic, not CSS rendering.']};
fs.mkdirSync(path.join(base,'validation'),{recursive:true});fs.writeFileSync(path.join(base,'validation/VIEWER_LOGIC_CHECK.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
