import subprocess
from datetime import datetime, timedelta, timezone


_MIN_COMMITS = 5
_LOOKBACK_DAYS = 182  # ~6 months


def check_commit_activity(repo_path: str) -> dict:
    """
    Check for recent commit activity (≥5 commits in the last 6 months).
    Maps to FAIR: Accessible — signals an actively maintained project.
    """
    since = (
        datetime.now(timezone.utc) - timedelta(days=_LOOKBACK_DAYS)
    ).strftime("%Y-%m-%d")

    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", f"--since={since}", "--oneline"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        return {
            "check": "Commit Activity",
            "fair": "A",
            "passed": False,
            "score": 0,
            "max_score": 10,
            "message": "git not found on PATH",
        }
    except subprocess.TimeoutExpired:
        return {
            "check": "Commit Activity",
            "fair": "A",
            "passed": False,
            "score": 0,
            "max_score": 10,
            "message": "git log timed out",
        }

    if result.returncode != 0:
        return {
            "check": "Commit Activity",
            "fair": "A",
            "passed": False,
            "score": 0,
            "max_score": 10,
            "message": "Not a git repository",
        }

    count = len([l for l in result.stdout.strip().splitlines() if l])

    if count >= _MIN_COMMITS:
        return {
            "check": "Commit Activity",
            "fair": "A",
            "passed": True,
            "score": 10,
            "max_score": 10,
            "message": f"{count} commits in the last 6 months",
        }
    return {
        "check": "Commit Activity",
        "fair": "A",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": f"Only {count} commit(s) in last 6 months (need ≥{_MIN_COMMITS})",
    }
