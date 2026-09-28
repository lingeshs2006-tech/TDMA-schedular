import json
import networkx as nx

RADIO_RANGE = 500.0

# Read coordinates
with open("sample_input.json", "r") as f:
    coordinates = json.load(f)

# Create communication graph
G = nx.Graph()

for node, position in coordinates.items():
    G.add_node(node, position=tuple(position))

nodes = list(coordinates.keys())

# Add communication links
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):

        node1 = nodes[i]
        node2 = nodes[j]

        x1, y1 = coordinates[node1]
        x2, y2 = coordinates[node2]

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        if distance <= RADIO_RANGE:
            G.add_edge(node1, node2, distance=distance)

# Display direct neighbors
print("=" * 60)
print("COMMUNICATION GRAPH")
print("=" * 60)

for node in G.nodes():
    neighbors = sorted(G.neighbors(node))

    print(f"{node}: {neighbors}")

# Create Distance-2 conflict graph
D2 = nx.Graph()
D2.add_nodes_from(G.nodes())

for node in G.nodes():

    # Nodes reachable within 2 hops
    reachable = nx.single_source_shortest_path_length(
        G,
        node,
        cutoff=2
    )

    for other, distance in reachable.items():

        if node != other and distance <= 2:
            D2.add_edge(node, other)

# Display conflicts
print("\n" + "=" * 60)
print("DISTANCE-2 CONFLICT GRAPH")
print("=" * 60)

for node in D2.nodes():
    conflicts = sorted(D2.neighbors(node))

    print(f"{node}: {conflicts}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Communication links: {G.number_of_edges()}")
print(f"Distance-2 conflict links: {D2.number_of_edges()}")
print("\n" + "=" * 60)
print("NODE CONFLICT DEGREES")
print("=" * 60)

for node in D2.nodes():
    print(f"{node}: {D2.degree(node)} conflicts")

print("\nMaximum conflict degree:",
      max(dict(D2.degree()).values()))

print("\nClique size:",
      nx.approximation.max_clique(D2).__len__())