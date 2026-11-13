"""Stage 4: graph construction and dependency load order."""

import sys

from src.config import parse_args
from src.graph import build_graph, load_order
from src.sources import CargoRepository, TestRepository


def create_source(config):
    """Create the selected dependency source."""
    if config.test_mode:
        return TestRepository(config.repository)
    return CargoRepository(config.repository)


def print_load_order(graph) -> None:
    """Print a dependencies-first order or explain a cycle."""
    order, cyclic = load_order(graph)
    print("Load order:")
    for node in order:
        print(f"  {node}")
    if cyclic:
        print("Cycle prevents a complete load order:")
        for node in cyclic:
            print(f"  {node}")


def run(argv=None) -> int:
    """Build the graph and optionally print its load order."""
    config = parse_args(argv)
    try:
        source = create_source(config)
        root, graph = build_graph(
            source,
            config.package,
            config.max_depth,
        )
        print(f"root={root}")
        for node in sorted(graph):
            values = ", ".join(graph[node])
            print(f"{node}: {values}")
        if config.load_order:
            print_load_order(graph)
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
