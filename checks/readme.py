"""
Check if a README file exists in the repository.
"""

import os


def check_readme(repo_path: str) -> dict:
    """
    Check if a README file exists in the repository root.
    
    Args:
        repo_path: Path to the repository root.
    
    Returns:
        A dictionary with the check result.
    """
    readme_variants = [
        "README.md",
        "README.rst",
        "README.txt",
        "README",
    ]

    for variant in readme_variants:
        if os.path.exists(os.path.join(repo_path, variant)):
            return {
                "check": "README",
                "passed": True,
                "message": f"✓ {variant} found",
                "score": 10,
            }

    return {
        "check": "README",
        "passed": False,
        "message": "⚠ No README file found",
        "score": 0,
    }
