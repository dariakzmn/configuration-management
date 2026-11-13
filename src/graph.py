"""Dependency graph construction and operations."""

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


def load_order(graph: dict[str, list[str]]):
    """Return dependencies-first load order and any cyclic nodes."""
    remaining = {
        node: set(dependencies)
        for node, dependencies in graph.items()
    }
    order = []
    while remaining:
        ready = sorted(
            node for node, dependencies in remaining.items()
            if not dependencies
        )
        if not ready:
            return order, sorted(remaining)
        for node in ready:
            order.append(node)
            remaining.pop(node)
        for dependencies in remaining.values():
            dependencies.difference_update(ready)
    return order, []


def ascii_tree(root: str, graph: dict[str, list[str]]) -> str:
    """Format the graph as an iterative ASCII dependency tree."""
    lines = [root]
    stack = []
    children = graph.get(root, [])
    for index in range(len(children) - 1, -1, -1):
        child = children[index]
        stack.append((child, "", index == len(children) - 1, {root}))
    while stack:
        node, prefix, is_last, path = stack.pop()
        marker = "last: " if is_last else "dep: "
        cycle = node in path
        suffix = " [cycle]" if cycle else ""
        lines.append(prefix + marker + node + suffix)
        if cycle:
            continue
        next_prefix = prefix + "  "
        descendants = graph.get(node, [])
        next_path = path | {node}
        for index in range(len(descendants) - 1, -1, -1):
            child = descendants[index]
            last = index == len(descendants) - 1
            stack.append((child, next_prefix, last, next_path))
    return "\n".join(lines)
