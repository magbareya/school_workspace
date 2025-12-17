import sys
from nbconvert.exporters import ScriptExporter

"""
Exports code from Jupyter notebooks to C# script files with cell separators.

Usage: python scripts/export_cs.py <notebook.ipynb> <output.cs>
"""

SEPARATOR = '\n\n/* ********************** */\n\n'

notebook = sys.argv[1]
outfile = sys.argv[2]

exporter = ScriptExporter()
exporter.exclude_markdown = True

# Get the raw code
body, _ = exporter.from_filename(notebook)

# Split the code into cells (nbconvert uses "# coding: utf-8" + cell markers)
# We'll split by double newlines, which is what ScriptExporter usually uses
cells = body.strip().split('\n\n')

# Prepare the final output with separators
final_body = SEPARATOR.join(cells)

# Write to file
with open(outfile, "w", encoding="utf-8") as f:
    f.write(final_body)
