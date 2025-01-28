import time
from math import log2, ceil
from graphviz import Digraph


def read_tree_from_file(filename):
    """Reads the tree from a file in the specified format."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    tree = [[] for _ in range(n + 1)]
    edges = []
    for line in lines[1:]:
        u, v = map(int, line.split())
        tree[u].append(v)
        tree[v].append(u)
        edges.append((u, v))
    return n, tree, edges

def binary_lifting_preprocessing(tree, n, root=1):
    """Prepares the binary lifting table and depth array."""
    max_jump = ceil(log2(n))
    up = [[-1] * (max_jump + 1) for _ in range(n + 1)]
    depth = [-1] * (n + 1)

    def dfs(node, parent):
        up[node][0] = parent
        depth[node] = depth[parent] + 1 if parent != -1 else 0
        for j in range(1, max_jump + 1):
            if up[node][j - 1] != -1:
                up[node][j] = up[up[node][j - 1]][j - 1]
        for neighbor in tree[node]:
            if neighbor != parent:
                dfs(neighbor, node)

    dfs(root, -1)
    return up, depth

def lca(u, v, up, depth):
    """Finds the LCA of two nodes using binary lifting."""
    if depth[u] < depth[v]:
        u, v = v, u

    # Bring u and v to the same depth
    diff = depth[u] - depth[v]
    for i in range(len(up[u])):
        if diff & (1 << i):
            u = up[u][i]

    if u == v:
        return u

    # Lift both nodes until their parents are the same
    for i in range(len(up[u]) - 1, -1, -1):
        if up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]

    return up[u][0]

def visualize_tree(edges, lca_node, query, output_file="tree.png"):
    """Visualizes the tree using Graphviz."""
    dot = Digraph(format="png")
    for u, v in edges:
        dot.edge(str(u), str(v))

    # Highlight the LCA node
    for node in set(u for u, _ in edges).union(v for _, v in edges):
        if node == lca_node:
            dot.node(str(node), color="red", style="filled", fillcolor="yellow")
        else:
            dot.node(str(node))

    dot.attr(label=f"LCA of {query[0]} and {query[1]} is {lca_node}", fontsize="16")
    dot.attr(labelloc="top", labeljust="center")
    dot.render(output_file, view=True)

def main():
    # Read the tree from a file
    filename = input("Enter the filename containing the tree: ").strip()
    n, tree, edges = read_tree_from_file(filename)
    up, depth = binary_lifting_preprocessing(tree, n)

    # Read queries and process them
    q = int(input("Enter number of queries: "))
    for _ in range(q):
        u, v = map(int, input("Enter query (u v): ").split())
        start_time = time.time()
        result = lca(u, v, up, depth)
        end_time = time.time()
        print(f"LCA of {u} and {v} is {result}. Query time: {(end_time - start_time) * 1000:.3f} ms")
        visualize_tree(edges, result, (u, v), output_file=f"tree_{u}_{v}.png")

if __name__ == "__main__":
    main()
