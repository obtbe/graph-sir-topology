from src.graph_loader import load_facebook_graph, graph_to_csr
from src.sir_core import SIRSimulation
import matplotlib.pyplot as plt

# Load Facebook graph
print("Loading graph...")
fb_graph = load_facebook_graph()
adj_csr = graph_to_csr(fb_graph)

# Run simulation
print("Running SIR simulation...")
sir = SIRSimulation(adj_csr, beta=0.3, gamma=0.1)
history = sir.run(max_steps=50)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(history['S'], label='Susceptible', linewidth=2)
plt.plot(history['I'], label='Infectious', linewidth=2)
plt.plot(history['R'], label='Recovered', linewidth=2)
plt.xlabel('Time steps')
plt.ylabel('Number of nodes')
plt.title('SIR Simulation on Facebook Graph')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/facebook_sir_curve.png', dpi=150)
plt.show()

print(f"Simulation completed in {len(history['I'])} steps")
print(f"Peak infection: {max(history['I'])} nodes")