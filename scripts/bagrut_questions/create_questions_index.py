"""Generate Bagrut question indexes and LaTeX collections."""

import argparse
from collections import Counter, defaultdict
import csv
import glob
import hashlib
import subprocess
from pathlib import Path
import html
import json
import os
import random
import re
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None

SRC_DIR = "src"
OUT_DIR = "out"
QUESTIONS_BASE_DIR = "bagrut_questions"

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    QuestionRecord,
    SUPPORTED_EXTENSIONS,
    natural_sort_key,
    parse_filename,
)

with Path(__file__).with_name("index_labels.json").open(encoding="utf-8") as labels_file:
    LABELS = json.load(labels_file)

# Ordered topic configuration and Arabic section titles per subject
AGGREGATE_TOPIC_CONFIG = LABELS["tex_topics"]

# Plain-text Arabic labels for the HTML UI (without LaTeX macros)
HTML_TOPIC_LABELS_AR = LABELS["html_topics"]

AGGREGATE_FILE_NAMES: Dict[str, str] = {
    "basics": "all_basics.tex",
    "computational_models": "all_computational_models.tex",
    "oop": "all_oop.tex",
}

AGGREGATE_TITLES = LABELS["subject_titles"]


def topic_title_ar(folder: str, topic: str) -> str:
    """Return LaTeX Arabic title for topic, falling back to topic key if missing."""
    for topic_key, arabic_title in AGGREGATE_TOPIC_CONFIG.get(folder, []):
        if topic_key == topic:
            return arabic_title
    escapes = {"\\": r"\textbackslash{}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    escaped = "".join(escapes.get(c, "\\" + c if c in "_%&#\u0024{}" else c) for c in topic)
    return rf"\textenglish{{{escaped}}}"


def texorpdfstring(latex_text: str) -> str:
    """Pair a LaTeX heading with a plain-text PDF bookmark to avoid math warnings."""
    if "$" not in latex_text and "\\" not in latex_text:
        return latex_text
    bookmark = re.sub(r"\\(?:textenglish|text)\{([^{}]*)\}", r"\1", latex_text)
    bookmark = bookmark.replace("$", "")
    return rf"\texorpdfstring{{{latex_text}}}{{{bookmark}}}"


def ordered_topics(folder: str, available_topics: Set[str]) -> List[str]:
    """Return topics ordered by AGGREGATE_TOPIC_CONFIG first, then remaining alphabetically."""
    ordered: List[str] = []
    configured = [k for k, _ in AGGREGATE_TOPIC_CONFIG.get(folder, [])]

    for topic in configured:
        if topic in available_topics:
            ordered.append(topic)

    for topic in sorted(available_topics):
        if topic not in ordered:
            ordered.append(topic)

    return ordered


def sort_questions(
    records: Sequence[QuestionRecord], sort_strategy: str, seed: Optional[int] = None
) -> List[QuestionRecord]:
    """Sort QuestionRecord items using natural alphanumeric ordering."""
    items = list(records)
    if sort_strategy == "random":
        random.Random(seed).shuffle(items)
        return items

    if sort_strategy == "exam":
        items.sort(
            key=lambda r: (
                natural_sort_key(r.year),
                natural_sort_key(r.model),
                natural_sort_key(r.qnum),
            )
        )
    elif sort_strategy == "year":
        items.sort(
            key=lambda r: (
                natural_sort_key(r.year),
                natural_sort_key(r.qnum),
                natural_sort_key(r.model),
            )
        )
    elif sort_strategy == "question":
        items.sort(
            key=lambda r: (
                natural_sort_key(r.qnum),
                natural_sort_key(r.year),
                natural_sort_key(r.model),
            )
        )
    elif sort_strategy == "model":
        items.sort(
            key=lambda r: (
                natural_sort_key(r.model),
                natural_sort_key(r.year),
                natural_sort_key(r.qnum),
            )
        )
    else:
        items.sort(
            key=lambda r: (
                natural_sort_key(r.year),
                natural_sort_key(r.model),
                natural_sort_key(r.qnum),
            )
        )
    return items


def deduplicate_by_stem(records: Iterable[QuestionRecord]) -> List[QuestionRecord]:
    """Keep at most one QuestionRecord per stem (case-insensitive) to avoid duplicate \\input lines."""
    seen: Set[Tuple[str, str]] = set()
    unique: List[QuestionRecord] = []
    for r in records:
        key = (r.folder.lower(), r.stem.lower())
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def load_topic_template() -> str:
    template_path = os.path.join(os.path.dirname(__file__), "bagrut_questions_by_topic_template.tex")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_latex_document(title: str, body_content: str) -> str:
    """Render a full LaTeX document using bagrut_questions_by_topic_template.tex."""
    template = load_topic_template()
    return template.replace("[[TITLE]]", title).replace("[[QUESTIONS_LIST]]", body_content)


def build_aggregate_tex(folder: str, folder_topics: Dict[str, List[QuestionRecord]]) -> str:
    """Build a complete TeX document with sections per topic."""
    title = AGGREGATE_TITLES.get(folder, LABELS["title"].format(folder))
    sections: List[str] = []

    for topic in ordered_topics(folder, set(folder_topics.keys())):
        section_title = topic_title_ar(folder, topic)
        questions = deduplicate_by_stem(folder_topics[topic])
        if not questions:
            continue

        lines = ["\\clearpage", f"\\section{{{texorpdfstring(section_title)}}}"]
        for q in questions:
            lines.append(q.latex_input)
        sections.append("\n".join(lines))

    return render_latex_document(title, "\n\n".join(sections))


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        if config_path.endswith((".yaml", ".yml")):
            if yaml is None:
                raise ImportError("PyYAML is not installed. Please install it or use JSON.")
            return yaml.safe_load(f)
        return json.load(f)


def filter_questions(records: Sequence[QuestionRecord], filters: dict) -> List[QuestionRecord]:
    filtered: List[QuestionRecord] = []
    requested_files = {
        os.path.normpath(path).replace("\\", "/").removeprefix("./").lower()
        for path in filters.get("files", [])
    }

    for r in records:
        if not r.has_tex:
            continue

        if requested_files:
            tex_rel = f"bagrut_questions/{r.folder}/{r.stem}.tex".lower()
            tex_name = f"{r.stem}.tex".lower()
            if tex_rel not in requested_files and tex_name not in requested_files and r.stem.lower() not in requested_files:
                continue

        year_match = re.match(r"\d{4}", r.year)
        year_int = int(year_match.group()) if year_match else None

        if "min_year" in filters and year_int is not None and year_int < filters["min_year"]:
            continue
        if "max_year" in filters and year_int is not None and year_int > filters["max_year"]:
            continue
        if "years" in filters:
            allowed_years = {str(y).lower() for y in filters["years"]}
            if r.year.lower() not in allowed_years and (year_int is None or str(year_int) not in allowed_years):
                continue
        if "models" in filters:
            allowed_models = {str(m).lower() for m in filters["models"]}
            if r.model.lower() not in allowed_models:
                continue
        if "topics" in filters and r.topic not in filters["topics"] and r.effective_topic not in filters["topics"]:
            continue
        if "exclude_topics" in filters and (r.topic in filters["exclude_topics"] or r.effective_topic in filters["exclude_topics"]):
            continue
        if "exclude_years" in filters:
            excluded_years = {str(y).lower() for y in filters["exclude_years"]}
            if r.year.lower() in excluded_years or (year_int is not None and str(year_int) in excluded_years):
                continue
        if "has_solution" in filters and r.has_sol != filters["has_solution"]:
            continue
        if "is_used" in filters and r.is_used != filters["is_used"]:
            continue

        filtered.append(r)

    return deduplicate_by_stem(filtered)


def build_custom_document(subject: str, doc_config: dict, filtered_records: Sequence[QuestionRecord]) -> str:
    title = doc_config.get("title", LABELS["custom"])
    sort_strategy = doc_config.get("sort", "year")
    group_by = doc_config.get("group_by")  # "year", "model", "topic"
    limit = doc_config.get("limit")

    sorted_records = sort_questions(filtered_records, sort_strategy, doc_config.get("seed"))
    if limit is not None:
        sorted_records = sorted_records[:limit]

    sections: List[str] = []
    if group_by:
        grouped: Dict[str, List[QuestionRecord]] = defaultdict(list)
        for r in sorted_records:
            if group_by == "year":
                key = texorpdfstring(f"${r.year}$")
            elif group_by == "model":
                key = texorpdfstring(rf"$\text{{{r.model}}}$")
            elif group_by == "topic":
                key = texorpdfstring(topic_title_ar(subject, r.effective_topic))
            else:
                key = "Group"
            grouped[key].append(r)

        for key, group_rows in grouped.items():
            lines = ["\\clearpage", f"\\section{{{key}}}"]
            lines.extend(r.latex_input for r in group_rows)
            sections.append("\n".join(lines))
    else:
        sections.append("\n".join(r.latex_input for r in sorted_records))

    return render_latex_document(title, "\n\n".join(sections))


def collection_header(body: str) -> str:
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return "% Generated by create_questions_index.py " + digest


INPUT_PATTERN = re.compile(r"\\input\{([^{}]+)\}")


def collection_dependencies(collection: Path) -> List[Path]:
    """
    Return the files a collection's PDF depends on beyond the collection itself:
    every directly \\input file (question fragments, preamble) and the media files
    sharing a fragment's stem. make only tracks the collection .tex, so these are
    checked here instead.
    """
    dependencies: List[Path] = []
    for match in INPUT_PATTERN.finditer(collection.read_text(encoding="utf-8")):
        fragment = (collection.parent / match.group(1).strip()).resolve()
        if fragment.suffix == "":
            fragment = fragment.with_suffix(".tex")
        if not fragment.is_file():
            continue
        dependencies.append(fragment)
        dependencies.extend(
            fragment.with_suffix(f".{ext}")
            for ext in SUPPORTED_EXTENSIONS
            if fragment.with_suffix(f".{ext}").is_file()
        )
    return dependencies


def mark_stale_collections(src_dir: Path, collections: dict, out_dir: Path) -> None:
    """Touch a collection whose PDFs are older than any dependency, so make rebuilds it."""
    for name in collections:
        collection = src_dir / name
        if not collection.is_file():
            continue  # A hand-edited collection that was preserved under another name.
        outputs = [out_dir / (collection.stem + suffix) for suffix in (".pdf", "_sols.pdf")]
        if not all(output.is_file() for output in outputs):
            continue  # make builds missing PDFs anyway.
        oldest_output = min(output.stat().st_mtime for output in outputs)
        if any(dep.stat().st_mtime > oldest_output for dep in collection_dependencies(collection)):
            os.utime(collection)
            print(f"  Rebuilding (a question file changed): {collection}")


def sync_collections(directory: Path, collections: dict) -> None:
    """Only delete stale documents whose generated body is still intact."""
    for path in directory.glob("*.tex"):
        if path.name not in collections and not path.is_symlink():
            header, _, body = path.read_text(encoding="utf-8").partition("\n")
            if header == collection_header(body):
                path.unlink()
    for name, body in collections.items():
        path = directory / name
        directory.mkdir(parents=True, exist_ok=True)
        result = collection_header(body) + "\n" + body
        if path.is_file():
            current = path.read_text(encoding="utf-8")
            if current == result:
                continue
            header, _, previous = current.partition("\n")
            if header.startswith("% Generated by ") and header != collection_header(previous):
                print(f"  Warning: preserving hand-edited collection: {path}", file=sys.stderr)
                continue
        path.write_text(result, encoding="utf-8")


def has_solution(media_path: str) -> bool:
    """Return True if a companion .tex file exists and has no 'TODO' placeholders."""
    base, _ = os.path.splitext(media_path)
    tex_file = f"{base}.tex"
    if not os.path.exists(tex_file):
        return False

    with open(tex_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        return "TODO" not in content


def build_usage_map(src_dir: str) -> Dict[str, List[str]]:
    """
    Scan all hand-authored .tex files under `src/` once and map each referenced
    question, keyed by lowercased "<folder>/<stem>", to the .tex files that reference it.
    Extensionless \\input arguments are recognised; exact path matching avoids
    false positives such as _1 vs _10 or same-named stems in different folders.
    """
    usage_map: Dict[str, List[str]] = defaultdict(list)
    if not os.path.isdir(src_dir):
        return usage_map

    # Match any filename stem inside bagrut_questions/<folder>/<stem>.<ext> or \input{.../<stem>.tex}
    ref_pattern = re.compile(
        r"bagrut_questions/((?:[^/{}\n]+/)+[^/{}\n]+?)(?:\.(?:tex|pdf|png|jpg|jpeg))?\s*\}",
        re.IGNORECASE,
    )

    pattern = os.path.join(src_dir, "**", "*.tex")
    for tex_path in sorted(glob.glob(pattern, recursive=True)):
        norm_tex = os.path.normpath(tex_path).replace("\\", "/")
        # Skip auto-generated topic/aggregate files inside src/<subject>/bagrut_questions/
        if "/bagrut_questions/" in norm_tex:
            continue

        rel_src_path = os.path.relpath(tex_path, src_dir).replace("\\", "/")
        try:
            with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue

        content = re.sub(r"(?<!\\)%[^\n]*", "", content)
        matched_stems = {m.group(1).lower() for m in ref_pattern.finditer(content)}
        for stem_lower in matched_stems:
            usage_map[stem_lower].append(rel_src_path)

    return usage_map


def create_checkbox_list(
    items: Sequence[str],
    counts: Counter,
    css_class: str,
    element_id_prefix: str,
    subtitles: Optional[Dict[str, str]] = None,
) -> str:
    """Generate HTML checkbox items with count badges and optional Arabic subtitles."""
    html_parts: List[str] = []
    for i, item in enumerate(items):
        count = counts.get(item, 0)
        sub_ar = subtitles.get(item, "") if subtitles else ""
        label_html = f'<span class="fw-semibold">{html.escape(item)}</span>'
        if sub_ar and sub_ar != item:
            label_html += f' <span class="text-muted small">({html.escape(sub_ar)})</span>'

        html_parts.append(
            f"""
            <label class="form-check-item" for="{element_id_prefix}_{i}">
                <div class="d-flex align-items-center gap-2 text-truncate">
                    <input class="form-check-input m-0 {css_class}" type="checkbox" value="{html.escape(item)}" id="{element_id_prefix}_{i}">
                    <span class="text-truncate">{label_html}</span>
                </div>
                <span class="count-pill">{count}</span>
            </label>
            """
        )
    return "\n".join(html_parts)


def vendor_asset(name: str) -> str:
    """Return a bundled third-party file for inlining, without its source-map comment."""
    text = Path(__file__).with_name("vendor").joinpath(name).read_text(encoding="utf-8")
    # The .map files are not bundled; drop the reference to avoid a browser 404 warning.
    return re.sub(r"\n?/\*# sourceMappingURL=[^*]*\*/\s*$|\n?//# sourceMappingURL=\S*\s*$", "", text)


def generate_html(
    subject: str,
    records: Sequence[QuestionRecord],
    html_output_file: str,
) -> None:
    """Generate the interactive modern HTML index for a subject."""
    topic_counts = Counter(r.topic for r in records if r.topic != "UNKNOWN")
    model_counts = Counter(r.model for r in records if r.model != "UNKNOWN")
    year_counts = Counter(r.year for r in records if r.year != "UNKNOWN")

    sorted_topics = ordered_topics(subject, set(topic_counts.keys()))
    sorted_models = sorted(model_counts.keys(), key=natural_sort_key)
    sorted_years = sorted(year_counts.keys(), key=natural_sort_key, reverse=True)

    topics_html = create_checkbox_list(
        sorted_topics, topic_counts, "topic-checkbox", "top", subtitles=HTML_TOPIC_LABELS_AR
    )
    models_html = create_checkbox_list(sorted_models, model_counts, "model-checkbox", "mod")
    years_html = create_checkbox_list(sorted_years, year_counts, "year-checkbox", "yr")

    row_template = Path(__file__).with_name("question_row.html").read_text(encoding="utf-8")
    table_rows: List[str] = []
    for r in records:
        try:
            rel_path = os.path.relpath(r.file_path, os.path.dirname(html_output_file)).replace(os.sep, "/")
        except ValueError:
            rel_path = r.repo_relative_path

        topic_ar = HTML_TOPIC_LABELS_AR.get(r.topic, "")
        topic_cell_html = f'<span class="fw-bold mono">{html.escape(r.topic)}</span>'
        if topic_ar:
            topic_cell_html += f'<span class="topic-ar-sub">{html.escape(topic_ar)}</span>'

        # Used status cell
        if r.is_used:
            files_tags = "".join(
                f'<span class="used-file-tag mono" title="{html.escape(path)}">{html.escape(os.path.basename(path))}</span> '
                for path in r.used_in
            )
            used_cell_html = (
                f'<div><span class="badge-pill badge-used-yes">📌 {LABELS["yes"]} ({len(r.used_in)})</span></div>'
                f'<div class="mt-1">{files_tags}</div>'
            )
            used_sort_val = f"1_{len(r.used_in):03d}"
        else:
            used_cell_html = f'<span class="badge-pill badge-used-no">{LABELS["unused"]}</span>'
            used_sort_val = "0_000"

        # Solution & .tex status cell
        if r.has_sol:
            sol_cell_html = f'<span class="badge-pill badge-solved">✅ {LABELS["solved"]}</span>'
            sol_sort_val = "2_solved"
        elif r.has_tex:
            sol_cell_html = f'<span class="badge-pill badge-stub">📝 {LABELS["stub"]}</span>'
            sol_sort_val = "1_stub"
        else:
            sol_cell_html = f'<span class="badge-pill badge-notex">⚪ {LABELS["missing"]}</span>'
            sol_sort_val = "0_notex"

        escaped_input = html.escape(r.latex_input, quote=True)
        escaped_repo_path = html.escape(r.repo_relative_path, quote=True)
        escaped_stem = html.escape(r.stem, quote=True)
        escaped_rel_path = html.escape(rel_path, quote=True)

        create_sol_btn = ""
        if not r.has_tex:
            create_cmd = f'python scripts/bagrut_questions/create_empty_sol.py "{r.repo_relative_path}"'
            escaped_cmd = html.escape(create_cmd, quote=True)
            create_sol_btn = (
                f'<button type="button" class="btn-action" '
                f'data-command="{escaped_cmd}" onclick="copyText(this.dataset.command)" '
                f'title="{LABELS["create"]}">⚡</button>'
            )

        table_rows.append(row_template.format(
            topic=html.escape(r.topic), subject=html.escape(subject), year=html.escape(r.year),
            model=html.escape(r.model), qnum=html.escape(r.qnum), ext=html.escape(r.ext),
            used="yes" if r.is_used else "no", solved="yes" if r.has_sol else "no",
            has_tex="yes" if r.has_tex else "no", copy_disabled="" if r.has_tex else "disabled",
            fragment=html.escape(Path(r.tex_path).as_posix()), escaped_stem=escaped_stem,
            escaped_rel_path=escaped_rel_path, escaped_repo_path=escaped_repo_path,
            escaped_input=escaped_input, topic_cell_html=topic_cell_html,
            used_cell_html=used_cell_html, sol_cell_html=sol_cell_html, create_sol_btn=create_sol_btn,
            used_sort_val=used_sort_val, sol_sort_val=sol_sort_val,
        ))

    total_questions = len(records)
    has_tex_count = sum(1 for r in records if r.has_tex)
    solved_count = sum(1 for r in records if r.has_sol)
    used_count = sum(1 for r in records if r.is_used)
    unused_count = total_questions - used_count
    solved_percent = round((solved_count / total_questions) * 100) if total_questions > 0 else 0

    subject_title = AGGREGATE_TITLES.get(subject, LABELS["title"].format(subject))

    template_path = os.path.join(os.path.dirname(__file__), "questions_index_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    replacements = {
        "[[SUBJECT_TITLE]]": subject_title,
        "[[TOTAL_QUESTIONS]]": str(total_questions),
        "[[HAS_TEX_COUNT]]": str(has_tex_count),
        "[[SOLVED_COUNT]]": str(solved_count),
        "[[SOLVED_PERCENT]]": str(solved_percent),
        "[[USED_COUNT]]": str(used_count),
        "[[UNUSED_COUNT]]": str(unused_count),
        "[[TOPICS_HTML]]": topics_html,
        "[[MODELS_HTML]]": models_html,
        "[[YEARS_HTML]]": years_html,
        "[[TABLE_ROWS]]": "\n".join(table_rows),
    }
    for placeholder, val in replacements.items():
        html_content = html_content.replace(placeholder, val)

    # Embed Bootstrap last, so its content is never scanned for placeholders.
    html_content = html_content.replace("[[BOOTSTRAP_CSS]]", vendor_asset("bootstrap.rtl.min.css"))
    html_content = html_content.replace("[[BOOTSTRAP_JS]]", vendor_asset("bootstrap.bundle.min.js"))

    os.makedirs(os.path.dirname(html_output_file), exist_ok=True)
    with open(html_output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  HTML Index written to {html_output_file}")


def scan_subject_questions(questions_dir: str, usage_map: Dict[str, List[str]]) -> List[QuestionRecord]:
    """Scan a subject directory under bagrut_questions/ and return sorted QuestionRecords."""
    ext_priority = {f".{ext}": idx for idx, ext in enumerate(SUPPORTED_EXTENSIONS)}
    by_stem: Dict[Tuple[str, str], QuestionRecord] = {}

    for root, _, files in os.walk(questions_dir):
        if "out" in root.split(os.sep):
            continue

        folder_name = os.path.relpath(root, os.path.dirname(questions_dir)).replace("\\", "/")
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext not in ext_priority:
                continue

            file_path = os.path.join(root, f)
            topic, year, model, qnum, _ = parse_filename(f)
            if topic == "UNKNOWN":
                continue
            stem = os.path.splitext(f)[0]
            stem_lower = stem.lower()

            record = QuestionRecord(
                folder=folder_name,
                topic=topic,
                model=model,
                year=year,
                qnum=qnum,
                has_sol=has_solution(file_path),
                has_tex=os.path.exists(os.path.splitext(file_path)[0] + ".tex"),
                file_path=file_path,
                ext=ext,
                used_in=usage_map.get(f"{folder_name}/{stem}".lower(), []),
            )

            # If multiple media files share the same stem (e.g. .pdf and .png), keep highest priority (.pdf)
            asset_key = (folder_name.lower(), stem_lower)
            existing = by_stem.get(asset_key)
            if existing is None or ext_priority[ext] < ext_priority[existing.ext]:
                by_stem[asset_key] = record

    records = list(by_stem.values())
    # Default table order: Topic -> Year -> Model -> QuestionNum -> Used(False first)
    records.sort(
        key=lambda r: (
            r.folder,
            r.topic,
            natural_sort_key(r.year),
            natural_sort_key(r.model),
            natural_sort_key(r.qnum),
            r.is_used,
        )
    )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate CSV/HTML indexes and LaTeX topic/aggregate files for Bagrut questions."
    )
    parser.add_argument(
        "--sort",
        choices=["year", "question", "model", "exam", "random"],
        default="year",
        help="Sorting strategy for questions in generated topic.tex files (default: year)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional random seed for reproducible --sort random output.",
    )
    parser.add_argument(
        "--config",
        help="Path to YAML/JSON configuration file for custom documents.",
    )
    parser.add_argument("--build", action="store_true", help="Build generated collections with make.")
    args = parser.parse_args()

    config_docs: List[dict] = []
    if args.config:
        try:
            config_data = load_config(args.config)
            config_docs = config_data.get("documents", [])
            print(f"Loaded {len(config_docs)} document configuration(s) from {args.config}")
        except Exception as e:
            parser.error(f"Error loading config file: {e}")

    if not os.path.isdir(QUESTIONS_BASE_DIR):
        print(f"Questions directory not found: {QUESTIONS_BASE_DIR}")
        return

    subject_dirs = [
        (item, os.path.join(QUESTIONS_BASE_DIR, item))
        for item in sorted(os.listdir(QUESTIONS_BASE_DIR))
        if os.path.isdir(os.path.join(QUESTIONS_BASE_DIR, item))
    ]

    if not subject_dirs:
        print(f"No subject directories found in {QUESTIONS_BASE_DIR}/")
        return

    print(f"Found {len(subject_dirs)} subject folder(s): {', '.join(s[0] for s in subject_dirs)}\n")

    # Build usage index across src/ in a single pass
    usage_map = build_usage_map(SRC_DIR)

    for subject, questions_dir in subject_dirs:
        print(f"Processing subject: {subject}")
        print(f"Questions directory: {questions_dir}")

        records = scan_subject_questions(questions_dir, usage_map)
        src_bagrut_dir = Path(SRC_DIR, subject, "bagrut_questions")
        collections = {}
        if not records:
            sync_collections(src_bagrut_dir, collections)
            print(f"  No questions found in {questions_dir}, skipping...\n")
            continue

        # 1. Write CSV Index
        output_subject_dir = os.path.join(OUT_DIR, subject, "bagrut_questions")
        os.makedirs(output_subject_dir, exist_ok=True)
        csv_output_file = os.path.join(output_subject_dir, "questions_index.csv")
        html_output_file = os.path.join(output_subject_dir, "questions_index.html")

        with open(csv_output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Folder", "Topic", "Model", "Year", "Question Number", "Has .tex", "Has Solution", "Is Used?", "Used In"]
            )
            for r in records:
                writer.writerow(
                    [
                        r.folder,
                        r.topic,
                        r.model,
                        r.year,
                        r.qnum,
                        "YES" if r.has_tex else "NO",
                        "YES" if r.has_sol else "NO",
                        "YES" if r.is_used else "NO",
                        "; ".join(r.used_in),
                    ]
                )
        print(f"  CSV Index written to {csv_output_file}")

        # 2. Write Interactive HTML Index
        generate_html(subject, records, html_output_file)

        # 3. Group questions with .tex files by effective topic
        topic_groups: Dict[str, List[QuestionRecord]] = defaultdict(list)
        for r in records:
            if r.has_tex:
                topic_groups[r.effective_topic].append(r)

        # 4. Generate per-topic .tex files
        sorted_folder_topics: Dict[str, List[QuestionRecord]] = {}
        for topic, group in topic_groups.items():
            sorted_group = deduplicate_by_stem(sort_questions(group, args.sort, args.seed))
            sorted_folder_topics[topic] = sorted_group

            questions_list_tex = "\n".join(q.latex_input for q in sorted_group)
            topic_ar = topic_title_ar(subject, topic)
            doc_title = LABELS["title"].format(topic_ar)
            content = render_latex_document(doc_title, questions_list_tex)

            collections[f"{topic}.tex"] = content

        # 5. Aggregate document with one section per topic
        if sorted_folder_topics:
            aggregate_name = AGGREGATE_FILE_NAMES.get(subject, f"all_{subject}.tex")
            collections[aggregate_name] = build_aggregate_tex(subject, sorted_folder_topics)

        # 6. Generate custom documents from config for this subject
        subject_docs = [
            doc for doc in config_docs if doc.get("subject") == subject or not doc.get("subject")
        ]
        for doc_config in subject_docs:
            filtered_records = filter_questions(records, doc_config.get("filters", {}))
            if not filtered_records:
                print(
                    f"  Warning: No questions matched filters for custom document "
                    f"'{doc_config.get('filename', 'custom')}' in subject {subject}"
                )
                continue
            name = doc_config.get("filename", "custom_document") + ".tex"
            if Path(name).name != name or name in collections:
                parser.error(f"Invalid or duplicate collection name: {name}")
            collections[name] = build_custom_document(subject, doc_config, filtered_records)

        sync_collections(src_bagrut_dir, collections)
        if args.build and collections:
            targets = [Path(output_subject_dir, name[:-4] + suffix).as_posix()
                       for name in collections for suffix in (".pdf", "_sols.pdf")]
            mark_stale_collections(src_bagrut_dir, collections, Path(output_subject_dir))
            subprocess.run(["make", *targets], check=True)

        print(f"[OK] Completed processing for subject: {subject}\n")


if __name__ == "__main__":
    main()
