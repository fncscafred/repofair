"""
Tests for all repofair check modules and the scorer.
Run with: pytest tests/ -v
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repofair.checks.readme import check_readme
from repofair.checks.license import check_license
from repofair.checks.citation import check_citation
from repofair.checks.ci import check_ci
from repofair.checks.environment import check_environment
from repofair.checks.version import check_version
from repofair.checks.contributing import check_contributing
from repofair.checks.commit_activity import check_commit_activity
from repofair.scorer import score_repo


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

class TestCheckReadme:
    def test_pass_readme_md(self, tmp_path):
        (tmp_path / "README.md").write_text("# Project")
        r = check_readme(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "F+R"

    def test_pass_readme_rst(self, tmp_path):
        (tmp_path / "README.rst").write_text("Project\n=======")
        assert check_readme(str(tmp_path))["passed"] is True

    def test_pass_readme_txt(self, tmp_path):
        (tmp_path / "README.txt").write_text("Project")
        assert check_readme(str(tmp_path))["passed"] is True

    def test_fail_no_readme(self, tmp_path):
        r = check_readme(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# LICENSE
# ---------------------------------------------------------------------------

class TestCheckLicense:
    def test_pass_license(self, tmp_path):
        (tmp_path / "LICENSE").write_text("MIT License")
        r = check_license(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "R"

    def test_pass_license_md(self, tmp_path):
        (tmp_path / "LICENSE.md").write_text("MIT License")
        assert check_license(str(tmp_path))["passed"] is True

    def test_fail_no_license(self, tmp_path):
        r = check_license(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# CITATION
# ---------------------------------------------------------------------------

class TestCheckCitation:
    def test_pass_citation_cff(self, tmp_path):
        (tmp_path / "CITATION.cff").write_text("cff-version: 1.2.0")
        r = check_citation(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "F"

    def test_pass_citation_bib(self, tmp_path):
        (tmp_path / "CITATION.bib").write_text("@software{repofair}")
        assert check_citation(str(tmp_path))["passed"] is True

    def test_fail_no_citation(self, tmp_path):
        r = check_citation(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# CI/CD
# ---------------------------------------------------------------------------

class TestCheckCI:
    def test_pass_github_actions(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI\non: [push]")
        r = check_ci(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "A"

    def test_pass_multiple_workflows(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        (wf / "release.yml").write_text("name: Release")
        r = check_ci(str(tmp_path))
        assert r["passed"] is True
        assert "2 workflow" in r["message"]

    def test_pass_travis(self, tmp_path):
        (tmp_path / ".travis.yml").write_text("language: python")
        assert check_ci(str(tmp_path))["passed"] is True

    def test_fail_no_ci(self, tmp_path):
        r = check_ci(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

class TestCheckEnvironment:
    def test_pass_dockerfile(self, tmp_path):
        (tmp_path / "Dockerfile").write_text("FROM python:3.11-slim")
        r = check_environment(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "I"

    def test_pass_requirements_txt(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rich\npytest")
        assert check_environment(str(tmp_path))["passed"] is True

    def test_pass_poetry_lock(self, tmp_path):
        (tmp_path / "poetry.lock").write_text("[metadata]")
        assert check_environment(str(tmp_path))["passed"] is True

    def test_fail_no_environment(self, tmp_path):
        r = check_environment(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# Versioning
# ---------------------------------------------------------------------------

class TestCheckVersion:
    def test_pass_version_in_init(self, tmp_path):
        (tmp_path / "__init__.py").write_text('__version__ = "1.2.3"')
        r = check_version(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "F+R"
        assert "1.2.3" in r["message"]

    def test_pass_version_in_nested_init(self, tmp_path):
        pkg = tmp_path / "repofair"
        pkg.mkdir()
        (pkg / "__init__.py").write_text('__version__ = "2.0.0"')
        r = check_version(str(tmp_path))
        assert r["passed"] is True
        assert "2.0.0" in r["message"]

    def test_fail_no_version(self, tmp_path):
        r = check_version(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0

    def test_fail_no_semver_in_file(self, tmp_path):
        (tmp_path / "__init__.py").write_text("# no version here")
        r = check_version(str(tmp_path))
        assert r["passed"] is False


# ---------------------------------------------------------------------------
# CONTRIBUTING
# ---------------------------------------------------------------------------

class TestCheckContributing:
    def test_pass_contributing_md(self, tmp_path):
        (tmp_path / "CONTRIBUTING.md").write_text("# How to contribute")
        r = check_contributing(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "A"

    def test_pass_contributing_rst(self, tmp_path):
        (tmp_path / "CONTRIBUTING.rst").write_text("Contributing")
        assert check_contributing(str(tmp_path))["passed"] is True

    def test_fail_no_contributing(self, tmp_path):
        r = check_contributing(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# Commit Activity
# ---------------------------------------------------------------------------

def _mock_git(stdout: str, returncode: int = 0) -> MagicMock:
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    return m


class TestCheckCommitActivity:
    def test_pass_five_commits(self, tmp_path):
        lines = "\n".join(f"abc{i:04d} fix: something" for i in range(5))
        with patch("subprocess.run", return_value=_mock_git(lines)):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is True
        assert r["score"] == 10
        assert r["fair"] == "A"

    def test_pass_many_commits(self, tmp_path):
        lines = "\n".join(f"abc{i:04d} commit" for i in range(20))
        with patch("subprocess.run", return_value=_mock_git(lines)):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is True
        assert "20 commits" in r["message"]

    def test_fail_four_commits(self, tmp_path):
        lines = "\n".join(f"abc{i:04d} commit" for i in range(4))
        with patch("subprocess.run", return_value=_mock_git(lines)):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is False
        assert r["score"] == 0

    def test_fail_zero_commits(self, tmp_path):
        with patch("subprocess.run", return_value=_mock_git("")):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is False

    def test_fail_not_git_repo(self, tmp_path):
        with patch("subprocess.run", return_value=_mock_git("", returncode=128)):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is False
        assert "git repository" in r["message"].lower()

    def test_fail_git_not_found(self, tmp_path):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            r = check_commit_activity(str(tmp_path))
        assert r["passed"] is False


# ---------------------------------------------------------------------------
# score_repo integration
# ---------------------------------------------------------------------------

class TestScoreRepo:
    def _full_repo(self, tmp_path):
        (tmp_path / "README.md").write_text("# Project")
        (tmp_path / "LICENSE").write_text("MIT")
        (tmp_path / "CITATION.cff").write_text("cff-version: 1.2.0")
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        (tmp_path / "Dockerfile").write_text("FROM python:3.11-slim")
        (tmp_path / "__init__.py").write_text('__version__ = "1.0.0"')
        (tmp_path / "CONTRIBUTING.md").write_text("# Contributing")

    def test_perfect_score(self, tmp_path):
        self._full_repo(tmp_path)
        commits = "\n".join(f"abc{i} commit" for i in range(5))
        with patch("subprocess.run", return_value=_mock_git(commits)):
            report = score_repo(str(tmp_path))
        assert report["total_score"] == 80
        assert report["max_score"] == 80
        assert report["percentage"] == 100.0
        assert len(report["checks"]) == 8

    def test_zero_score(self, tmp_path):
        with patch("subprocess.run", return_value=_mock_git("", returncode=128)):
            report = score_repo(str(tmp_path))
        assert report["total_score"] == 0
        assert report["percentage"] == 0.0

    def test_report_structure(self, tmp_path):
        with patch("subprocess.run", return_value=_mock_git("")):
            report = score_repo(str(tmp_path))
        assert "repo_path" in report
        assert "checks" in report
        assert "total_score" in report
        assert "max_score" in report
        assert "percentage" in report
        for check in report["checks"]:
            assert "check" in check
            assert "fair" in check
            assert "passed" in check
            assert "score" in check
            assert "max_score" in check
            assert "message" in check
