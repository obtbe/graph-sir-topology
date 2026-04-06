# Graph SIR Simulation: How Topology Shapes Epidemics

## The Question

Does the way we organize our social networks (tight friend groups vs hub-dominated) change how a virus spreads?

## The Experiment

- **Real graph:** Facebook social network (4,039 nodes, 88,234 edges) – high clustering, friend groups
- **Synthetic graph:** Barabasi-Albert (4,039 nodes, 40,290 edges) – preferential attachment, dominant hubs
- **SIR parameters:** beta = 0.3 (infection probability), gamma = 0.1 (recovery probability)

## Visual Results

### Facebook SIR Curve
![Facebook SIR Curve](results/facebook_sir_curve.png)

### Facebook vs Barabasi-Albert Comparison
![Comparison Plot](results/comparison_plot.png)

### Immunization Strategies: Targeted vs Random
![Scenarios Comparison](results/scenarios_comparison.png)

## The Results

| Metric | Facebook (Real) | Barabasi-Albert (Synthetic) |
|--------|-----------------|-----------------------------|
| Time to peak | Step 6 | Step 3 (2x faster) |
| Peak infection | 2,994 nodes (74%) | 3,580 nodes (89%) |
| Curve shape | Gradual rise, bumpy, long tail | Sharp spike, smooth, rapid decline |

## The Interpretation

The Barabasi-Albert graph is an **accelerant**. Once a hub gets infected, the virus reaches the entire network almost instantly.

The Facebook graph has **natural firewalls** – friend groups create "hesitation" as the virus jumps between communities.

## Immunization Strategies: Targeted vs Random

We tested two intervention strategies on the Facebook graph:

- **Targeted:** Remove top 10% highest-degree nodes (the "superspreaders")
- **Random:** Remove random 10% of nodes

### Results

| Strategy | Peak Infection | Nodes Removed | Edges Removed | Initial Delay |
|----------|---------------|---------------|---------------|----------------|
| Baseline | 3,029 | 0 | 0 | No |
| Targeted | 2,545 | 404 | 87,724 | Yes (flat start) |
| Random | 2,394 | 403 | 33,006 | No |

### The Counterintuitive Finding

Random immunization outperformed targeted immunization, even though targeted removed 2.6x more edges.

**Why?** The Facebook graph is made of dense friend groups (clusters). Targeted removed the bridges between clusters but left each cluster intact. Once the infection entered a cluster, it spread rapidly.

Random immunization poked holes in every cluster, fragmenting the internal structure and reducing spread everywhere.

### The Lesson

Network topology determines which intervention works best. For highly clustered networks (like social media), random vaccination may be more effective than targeting hubs.

## Why This Matters

Understanding network topology helps predict:
- How fast misinformation spreads
- Where to vaccinate first
- Why some networks are more resilient than others

## How to Run

```bash
git clone https://github.com/obtbe/graph-sir-topology
cd graph-sir-topology
pip install -r requirements.txt
python test_comparison.py
python test_scenarios.py