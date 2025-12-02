import os
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/rename_file.py <old_filename> <new_filename>")
        sys.exit(1)

    old_filename = sys.argv[1]
    new_filename = sys.argv[2]

    root_dir = os.getcwd()

    print(f"Starting process: replacing '{old_filename}' with '{new_filename}' in {root_dir}...")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)

            if file.endswith(".tex"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if old_filename in content:
                        new_content = content.replace(old_filename, new_filename)

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"[Content Updated] inside: {file}")
                except Exception as e:
                    print(f"Error reading/writing {file}: {e}")

            name, ext = os.path.splitext(file)

            if name == old_filename:
                new_file_path = os.path.join(dirpath, new_filename + ext)

                try:
                    os.rename(file_path, new_file_path)
                    print(f"[File Renamed] {file} -> {new_filename + ext}")
                except OSError as e:
                    print(f"Error renaming {file}: {e}")

if __name__ == "__main__":
    main()