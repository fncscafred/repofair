import os
import re
from typing import Optional


_SEMVER_RE = re.compile(r'\b(\d+)\.(\d+)\.(\d+)\b')


def _find_version(filepath: str) -> Optional[str]:
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as fh:
            match = _SEMVER_RE.search(fh.read())
            return match.group(0) if match else None
    except OSError:
        return None


def check_version(repo_path: str) -> dict:
    """Check for semantic versioning (x.y.z). Maps to FAIR: Findable + Reusable."""
    candidates = [
        os.path.join(repo_path, "repofair", "__init__.py"),
        os.path.join(repo_path, "__init__.py"),
        os.path.join(repo_path, "setup.py"),
        os.path.join(repo_path, "pyproject.toml"),
        os.path.join(repo_path, "setup.cfg"),
        os.path.join(repo_path, "VERSION"),
        os.path.join(repo_path, "version.py"),
    ]
    for path in candidates:
        if os.path.exists(path):
            ver = _find_version(path)
            if ver:
                return {
                    "check": "Versioning",
                    "fair": "F+R",
                    "passed": True,
                    "score": 10,
                    "max_score": 10,
                    "message": f"Version {ver} in {os.path.basename(path)}",
                }
    return {
        "check": "Versioning",
        "fair": "F+R",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No semantic version (x.y.z) found",
    }
