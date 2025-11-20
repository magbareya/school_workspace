import os
import re

# folder containing the PDF files (current folder)
FOLDER = "bagrut_questions/computational_models"
BASE_PATH = "../../../bagrut_questions/computational_models/"

# regex to extract parts: prefixes_year_model_number.pdf
PATTERN = re.compile(r"(.+?)_(\d{4})_(\d+)_(\d+)\.pdf$")

for filename in os.listdir(FOLDER):
    if not filename.lower().endswith(".pdf"):
        continue

    match = PATTERN.match(filename)
    if not match:
        print(f"Skipping (bad format): {filename}")
        continue

    prefixes, year, model, number = match.groups()

    tex_filename = filename.replace(".pdf", ".tex")

    # If tex file already exists → skip
    if os.path.exists(os.path.join(FOLDER, tex_filename)):
        print(f"Exists, skipping: {tex_filename}")
        continue

    # Build LaTeX content
    content = f"""\\importpdfpage{{{BASE_PATH}{filename}}}{{1}}

\\ifwithsols

\\paragraph*{{حل سؤال {number} امتحان {model} سنة {year}}}:
\\bigskip

% // TODO:

\\fi
"""

    # Write .tex file
    with open(os.path.join(FOLDER, tex_filename), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {tex_filename}")
