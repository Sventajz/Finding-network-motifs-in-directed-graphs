import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
startTime = datetime.now()

def find_subgraphs(graph, subgraph_size):
    subgraphs = []

    for i in range(len(graph) - subgraph_size + 1):
        subgraph_nodes = list(graph.nodes())[i:i + subgraph_size]
        subgraph = graph.subgraph(subgraph_nodes)
        subgraphs.append(subgraph)

    return subgraphs

def create_directed_graph(num_nodes, random_seed=None):
    random.seed(random_seed)
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes + 1))
    all_edges = [(i, j) for i in range(1, num_nodes + 1) for j in range(1, num_nodes + 1) if i != j]
    random.shuffle(all_edges)
    selected_edges = all_edges[:len(all_edges) // 2]
    G.add_edges_from(selected_edges)

    return G, selected_edges

def visualize_graph(G):
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    plt.show()


if __name__ == "__main__":
    num_nodes = 200
    random_seed = 42 
    G, edges = create_directed_graph(num_nodes, random_seed=random_seed)

    subgraph_size = 6
    subgraphs = find_subgraphs(G, subgraph_size)
    numberISO = 0
    isMotif = 0
    for i in range(len(subgraphs)):
        for j in range(i+1, len(subgraphs)):

            if nx.is_isomorphic(subgraphs[i], subgraphs[j]):
                
                numberISO+=1
                if numberISO >=3:
                    isMotif = 1
                    print(f"graphs {i} and {j} are motifs: ")
                    print('subgraph nodes:', subgraphs[i].nodes())
                    print('subgraph edges:', subgraphs[i].edges())
                    print('subgraph nodes:', subgraphs[j].nodes())
                    print('subgraph edges:', subgraphs[j].edges())

    print('number of isomorphic graphs: ', numberISO)
    print(datetime.now() - startTime)
    visualize_graph(G)
