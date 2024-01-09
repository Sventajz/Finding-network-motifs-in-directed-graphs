import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from mpi4py import MPI

startTime = datetime.now()

num_nodes = 200
random_seed = 42
subgraph_size = 10


def find_subgraphs(graph, subgraph_size, comm):
    subgraphs = []
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_subgraphs = []
    for i in range(rank, num_nodes - subgraph_size + 1, size):
        subgraph_nodes = list(graph.nodes())[i:i + subgraph_size]
        subgraph = graph.subgraph(subgraph_nodes)
        local_subgraphs.append(subgraph)

    serialized_subgraphs = [nx.to_dict_of_lists(subgraph) for subgraph in local_subgraphs]

    all_serialized_subgraphs = comm.gather(serialized_subgraphs, root=0)

    if rank == 0:
        all_subgraphs = [nx.from_dict_of_lists(serialized_subgraph) for sublist in all_serialized_subgraphs for serialized_subgraph in sublist]
        subgraphs = all_subgraphs

    return subgraphs

def create_directed_graph(num_nodes, random_seed=None):
    random.seed(random_seed)
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes + 1))
    all_edges = [(i, j) for i in range(1, num_nodes + 1) for j in range(1, num_nodes + 1) if i != j]
    random.shuffle(all_edges)
    selected_edges = all_edges[:len(all_edges) // 25]
    G.add_edges_from(selected_edges)

    return G, selected_edges

def check_isomorphic_range(args):
    i, j, subgraphs = args
    return i, j, nx.is_isomorphic(subgraphs[i], subgraphs[j])

def visualize_graph(G, comm):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)

    plt.show()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
G, edges = create_directed_graph(num_nodes, random_seed=random_seed)

subgraphs = find_subgraphs(G, subgraph_size, comm)
local_start = rank * len(subgraphs) // size
local_end = (rank + 1) * len(subgraphs) // size
local_motifs = []



motif_buckets = {}
motif_counter = {}

print(f"Process {rank} handling subgraphs {local_start} to {local_end - 1}")
for i in range(local_start, local_end):
    for j in range(i + 1, len(subgraphs)):
        if nx.is_isomorphic(subgraphs[i], subgraphs[j]):
            local_motifs.append((i, j))
            motif_type = (len(subgraphs[i].nodes()), (len(subgraphs[i].edges)))
   
            if motif_type not in motif_buckets:
                motif_buckets[motif_type] = []
                motif_counter[motif_type] = 0
            motif_buckets[motif_type].extend([subgraphs[i], subgraphs[j]])
            motif_counter[motif_type] += 2
            
print(f"Process {rank} found {len(local_motifs)} isomorphic subgraphs")
local_motifs_set = set(local_motifs)
all_motifs_set = comm.gather(local_motifs_set, root=0)
if rank == 0:
    flattened_motifs = list(set.union(*all_motifs_set))
    numberISO = len(flattened_motifs)
    print(f"Total unique isomorphic graphs: {numberISO}")
    for i, j in flattened_motifs:
        print(f"Graphs {i} and {j} are isomorphic:")
        print('Subgraph nodes:', subgraphs[i].nodes())
        print('Subgraph edges:', subgraphs[i].edges())
        print('Subgraph nodes:', subgraphs[j].nodes())
        print('Subgraph edges:', subgraphs[j].edges())
    print('Number of unique isomorphic graphs:', numberISO)

print(f"Number of motifs: {len(motif_buckets)}")
for motif_type, graphs in motif_buckets.items():
    print(f"Motif type: {motif_type}, Count of pairs: {motif_counter[motif_type]}")
print('rank: ', rank)
print('size: ', size)
print(datetime.now() - startTime)
visualize_graph(G, comm)
