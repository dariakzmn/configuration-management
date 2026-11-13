"""Mermaid generation and PNG rendering."""

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


KROKI_URL = "https://kroki.io/mermaid/png"


def to_mermaid(root: str, graph: dict[str, list[str]]) -> str:
    """Create Mermaid text for a dependency graph."""
    nodes = sorted(graph)
    identifiers = {node: f"N{index}" for index, node in enumerate(nodes)}
    lines = ["graph TD"]
    for node in nodes:
        label = node.replace('"', "'")
        lines.append(f'    {identifiers[node]}["{label}"]')
    for parent in nodes:
        for dependency in graph[parent]:
            lines.append(
                f"    {identifiers[parent]} --> {identifiers[dependency]}"
            )
    root_id = identifiers[root]
    lines.append(f"    style {root_id} stroke-width:3px")
    return "\n".join(lines) + "\n"


def save_mermaid(png_path: str, source: str) -> Path:
    """Save Mermaid source beside the PNG result."""
    path = Path(png_path).with_suffix(".mmd")
    path.write_text(source, encoding="utf-8")
    return path


def render_png(source: str, output: str) -> None:
    """Render Mermaid to PNG through the public Kroki HTTP API."""
    request = Request(
        KROKI_URL,
        data=source.encode("utf-8"),
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "mirea-config-management-practice/2",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            Path(output).write_bytes(response.read())
    except HTTPError as error:
        raise ValueError(f"PNG renderer returned HTTP {error.code}") from error
    except URLError as error:
        message = f"PNG renderer request failed: {error.reason}"
        raise ValueError(message) from error
