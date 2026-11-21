#!/usr/bin/env python3
"""Validate an authored route or compute one shortest modeled-distance path; join saved environmental profiles."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import networkx as nx

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='New output directory; existing directories are refused')
    parser.add_argument('--route-json', type=Path, help='Use exact outbound_nodes from an authored route, without optimization')
    parser.add_argument('--start', help='Start node for shortest-modeled-distance calculation')
    parser.add_argument('--target', help='Target node for shortest-modeled-distance calculation')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output directory exists. Choose a new directory.')
    if args.route_json and (args.start or args.target):
        parser.error('Use --route-json OR both --start and --target.')
    if not args.route_json and not (args.start and args.target):
        parser.error('Supply --route-json OR both --start and --target.')
    try:
        graph_file = args.atlas_dir / 'data/dungeon_graph.json'
        model = json.loads(graph_file.read_text(encoding='utf-8'))
        nodes = {row['node_id']: row for row in model['nodes']}
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        for edge in model['edges']:
            if graph.has_edge(edge['source'], edge['target']):
                raise ValueError('Parallel passages require an edge-explicit MultiGraph route implementation.')
            graph.add_edge(edge['source'], edge['target'], **edge, weight=edge['modeled_centerline_mi'])
        route_meta = json.loads(args.route_json.read_text(encoding='utf-8')) if args.route_json else {}
        if args.route_json:
            route = route_meta.get('outbound_nodes', [])
            selection = 'Authored itinerary; not replaced by a shortest-path query'
        else:
            route = nx.shortest_path(graph, args.start, args.target, weight='weight')
            selection = 'One shortest path by modeled centerline distance only'
        if not isinstance(route, list) or len(route) < 2 or any(n not in nodes for n in route):
            raise ValueError('A route needs at least two valid node IDs.')
        for u, v in zip(route, route[1:]):
            if not graph.has_edge(u, v):
                raise ValueError(f'No actual passage connects {u} to {v}.')
        node_file = args.atlas_dir / 'data/environment_nodes_003.csv'
        edge_file = args.atlas_dir / 'data/environment_passages_003.csv'
        node_env = {r['node_id']: r for r in read_csv(node_file)} if node_file.exists() else {}
        edge_env = {r['edge_id']: r for r in read_csv(edge_file)} if edge_file.exists() else {}
        rows = []
        cumulative = 0.0
        sequence_edges = []
        for i, node_id in enumerate(route):
            node = nodes[node_id]
            outgoing = graph[node_id][route[i+1]] if i + 1 < len(route) else None
            env = node_env.get(node_id, {})
            attributes = ['genesis_flora', 'hydrology', 'genesis_crystals', 'vaen_formation', 'natural_velis', 'eldris_formation_potential']
            features = '; '.join(f'{k}={env[k]}' for k in attributes if k in env)
            row = {'step': i+1, 'node_id': node_id, 'stratum': node['stratum'],
                   'depth_mi': node['depth_mi'], 'cumulative_modeled_mi': round(cumulative, 6),
                   'geological_type': env.get('geological_type', 'OPEN'), 'expected_features': features or 'OPEN',
                   'environment_status': env.get('status', 'UNASSIGNED'),
                   'outgoing_edge': outgoing['edge_id'] if outgoing else '',
                   'next_node': route[i+1] if outgoing else '',
                   'outgoing_modeled_mi': outgoing['modeled_centerline_mi'] if outgoing else '',
                   'outgoing_difficulty': edge_env.get(outgoing['edge_id'], {}).get('difficulty', 'OPEN') if outgoing else '',
                   'actual_encounters': 'NOT_ESTABLISHED', 'travel_time': 'OPEN', 'fatigue_cost': 'OPEN'}
            rows.append(row)
            if outgoing:
                cumulative += outgoing['modeled_centerline_mi']
                sequence_edges.append(outgoing['edge_id'])
        report = {'selection': selection, 'route_id': route_meta.get('route_id', 'ANALYSIS_ONLY'),
                  'route_status': route_meta.get('status', 'UNLOCKED_ANALYSIS'),
                  'graph_revision': model['metadata'].get('revision'),
                  'graph_sha256': hashlib.sha256(graph_file.read_bytes()).hexdigest(),
                  'nodes': route, 'edges': sequence_edges, 'node_visits': len(route), 'passages': len(sequence_edges),
                  'modeled_one_way_mi': round(cumulative, 6), 'end_depth_mi': nodes[route[-1]]['depth_mi'],
                  'return_policy': route_meta.get('return_policy', 'NOT_SELECTED'),
                  'environment_is_provisional': True,
                  'qualification': 'No elapsed time, exact encounter count, safe crossing method, or narrative day is inferred.'}
        if route_meta.get('return_policy') == 'REVERSE_OUTBOUND':
            report['return_nodes'] = list(reversed(route))
            report['modeled_round_trip_mi'] = round(2*cumulative, 6)
        args.output.mkdir(parents=True)
        (args.output/'route_report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        with (args.output/'route_nodes.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer=csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        lines=['# Dungeon route report', '', selection, '', '**Route:** '+' → '.join(route), '',
               f'**Modeled one-way distance:** {cumulative:.6f} miles. **Endpoint depth:** {nodes[route[-1]]["depth_mi"]:.6f} miles.', '',
               'These are graph-centerline distances, not travel times or a survey claim. Environmental expectations are provisional; actual encounters remain open.', '']
        for row in rows:
            lines += [f'## {row["step"]}. {row["node_id"]}', '',
                      f'Depth: {row["depth_mi"]} miles. Cumulative modeled travel: {row["cumulative_modeled_mi"]} miles.', '',
                      f'Geology: {row["geological_type"]}.', '', row['expected_features']+'.', '',
                      f'Next: {row["outgoing_edge"]} → {row["next_node"]}; provisional difficulty: {row["outgoing_difficulty"]}.' if row['next_node'] else 'Endpoint.', '']
        (args.output/'route_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2))
        return 0
    except (OSError, ValueError, KeyError, nx.NetworkXException) as exc:
        print(f'Route report failed: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
