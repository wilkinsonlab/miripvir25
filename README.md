# MIRIPVIR25 🦠🧫

**Multiple Infection Role in Plant Virus Infection Risk**

## Project overview

MIRIPVIR25 explores virus–bacteria interactions in plant-associated metatranscriptomes. To our knowledge, this is a pioneering effort in the field of environmental microbiology. The repository contains data and analysis notebooks.

---

## Table of contents

- [Quick start](#quick-start) ✅
- [Prerequisites](#prerequisites) 🔧
- [Install & run (using uv)](#install--run-using-uv) ⚙️
- [Repository structure](#repository-structure) 📁
- [Running analyses & docs](#running-analyses--docs) 📊
- [Tests & quality checks](#tests--quality-checks) ✅
- [License & contact](#license--contact) 📜

---

## Quick start

1. Install the `uv` package manager (recommended via pipx) and use it to install dependencies (see below).
2. Clone the repo:

   ```bash
   git clone https://github.com/wilkinsonlab/miripvir25.git
   cd miripvir25
   ```
3. Run the analysis or serve docs (examples below).

---

## Prerequisites

- macOS / Linux / WSL (Linux)
- Python 3.10+ recommended
- git, make, and basic Unix tools
- `uv` (https://docs.astral.sh/uv/)

---

## Install & run (using uv)

Install `uv`:

Please see the official documentation and installation instructions at: https://docs.astral.sh/uv/

Install project dependencies with `uv`:

```bash
# from project root
uv install         # installs dependencies defined in `pyproject.toml`
```

Install manually `daforfer`

```bash
uv pip install git+https://github.com/brunocuevas/daforfer
```

Run common commands through `uv` (delegates to the project's environment):

```bash
# Serve the docs locally
uv run mkdocs serve
# Run notebooks or a Jupyter server
uv run jupyter lab
```

Notes:
- If you don't have `uv` available, you can fall back to `python -m pip install -e .` or use the provided `environment.yml` to create a conda environment.

---

## Repository structure

Top-level layout (selected):

- `analysis/` — Jupyter notebooks and analysis scripts
- `data/` — reference files and genomes
- `docs/` — MkDocs documentation and site content
- `pipelines/` — reproducible pipelines (e.g., `b2s`)
- `results/` — pipeline output and reports
- `scripts/` — helper scripts and utilities
- `src/` — source code and modules
- `test/` — tests and QA
- `pyproject.toml`, `environment.yml`, `setup.cfg` — project metadata and dependency specs

---

## Running analyses & docs

- Analysis notebooks: open with `uv run jupyter lab` and run notebooks in `analysis/`.
- Pipelines: many pipelines include a `run.sh` or README in their folder (e.g., `analysis/run.sh`). Follow the comments in those scripts.
- Docs: to preview documentation locally:

```bash
uv run mkdocs serve
# open http://127.0.0.1:8000 in your browser
```

---

## Tests & quality checks

Run tests and linters via `uv`:

```bash
# run tests using Python's builtin unittest via uv
uv run python -m unittest discover -v
```

---

## License & contact

See the `LICENCE.md` file in the repository for license details. For questions, open an issue or contact the maintainers listed in `pyproject.toml`.

---

## FUNDING

PID2021-124671OB-I00. MULTIPLE INFECTIONS IN PLANT VIRUS RISK (MULVIRISK) 01/09/2023- 31/08/2025 (+ 6 months extension). Ministerio de Ciencia, Innovación/Agencia Estatal de Investigación (MCIN/AEI). PI: Fernando Garcia Arenal, Co-PI: Mark D Wilkinson

![MICIN/AEI](https://www.cbgp.upm.es/images/mark/micin-aei.png)

<p align="center">
  <a href="https://www.aei.gob.es/">
    <img src="https://www.cbgp.upm.es/images/mark/micin-aei.png" alt="MICIN/AEI logo" width="300"/>
  </a>
</p>
