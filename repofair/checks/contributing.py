import os


def check_contributing(repo_path: str) -> dict:
    """Check for contribution guidelines. Maps to FAIR: Accessible."""
    variants = [
        "CONTRIBUTING.md",
        "CONTRIBUTING.rst",
        "CONTRIBUTING.txt",
        "CONTRIBUTING",
        os.path.join(".github", "CONTRIBUTING.md"),
    ]
    for variant in variants:
        if os.path.exists(os.path.join(repo_path, variant)):
            label = os.path.basename(variant)
            return {
                "check": "CONTRIBUTING",
                "fair": "A",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{label} found",
            }
    return {
        "check": "CONTRIBUTING",
        "fair": "A",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No CONTRIBUTING file found",
    }
