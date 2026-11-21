"""Optional full-browser check; requires Playwright and a launchable Chromium.

This optional check is not part of the completed build validation. The completed
Node-only functional check is check_viewer_logic.js; CSS and touch remain unverified.
"""
from pathlib import Path
import argparse, hashlib, json, shutil
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
p.add_argument('--screenshots-dir',type=Path)
a=p.parse_args();base=a.atlas_dir
model=json.loads((base/'data/dungeon_graph.json').read_text());nodes=model['nodes'];edges=model['edges']
layer_codes=[l['code'] for l in model['metadata']['layers']];last_code=layer_codes[-1]
expected_views=['xz','yz','3d']+layer_codes+['xy']
absent_codes=[c for c in 'ROYGBV' if c not in layer_codes]
checks=[];errors=[];external=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda req:external.append(req.url) if not req.url.startswith(('file:','data:')) else None)
    page.goto((base/'DUNGEON_EXPLORER.html').resolve().as_uri())
    assert page.locator('#view option').evaluate_all('(els)=>els.map(e=>e.value)')==expected_views
    original=page.evaluate('JSON.stringify(MODEL)')
    for view in expected_views:
        page.select_option('#view',view)
        ids={n['node_id'] for n in nodes if len(view)!=1 or n['code']==view}
        selected_edges=[e for e in edges if e['source'] in ids or e['target'] in ids]
        visible_ids=ids|{e[k] for e in selected_edges for k in ('source','target')}
        actual_ids=set(page.locator('g.node').evaluate_all('(els)=>els.map(e=>e.dataset.id)'))
        assert actual_ids==visible_ids,view
        assert page.locator('polyline').count()==len(selected_edges),view
        assert page.locator('.nodeLabel').count()==len(visible_ids),view
        assert page.locator('polyline').evaluate_all('(els)=>els.every(e=>e.getAttribute("points").trim().split(/\\s+/).length===4)'),view
        checks.append({'view':view,'node_count':len(visible_ids),'edge_count':len(selected_edges),'all_node_ids_and_polyline_counts_match':True})
    example=max((n for n in nodes if n['code']==last_code),key=lambda n:n['depth_mi'])
    for query,expected in [('R1','R001'),(model['metadata']['dungeon_id']+'-'+example['node_id'],example['node_id']),(example['west_to_east_index'],example['node_id'])]:
        page.fill('#search',query);page.click('#find')
        assert page.locator('#selection h2').inner_text()==expected
    for code in absent_codes:
        for query in [code+'001',model['metadata']['dungeon_id']+'-'+code+'001',code+'-W001']:
            old_selected=page.evaluate('selected');page.fill('#search',query);page.click('#find')
            assert page.evaluate('selected')==old_selected
            assert page.locator('#note').inner_text()=='No node matches that ID or width index.'
    page.select_option('#view',last_code)
    page.fill('#search',example['node_id']);page.click('#find')
    first_neighbor=example['neighbors'].split('|')[0]
    page.locator('#neighbors button').filter(has_text=first_neighbor).click()
    assert page.locator('#selection h2').inner_text()==first_neighbor
    if first_neighbor[0]!=last_code:assert page.locator('#view').input_value()==first_neighbor[0]
    page.click('#reset');page.select_option('#view','xz');page.uncheck('#arms')
    assert page.locator('polyline').count()==sum(e['kind']!='lateral_terminal_passage' for e in edges)
    assert page.locator('g.node').count()==sum(n['network_role']=='principal' for n in nodes)
    page.check('#arms');page.uncheck('#labels');assert page.locator('.nodeLabel').count()==0
    page.check('#labels');oldbox=page.locator('#map').get_attribute('viewBox');page.click('#zin')
    assert page.locator('#map').get_attribute('viewBox')!=oldbox
    page.click('#reset');page.select_option('#view','3d')
    oldpoints=page.locator('polyline').first.get_attribute('points')
    page.locator('#yaw').fill('80');page.locator('#yaw').dispatch_event('input')
    assert page.locator('polyline').first.get_attribute('points')!=oldpoints
    page.select_option('#view',last_code);page.check('#shared')
    assert page.locator('polyline').count()>0
    assert page.evaluate('JSON.stringify(MODEL)')==original
    if a.screenshots_dir:
        a.screenshots_dir.mkdir(parents=True,exist_ok=True)
        page.uncheck('#shared');page.screenshot(path=str(a.screenshots_dir/f'viewer-desktop-{last_code.lower()}.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844});page.select_option('#view','R')
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1')
    page.fill('#search',model['metadata']['dungeon_id']+'-R001');page.click('#find');assert page.locator('#selection h2').inner_text()=='R001'
    if a.screenshots_dir:page.screenshot(path=str(a.screenshots_dir/'viewer-mobile-red.png'),full_page=True)
    browser.close()
assert not errors,errors
assert not external,external
result={'status':'PASS','graph_sha256':hashlib.sha256((base/'data/dungeon_graph.json').read_bytes()).hexdigest(),'included_layer_codes':layer_codes,'last_stratum_code':last_code,'view_menu_matches_included_strata':True,'absent_stratum_searches_rejected':absent_codes,'views':checks,'local_alias_and_global_search':True,'neighbor_navigation':True,'visibility_controls':True,'zoom_and_rotation':True,'source_geometry_unchanged':True,'mobile_390px_no_horizontal_overflow':True,'external_requests':external,'javascript_errors':errors}
(base/'validation').mkdir(exist_ok=True)
(base/'validation/VIEWER_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
