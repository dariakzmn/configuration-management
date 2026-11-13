"""Stage 3: build the transitive dependency graph."""

import sys

from src.config import parse_args
from src.graph import build_graph
from src.sources import CargoRepository, TestRepository


def create_source(config):
    """Create the selected dependency source."""
    if config.test_mode:
        return TestRepository(config.repository)
    return CargoRepository(config.repository)


def run(argv=None) -> int:
    """Build and print the dependency graph."""
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
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
