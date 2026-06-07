# Contributing to repofair

Thank you for your interest in contributing to repofair! This document explains how to get involved, from reporting issues to submitting code changes.

---

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Development Environment Setup](#development-environment-setup)
3. [Running Tests](#running-tests)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Submitting a Pull Request](#submitting-a-pull-request)
6. [Reporting Issues](#reporting-issues)

---

## Ways to Contribute

- **Bug reports** — open an issue describing the unexpected behaviour and how to reproduce it
- **Feature requests** — open an issue explaining the use case and proposed behaviour
- **New checks** — add a new FAIR-aligned check module under `repofair/checks/`
- **Documentation** — improve the README, docstrings, or this guide
- **Tests** — increase coverage or add edge-case tests

Please search existing issues before opening a new one to avoid duplicates.

---

## Development Environment Setup

### Prerequisites

- Python 3.9 or newer
- Git

### 1. Fork and clone the repository

```bash
git clone https://github.com/fncscafred/repofair.git
cd repofair
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .                 # installs repofair as an editable package
```

### 4. Verify the installation

```bash
repofair .
# or
python3 -m repofair.cli .
```

You should see the FAIR audit table for the repofair repository itself.

---

## Running Tests

Tests live in `tests/test_checks.py` and use [pytest](https://pytest.org) with the standard `tmp_path` fixture — no external services or network access required.

### Run the full suite

```bash
pytest tests/ -v
```

### Run a single test class

```bash
pytest tests/ -v -k TestCheckCI
```

### Check test coverage (optional)

```bash
pip install pytest-cov
pytest tests/ --cov=repofair --cov-report=term-missing
```

All 34 tests must pass before a pull request will be reviewed. New check modules must include both a passing and a failing test case.

---

## Code Style Guidelines

### General

- Follow [PEP 8](https://peps.python.org/pep-0008/) for formatting.
- Keep functions small and single-purpose.
- Prefer explicit over implicit.

### Check modules

Every file under `repofair/checks/` must follow this contract:

```python
def check_<name>(repo_path: str) -> dict:
    """One-line description. Maps to FAIR: <principle(s)>."""
    ...
    return {
        "check":     str,   # Display name shown in the CLI table
        "fair":      str,   # FAIR principle(s), e.g. "F", "A", "F+R"
        "passed":    bool,
        "score":     int,   # Points earned (0 or max_score)
        "max_score": int,   # Maximum possible points (10)
        "message":   str,   # Human-readable detail shown in Details column
    }
```

- `max_score` is always `10`.
- `score` is either `0` (fail) or `10` (pass) — no partial credit.
- `message` should be concise (≤60 characters) and plain text (no ANSI codes).
- The function must handle `OSError`, missing `git`, and malformed files gracefully — never raise an uncaught exception.

### FAIR principle assignment

| Principle | Meaning | Typical checks |
|---|---|---|
| F — Findable | Metadata and identifiers make the software discoverable | README, CITATION, Versioning |
| A — Accessible | Software and its metadata can be retrieved | CI/CD, CONTRIBUTING, Commit Activity |
| I — Interoperable | Uses standard formats and interfaces | Dockerfile, lockfiles |
| R — Reusable | Clear licence, documentation, and provenance | LICENSE, README, Versioning |

Use `"F+R"` (joined with `+`) when a check supports more than one principle.

### Imports and typing

- Use `from typing import Optional` for Python 3.9 compatibility (avoid `X | None` syntax).
- Standard library only inside check modules — no third-party imports.
- `rich` may be used in `cli.py` only.

### Comments

Write a comment only when the *why* is non-obvious (a hidden constraint, a workaround, an invariant). Do not describe *what* the code does — the code itself does that.

---

## Submitting a Pull Request

1. **Create a branch** from `main` with a descriptive name:
   ```bash
   git checkout -b add-doi-check
   ```

2. **Make your changes** following the guidelines above.

3. **Add or update tests** in `tests/test_checks.py`. New check modules need at minimum:
   - A test for the passing case
   - A test for the failing case
   - A test for a graceful failure (e.g. missing file, git not available)

4. **Run the full test suite** and confirm all tests pass:
   ```bash
   pytest tests/ -v
   ```

5. **Audit repofair itself** and ensure the score does not decrease:
   ```bash
   python3 -m repofair.cli .
   ```

6. **Commit** with a clear, imperative message:
   ```
   Add DOI presence check (FAIR: F)
   ```

7. **Push** and open a pull request against the `main` branch.

8. **Fill in the PR description** — explain what the change does, why it is needed, and reference any related issues.

Pull requests are reviewed for correctness, test coverage, FAIR alignment, and consistency with the existing check contract. Small, focused PRs are reviewed faster than large ones.

---

## Reporting Issues

Open an issue on [GitHub](https://github.com/fncscafred/repofair/issues) and include:

- repofair version (`python3 -m repofair.cli --version` once implemented, or check `repofair/__init__.py`)
- Python version (`python3 --version`)
- Operating system
- The repository path you were auditing (if applicable)
- The full output or error message
- Steps to reproduce

---

## Code of Conduct

Be respectful and constructive. Contributions of all experience levels are welcome.
