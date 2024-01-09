import networkx as nx
import random
import matplotlib.pyplot as plt
from datetime import datetime
startTime = datetime.now()

num_nodes = 200
random_seed = 42 
subgraph_size = 4

def create_directed_graph(num_nodes, random_seed=None):
    random.seed(random_seed)
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes + 1))
    all_edges = [(i, j) for i in range(1, num_nodes + 1) for j in range(1, num_nodes + 1) if i != j]
    #print(all_edges)
    random.shuffle(all_edges)
    selected_edges = all_edges[:len(all_edges) // 25]
    print(selected_edges)
    print(len(selected_edges))
    G.add_edges_from(selected_edges)
    

    return G, selected_edges

def find_subgraphs(graph, subgraph_size):
    subgraphs = []

    for i in range(len(graph) - subgraph_size + 1):
        subgraph_nodes = list(graph.nodes())[i:i + subgraph_size]
        subgraph = graph.subgraph(subgraph_nodes)
        subgraphs.append(subgraph)

    return subgraphs

def visualize_graph(G):
    pos = nx.spring_layout(G, threshold=0.9) 
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    plt.show()


motif_buckets = {}
motif_counter = {}
G, edges = create_directed_graph(num_nodes, random_seed=random_seed)
subgraphs = find_subgraphs(G, subgraph_size)
numer_iso = 0
for i in range(len(subgraphs)):
    for j in range(i + 1, len(subgraphs)):
        if nx.is_isomorphic(subgraphs[i], subgraphs[j]):
            numer_iso += 1
            if numer_iso >= 3:
                motif_type = (len(subgraphs[i].nodes()), (len(subgraphs[i].edges)))
                # Check if the motif type is already a key in the dictionary
                if motif_type not in motif_buckets:
                    motif_buckets[motif_type] = []
                    motif_counter[motif_type] = 0
                motif_buckets[motif_type].extend([subgraphs[i], subgraphs[j]])
                motif_counter[motif_type] += 2

# Print information about isomorphic graphs in each motif type bucket
for motif_type, graphs in motif_buckets.items():
    print(f"Motif type: {motif_type}")
    for idx, graph in enumerate(graphs):
        print(f"Graph {idx + 1}:")
        print('Subgraph nodes:', graph.nodes())
        print('Subgraph edges:', graph.edges())

print(f"Number of motifs: {len(motif_buckets)}")
for motif_type, graphs in motif_buckets.items():
    print(f"Motif type: {motif_type}, Count of pairs: {motif_counter[motif_type]}")
print('Number of isomorphic graphs: ', numer_iso)
print(datetime.now() - startTime)
visualize_graph(G)
