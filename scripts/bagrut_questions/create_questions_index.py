import os
import csv
import glob
import sys

"""
Generates CSV and HTML indexes of bagrut questions, including solution status and usage tracking.

Usage: python scripts/bagrut_questions/create_questions_index.py
"""

# -------------------------------
# CONFIGURATION
# -------------------------------
QUESTIONS_DIR = "bagrut_questions"
SRC_DIR = "src"
CSV_OUTPUT_FILE = "out/bagrut_questions/questions_index.csv"
HTML_OUTPUT_FILE = "out/bagrut_questions/questions_index.html"
# -------------------------------

sys.path.insert(0, os.path.dirname(__file__))
from utils import parse_filename


def has_solution(pdf_path):
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
    pattern = os.path.join(SRC_DIR, "**", "*.tex")
    for tex in glob.glob(pattern, recursive=True):
        if "src\\bagrut_questions" in tex:
            continue
        with open(tex, "r", encoding="utf-8", errors="ignore") as f:
            if qname in f.read():
                return True
    return False


def create_checkbox_list(items, css_class, element_id_prefix):
    """Helper to generate HTML for checkbox lists"""
    html = ""
    for i, item in enumerate(items):
        html += f"""
        <div class="form-check">
            <input class="form-check-input {css_class}" type="checkbox" value="{item}" id="{element_id_prefix}_{i}">
            <label class="form-check-label w-100" for="{element_id_prefix}_{i}">
                {item}
            </label>
        </div>
        """
    return html


def generate_html(rows, folders_set, topics_set, models_set, years_set, total_questions, solved_count, used_count, unused_count):
    """
    Generates HTML with Multi-Select Checkboxes and Reordered Columns.
    """

    # Prepare Checkbox Lists HTML
    folders_html = create_checkbox_list(sorted(list(folders_set)), "folder-checkbox", "fold")
    topics_html = create_checkbox_list(sorted(list(topics_set)), "topic-checkbox", "top")
    models_html = create_checkbox_list(sorted(list(models_set)), "model-checkbox", "mod")
    years_html = create_checkbox_list(sorted(list(years_set), reverse=True), "year-checkbox", "yr")

    # Build table rows
    table_rows = ""
    for row in rows:
        folder, topic, model, year, qnum, has_sol, is_used_val, file_path, f_type = row

        try:
            rel_path = os.path.relpath(file_path, os.path.dirname(HTML_OUTPUT_FILE))
            rel_path = rel_path.replace(os.sep, '/')
        except ValueError:
            rel_path = file_path

        sol_html = '<span class="status-yes">نعم</span>' if has_sol else '<span class="status-no">لا</span>'
        used_html = '<span class="status-yes">نعم</span>' if is_used_val else '<span class="status-no">لا</span>'
        used_text_val = "نعم" if is_used_val else "لا"

        if f_type in ['.png', '.jpg', '.jpeg']:
            view_action = f'''<button class="btn-preview"
                                onclick="showImage('{rel_path}', '{topic} - {year}')">
                                👁️ معاينة
                             </button>'''
        else:
            view_action = f'<a href="{rel_path}" target="_blank" class="btn btn-sm btn-outline-danger">📄 PDF</a>'

        table_rows += f"""
            <tr data-folder="{folder}" data-topic="{topic}" data-model="{model}" data-year="{year}" data-used="{used_text_val}">
                <td class="small text-muted">{folder}</td>
                <td class="fw-bold">{topic}</td>
                <td>{year}</td>
                <td>{model}</td>
                <td>{qnum}</td>
                <td>{used_html}</td>
                <td>{sol_html}</td>
                <td class="text-center">{view_action}</td>
            </tr>
        """

    # Read template
    template_path = os.path.join(os.path.dirname(__file__), "questions_index_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Format with data
    html_content = html_content.format(
        total_questions=total_questions,
        solved_count=solved_count,
        used_count=used_count,
        unused_count=unused_count,
        folders_html=folders_html,
        topics_html=topics_html,
        models_html=models_html,
        years_html=years_html,
        table_rows=table_rows
    )

    with open(HTML_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Index written to {HTML_OUTPUT_FILE}")


def main():
    rows_data = []
    csv_rows = []

    all_folders = set()
    all_topics = set()
    all_models = set()
    all_years = set()

    for root, _, files in os.walk(QUESTIONS_DIR):
        folder_name = os.path.basename(root)

        if "out" in root:
            continue

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in [".pdf", ".png", ".jpg", ".jpeg"]:
                file_path = os.path.join(root, f)

                topic, year, model, qnum, _ = parse_filename(f)

                all_folders.add(folder_name)
                if topic != "UNKNOWN": all_topics.add(topic)
                if model != "UNKNOWN": all_models.add(model)
                if year != "UNKNOWN": all_years.add(year)

                solution = has_solution(file_path)
                used = is_used(os.path.splitext(f)[0])

                rows_data.append([
                    folder_name, topic, model, year, qnum,
                    solution, used, file_path, ext
                ])

    # Sort Logic: Folder -> Topic -> Year -> Model -> Num -> Used(False first)
    # Note: False sorts before True (0 < 1), so unused comes first as requested
    rows_data.sort(key=lambda x: (x[0], x[1], x[3], x[2], x[4], x[6]))

    # CSV Generation
    for r in rows_data:
        csv_rows.append([
            r[0], r[1], r[2], r[3], r[4],
            "YES" if r[5] else "NO",
            "YES" if r[6] else "NO"
        ])

    if os.path.exists(CSV_OUTPUT_FILE):
        os.remove(CSV_OUTPUT_FILE)
    with open(CSV_OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Folder", "Topic", "Model", "Year", "Question Number", "Has Solution", "Is Used?"])
        writer.writerows(csv_rows)
    print(f"CSV Index written to {CSV_OUTPUT_FILE}")

    # Calculate summary statistics
    total_questions = len(rows_data)
    solved_count = sum(1 for r in rows_data if r[5])
    used_count = sum(1 for r in rows_data if r[6])
    unused_count = total_questions - used_count

    # HTML Generation
    generate_html(rows_data, all_folders, all_topics, all_models, all_years, total_questions, solved_count, used_count, unused_count)

    # Generate topic files
    from collections import defaultdict
    topic_files = defaultdict(list)
    for row in rows_data:
        folder, topic, model, year, qnum, solution, used, file_path, ext = row
        tex_file = f"{os.path.splitext(file_path)[0]}.tex"
        if os.path.exists(tex_file):  # Include questions that have tex files
            topic_files[(folder, topic)].append((year, model, qnum, file_path))

    # Delete existing topic files
    for folder in ["basics", "computational_models"]:
        folder_path = os.path.join("src", "bagrut_questions", folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".tex"):
                    os.remove(os.path.join(folder_path, file))

    template_path = os.path.join(os.path.dirname(__file__), "bagrut_questions_by_topic_template.tex")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    for (folder, topic), questions in topic_files.items():
        questions.sort(key=lambda x: (x[0], x[1], x[2]))  # year, model, qnum
        questions_list = "\n".join([f"\\input{{../../../bagrut_questions/{folder}/{os.path.splitext(os.path.basename(q[3]))[0]}.tex}}" for q in questions if os.path.exists(f"bagrut_questions/{folder}/{os.path.splitext(os.path.basename(q[3]))[0]}.tex")])

        content = template_content.replace("[[QUESTIONS_LIST]]", questions_list)

        output_dir = os.path.join("src", "bagrut_questions", folder)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{topic}.tex")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated topic file: {output_file}")


if __name__ == "__main__":
    main()
