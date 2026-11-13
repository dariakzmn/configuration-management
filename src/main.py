"""Stage 1 CLI entry point."""

from src.config import parse_args


def main() -> None:
    """Print all configurable parameters as key-value pairs."""
    config = parse_args()
    values = {
        "package": config.package,
        "repository": config.repository,
        "test_mode": config.test_mode,
        "output": config.output,
        "ascii_tree": config.ascii_tree,
        "max_depth": config.max_depth,
    }
    for key, value in values.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
