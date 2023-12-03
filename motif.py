import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

def find_motifs(graph, motif_size):
    adjacency_matrix = nx.adjacency_matrix(graph, nodelist=sorted(graph.nodes())).todense()
    motifs = []

    for i in range(len(graph) - motif_size + 1):
        motif = adjacency_matrix[i:i + motif_size, i:i + motif_size]
        motifs.append(motif)

    return motifs
def create_directed_graph(num_nodes):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(range(1, num_nodes + 1))

    # Create a list of all possible edges
    all_edges = [(i, j) for i in range(1, num_nodes + 1) for j in range(1, num_nodes + 1) if i != j]

    # Randomly shuffle the edges
    random.shuffle(all_edges)

    # Choose a subset of edges (e.g., the first half of the shuffled list)
    selected_edges = all_edges[:len(all_edges) // 2]

    # Add the selected edges to the graph
    G.add_edges_from(selected_edges)

    return G
def visualize_graph(G):
    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    # Display the plot
    plt.show()

if __name__ == "__main__":
    # Create a directed graph (replace this with your graph)
    # G = nx.DiGraph()
    # G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])

    num_nodes = 10
    G = create_directed_graph(num_nodes)
    # Define the motif size
    motif_size = 5

    # Find motifs in the graph
    motifs = find_motifs(G, motif_size)

    # Print the motifs
    print("Motifs:")
    for motif in motifs:
        print('motif : ', motif)
    visualize_graph(G)
