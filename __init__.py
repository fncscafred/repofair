"""
repofair: A FAIR-aligned Python library for auditing
Git repository health and Open Science readiness.
"""

__version__ = "1.0.0"
__author__ = "Francisca Frederick"
__license__ = "MIT"

from .scorer import score_repo

__all__ = ["score_repo"]
