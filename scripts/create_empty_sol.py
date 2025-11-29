import os
import re
import sys

# === Configuration ===
FOLDERS = [
    "bagrut_questions/computational_models",
    "bagrut_questions/basics",
]

TEMPLATE_FILE = "scripts/empty_sol_template.tex"

# Map extension to LaTeX command
EXTENSION_TEMPLATES = {
    "pdf": "\\importpdfpage{{{filepath}}}{{1}}",
    "png": "\\insertFullImg{{{filepath}}}",
    "jpg": "\\insertFullImg{{{filepath}}}",
    "jpeg": "\\insertFullImg{{{filepath}}}",
}

# === Load Template ===
if not os.path.exists(TEMPLATE_FILE):
    print(f"Error: Template file '{TEMPLATE_FILE}' not found!")
    exit(1)

with open(TEMPLATE_FILE, "r", encoding="utf-8") as t:
    RAW_TEMPLATE = t.read()

# Build Regex
supported_extensions = "|".join(EXTENSION_TEMPLATES.keys())
PATTERN = re.compile(rf"(.+?)_(\d{{4}}[A-Z]?)_(\d+)_(\d+[A-Z]?)\.({supported_extensions})$")

def process_file(file_path):
    """
    Generates a .tex solution file for a specific image/pdf path.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    # 1. Validate Extension
    file_ext = filename.lower().split('.')[-1]
    if file_ext not in EXTENSION_TEMPLATES:
        # Silently skip in batch mode, but maybe warn if it was a direct single-file call?
        # For now, we just return to keep output clean.
        return

    # 2. Validate Filename Format (Regex)
    match = PATTERN.match(filename)
    if not match:
        print(f"Skipping (bad format): {filename}")
        return

    prefixes, year, model, number, extension = match.groups()
    tex_filename = filename.replace(f".{extension}", ".tex")
    full_tex_path = os.path.join(directory, tex_filename)

    # 3. Check if Tex file already exists
    if os.path.exists(full_tex_path):
        print(f"Exists, skipping: {tex_filename}")
        return

    # 4. Construct the LaTeX path
    # Original logic: "../../../bagrut_questions/{folder_name}/{filename}"
    folder_name = os.path.basename(directory)

    # NOTE: This assumes the standard structure.
    # If you run this on a file outside 'bagrut_questions', you might want to change this logic.
    latex_relative_path = f"../../../bagrut_questions/{folder_name}/{filename}"

    image_command = EXTENSION_TEMPLATES[extension].format(filepath=latex_relative_path)

    # 5. Fill Template
    content = RAW_TEMPLATE.replace("[[NUMBER]]", number) \
                          .replace("[[MODEL]]", model) \
                          .replace("[[YEAR]]", year) \
                          .replace("[[IMAGE_COMMAND]]", image_command)

    # 6. Write File
    with open(full_tex_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {tex_filename}")


# === Main Execution ===
if __name__ == "__main__":

    # Case 1: Argument provided (Single File)
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        print(f"=== Processing single file: {target_file} ===")
        process_file(target_file)

    # Case 2: No arguments (Batch Mode)
    else:
        print("=== No arguments provided. Running batch mode on configured folders... ===")
        for folder in FOLDERS:
            if not os.path.exists(folder):
                print(f"Folder does not exist: {folder}")
                continue

            print(f"\n--- Checking folder: {folder} ---")
            for filename in os.listdir(folder):
                full_path = os.path.join(folder, filename)
                # Ensure we only process files, not subdirectories
                if os.path.isfile(full_path):
                    process_file(full_path)

    print("\n=== Done ===")
