# repofair

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20579202.svg)](https://doi.org/10.5281/zenodo.20579202)
[![CI](https://github.com/fncscafred/repofair/actions/workflows/ci.yml/badge.svg)](https://github.com/fncscafred/repofair/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

**repofair** is a FAIR-aligned Python library and command-line tool for auditing the health and Open Science readiness of Git repositories. It evaluates eight evidence-based dimensions — mapped to the [FAIR data principles](https://www.go-fair.org/fair-principles/) (Findable, Accessible, Interoperable, Reusable) — and produces a scored compliance report with a rich terminal interface.

Developed as part of the **KI71703 Open Science for Computing** course at Universiti Malaysia Sabah.

---

## Features

repofair checks eight dimensions of repository health, each mapped to one or more FAIR principles:

| Check | FAIR | What is evaluated |
|---|:---:|---|
| README | F + R | Presence of `README.md`, `.rst`, or `.txt` |
| LICENSE | R | Presence of a recognised licence file |
| CITATION | F | Presence of `CITATION.cff`, `.bib`, or `.md` |
| CI/CD | A | GitHub Actions workflows, Travis CI, GitLab CI, and others |
| Environment | I | `Dockerfile`, `requirements.txt`, `poetry.lock`, or Conda spec |
| Versioning | F + R | Semantic version (`x.y.z`) in package metadata or `VERSION` file |
| CONTRIBUTING | A | Presence of `CONTRIBUTING.md` or equivalent |
| Commit Activity | A | At least 5 commits in the last 6 months |

- Coloured terminal table with per-check pass/fail status and FAIR tagging
- Animated score bar graded Excellent / Good / Fair / Needs Work
- `--json` flag for machine-readable output in CI pipelines
- Exits with code `1` when overall score falls below 50% — useful as a CI gate
- Zero configuration required; works on any local Git repository

---

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/fncscafred/repofair.git
cd repofair
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Requirements

- Python 3.9 or newer
- [`rich`](https://github.com/Textualize/rich) >= 13.0 (installed automatically)
- Git available on `PATH` (for the commit activity check)

---

## Usage

### Audit the current directory

```bash
repofair .
```

### Audit any local repository

```bash
repofair /path/to/your/repo
```

### JSON output for CI pipelines

```bash
repofair . --json
```

### Run without installing (from the project root)

```bash
python3 -m repofair.cli /path/to/repo
```

### Example terminal output

```
╭────────────────────────────────────╮
│ repofair  ·  FAIR Repository Audit │
╰──────────────── . ─────────────────╯

╭──────────────────┬─────────┬────────────┬─────────┬──────────────────────────╮
│ Check            │  FAIR   │   Status   │   Score │ Details                  │
├──────────────────┼─────────┼────────────┼─────────┼──────────────────────────┤
│ README           │   F+R   │   ✓ PASS   │   10/10 │ README.md found          │
│ LICENSE          │    R    │   ✓ PASS   │   10/10 │ LICENSE found            │
│ CITATION         │    F    │   ✓ PASS   │   10/10 │ CITATION.cff found       │
│ CI/CD            │    A    │   ✓ PASS   │   10/10 │ GitHub Actions: 1        │
│                  │         │            │         │ workflow(s) found        │
│ Environment      │    I    │   ✓ PASS   │   10/10 │ Dockerfile found         │
│ Versioning       │   F+R   │   ✓ PASS   │   10/10 │ Version 1.0.0 in         │
│                  │         │            │         │ __init__.py              │
│ CONTRIBUTING     │    A    │   ✓ PASS   │   10/10 │ CONTRIBUTING.md found    │
│ Commit Activity  │    A    │   ✗ FAIL   │    0/10 │ Only 4 commit(s) in last │
│                  │         │            │         │ 6 months (need ≥5)       │
╰──────────────────┴─────────┴────────────┴─────────┴──────────────────────────╯

╭───────────────────────────────── FAIR Score ──────────────────────────────────╮
│  ████████████████████████████████████░░░░  87.5%  (70/80 pts)  Excellent      │
╰───────────────────────────────────────────────────────────────────────────────╯

FAIR key: F=Findable  A=Accessible  I=Interoperable  R=Reusable
```

### Example JSON output

```json
{
  "repo_path": ".",
  "checks": [
    { "check": "README", "fair": "F+R", "passed": true, "score": 10, "max_score": 10, "message": "README.md found" },
    { "check": "LICENSE", "fair": "R",   "passed": true, "score": 10, "max_score": 10, "message": "LICENSE found" }
  ],
  "total_score": 70,
  "max_score": 80,
  "percentage": 87.5
}
```

---

## Project Structure

```
repofair/
├── repofair/                   # Python package
│   ├── __init__.py             # Package metadata and public API
│   ├── scorer.py               # Aggregates all checks into a scored report
│   ├── cli.py                  # Rich terminal interface and --json flag
│   └── checks/                 # One module per FAIR check
│       ├── __init__.py
│       ├── readme.py
│       ├── license.py
│       ├── citation.py
│       ├── ci.py
│       ├── environment.py
│       ├── version.py
│       ├── contributing.py
│       └── commit_activity.py
├── tests/
│   └── test_checks.py          # 34 pytest tests covering all checks
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions — Python 3.9 to 3.12
├── Dockerfile                  # Container entry point
├── requirements.txt
├── pyproject.toml
├── CITATION.cff                # Software citation metadata (CFF v1.2.0)
├── CONTRIBUTING.md
├── CHANGELOG.md
├── MANAGEMENT_PLAN.md          # Open Science data management plan
└── LICENSE
```

---

## Running the Tests

```bash
pytest tests/ -v
```

All 34 tests run without network access or a real Git repository — check functions are tested with temporary directories and mocked `subprocess` calls.

---

## Docker

Build and run repofair in a container, mounting any local repository as a volume:

```bash
docker build -t repofair .
docker run --rm -v /path/to/repo:/repo repofair /repo
```

---

## Citation

If you use repofair in your research or teaching, please cite it:

```bibtex
@software{frederick2026repofair,
  author    = {Frederick, Francisca},
  title     = {repofair: A FAIR-aligned Python library for auditing Git repository health},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20579202},
  url       = {https://doi.org/10.5281/zenodo.20579202}
}
```

Or see [`CITATION.cff`](CITATION.cff) for the full machine-readable metadata.

---

## License

Released under the [MIT License](LICENSE).  
Copyright © 2026 Francisca Frederick — Universiti Malaysia Sabah.
