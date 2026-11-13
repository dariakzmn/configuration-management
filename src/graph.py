"""Dependency graph construction."""

from collections import deque


def build_graph(source, package: str, max_depth: int):
    """Build a dependency graph using iterative breadth-first search."""
    root = source.root(package)
    graph = {root: []}
    queue = deque([(root, 0)])
    expanded = set()
    while queue:
        node, depth = queue.popleft()
        if node in expanded:
            continue
        expanded.add(node)
        if depth >= max_depth:
            graph.setdefault(node, [])
            continue
        dependencies = source.dependencies(node)
        graph[node] = dependencies
        for dependency in dependencies:
            graph.setdefault(dependency, [])
            if dependency not in expanded:
                queue.append((dependency, depth + 1))
    return root, graph
