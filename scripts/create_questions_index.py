import os
import csv
import glob

# -------------------------------
# CONFIGURATION
# -------------------------------
QUESTIONS_DIR = "bagrut_questions"
SRC_DIR = "src"
OUTPUT_FILE = "bagrut_questions/questions_index.csv"
# -------------------------------

def parse_filename(filename):
    """
    Parse filename like: <topic_name>_<year>_<model>_<question_number>.pdf
    Topic name can contain underscores.
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.split("_")
    if len(parts) < 4:
        return ("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")

    topic = "_".join(parts[:-3])  # everything except last three parts
    year = parts[-3]
    model = parts[-2]
    qnum = parts[-1]
    return topic, year, model, qnum


def has_solution(pdf_path):
    """
    A question has a solution if corresponding .tex exists and does not contain "TODO"
    """
    base, _ = os.path.splitext(pdf_path)
    tex_file = f"{base}.tex"
    if not os.path.exists(tex_file):
        return False

    with open(tex_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        if "TODO" in content:
            return False
    return True


def is_used(qname):
    """
    Check if qname appears in any .tex file under SRC_DIR
    """
    pattern = os.path.join(SRC_DIR, "**", "*.tex")
    for tex in glob.glob(pattern, recursive=True):
        with open(tex, "r", encoding="utf-8", errors="ignore") as f:
            if qname in f.read():
                return True
    return False


def main():
    rows = []

    # Walk recursively through QUESTIONS_DIR
    for root, _, files in os.walk(QUESTIONS_DIR):
        folder_name = os.path.basename(root)  # only folder name
        for f in files:
            if f.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
                pdf_path = os.path.join(root, f)

                topic, year, model, qnum = parse_filename(f)
                solution = has_solution(pdf_path)
                used = is_used(os.path.splitext(f)[0])

                rows.append([folder_name, topic, model, year, qnum,
                             "YES" if solution else "NO",
                             "YES" if used else "NO"])

    # Sort by topic, year, model, question number
    rows.sort(key=lambda x: (x[1], x[3], x[2], x[4]))

    # Write CSV
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Folder", "Topic", "Model", "Year", "Question Number",
                         "Has Solution", "Is Used?"])
        writer.writerows(rows)

    print(f"Index written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()