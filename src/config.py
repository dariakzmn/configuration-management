"""Command-line configuration for practice work 2."""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_REPOSITORY = "https://crates.io/api/v1"


@dataclass(frozen=True)
class Config:
    """Validated application settings."""

    package: str
    repository: str
    test_mode: bool
    output: str
    ascii_tree: bool
    max_depth: int
    load_order: bool


def build_parser() -> ArgumentParser:
    """Create the argument parser."""
    parser = ArgumentParser(
        description="Cargo dependency graph visualizer, variant 18",
    )
    parser.add_argument("--package", required=True)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--output", default="graph.png")
    parser.add_argument("--ascii-tree", action="store_true")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--load-order", action="store_true")
    return parser


def validate_args(namespace) -> Config:
    """Validate raw argparse values and return Config."""
    package = namespace.package.strip()
    if not package:
        raise ValueError("package name must not be empty")
    if namespace.max_depth < 0:
        raise ValueError("max depth must be zero or greater")
    if not namespace.output.lower().endswith(".png"):
        raise ValueError("output file must use the .png extension")
    validate_repository(namespace.repository, namespace.test_mode)
    return Config(
        package=package,
        repository=namespace.repository,
        test_mode=namespace.test_mode,
        output=namespace.output,
        ascii_tree=namespace.ascii_tree,
        max_depth=namespace.max_depth,
        load_order=namespace.load_order,
    )


def validate_repository(repository: str, test_mode: bool) -> None:
    """Validate repository URL or local test repository path."""
    if test_mode:
        path = Path(repository)
        if not path.is_file():
            raise ValueError(f"test repository does not exist: {repository}")
        return
    parsed = urlparse(repository)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("repository must be an HTTP(S) URL")


def parse_args(argv=None) -> Config:
    """Parse and validate command-line arguments."""
    parser = build_parser()
    namespace = parser.parse_args(argv)
    try:
        return validate_args(namespace)
    except ValueError as error:
        parser.error(str(error))
