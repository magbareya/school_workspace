import os
import re

FOLDERS = [
    "bagrut_questions/computational_models",
    "bagrut_questions/basics",
]

# Configuration: map each extension to its LaTeX template
# Use {filepath} as placeholder for the file path
EXTENSION_TEMPLATES = {
    "pdf": "\\importpdfpage{{{filepath}}}{{1}}",
    "png": "\\insertFullImg{{{filepath}}}",
    "jpg": "\\insertFullImg{{{filepath}}}",
    "jpeg": "\\insertFullImg{{{filepath}}}",
}

# Build regex pattern dynamically from supported extensions
supported_extensions = "|".join(EXTENSION_TEMPLATES.keys())
PATTERN = re.compile(rf"(.+?)_(\d{{4}})_(\d+)_(\d+[A-Z]?)\.({supported_extensions})$")

# Process each folder
for FOLDER in FOLDERS:
    print(f"\n=== Processing folder: {FOLDER} ===")

    # Calculate relative path from the folder to bagrut_questions
    # Assuming script is run from a location where these paths make sense
    folder_name = os.path.basename(FOLDER)
    BASE_PATH = f"../../../bagrut_questions/{folder_name}/"

    if not os.path.exists(FOLDER):
        print(f"Folder does not exist: {FOLDER}")
        continue

    for filename in os.listdir(FOLDER):
        # Check if file has a supported extension
        file_ext = filename.lower().split('.')[-1]
        if file_ext not in EXTENSION_TEMPLATES:
            continue

        match = PATTERN.match(filename)
        if not match:
            print(f"Skipping (bad format): {filename}")
            continue

        prefixes, year, model, number, extension = match.groups()
        tex_filename = filename.replace(f".{extension}", ".tex")

        # If tex file already exists → skip
        if os.path.exists(os.path.join(FOLDER, tex_filename)):
            print(f"Exists, skipping: {tex_filename}")
            continue

        # Get the appropriate template and insert the filepath
        filepath = f"{BASE_PATH}{filename}"
        image_command = EXTENSION_TEMPLATES[extension].format(filepath=filepath)

        content = f"""\\subsection*{{سؤال {number} امتحان {model} سنة {year}}}

{image_command}

\\ifwithsols
\\subsubsection*{{حل سؤال {number} امتحان {model} سنة {year}}}:
\\bigskip
% // TODO:
\\fi
"""

        # Write .tex file
        with open(os.path.join(FOLDER, tex_filename), "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created: {tex_filename}")

print("\n=== Done processing all folders ===")