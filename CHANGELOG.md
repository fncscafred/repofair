# Changelog

All notable changes to repofair are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-07

### Added
- `score_repo()` public API — runs all checks and returns a structured report dict
- **8 FAIR-aligned check modules**, each returning a typed `CheckResult` dict:
  - `checks/readme.py` — README file presence (FAIR: F+R)
  - `checks/license.py` — LICENSE file presence (FAIR: R)
  - `checks/citation.py` — CITATION.cff / .bib / .md presence (FAIR: F)
  - `checks/ci.py` — GitHub Actions / Travis / GitLab CI / Jenkinsfile detection (FAIR: A)
  - `checks/environment.py` — Dockerfile / requirements.txt / lockfile detection (FAIR: I)
  - `checks/version.py` — Semantic versioning (x.y.z) detection (FAIR: F+R)
  - `checks/contributing.py` — CONTRIBUTING.md presence (FAIR: A)
  - `checks/commit_activity.py` — ≥5 commits in last 6 months (FAIR: A)
- `cli.py` — Rich terminal table with FAIR column, coloured pass/fail rows, and score progress bar
- `--json` flag on the CLI for machine-readable output in CI pipelines
- CI exits with code 1 when overall score falls below 50%
- GitHub Actions workflow (`ci.yml`) testing on Python 3.9–3.12
- `Dockerfile` for containerised auditing
- `CITATION.cff` for software citation metadata
- `MANAGEMENT_PLAN.md` — Open Science data management plan
- Comprehensive `pytest` test suite covering all check functions and `score_repo`

---

## [Unreleased]

- `--output` flag for writing reports to file
- Remote repository support via URL
- Configuration file (`repofair.toml`) for custom thresholds
- HTML report export
