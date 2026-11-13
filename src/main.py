"""Stage 2: collect direct Cargo dependencies."""

import sys

from src.config import parse_args
from src.sources import CargoRepository, TestRepository


def create_source(config):
    """Create the selected dependency source."""
    if config.test_mode:
        return TestRepository(config.repository)
    return CargoRepository(config.repository)


def run(argv=None) -> int:
    """Print direct dependencies of the selected package."""
    config = parse_args(argv)
    try:
        source = create_source(config)
        root = source.root(config.package)
        print(f"package={root}")
        for dependency in source.dependencies(root):
            print(dependency)
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
