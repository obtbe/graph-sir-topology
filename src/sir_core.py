import numpy as np
from scipy.sparse import csr_matrix

class SIRSimulation:
    def __init__(self, adjacency: csr_matrix, beta: float = 0.3, gamma: float = 0.1):
        """
        Initialize SIR simulation on a graph.
        
        Parameters:
        -----------
        adjacency : csr_matrix
            Sparse adjacency matrix of the graph
        beta : float
            Infection probability (per edge, per time step)
        gamma : float
            Recovery probability (per time step)
        """
        self.adj = adjacency
        self.n = adjacency.shape[0]
        self.beta = beta
        self.gamma = gamma
        
    def initialize_states(self, seed_nodes=None):
        """
        Initialize S, I, R state vectors.
        
        Parameters:
        -----------
        seed_nodes : list or None
            List of initially infected nodes. If None, picks one random node.
        """
        self.S = np.ones(self.n, dtype=bool)  # Susceptible
        self.I = np.zeros(self.n, dtype=bool)  # Infectious
        self.R = np.zeros(self.n, dtype=bool)  # Recovered
        
        if seed_nodes is None:
            # Pick one random node as initial infection
            seed_nodes = [np.random.randint(0, self.n)]
        
        for node in seed_nodes:
            self.S[node] = False
            self.I[node] = True
    
    def step(self):
        """
        Perform one time step of the SIR model.
        
        Returns:
        --------
        counts : tuple (S_count, I_count, R_count)
        """
        # Find currently infected nodes
        infected_nodes = np.where(self.I)[0]
        
        if len(infected_nodes) == 0:
            return (np.sum(self.S), np.sum(self.I), np.sum(self.R))
        
        # Step 1: Infections (S -> I)
        # For each infected node, find its neighbors
        # Using CSR format: adjacency.indices and adjacency.indptr
        new_infections = np.zeros(self.n, dtype=bool)
        
        for node in infected_nodes:
            # Get neighbors of this node from CSR matrix
            start = self.adj.indptr[node]
            end = self.adj.indptr[node + 1]
            neighbors = self.adj.indices[start:end]
            
            # Find susceptible neighbors
            susceptible_neighbors = neighbors[self.S[neighbors]]
            
            # Infect with probability beta
            for neighbor in susceptible_neighbors:
                if np.random.random() < self.beta:
                    new_infections[neighbor] = True
        
        # Step 2: Recoveries (I -> R)
        new_recoveries = np.zeros(self.n, dtype=bool)
        for node in infected_nodes:
            if np.random.random() < self.gamma:
                new_recoveries[node] = True
        
        # Update states
        self.S = self.S & ~new_infections  # S loses newly infected
        self.I = (self.I & ~new_recoveries) | new_infections  # I loses recovered, gains new infections
        self.R = self.R | new_recoveries  # R gains recovered
        
        return (np.sum(self.S), np.sum(self.I), np.sum(self.R))
    
    def run(self, max_steps=100, seed_nodes=None):
        """
        Run full simulation until no infected nodes remain or max_steps reached.
        
        Returns:
        --------
        history : dict with keys 'S', 'I', 'R' containing lists of counts over time
        """
        self.initialize_states(seed_nodes)
        
        history = {'S': [], 'I': [], 'R': []}
        
        for step in range(max_steps):
            S_count, I_count, R_count = self.step()
            history['S'].append(S_count)
            history['I'].append(I_count)
            history['R'].append(R_count)
            
            # Stop if no infected nodes remain
            if I_count == 0:
                break
        
        return history