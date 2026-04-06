from src.graph_loader import load_facebook_graph, generate_barabasi_albert_graph, graph_to_csr

print("Testing Facebook graph...")
fb_graph = load_facebook_graph()
fb_csr = graph_to_csr(fb_graph)
print(f"CSR shape: {fb_csr.shape}, Non-zero entries: {fb_csr.nnz}")

print("\nTesting Barabasi-Albert graph...")
ba_graph = generate_barabasi_albert_graph(4039, 10)
ba_csr = graph_to_csr(ba_graph)
print(f"CSR shape: {ba_csr.shape}, Non-zero entries: {ba_csr.nnz}")

print("\nBoth graphs loaded successfully!")