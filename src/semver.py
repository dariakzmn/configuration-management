"""Small Cargo-compatible SemVer requirement helper."""

import re


VERSION_RE = re.compile(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?")


def parse_version(text: str) -> tuple[int, int, int]:
    """Parse the numeric SemVer core and ignore prerelease metadata."""
    match = VERSION_RE.match(text.strip())
    if not match:
        raise ValueError(f"invalid semantic version: {text}")
    parts = [int(value or 0) for value in match.groups()]
    return tuple(parts)


def satisfies(version: str, requirement: str) -> bool:
    """Return whether a version satisfies a common Cargo requirement."""
    req = requirement.strip()
    if not req or req == "*":
        return True
    if "," in req:
        parts = [part.strip() for part in req.split(",")]
        return all(satisfies(version, part) for part in parts)
    if req.startswith("^"):
        raw = req[1:].strip()
        return _caret(
            parse_version(version),
            parse_version(raw),
            len(raw.split(".")),
        )
    if req.startswith("~"):
        return _tilde(parse_version(version), req[1:])
    if req.startswith((">=", "<=", ">", "<", "=")):
        return _compare(parse_version(version), req)
    if "*" in req or "x" in req.lower():
        return _wildcard(parse_version(version), req)
    raw = req
    return _caret(
        parse_version(version),
        parse_version(raw),
        len(raw.split(".")),
    )


def _caret(version, minimum, component_count) -> bool:
    """Implement Cargo caret compatibility bounds."""
    major, minor, patch = minimum
    if major > 0 or component_count == 1:
        upper = (major + 1, 0, 0)
    elif minor > 0 or component_count == 2:
        upper = (0, minor + 1, 0)
    else:
        upper = (0, 0, patch + 1)
    return minimum <= version < upper


def _tilde(version, raw_minimum: str) -> bool:
    """Implement Cargo tilde compatibility bounds."""
    minimum = parse_version(raw_minimum)
    count = len(raw_minimum.split("."))
    if count <= 1:
        upper = (minimum[0] + 1, 0, 0)
    else:
        upper = (minimum[0], minimum[1] + 1, 0)
    return minimum <= version < upper


def _compare(version, requirement: str) -> bool:
    """Evaluate one comparator requirement."""
    operators = (">=", "<=", ">", "<", "=")
    operator = next(op for op in operators if requirement.startswith(op))
    target = parse_version(requirement[len(operator):])
    operations = {
        ">=": version >= target,
        "<=": version <= target,
        ">": version > target,
        "<": version < target,
        "=": version == target,
    }
    return operations[operator]


def _wildcard(version, requirement: str) -> bool:
    """Evaluate x/* wildcard requirements."""
    tokens = requirement.lower().replace("x", "*").split(".")
    current = version
    for index, token in enumerate(tokens):
        if token == "*":
            return True
        if int(token) != current[index]:
            return False
    return True
