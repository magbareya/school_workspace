import os
import csv
import glob
import sys
import argparse

"""
Generates CSV and HTML indexes of bagrut questions, including solution status and usage tracking.

Usage: python scripts/bagrut_questions/create_questions_index.py [--sort {year,question,model}]
"""

# -------------------------------
# CONFIGURATION
# -------------------------------
SRC_DIR = "src"
OUT_DIR = "out"
# QUESTIONS_DIR will be determined dynamically per subject
# CSV and HTML output paths will be generated per subject
# -------------------------------

sys.path.insert(0, os.path.dirname(__file__))
from utils import parse_filename


# Ordered topic config and Arabic section titles for aggregate files.
AGGREGATE_TOPIC_CONFIG = {
    "basics": [
        ("if", "الشرط"),
        ("loops", "الحلقات"),
        ("strings", "النص"),
        ("arrays", "المصفوفات"),
    ],
    "computational_models": [
        ("languages", "اللغات"),
        ("dfa", "الأوتومات النهائي المحدد"),
        ("nfa", "الأوتومات النهائي غير المحدد"),
        ("regularity", "اللغات النظامية"),
        ("irregularity", "إثبات عدم النظامية"),
        ("pda", "أوتومات الراصة"),
        ("turing", "آلة تورينج"),
    ],
}

AGGREGATE_FILE_NAMES = {
    "basics": "all_basics.tex",
    "computational_models": "all_computational_models.tex",
}


AGGREGATE_TITLES = {
    "basics": "أسئلة بجروت - أساسيات",
    "computational_models": "أسئلة بجروت - موديلات حسابية",
}


def sort_questions_list(questions, sort_key):
    """Sort questions by the selected strategy."""
    if sort_key == "year":
        return sorted(questions, key=lambda x: (x[0], x[1], x[2]))  # year, model, qnum
    if sort_key == "question":
        return sorted(questions, key=lambda x: (x[2], x[0], x[1]))  # qnum, year, model
    return sorted(questions, key=lambda x: (x[1], x[0], x[2]))  # model, year, qnum


def topic_title_ar(folder, topic):
    """Return Arabic title for topic, fallback to topic key if missing."""
    for topic_key, arabic_title in AGGREGATE_TOPIC_CONFIG.get(folder, []):
        if topic_key == topic:
            return arabic_title
    return topic


def ordered_topics(folder, available_topics):
    """Return topics ordered by config first, then any remaining topics alphabetically."""
    ordered = []
    configured = [k for k, _ in AGGREGATE_TOPIC_CONFIG.get(folder, [])]

    for topic in configured:
        if topic in available_topics:
            ordered.append(topic)

    for topic in sorted(available_topics):
        if topic not in ordered:
            ordered.append(topic)

    return ordered


def build_aggregate_tex(folder, folder_topics):
    """Build a complete TeX document with sections per topic."""
    title = AGGREGATE_TITLES.get(folder, f"أسئلة بجروت - {folder}")
    sections = []

    for topic in ordered_topics(folder, set(folder_topics.keys())):
        section_title = topic_title_ar(folder, topic)
        questions = folder_topics[topic]

        lines = [f"\\clearpage", f"\\section{{{section_title}}}"]
        for _, _, _, file_path in questions:
            stem = os.path.splitext(os.path.basename(file_path))[0]
            lines.append(f"\\input{{../../../bagrut_questions/{folder}/{stem}.tex}}")

        sections.append("\n".join(lines))

    sections_content = "\n\n".join(sections)

    return f"""\\documentclass[12pt]{{article}}
\\input{{../../../scripts/tex_preamble.tex}}

\\ifwithsols
\\title{{حل {title}}}
\\else
\\title{{{title}}}
\\fi

\\begin{{document}}

\\maketitle
\\renewcommand{{\\contentsname}}{{جدول المحتويات}}
\\tableofcontents
\\clearpage

{sections_content}

\\end{{document}}
"""


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
        if "bagrut_questions" in tex:
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


