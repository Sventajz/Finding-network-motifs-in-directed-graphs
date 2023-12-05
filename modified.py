import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from mpi4py import MPI

startTime = datetime.now()

def find_subgraphs(graph, subgraph_size, comm):
    subgraphs = []

    rank = comm.Get_rank()
    size = comm.Get_size()

    local_subgraphs = []
    for i in range(rank, len(graph) - subgraph_size + 1, size):
        subgraph_nodes = list(graph.nodes())[i:i + subgraph_size]
        subgraph = graph.subgraph(subgraph_nodes)
        local_subgraphs.append(subgraph)

    # Serialize subgraphs to adjacency lists
    serialized_subgraphs = [nx.to_dict_of_lists(subgraph) for subgraph in local_subgraphs]

    all_serialized_subgraphs = comm.gather(serialized_subgraphs, root=0)
    if rank == 0:
        # Deserialize and reconstruct subgraphs
        all_subgraphs = [nx.from_dict_of_lists(serialized_subgraph) for sublist in all_serialized_subgraphs for serialized_subgraph in sublist]
        subgraphs = all_subgraphs

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

def check_isomorphic_range(args):
    i, j, subgraphs = args
    return i, j, nx.is_isomorphic(subgraphs[i], subgraphs[j])

def visualize_graph(G, comm):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    plt.show()

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    num_nodes = 200
    random_seed = 42
    G, edges = create_directed_graph(num_nodes, random_seed=random_seed)

    subgraph_size = 4
    subgraphs = find_subgraphs(G, subgraph_size, comm)

    local_start = rank * len(subgraphs) // size
    local_end = (rank + 1) * len(subgraphs) // size

    local_isomorphic_results = []

    for i in range(local_start, local_end):
        for j in range(i + 1, len(subgraphs)):
            isomorphic_result = check_isomorphic_range((i, j, subgraphs))
            local_isomorphic_results.append(isomorphic_result)

    all_isomorphic_results = comm.gather(local_isomorphic_results, root=0)

    if rank == 0:
        flattened_results = [result for sublist in all_isomorphic_results for result in sublist]
        numberISO = sum(result[2] for result in flattened_results)
        isMotif = 1 if numberISO >= 3 else 0

        for i, j, is_isomorphic in flattened_results:
            if is_isomorphic:
                print(f"graphs {i} and {j} are motifs: ")
                print('subgraph nodes:', subgraphs[i].nodes())
                print('subgraph edges:', subgraphs[i].edges())
                print('subgraph nodes:', subgraphs[j].nodes())
                print('subgraph edges:', subgraphs[j].edges())

        print('Number of isomorphic graphs:', numberISO)
    print(datetime.now() - startTime)
    visualize_graph(G, comm)
