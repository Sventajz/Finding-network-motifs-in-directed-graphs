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

def print_motif(motif):
    print("Motif:")
    for row in motif:
        print(' '.join(map(str, row)))

def create_directed_graph(num_nodes, random_seed=None):
    # Set the random seed for reproducibility
    random.seed(random_seed)

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

    return G, selected_edges

def visualize_graph(G):
    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    # Display the plot
    plt.show()

if __name__ == "__main__":
    num_nodes = 10

    # Set the random seed for graph generation
    random_seed = 42  # You can choose any seed value
    G, edges = create_directed_graph(num_nodes, random_seed=random_seed)

    # Define the motif size
    motif_size = 5

    # Find motifs in the graph
    motifs = find_motifs(G, motif_size)

    # Print the motifs
    for i, motif in enumerate(motifs, 1):
        print(f"Motif {i}:")
        print_motif(motif)
        print()

    # Print the edges
    print("Edges:")
    print(edges)

    # Visualize the graph
    visualize_graph(G)
