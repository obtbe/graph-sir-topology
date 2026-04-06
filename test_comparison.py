from src.graph_loader import load_facebook_graph, generate_barabasi_albert_graph, graph_to_csr
from src.sir_core import SIRSimulation
import matplotlib.pyplot as plt
import numpy as np

# Load both graphs
print("=" * 50)
print("Loading graphs...")
print("=" * 50)

fb_graph = load_facebook_graph()
fb_adj = graph_to_csr(fb_graph)

ba_graph = generate_barabasi_albert_graph(4039, 10)
ba_adj = graph_to_csr(ba_graph)

# Run simulations with same parameters
beta = 0.3
gamma = 0.1

print("\n" + "=" * 50)
print(f"Running SIR (beta={beta}, gamma={gamma})...")
print("=" * 50)

print("\nFacebook graph...")
sir_fb = SIRSimulation(fb_adj, beta=beta, gamma=gamma)
history_fb = sir_fb.run(max_steps=50)

print("\nBarabasi-Albert graph...")
sir_ba = SIRSimulation(ba_adj, beta=beta, gamma=gamma)
history_ba = sir_ba.run(max_steps=50)

# Plot comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Facebook plot
axes[0].plot(history_fb['S'], label='Susceptible', linewidth=2)
axes[0].plot(history_fb['I'], label='Infectious', linewidth=2)
axes[0].plot(history_fb['R'], label='Recovered', linewidth=2)
axes[0].set_xlabel('Time steps')
axes[0].set_ylabel('Number of nodes')
axes[0].set_title(f'Facebook Graph (real)\nPeak infection: {max(history_fb["I"])} nodes')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Barabasi-Albert plot
axes[1].plot(history_ba['S'], label='Susceptible', linewidth=2)
axes[1].plot(history_ba['I'], label='Infectious', linewidth=2)
axes[1].plot(history_ba['R'], label='Recovered', linewidth=2)
axes[1].set_xlabel('Time steps')
axes[1].set_ylabel('Number of nodes')
axes[1].set_title(f'Barabasi-Albert Graph (synthetic)\nPeak infection: {max(history_ba["I"])} nodes')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/comparison_plot.png', dpi=150)
print("\n" + "=" * 50)
print("Comparison plot saved to results/comparison_plot.png")
print("=" * 50)

# Print statistics
print("\n STATISTICS:")
print(f"Facebook graph      - Peak infection: {max(history_fb['I'])} nodes ({max(history_fb['I'])/4039*100:.1f}%)")
print(f"Barabasi-Albert     - Peak infection: {max(history_ba['I'])} nodes ({max(history_ba['I'])/4039*100:.1f}%)")