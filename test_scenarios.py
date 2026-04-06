from src.graph_loader import load_facebook_graph, graph_to_csr
from src.scenarios import run_scenario
import matplotlib.pyplot as plt

print("Loading Facebook graph...")
fb_graph = load_facebook_graph()
adj = graph_to_csr(fb_graph)

beta = 0.3
gamma = 0.1
removal_fraction = 0.1

print(f"\nRunning scenarios (beta={beta}, gamma={gamma}, removal={removal_fraction})...")

# Run three scenarios
scenarios = ['baseline', 'targeted', 'random']
results = {}

for scenario in scenarios:
    print(f"\n{scenario.upper()} scenario...")
    history, metadata = run_scenario(adj, scenario, beta, gamma, removal_fraction)
    results[scenario] = {'history': history, 'metadata': metadata}
    print(f"  Peak infection: {max(history['I'])} nodes")
    if scenario != 'baseline':
        print(f"  Nodes removed: {metadata['nodes_removed']}")
        print(f"  Edges removed: {metadata['edges_removed']}")

# Plot comparison
fig, ax = plt.subplots(figsize=(12, 6))

colors = {'baseline': 'blue', 'targeted': 'green', 'random': 'orange'}
labels = {'baseline': 'Baseline (no intervention)', 
          'targeted': f'Targeted immunization (top {removal_fraction*100:.0f}%)',
          'random': f'Random immunization ({removal_fraction*100:.0f}%)'}

for scenario in scenarios:
    history = results[scenario]['history']
    ax.plot(history['I'], color=colors[scenario], linewidth=2, label=labels[scenario])

ax.set_xlabel('Time steps')
ax.set_ylabel('Number of infectious nodes')
ax.set_title(f'SIR Simulation on Facebook Graph\nTargeted vs Random Immunization')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('results/scenarios_comparison.png', dpi=150)
print("\nScenarios comparison plot saved to results/scenarios_comparison.png")