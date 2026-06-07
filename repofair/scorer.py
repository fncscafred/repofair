"""
Aggregate all FAIR checks and produce a scored report for a repository.
"""

from .checks.readme import check_readme
from .checks.license import check_license
from .checks.citation import check_citation
from .checks.ci import check_ci
from .checks.environment import check_environment
from .checks.version import check_version
from .checks.contributing import check_contributing
from .checks.commit_activity import check_commit_activity


def score_repo(repo_path: str = ".") -> dict:
    """
    Run all FAIR checks against a local repository and return a scored report.

    Args:
        repo_path: Path to the local repository root.

    Returns:
        A dict containing individual check results, total score, and percentage.
    """
    checks = [
        check_readme(repo_path),
        check_license(repo_path),
        check_citation(repo_path),
        check_ci(repo_path),
        check_environment(repo_path),
        check_version(repo_path),
        check_contributing(repo_path),
        check_commit_activity(repo_path),
    ]

    total_score = sum(c["score"] for c in checks)
    max_score = sum(c["max_score"] for c in checks)
    percentage = round(total_score / max_score * 100, 1) if max_score > 0 else 0.0

    return {
        "repo_path": str(repo_path),
        "checks": checks,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
    }
