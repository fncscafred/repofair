import os


def check_license(repo_path: str) -> dict:
    """Check for the presence of a LICENSE file. Maps to FAIR: Reusable."""
    variants = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"]
    for variant in variants:
        if os.path.exists(os.path.join(repo_path, variant)):
            return {
                "check": "LICENSE",
                "fair": "R",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{variant} found",
            }
    return {
        "check": "LICENSE",
        "fair": "R",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No LICENSE file found",
    }
