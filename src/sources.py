"""Dependency sources for crates.io and local test repositories."""

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from src.semver import parse_version, satisfies


USER_AGENT = "mirea-config-management-practice/2"


class TestRepository:
    """Read a dependency graph from a local JSON file."""

    def __init__(self, path: str):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("test repository must contain a JSON object")
        self.graph = data

    def root(self, package: str) -> str:
        """Validate and return the requested root package."""
        if package not in self.graph:
            message = (
                f"package {package} is absent from test repository"
            )
            raise ValueError(message)
        return package

    def dependencies(self, package: str) -> list[str]:
        """Return direct test dependencies."""
        values = self.graph.get(package, [])
        if not isinstance(values, list):
            raise ValueError(f"dependencies for {package} must be a list")
        return [str(value) for value in values]


class CargoRepository:
    """Read Cargo package metadata directly from a crates.io-style API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.info_cache = {}
        self.dependency_cache = {}

    def root(self, package: str) -> str:
        """Resolve the newest non-yanked version of the root crate."""
        version = self.select_version(package, "*")
        return self.node(package, version)

    def dependencies(self, node: str) -> list[str]:
        """Return resolved normal, non-optional dependencies."""
        name, version = self.split_node(node)
        key = (name, version)
        if key in self.dependency_cache:
            return self.dependency_cache[key]
        payload = self._request(
            f"/crates/{quote(name)}/{quote(version)}/dependencies"
        )
        resolved = self._resolve_dependencies(payload.get("dependencies", []))
        self.dependency_cache[key] = resolved
        return resolved

    def select_version(self, package: str, requirement: str) -> str:
        """Choose the newest non-yanked version matching a requirement."""
        payload = self._crate_info(package)
        versions = payload.get("versions", [])
        candidates = []
        for item in versions:
            number = item.get("num", "")
            if item.get("yanked") or "-" in number:
                continue
            if satisfies(number, requirement):
                candidates.append(number)
        if not candidates:
            raise ValueError(
                f"no version of {package} satisfies {requirement}"
            )
        return max(candidates, key=parse_version)

    def _crate_info(self, package: str) -> dict:
        if package not in self.info_cache:
            self.info_cache[package] = self._request(
                f"/crates/{quote(package)}"
            )
        return self.info_cache[package]

    def _resolve_dependencies(self, dependencies) -> list[str]:
        resolved = []
        for item in dependencies:
            if item.get("kind") != "normal" or item.get("optional"):
                continue
            package = item.get("crate_id") or item.get("name")
            requirement = item.get("req", "*")
            version = self.select_version(package, requirement)
            resolved.append(self.node(package, version))
        return sorted(set(resolved))

    def _request(self, path: str) -> dict:
        request = Request(
            self.base_url + path,
            headers={"User-Agent": USER_AGENT},
        )
        try:
            with urlopen(request, timeout=20) as response:
                return json.load(response)
        except HTTPError as error:
            message = f"repository returned HTTP {error.code}"
            raise ValueError(message) from error
        except URLError as error:
            message = f"repository request failed: {error.reason}"
            raise ValueError(message) from error

    @staticmethod
    def node(package: str, version: str) -> str:
        """Build a stable graph node identifier."""
        return f"{package}@{version}"

    @staticmethod
    def split_node(node: str) -> tuple[str, str]:
        """Split a node identifier into crate name and version."""
        return tuple(node.rsplit("@", 1))
