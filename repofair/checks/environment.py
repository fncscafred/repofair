import os


def check_environment(repo_path: str) -> dict:
    """Check for reproducible environment specification. Maps to FAIR: Interoperable."""
    candidates = [
        ("Dockerfile", "Dockerfile"),
        ("requirements.txt", "requirements.txt"),
        ("Pipfile.lock", "Pipfile.lock"),
        ("poetry.lock", "poetry.lock"),
        ("environment.yml", "Conda environment.yml"),
        ("conda.yml", "Conda conda.yml"),
        ("pyproject.toml", "pyproject.toml"),
    ]
    for filename, label in candidates:
        if os.path.exists(os.path.join(repo_path, filename)):
            return {
                "check": "Environment",
                "fair": "I",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{label} found",
            }
    return {
        "check": "Environment",
        "fair": "I",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No Dockerfile or dependency lockfile found",
    }
