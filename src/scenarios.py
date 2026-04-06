import numpy as np
from scipy.sparse import csr_matrix
from src.sir_core import SIRSimulation

def remove_nodes_by_degree(adj, fraction, remove_highest=True):
    """
    Remove a fraction of nodes based on degree.
    
    Parameters:
    -----------
    adj : csr_matrix
        Sparse adjacency matrix
    fraction : float
        Fraction of nodes to remove (0.0 to 1.0)
    remove_highest : bool
        If True, remove highest-degree nodes (targeted).
        If False, remove random nodes (random immunization).
    
    Returns:
    --------
    new_adj : csr_matrix
        Adjacency matrix with nodes removed
    removed_mask : np.ndarray
        Boolean mask of removed nodes
    """
    n = adj.shape[0]
    
    # Calculate degrees
    degrees = np.array(adj.sum(axis=1)).flatten()
    
    if remove_highest:
        # Targeted: remove highest degree nodes
        threshold = np.percentile(degrees, 100 * (1 - fraction))
        removed_mask = degrees >= threshold
    else:
        # Random: randomly select nodes
        n_remove = int(n * fraction)
        removed_indices = np.random.choice(n, n_remove, replace=False)
        removed_mask = np.zeros(n, dtype=bool)
        removed_mask[removed_indices] = True
    
    # Keep only nodes not removed
    keep_mask = ~removed_mask
    keep_indices = np.where(keep_mask)[0]
    
    # Create new adjacency matrix with removed nodes excluded
    new_adj = adj[keep_mask, :][:, keep_mask]
    
    return new_adj, removed_mask

def run_scenario(adj, scenario_name, beta=0.3, gamma=0.1, removal_fraction=0.1):
    """
    Run SIR simulation for a specific scenario.
    
    Parameters:
    -----------
    adj : csr_matrix
        Original adjacency matrix
    scenario_name : str
        'baseline', 'targeted', or 'random'
    beta, gamma : float
        SIR parameters
    removal_fraction : float
        Fraction of nodes to remove (for targeted/random)
    
    Returns:
    --------
    history : dict
        Simulation history
    metadata : dict
        Additional info about the scenario
    """
    metadata = {'scenario': scenario_name}
    
    if scenario_name == 'baseline':
        sim_adj = adj
        metadata['nodes_removed'] = 0
        metadata['edges_removed'] = 0
        
    elif scenario_name == 'targeted':
        sim_adj, removed_mask = remove_nodes_by_degree(adj, removal_fraction, remove_highest=True)
        metadata['nodes_removed'] = np.sum(removed_mask)
        metadata['edges_removed'] = adj.nnz - sim_adj.nnz
        
    elif scenario_name == 'random':
        sim_adj, removed_mask = remove_nodes_by_degree(adj, removal_fraction, remove_highest=False)
        metadata['nodes_removed'] = np.sum(removed_mask)
        metadata['edges_removed'] = adj.nnz - sim_adj.nnz
    
    sir = SIRSimulation(sim_adj, beta=beta, gamma=gamma)
    history = sir.run(max_steps=50)
    
    return history, metadata