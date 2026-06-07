# Data Management Plan — repofair

**Project:** repofair — FAIR Repository Audit Library  
**Author:** Francisca Frederick  
**Affiliation:** Universiti Malaysia Sabah  
**Course:** KI71703 Open Science for Computing  
**Date:** 2026-06-07  
**Version:** 1.0.0  

---

## 1. Data Description

### 1.1 Software and Source Code
repofair is a Python library and CLI tool. The primary research output is the source code itself, comprising approximately 600 lines of Python across 12 modules.

### 1.2 Runtime Data
When executed, repofair reads only the local file system of the target repository — no data is collected, stored, or transmitted. Inputs are file paths; outputs are ephemeral scored reports printed to stdout or returned as Python dicts.

### 1.3 Test Data
The test suite uses `tmp_path` (pytest) to create isolated temporary directories at runtime. No persistent test data files are committed to the repository.

---

## 2. Data Collection and Generation

- **Source code** is authored by Francisca Frederick and version-controlled in Git on GitHub at `https://github.com/fncscafred/repofair`.
- **No external datasets** are collected, downloaded, or stored.
- **No personal data** is processed at any stage.
- All auditing happens locally: the tool reads the file tree and git log of the target repository on the user's machine.

---

## 3. Documentation and Metadata

| Artefact | Identifier / Location |
|---|---|
| Source repository | https://github.com/fncscafred/repofair |
| Zenodo archive | https://doi.org/10.5281/zenodo.20579202 |
| DOI | `10.5281/zenodo.20579202` |
| `README.md` | User-facing documentation: installation, usage, examples |
| `CITATION.cff` | Machine-readable citation metadata (CFF v1.2.0) |
| `CHANGELOG.md` | Chronological record of all changes (Keep a Changelog format) |
| `MANAGEMENT_PLAN.md` | This document — data stewardship and Open Science alignment |
| Docstrings | Inline API documentation for every public function |
| `repofair/__init__.py` | Exposes `__version__`, `__author__`, `__license__` |

The project follows [Semantic Versioning 2.0.0](https://semver.org/) — every release is tagged `vMAJOR.MINOR.PATCH` in Git.

---

## 4. Storage and Backup

| Layer | Medium | Retention |
|---|---|---|
| Primary | GitHub repository (remote Git) | Indefinite |
| Secondary | Developer workstation (local Git clone) | Duration of project |
| Tertiary | GitHub Releases (tagged archives) | Indefinite |

GitHub provides automatic geographic redundancy. Commits are signed with the developer's git identity. The CI pipeline (`ci.yml`) runs on every push, providing independent verification of the code state.

---

## 5. Legal and Ethical Requirements

- **License:** MIT License — permissive, allows reuse, modification, and redistribution with attribution.
- **Personal data:** None collected or processed.
- **Intellectual property:** All code is original work by Francisca Frederick unless noted in comments. Dependencies (`rich`, `pytest`) are used under their respective OSI-approved licences.
- **Export control:** Not applicable.
- **Ethics review:** Not required (software tool, no human subjects, no sensitive data).

---

## 6. Data Sharing and Long-Term Preservation

- **Source code** is publicly available on GitHub under the MIT licence, making it immediately reusable by the research community.
- **CITATION.cff** ensures the software can be cited correctly in academic publications, supporting the Findability principle.
- **PyPI publication** (planned post-assignment) will allow installation via `pip install repofair`, maximising Accessibility.
- **Zenodo** archival at [doi.org/10.5281/zenodo.20579202](https://doi.org/10.5281/zenodo.20579202) provides a persistent identifier and long-term preservation beyond GitHub's availability guarantees.
- The project is designed to be self-auditing: running `repofair .` on this repository should score ≥70/80.

---

## 7. Responsibilities

| Role | Responsible Party |
|---|---|
| Software design and implementation | Francisca Frederick |
| Version control and releases | Francisca Frederick |
| Documentation maintenance | Francisca Frederick |
| CI/CD pipeline | GitHub Actions (automated) |
| Long-term preservation (planned) | Zenodo / GitHub Releases |

---

## 8. FAIR Self-Assessment

This project is designed to be a demonstration of FAIR principles applied to research software:

| Principle | Implementation |
|---|---|
| **Findable** | README, CITATION.cff, semantic versioning, DOI: 10.5281/zenodo.20579202 |
| **Accessible** | MIT licence, public GitHub repository, CI/CD pipeline, CONTRIBUTING.md |
| **Interoperable** | Dockerfile, requirements.txt, standard Python packaging conventions |
| **Reusable** | MIT licence, clear documentation, versioned releases, contribution guidelines |
