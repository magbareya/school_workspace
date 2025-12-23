# Computer Science Basics Course Materials

This repository contains educational materials for a Computer Science Basics course, including lesson notes, exercises, homeworks, exams, and bagrut (matriculation) questions. The materials are written in LaTeX, Jupyter notebooks, and Markdown, and can be compiled to PDF using the provided Makefile.

## Project Structure

- `src/`: Source files
  - `lessonNotes/`: Lesson notes in Jupyter notebooks
  - `exams/`: Exam files in LaTeX
  - `exs/`: Exercises in LaTeX
  - `bagrut_questions/`: Generated topic files for bagrut questions
- `bagrut_questions/`: Original bagrut question PDFs and generated solution TeX files
- `images/`: Images used in the materials
- `interactive_apps/`: HTML interactive applications
- `jff_files/`: JFLAP files for automata
- `scripts/`: Utility scripts and templates
- `out/`: Generated output files (created by Makefile)

## Scripts

### Bagrut Questions Scripts (`scripts/bagrut_questions/`)

- `create_empty_sol.py`: Generates empty LaTeX solution files for bagrut question images/PDFs. Selects the appropriate template based on the folder (C# template for `basics`, default for others).
  - Usage: `python scripts/bagrut_questions/create_empty_sol.py [file_path]`
  - Example: `python scripts/bagrut_questions/create_empty_sol.py bagrut_questions/basics/if_2011_899222_3.pdf`

- `create_questions_index.py`: Generates CSV and HTML indexes of bagrut questions, including solution status and usage tracking.
  - Usage: `python scripts/bagrut_questions/create_questions_index.py`
  - Outputs: `out/bagrut_questions/questions_index.csv` and `out/bagrut_questions/questions_index.html`

- `split_pdf_to_pages.py`: Splits PDF files into individual pages or converts PDFs to cropped images.
  - Usage: `python scripts/bagrut_questions/split_pdf_to_pages.py`

- Templates:
  - `empty_sol_template.tex`: Default template for solution files
  - `empty_sol_template_csharp.tex`: C# template for basics folder
  - `bagrut_questions_by_topic_template.tex`: Template for topic files
  - `questions_index_template.html`: HTML template for the questions index

### Other Scripts (`scripts/`)

- `clean.py`: Cleaning script for output directories
- `export_cs.py`: Exports C# code from Jupyter notebooks
- `rename_file.py`: File renaming utility
- LaTeX templates: `beamer_preamble.tex`, `simple_beamer.tex`, `tex_preamble.tex`, `usefule_tex_things.tex`
- `first_cell_to_handle_arabic.html`: HTML for handling Arabic text

## Makefile Targets

### Main Targets

- `make all` or `make`: Generate everything (runs index, pdf, printable, sols, sclean)
- `make pdf`: Generate PDF files from all sources
- `make printable`: Generate printing-friendly PDFs (removes code and solutions)
- `make sols`: Generate PDFs with solutions
- `make index`: Run the create_questions_index.py script to generate question indexes and topic files

### Component Targets

- `make ipynb`: Convert Jupyter notebooks to PDFs
- `make md`: Convert Markdown files to PDFs
- `make tex`: Convert LaTeX files to PDFs
- `make cs`: Export C# code from Jupyter notebooks

### Cleaning Targets

- `make clean`: Remove the entire `out/` directory and minted directories
- `make sclean`: Clean auxiliary LaTeX files (log, aux, toc, etc.) and empty files
- `make dclean`: Run the clean.py script on the output directory

### Notes

- The `all` target first runs `index` to generate bagrut question indexes and topic TeX files, then compiles all PDFs.
- PDFs are generated with different variants:
  - Regular PDFs include detailed content
  - Printable PDFs exclude code and solutions
  - Solutions PDFs include solutions
- Output files are placed in `out/` mirroring the `src/` structure

## Usage

1. Clone the repository
2. Install dependencies: Jupyter, Pandoc, XeLaTeX, Python
3. Run `make` to generate all materials
4. View generated PDFs in `out/`

## Dependencies

- Python 3
- Jupyter Notebook
- Pandoc
- XeLaTeX
- LaTeX packages (minted, etc.)
- JFLAP (for automata files)
