import networkx as nx
import matplotlib.pyplot as plt
import random

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
    # Number of nodes in the graph
    num_nodes = 10

    # Create a directed graph with randomized edges
    directed_graph = create_directed_graph(num_nodes)

    # Visualize the directed graph
    visualize_graph(directed_graph)
