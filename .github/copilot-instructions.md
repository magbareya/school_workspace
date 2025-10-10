This repository contains course materials (TeX, Jupyter notebooks, markdown and images) and a Makefile-driven build that emits PDF and extracted source artifacts into an `out/` directory mirroring `src/`.

Key facts for an AI coding agent to be productive
- Big picture: source files live under `src/` and include `*.tex`, `*.ipynb`, and `*.md`. The Makefile finds those sources and emits PDFs (and other artifacts) under `out/` while preserving the `src/` directory structure.
- Build entry points: use the Makefile targets. Common commands:
  - `make` or `make all` — build everything (pdf, printable, sols)
  - `make pdf` — build regular PDFs (all `ipynb`, `md`, `tex`)
  - `make printable` — build printing-friendly PDFs (removes code/solutions)
  - `make sols` — build PDFs that include solutions (`_sols.pdf` outputs)
  - `make sclean` — remove duplicate/unneeded files (uses `scripts/sclean.py`)

- Important files / patterns to reference in code changes:
  - `Makefile` — central build rules. Note it hardcodes `SHELL := /bin/bash` and uses `find`, so on Windows use WSL/Git Bash or adapt the Makefile.
  - `scripts/export_cs.py` — converts `.ipynb` code cells to a single `.cs` file (used by the `out/%.cs` rule).
  - `scripts/sclean.py` — removes near-duplicate PDFs created by multiple build modes (`_printable` and `_sols` suffixes).
  - `README.md` — short usage examples and notes (e.g., copy to OneDrive example).

- Conventions and project-specific patterns:
  - Output layout: `out/<same-path-as-src>.pdf` (the Makefile strips leading `src/` when constructing targets). When adding a new source file under `src/`, the Makefile will automatically include it.
  - TeX build toggles: the TeX rules pass LaTeX macros to `xelatex` to control content:
    - `\def\setdetailed{\detailedtrue}` vs `\detailedfalse` — controls whether detailed content (such as long code) is kept
    - `\def\setwithsols{\withsolstrue}` vs `\withsolsfalse` — controls whether solutions are included
    Example (from Makefile):
    xelatex -output-directory=out/... -jobname=NAME "\\def\\setdetailed{\\detailedtrue} \\\def\\setwithsols{\\withsolstrue} \\\input{src/path/to/file.tex}"
  - Notebook -> printable: `nbconvert` is configured to exclude inputs/outputs for printable PDFs. See the `_printable` rule in the `Makefile` for flags.
  - Notebook -> code: `out/%.cs` is produced by `scripts/export_cs.py` — the project uses this to extract only code cells (useful when turning notebooks into language-specific examples).

- Dependencies an agent should assume exist or request to install before running builds:
  - Python 3 (used by `scripts/*.py` and `jupyter nbconvert`)
  - jupyter (nbconvert)
  - pandoc (for `md -> pdf` rule)
  - a TeX distribution with `xelatex` (XeLaTeX required for Arabic and custom fonts)
  - GNU make + a POSIX shell (`find` is used) — on Windows prefer WSL or Git Bash

- Editing and testing guidance for small changes:
  - To add a new exercise: place `src/.../newfile.tex` (or `.ipynb`/`.md`) and run `make pdf` or `make tex`.
  - To generate a solutions PDF for a single TeX file, use the `out/%_sols.pdf` rule or run the `xelatex` command shown above (ensure the macros `setdetailed` and `setwithsols` are set appropriately).
  - To extract C# from a notebook for quick inspection, run the `out/%.cs` rule or call `python scripts/export_cs.py src/.../notebook.ipynb out/.../notebook.cs`.

- What NOT to change without coordination:
  - Global Makefile assumptions (shell, `find`, and path transformations). If you must adapt for native Windows `cmd.exe`, prefer adding a short `Makefile.windows` and document usage rather than editing the canonical Makefile used by CI/maintainers.
  - The LaTeX toggle names: other files (TeX sources) rely on `\setdetailed` and `\setwithsols` names and boolean semantics.

Examples from this repo (use as pattern examples when generating code or edits):
- `Makefile` — shows rules and macros for TeX, notebooks and md to PDF conversions.
- `scripts/export_cs.py` — simple, deterministic extraction of code cells (good reference for extracting cell-level content).
- `scripts/sclean.py` — example of how duplicate outputs are detected and pruned.

If something in these instructions is unclear, tell me which file or workflow you want expanded (examples: a step-by-step WSL build on Windows, precise nbconvert flags for a custom notebook, or where the TeX macros are declared). I'll iterate quickly.
