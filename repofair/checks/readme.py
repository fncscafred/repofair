import os


def check_readme(repo_path: str) -> dict:
    """Check for the presence of a README file. Maps to FAIR: Findable + Reusable."""
    variants = ["README.md", "README.rst", "README.txt", "README"]
    for variant in variants:
        if os.path.exists(os.path.join(repo_path, variant)):
            return {
                "check": "README",
                "fair": "F+R",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{variant} found",
            }
    return {
        "check": "README",
        "fair": "F+R",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No README file found",
    }
