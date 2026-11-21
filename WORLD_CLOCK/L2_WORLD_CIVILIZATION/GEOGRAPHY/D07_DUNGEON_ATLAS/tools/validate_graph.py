#!/usr/bin/env python3
"""Independently validate a method-aligned atlas and every graph export.

Adapted from the D06 independent validator and preserved D01 method, with specification, terminal-chain,
intermediate-geometry, index, GraphML-attribute and complete export checks.
Read only except for the explicitly requested JSON report. This validates the
structural Phase 2 atlas; it does not certify ecology, accessibility or travel.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

NODE_FIELDS = [
    'stratum', 'code', 'x_mi', 'y_mi', 'depth_mi', 'network_role',
    'branch_id', 'site_type', 'node_id', 'west_to_east_index',
    'north_to_south_index', 'global_index', 'geography_status',
    'in_world_survey_status', 'degree', 'neighbors',
]
EDGE_FIELDS = [
    'edge_id', 'source', 'target', 'kind', 'strata', 'straight_line_mi',
    'modeled_centerline_mi', 'depth_change_source_to_target_mi',
    'geometry_xyz_mi', 'direction', 'traversal_method', 'travel_time',
    'terrain_detail', 'geography_status',
]
ADJACENCY_FIELDS = ['node_id', 'neighbors', 'degree']
VIEW_FIELDS = [
    'node_id', 'global_index', 'stratum', 'west_to_east_index',
    'north_to_south_index', 'x_mi', 'y_mi', 'depth_mi',
]
CONNECTION_FIELDS = [
    'edge_id', 'source', 'target', 'strata', 'modeled_centerline_mi',
]
COORDS = ('x_mi', 'y_mi', 'depth_mi')
EPS = 1e-5


def audit(base: Path) -> dict:
    failures = []
    count = 0

    def ck(condition, label):
        nonlocal count
        count += 1
        if not condition:
            failures.append(label)
        return bool(condition)

    graph_file = base / 'data/dungeon_graph.json'
    spec_file = base / 'config/dungeon_spec.json'
    model = json.loads(graph_file.read_text(encoding='utf-8'))
    spec = json.loads(spec_file.read_text(encoding='utf-8'))
    meta, nodes, edges = model['metadata'], model['nodes'], model['edges']
    by = {n['node_id']: n for n in nodes}
    eb = {e['edge_id']: e for e in edges}
    layers = meta['layers']
    layer_by = {l['code']: l for l in layers}
    specs = spec['layers']
    spec_by = {l['code']: l for l in specs}
    order = {l['code']: i for i, l in enumerate(layers)}
    policies = spec['topology_policy']
    ck(meta['dungeon_id'] == spec['dungeon_id'] == 'D07', 'D07 global namespace')
    ck(meta['revision'] == spec['revision'] == 'D07_ATLAS_001', 'metadata/spec fixed D07 revision')
    ck(meta['seed'] == spec['seed'] == 1630701, 'metadata/spec frozen D07 seed')
    ck(spec['geography_status'] == 'DESIGN_PROPOSAL_D07_001', 'fixed D07 geography status')
    ck(meta['generator_version'] == spec['generator_version'], 'metadata/spec generator version')
    ck(meta['spec_sha256'] == hashlib.sha256(spec_file.read_bytes()).hexdigest(),
       'graph records exact specification hash')
    params_file = base / 'config' / spec['generation_parameters_file']
    ck(meta['generation_parameters_sha256'] == hashlib.sha256(params_file.read_bytes()).hexdigest(),
       'graph records exact generation-parameter hash')
    ck(list(layer_by) == list(spec_by), 'metadata/spec ordered layers')
    ck(list(spec_by) == list('ROYGBV'), 'D07 selected Red through Violet strata')
    ck({n['code'] for n in nodes} == set('ROYGBV'), 'D07 contains exactly the six selected ROYGBV strata')
    ck([s['depth_min_mi'] for s in specs] == [0, 1.5, 3.5, 6.5, 11, 17],
       'D07 approved stratum minimum depths')
    ck([s['depth_max_mi'] for s in specs] == [1.5, 3.5, 6.5, 11, 17, 24],
       'D07 approved stratum maximum depths')
    ck(len(by) == len(nodes), 'unique permanent node IDs')
    ck(len(eb) == len(edges), 'unique permanent passage IDs')
    ck(len(layer_by) == len(layers), 'unique strata')

    g = nx.Graph()
    g.add_nodes_from(by)
    for idx, n in enumerate(nodes, 1):
        nid = n['node_id']
        ck(list(n) == NODE_FIELDS, nid + ' exact graph node schema/order')
        ck(n['code'] in layer_by, nid + ' valid stratum code')
        ck(bool(re.fullmatch(re.escape(n['code']) + r'[0-9]{3,}', nid)),
           nid + ' permanent local ID format')
        ck(n['global_index'] == idx, nid + ' snapshot global index')
        ck(all(isinstance(n[k], (int, float)) and math.isfinite(n[k]) for k in COORDS),
           nid + ' finite 3D coordinate')
        if n['code'] not in layer_by:
            continue
        l = layer_by[n['code']]
        ck(n['stratum'] == l['stratum'], nid + ' stratum name/code agreement')
        ck(l['depth_min_mi'] <= n['depth_mi'] <= l['depth_max_mi'],
           nid + ' within stratum depth interval')
        ck(n['network_role'] in {'principal', 'terminal_branch'},
           nid + ' selected network role')
        ck(bool(n['branch_id']) == (n['network_role'] == 'terminal_branch'),
           nid + ' branch identity matches role')
        ck(n['in_world_survey_status'] == 'UNASSIGNED', nid + ' no invented survey')
        ck('PROPOSAL' in n['geography_status'], nid + ' geography proposal status retained')
        ck(n['geography_status'] == spec['geography_status'], nid + ' exact configured D07 geography status')

    pair_links = defaultdict(list)
    for e in edges:
        eid = e['edge_id']
        ck(list(e) == EDGE_FIELDS, eid + ' exact graph edge schema/order')
        ck(bool(re.fullmatch(r'E[0-9]{4,}', eid)), eid + ' permanent passage ID format')
        if not ck(e['source'] in by and e['target'] in by, eid + ' valid endpoints'):
            continue
        a, b = by[e['source']], by[e['target']]
        ck(e['source'] != e['target'], eid + ' no self loop')
        ck(not g.has_edge(e['source'], e['target']), eid + ' unique unordered endpoint pair')
        g.add_edge(e['source'], e['target'], edge_id=eid, weight=e['modeled_centerline_mi'], kind=e['kind'])
        points = e['geometry_xyz_mi']
        valid_points = (isinstance(points, list) and len(points) >= 3
                        and all(isinstance(p, list) and len(p) == 3
                                and all(isinstance(v, (int, float)) and math.isfinite(v) for v in p)
                                for p in points))
        if not ck(valid_points, eid + ' actual finite 3D polyline with bends'):
            continue
        ck(points[0] == [a[k] for k in COORDS], eid + ' exact source geometry')
        ck(points[-1] == [b[k] for k in COORDS], eid + ' exact target geometry')
        chord = math.dist([a[k] for k in COORDS], [b[k] for k in COORDS])
        length = sum(math.dist(u, v) for u, v in zip(points, points[1:]))
        ck(abs(chord - e['straight_line_mi']) < EPS, eid + ' recomputed 3D chord')
        ck(abs(length - e['modeled_centerline_mi']) < EPS, eid + ' recomputed polyline length')
        ck(length > 0 and e['modeled_centerline_mi'] + EPS >= e['straight_line_mi'],
           eid + ' positive centerline length/chord bound')
        ck(abs(b['depth_mi'] - a['depth_mi'] - e['depth_change_source_to_target_mi']) < EPS,
           eid + ' recomputed signed depth change')
        ck(e['direction'] == 'UNDIRECTED_TOPOLOGY', eid + ' undirected geological connection')
        ck(all(e[k] == 'OPEN' for k in ('traversal_method', 'travel_time', 'terrain_detail')),
           eid + ' unresolved traversal retained')
        ck('PROPOSAL' in e['geography_status'], eid + ' geography proposal status retained')
        ck(e['geography_status'] == spec['geography_status'], eid + ' exact configured D07 geography status')
        expected_strata = a['stratum'] if a['code'] == b['code'] else a['stratum'] + '|' + b['stratum']
        ck(e['strata'] == expected_strata, eid + ' named strata synchronized')
        if e['kind'] == 'inter_stratum_passage':
            ck(abs(order[a['code']] - order[b['code']]) == 1, eid + ' adjacent strata only')
            ck(a['network_role'] == b['network_role'] == 'principal',
               eid + ' principal-only inter-stratum endpoints')
            low = min(a['depth_mi'], b['depth_mi'])
            high = max(a['depth_mi'], b['depth_mi'])
            ck(all(low - EPS <= p[2] <= high + EPS for p in points),
               eid + ' intermediate depth within endpoint span')
            ds = [q[2] - p[2] for p, q in zip(points, points[1:])]
            ck(all(d >= -EPS for d in ds) or all(d <= EPS for d in ds),
               eid + ' coherent monotone boundary traversal')
            pair = tuple(sorted((a['code'], b['code']), key=order.get))
            pair_links[pair].append(e)
        else:
            ck(e['kind'] in {'principal_passage', 'lateral_terminal_passage'}, eid + ' allowed local passage kind')
            ck(a['code'] == b['code'], eid + ' local passage same stratum')
            l = layer_by[a['code']]
            ck(all(l['depth_min_mi'] - EPS <= p[2] <= l['depth_max_mi'] + EPS for p in points),
               eid + ' complete local polyline stays in band')
            if e['kind'] == 'principal_passage':
                ck(a['network_role'] == b['network_role'] == 'principal', eid + ' principal passage endpoints')
            if e['kind'] == 'lateral_terminal_passage':
                ck(a['network_role'] == 'terminal_branch' or b['network_role'] == 'terminal_branch',
                   eid + ' terminal passage belongs to branch')
                if policies['terminal_arms_constant_depth']:
                    ck(all(abs(p[2] - a['depth_mi']) < EPS for p in points),
                       eid + ' all lateral polyline vertices constant depth')

    ck(g.number_of_edges() == len(edges), 'no duplicate undirected edges')
    ck(nx.number_of_selfloops(g) == 0, 'no self loops')
    ck(nx.is_connected(g), 'whole graph connected')
    core_ids = [n['node_id'] for n in nodes if n['network_role'] == 'principal']
    core = g.subgraph(core_ids)
    if policies['principal_core_biconnected'] is True:
        ck(nx.is_biconnected(core), 'global principal core vertex biconnected')
    ck('R001' in by and all(by['R001'][k] == 0 for k in COORDS), 'R001 exact origin')
    ck(by['R001']['site_type'] == 'surface_entrance', 'R001 entrance role')
    ck(sum(n['site_type'] == 'surface_entrance' for n in nodes) == 1, 'one configured primary entrance')
    ck(max(n['depth_mi'] for n in nodes) == 24, 'exact approved 24-mile maximum depth')
    ck(any(n['depth_mi'] == 24 and n['code'] == 'V' and n['network_role'] == 'principal'
           for n in nodes), 'at least one Violet principal node at exact maximum depth')

    for n in nodes:
        nid = n['node_id']
        ck(n['degree'] == g.degree(nid), nid + ' recomputed degree')
        ck(n['neighbors'] == '|'.join(sorted(g.neighbors(nid))), nid + ' recomputed sorted adjacency')
        if n['site_type'] == 'terminal_chamber_unassigned':
            ck(g.degree(nid) == 1, nid + ' terminal tip degree one')

    per_layer = []
    for i, s in enumerate(specs):
        code = s['code']
        l = layer_by[code]
        local = [n for n in nodes if n['code'] == code]
        cn = [n for n in local if n['network_role'] == 'principal']
        tn = [n for n in local if n['network_role'] == 'terminal_branch']
        local_core = g.subgraph(n['node_id'] for n in cn)
        local_graph = g.subgraph(n['node_id'] for n in local)
        ck(l['stratum'] == s['stratum'], code + ' selected name')
        for lk, sk in [('depth_min_mi', 'depth_min_mi'), ('depth_max_mi', 'depth_max_mi'),
                       ('principal_ew_span_mi', 'principal_ew_span_mi'),
                       ('provisional_ns_span_mi', 'provisional_ns_span_mi'),
                       ('core_node_count', 'core_node_count'), ('terminal_node_count', 'terminal_node_count'),
                       ('terminal_branch_count', 'terminal_branch_count')]:
            ck(l[lk] == s[sk], code + ' metadata/spec ' + sk)
        ck(len(cn) == s['core_node_count'], code + ' configured principal node count')
        ck(len(tn) == s['terminal_node_count'], code + ' configured terminal node count')
        ck(len(local) == l['node_count'], code + ' metadata node count')
        ck(abs(max(n['x_mi'] for n in cn) - min(n['x_mi'] for n in cn)
               - s['principal_ew_span_mi']) < EPS, code + ' principal total E-W span')
        ck(abs(min(n['x_mi'] for n in cn) + s['principal_ew_span_mi'] / 2) < EPS
           and abs(max(n['x_mi'] for n in cn) - s['principal_ew_span_mi'] / 2) < EPS,
           code + ' centered principal width anchors')
        ck(all(abs(n['y_mi']) <= s['provisional_ns_span_mi'] / 2 + EPS for n in cn),
           code + ' principal N-S placement envelope')
        if policies['principal_core_biconnected'] is True:
            ck(nx.is_biconnected(local_core), code + ' local principal core vertex biconnected')
        ck(nx.is_connected(local_graph), code + ' complete stratum connected')
        ck(local_graph.number_of_edges() == l['internal_edges'], code + ' metadata internal edges')
        rank = local_graph.number_of_edges() - len(local) + 1
        ck(rank == l['cycle_rank_internal'], code + ' metadata internal cycle rank')
        ck(round(max(n['x_mi'] for n in local) - min(n['x_mi'] for n in local), 3)
           == l['lateral_extent_ew_mi'], code + ' metadata total lateral E-W extent')
        west = sorted(local, key=lambda n: (n['x_mi'], n['y_mi'], n['depth_mi']))
        north = sorted(local, key=lambda n: (-n['y_mi'], n['x_mi'], n['depth_mi']))
        for j, n in enumerate(west, 1):
            ck(n['west_to_east_index'] == f'{code}-W{j:03d}', n['node_id'] + ' recomputed west-east alias')
        for j, n in enumerate(north, 1):
            ck(n['north_to_south_index'] == f'{code}-N{j:03d}', n['node_id'] + ' recomputed north-south alias')
        branches = defaultdict(list)
        for n in tn:
            branches[n['branch_id']].append(n['node_id'])
        ck(len(branches) == s['terminal_branch_count'], code + ' configured terminal branch count')
        for branch, ids in branches.items():
            external = set(v for u in ids for v in g.neighbors(u) if v not in ids)
            ck(len(external) == 1, branch + ' exactly one external attachment')
            ck(all(by[v]['network_role'] == 'principal' and by[v]['code'] == code for v in external),
               branch + ' attachment local principal')
            bg = g.subgraph(set(ids) | external)
            ck(nx.is_tree(bg), branch + ' connected acyclic terminal chain')
            ck(max(dict(bg.degree()).values()) <= 2, branch + ' chain degree at most two')
            ck(sum(g.degree(v) == 1 for v in ids) == 1, branch + ' exactly one terminal tip')
            ck(all(g.degree(v) in {1, 2} for v in ids), branch + ' terminal node full-graph degrees')
            ck(len({by[v]['depth_mi'] for v in set(ids) | external}) == 1, branch + ' attachment and chain same depth')
            ck(all(g[u][v]['kind'] == 'lateral_terminal_passage' for u, v in bg.edges()),
               branch + ' chain uses only lateral passages')
        if i + 1 < len(specs):
            other = specs[i + 1]['code']
            linked = pair_links[(code, other)]
            ck(len(linked) == s['links_to_next_layer'], code + '-' + other + ' configured link count')
            for side in (code, other):
                ends = [e['source'] if by[e['source']]['code'] == side else e['target'] for e in linked]
                ck(len(set(ends)) == len(ends), code + '-' + other + ' distinct ' + side + ' endpoints')
        else:
            ck(s['links_to_next_layer'] in {None, 0}, code + ' final layer no next links')
        per_layer.append({'stratum': s['stratum'], 'nodes': len(local), 'principal_nodes': len(cn),
                          'terminal_nodes': len(tn), 'terminal_branches': len(branches),
                          'internal_edges': local_graph.number_of_edges(), 'independent_cycles': rank})

    def check_csv(name, fields, expected):
        with (base / 'data' / name).open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            ck(reader.fieldnames == fields, name + ' exact reference header/order')
            rows = list(reader)
        ck(len(rows) == len(expected), name + ' exact row coverage')
        for index, (actual, wanted) in enumerate(zip(rows, expected), 1):
            for key in fields:
                if key == 'geometry_xyz_mi':
                    try:
                        value = json.loads(actual[key])
                    except (KeyError, ValueError, TypeError):
                        value = None
                    ck(value == wanted[key], f'{name} row {index} {key}')
                else:
                    ck(actual.get(key) == str(wanted[key]), f'{name} row {index} {key}')
    check_csv('nodes.csv', NODE_FIELDS, nodes)
    check_csv('edges.csv', EDGE_FIELDS, edges)
    check_csv('adjacency.csv', ADJACENCY_FIELDS, nodes)
    check_csv('view_index.csv', VIEW_FIELDS, nodes)
    check_csv('stratum_connections.csv', CONNECTION_FIELDS,
              [e for e in edges if e['kind'] == 'inter_stratum_passage'])

    gm = nx.read_graphml(base / 'data/dungeon_graph.graphml')
    ck(not gm.is_directed(), 'GraphML undirected')
    ck(not gm.is_multigraph(), 'GraphML simple graph')
    ck(set(gm) == set(g), 'GraphML exact node identity coverage')
    ck({frozenset(p) for p in gm.edges()} == {frozenset(p) for p in g.edges()},
       'GraphML exact connectivity')
    for nid in set(gm) & set(g):
        for key, value in by[nid].items():
            ck(gm.nodes[nid].get(key, '') == value, nid + ' GraphML node ' + key)
    for u, v, attrs in gm.edges(data=True):
        if not g.has_edge(u, v):
            continue
        edge = eb[g[u][v]['edge_id']]
        ck(attrs.get('edge_id') == edge['edge_id'], edge['edge_id'] + ' GraphML passage identity')
        ck(attrs.get('kind') == edge['kind'], edge['edge_id'] + ' GraphML passage kind')
        ck(abs(float(attrs.get('weight', -1)) - edge['modeled_centerline_mi']) < EPS,
           edge['edge_id'] + ' GraphML centerline weight')

    components = nx.number_connected_components(g)
    metrics = dict(nodes=len(nodes), edges=len(edges), principal_nodes=len(core_ids),
                   terminal_arm_nodes=len(nodes) - len(core_ids),
                   terminal_tips=sum(d == 1 for _, d in g.degree()),
                   interstratum_edges=sum(len(es) for es in pair_links.values()),
                   connected_components=components,
                   independent_cycles=len(edges) - len(nodes) + components,
                   average_degree=round(sum(dict(g.degree()).values()) / len(nodes), 3),
                   maximum_degree=max(dict(g.degree()).values()),
                   principal_articulation_points=list(nx.articulation_points(core)),
                   entrance_degree=g.degree('R001'))
    for key, value in metrics.items():
        ck(meta['metrics'][key] == value, 'metadata recomputed metric ' + key)
    generated_validation = json.loads((base / 'data/VALIDATION.json').read_text(encoding='utf-8'))
    ck(all(generated_validation['checks'].values()), 'generator self-checks report true')
    ck(generated_validation['metrics'] == meta['metrics'], 'generator validation metrics synchronized')
    ck(generated_validation['layers'] == layers, 'generator validation layers synchronized')
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((base / 'data').iterdir()) if p.is_file()}
    return {
        'status': 'FAIL' if failures else 'PASS',
        'validator_version': 'D07_METHOD_ALIGNED_INDEPENDENT_001',
        'dungeon_id': meta['dungeon_id'], 'revision': meta['revision'],
        'source_graph_sha256': hashes['dungeon_graph.json'],
        'source_spec_sha256': hashlib.sha256(spec_file.read_bytes()).hexdigest(),
        'scope': 'Structural Phase 2 graph, selected constraints and synchronized exports. '
                 'No ecological, geological-realism, accessibility, travel-time or narrative-event certification.',
        'check_count': count, 'failure_count': len(failures), 'failures': failures,
        'metrics': metrics, 'layers': per_layer,
        'interstratum_link_counts': {a + '-' + b: len(es) for (a, b), es in pair_links.items()},
        'graph_export_sha256': hashes,
        'pending_later_phases': ['Environmental companion', 'Party traversal classifications',
                                 'Authored expedition routes and schedules'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas-dir', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.atlas_dir)
    except (OSError, KeyError, ValueError, TypeError, IndexError, nx.NetworkXException) as exc:
        result = {'status': 'FAIL', 'failure_count': 1, 'failures': [str(exc)],
                  'scope': 'Input/schema failure; audit did not finish.'}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 1 if result['status'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
