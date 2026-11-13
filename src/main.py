"""CLI entry point for practice work 2, variant 18."""

import sys

from src.config import parse_args
from src.graph import ascii_tree, build_graph, load_order
from src.sources import CargoRepository, TestRepository
from src.visualize import render_png, save_mermaid, to_mermaid


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
    """Run the dependency visualizer."""
    config = parse_args(argv)
    try:
        source = create_source(config)
        root, graph = build_graph(
            source,
            config.package,
            config.max_depth,
        )
        if config.ascii_tree:
            print(ascii_tree(root, graph))
        if config.load_order:
            print_load_order(graph)
        mermaid = to_mermaid(root, graph)
        mermaid_path = save_mermaid(config.output, mermaid)
        render_png(mermaid, config.output)
        print(f"Mermaid: {mermaid_path}")
        print(f"PNG: {config.output}")
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
