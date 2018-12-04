import networkx as nx
import json

with open('state_net.json', 'r') as f:
    network = json.loads(f.read())

network_map = {}
for node, params in network.items():
    new_name = (node + ' ' + params['info']['type'] + "\n" +
                str(tuple(params["shape"]["output"])))
    network_map[node] = new_name

graph = nx.DiGraph()
for node, params in network.items():
    output_nodes = params['connection']['output']
    for o_node in output_nodes:
        graph.add_edge(network_map[node], network_map[o_node])

dotgraph = nx.nx_pydot.to_pydot(graph)
dotgraph.set('rankdir', 'LR')
dotgraph.set('dpi', 300)
dotgraph.write('PureVis.png', format='png')
