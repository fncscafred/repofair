import os


def check_citation(repo_path: str) -> dict:
    """Check for citation metadata. Maps to FAIR: Findable."""
    variants = ["CITATION.cff", "CITATION.md", "CITATION.bib", "CITATION"]
    for variant in variants:
        if os.path.exists(os.path.join(repo_path, variant)):
            return {
                "check": "CITATION",
                "fair": "F",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{variant} found",
            }
    return {
        "check": "CITATION",
        "fair": "F",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No CITATION file found",
    }
