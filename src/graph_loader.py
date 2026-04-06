import numpy as np
import networkx as nx
import pandas as pd
import requests
import gzip
import io
from scipy.sparse import csr_matrix

def load_facebook_graph():
    """
    Downloads and loads the SNAP Facebook dataset.
    Returns NetworkX graph and adjacency matrix (CSR).
    """
    print("Downloading Facebook dataset...")
    url = "https://snap.stanford.edu/data/facebook_combined.txt.gz"
    response = requests.get(url)
    
    print("Loading graph...")
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
        df = pd.read_csv(f, sep=" ", names=["start_node", "end_node"])
        G = nx.from_pandas_edgelist(df, "start_node", "end_node")
    
    print(f"Facebook graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def generate_barabasi_albert_graph(n_nodes=4039, m=10):
    """
    Generates a Barabasi-Albert graph with same size as Facebook dataset.
    m = number of edges to attach from new node to existing nodes.
    """
    print(f"Generating Barabasi-Albert graph ({n_nodes} nodes, m={m})...")
    G = nx.barabasi_albert_graph(n_nodes, m)
    print(f"BA graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def graph_to_csr(G):
    """Convert NetworkX graph to CSR sparse matrix."""
    adj = nx.adjacency_matrix(G)
    return adj.tocsr()

def get_degree_info(G):
    """Return array of degrees for all nodes."""
    degrees = np.array([d for n, d in G.degree()])
    return degrees