def generate_html(rows, folders_set, topics_set, models_set, years_set, total_questions, solved_count, used_count, unused_count, html_output_file):
    """
    Generates HTML with Multi-Select Checkboxes and Reordered Columns.
    """

    # Prepare Checkbox Lists HTML
    # Folder filter removed since each subject has its own index
    topics_html = create_checkbox_list(sorted(list(topics_set)), "topic-checkbox", "top")
    models_html = create_checkbox_list(sorted(list(models_set)), "model-checkbox", "mod")
    years_html = create_checkbox_list(sorted(list(years_set), reverse=True), "year-checkbox", "yr")

    # Build table rows
    table_rows = ""
    for row in rows:
        folder, topic, model, year, qnum, has_sol, is_used_val, file_path, f_type = row

        try:
            rel_path = os.path.relpath(file_path, os.path.dirname(html_output_file))
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
            <tr data-topic="{topic}" data-model="{model}" data-year="{year}" data-used="{used_text_val}">
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
        topics_html=topics_html,
        models_html=models_html,
        years_html=years_html,
        table_rows=table_rows
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(html_output_file), exist_ok=True)

    with open(html_output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Index written to {html_output_file}")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate indexes and topic files for bagrut questions.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--sort",
        choices=["year", "question", "model"],
        default="year",
        help="Sorting strategy for questions in topic.tex files (default: year)"
    )
    args = parser.parse_args()

    # Find all subject directories in bagrut_questions/
    questions_base_dir = "bagrut_questions"
    subject_dirs = []

    if not os.path.isdir(questions_base_dir):
        print(f"Questions directory not found: {questions_base_dir}")
        return

    for item in os.listdir(questions_base_dir):
        potential_path = os.path.join(questions_base_dir, item)
        if os.path.isdir(potential_path):
            subject_dirs.append((item, potential_path))

    if not subject_dirs:
        print(f"No subject directories found in {questions_base_dir}/")
        return

    print(f"Found {len(subject_dirs)} subject folder(s): {', '.join(s[0] for s in subject_dirs)}\n")

    # Process each subject separately
    for subject, questions_dir in subject_dirs:
        print(f"Processing subject: {subject}")
        print(f"Questions directory: {questions_dir}")

        rows_data = []
        csv_rows = []

        all_folders = set()
        all_topics = set()
        all_models = set()
        all_years = set()

        # Walk through the questions directory for this subject
        for root, _, files in os.walk(questions_dir):
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

        if not rows_data:
            print(f"  No questions found in {questions_dir}, skipping...\n")
            continue

        # Sort Logic: Folder -> Topic -> Year -> Model -> Num -> Used(False first)
        rows_data.sort(key=lambda x: (x[0], x[1], x[3], x[2], x[4], x[6]))

        # CSV Generation
        for r in rows_data:
            csv_rows.append([
                r[0], r[1], r[2], r[3], r[4],
                "YES" if r[5] else "NO",
                "YES" if r[6] else "NO"
            ])

        # Set output paths for this subject
        output_subject_dir = os.path.join(OUT_DIR, subject, "bagrut_questions")
        csv_output_file = os.path.join(output_subject_dir, "questions_index.csv")
        html_output_file = os.path.join(output_subject_dir, "questions_index.html")

        # Ensure output directory exists
        os.makedirs(output_subject_dir, exist_ok=True)

        if os.path.exists(csv_output_file):
            os.remove(csv_output_file)
        with open(csv_output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Folder", "Topic", "Model", "Year", "Question Number", "Has Solution", "Is Used?"])
            writer.writerows(csv_rows)
        print(f"  CSV Index written to {csv_output_file}")

        # Calculate summary statistics
        total_questions = len(rows_data)
        solved_count = sum(1 for r in rows_data if r[5])
        used_count = sum(1 for r in rows_data if r[6])
        unused_count = total_questions - used_count

        # HTML Generation
        generate_html(rows_data, all_folders, all_topics, all_models, all_years, total_questions, solved_count, used_count, unused_count, html_output_file)

        # Generate topic files
        from collections import defaultdict
        topic_files = defaultdict(list)
        for row in rows_data:
            folder, topic, model, year, qnum, solution, used, file_path, ext = row
            tex_file = f"{os.path.splitext(file_path)[0]}.tex"
            if os.path.exists(tex_file):  # Include questions that have tex files
                effective_topic = topic
                if topic.startswith("loops_"):
                    effective_topic = "loops"
                topic_files[(folder, effective_topic)].append((year, model, qnum, file_path))

        # Delete existing topic files
        folder_path = os.path.join(SRC_DIR, subject, "bagrut_questions")
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".tex"):
                    os.remove(os.path.join(folder_path, file))

        template_path = os.path.join(os.path.dirname(__file__), "bagrut_questions_by_topic_template.tex")
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        for (folder, topic), questions in topic_files.items():
            # questions tuple: (year, model, qnum, file_path)
            questions = sort_questions_list(questions, args.sort)

            questions_list = "\n".join([f"\\input{{../../../bagrut_questions/{folder}/{os.path.splitext(os.path.basename(q[3]))[0]}.tex}}" for q in questions if os.path.exists(f"bagrut_questions/{folder}/{os.path.splitext(os.path.basename(q[3]))[0]}.tex")])

            content = template_content.replace("[[QUESTIONS_LIST]]", questions_list)

            output_dir = os.path.join(SRC_DIR, subject, "bagrut_questions")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{topic}.tex")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Generated topic file: {output_file}")

        # Generate aggregate files (all topics in one file per folder)
        folder_topics = {}

        for (f_name, topic), questions in topic_files.items():
            folder_topics[topic] = sort_questions_list(questions, args.sort)

        if folder_topics:
            output_dir = os.path.join(SRC_DIR, subject, "bagrut_questions")
            os.makedirs(output_dir, exist_ok=True)

            aggregate_name = AGGREGATE_FILE_NAMES.get(subject, f"all_{subject}.tex")
            aggregate_path = os.path.join(output_dir, aggregate_name)
            aggregate_content = build_aggregate_tex(subject, folder_topics)

            with open(aggregate_path, "w", encoding="utf-8") as f:
                f.write(aggregate_content)

            print(f"  Generated aggregate file: {aggregate_path}")

        print(f"[OK] Completed processing for subject: {subject}\n")


if __name__ == "__main__":
    main()
