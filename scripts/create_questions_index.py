import os
import csv
import glob

# -------------------------------
# CONFIGURATION
# -------------------------------
QUESTIONS_DIR = "bagrut_questions"
SRC_DIR = "src"
CSV_OUTPUT_FILE = os.path.join(QUESTIONS_DIR, "questions_index.csv")
HTML_OUTPUT_FILE = os.path.join(QUESTIONS_DIR, "questions_index.html")
# -------------------------------

def parse_filename(filename):
    """
    Parse filename like: <topic_name>_<year>_<model>_<question_number>.pdf
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.split("_")
    if len(parts) < 4:
        return ("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")

    topic = "_".join(parts[:-3])
    year = parts[-3]
    model = parts[-2]
    qnum = parts[-1]
    return topic, year, model, qnum


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

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>فهرس أسئلة البجروت</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .container-fluid {{ max-width: 98%; margin-top: 20px; }}

            /* Table Styling */
            .table-responsive {{ border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            .table thead {{ background-color: #34495e; color: white; position: sticky; top: 0; z-index: 100; }}
            .table tbody tr:hover {{ background-color: #f1f1f1; }}

            /* Badges */
            .status-yes {{ background-color: #d1e7dd; color: #0f5132; font-weight: bold; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; }}
            .status-no {{ background-color: #f8d7da; color: #842029; font-weight: bold; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; }}

            /* Filter Section */
            .filter-section {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            .filter-label {{ font-weight: 700; margin-bottom: 5px; color: #495057; font-size: 0.9em; }}

            /* Custom Dropdown for Checkboxes */
            .dropdown-menu-custom {{
                max-height: 300px;
                overflow-y: auto;
                width: 100%;
                padding: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.15);
            }}
            .form-check {{ margin-bottom: 5px; cursor: pointer; }}
            .form-check:hover {{ background-color: #f8f9fa; }}
            .form-check-label {{ cursor: pointer; user-select: none; }}

            /* Image Modal */
            #imgModal .modal-body {{ text-align: center; background: #222; padding: 0; }}
            #imgModal img {{ max-width: 100%; max-height: 90vh; border: none; }}
            .btn-preview {{ color: #0d6efd; cursor: pointer; border: none; background: none; font-weight: 600; font-size: 0.9rem; }}
            .btn-preview:hover {{ text-decoration: underline; color: #0a58ca; }}
        </style>
    </head>
    <body>

    <div class="container-fluid">
        <h3 class="mb-4 text-center fw-bold text-dark">📚 بنك أسئلة البجروت</h3>

        <!-- Summary Statistics -->
        <div class="row mb-4">
            <div class="col-md-12">
                <div class="card bg-light">
                    <div class="card-body text-center">
                        <h5 class="card-title">إحصائيات عامة</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="fw-bold text-primary">إجمالي الأسئلة</div>
                                <div class="h4">{total_questions}</div>
                            </div>
                            <div class="col-md-3">
                                <div class="fw-bold text-success">محلولة</div>
                                <div class="h4">{solved_count}</div>
                            </div>
                            <div class="col-md-3">
                                <div class="fw-bold text-info">مستخدمة</div>
                                <div class="h4">{used_count}</div>
                            </div>
                            <div class="col-md-3">
                                <div class="fw-bold text-warning">غير مستخدمة</div>
                                <div class="h4">{unused_count}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="filter-section">

            <div class="row mb-3">
                <div class="col-md-12">
                    <input type="text" id="searchInput" class="form-control form-control-lg" placeholder="🔍 بحث حر في اسم الملف، الرقم، أو أي نص...">
                </div>
            </div>

            <div class="row g-2">

                <div class="col-md-2">
                     <div class="filter-label">📂 المجلد</div>
                     <div class="dropdown">
                        <button class="btn btn-outline-secondary dropdown-toggle w-100 text-end text-truncate" type="button" id="folderBtn" data-bs-toggle="dropdown" aria-expanded="false">
                            كل المجلدات
                        </button>
                        <ul class="dropdown-menu dropdown-menu-custom" aria-labelledby="folderBtn">
                            <li><button class="btn btn-sm btn-link text-decoration-none w-100 text-end" onclick="clearChecks('folder-checkbox')">❌ إلغاء الكل</button></li>
                            <li><hr class="dropdown-divider"></li>
                            {folders_html}
                        </ul>
                     </div>
                </div>

                <div class="col-md-3">
                     <div class="filter-label">📖 الموضوع</div>
                     <div class="dropdown">
                        <button class="btn btn-outline-secondary dropdown-toggle w-100 text-end text-truncate" type="button" id="topicBtn" data-bs-toggle="dropdown" aria-expanded="false">
                            كل المواضيع
                        </button>
                        <ul class="dropdown-menu dropdown-menu-custom" aria-labelledby="topicBtn">
                            <li><button class="btn btn-sm btn-link text-decoration-none w-100 text-end" onclick="clearChecks('topic-checkbox')">❌ إلغاء الكل</button></li>
                            <li><hr class="dropdown-divider"></li>
                            {topics_html}
                        </ul>
                     </div>
                </div>

                <div class="col-md-2">
                     <div class="filter-label">📅 السنة</div>
                     <div class="dropdown">
                        <button class="btn btn-outline-secondary dropdown-toggle w-100 text-end text-truncate" type="button" id="yearBtn" data-bs-toggle="dropdown" aria-expanded="false">
                            كل السنوات
                        </button>
                        <ul class="dropdown-menu dropdown-menu-custom" aria-labelledby="yearBtn">
                            <li><button class="btn btn-sm btn-link text-decoration-none w-100 text-end" onclick="clearChecks('year-checkbox')">❌ إلغاء الكل</button></li>
                            <li><hr class="dropdown-divider"></li>
                            {years_html}
                        </ul>
                     </div>
                </div>

                <div class="col-md-2">
                     <div class="filter-label">🔢 النموذج</div>
                     <div class="dropdown">
                        <button class="btn btn-outline-secondary dropdown-toggle w-100 text-end text-truncate" type="button" id="modelBtn" data-bs-toggle="dropdown" aria-expanded="false">
                            كل النماذج
                        </button>
                        <ul class="dropdown-menu dropdown-menu-custom" aria-labelledby="modelBtn">
                            <li><button class="btn btn-sm btn-link text-decoration-none w-100 text-end" onclick="clearChecks('model-checkbox')">❌ إلغاء الكل</button></li>
                            <li><hr class="dropdown-divider"></li>
                            {models_html}
                        </ul>
                     </div>
                </div>

                <div class="col-md-3">
                     <div class="filter-label">✅ حالة الاستخدام</div>
                     <select id="usedFilter" class="form-select">
                        <option value="">الكل (مستخدم وغير مستخدم)</option>
                        <option value="نعم">نعم (تم استخدامه)</option>
                        <option value="لا">لا (لم يتم استخدامه)</option>
                     </select>
                </div>
            </div>
        </div>

        <div class="table-responsive bg-white" style="max-height: 70vh; overflow-y: auto;">
            <table class="table table-bordered mb-0 align-middle" id="questionsTable">
                <thead>
                    <tr>
                        <th style="width: 15%">المجلد</th>
                        <th style="width: 25%">الموضوع</th>
                        <th style="width: 10%">السنة</th>
                        <th style="width: 10%">النموذج</th>
                        <th style="width: 10%">السؤال</th>
                        <th style="width: 10%">مستخدم</th>
                        <th style="width: 10%">الحل</th>
                        <th style="width: 10%">معاينة</th>
                    </tr>
                </thead>
                <tbody>
    """

    for row in rows:
        folder, topic, model, year, qnum, has_sol, is_used_val, file_path, f_type = row

        try:
            rel_path = os.path.relpath(file_path, QUESTIONS_DIR)
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

        html_content += f"""
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

    html_content += """
                </tbody>
            </table>
        </div>
        <div class="d-flex justify-content-between mt-2 px-2">
             <div class="text-muted small">تم إنشاء الفهرس تلقائياً</div>
             <div class="text-primary fw-bold">النتائج: <span id="rowCount">0</span> سؤال</div>
        </div>
    </div>

    <div class="modal fade" id="imgModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header py-2">
            <h6 class="modal-title" id="imgModalLabel">معاينة</h6>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img id="modalImage" src="" alt="Preview">
          </div>
        </div>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // DOM Elements
        const searchInput = document.getElementById('searchInput');
        const usedFilter = document.getElementById('usedFilter');

        const table = document.getElementById('questionsTable');
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        const rowCountDisplay = document.getElementById('rowCount');

        function getCheckedValues(className) {
            const checkboxes = document.querySelectorAll('.' + className + ':checked');
            return Array.from(checkboxes).map(cb => cb.value);
        }

        function updateButtonText(btnId, checkedCount, defaultText) {
            const btn = document.getElementById(btnId);
            if (checkedCount === 0) {
                btn.innerText = defaultText;
                btn.classList.remove('btn-secondary');
                btn.classList.add('btn-outline-secondary');
            } else {
                btn.innerText = checkedCount + " محدد";
                btn.classList.remove('btn-outline-secondary');
                btn.classList.add('btn-secondary');
            }
        }

        function filterTable() {
            const searchText = searchInput.value.toLowerCase();
            const selectedUsed = usedFilter.value;

            const checkedFolders = getCheckedValues('folder-checkbox');
            const checkedTopics = getCheckedValues('topic-checkbox');
            const checkedModels = getCheckedValues('model-checkbox');
            const checkedYears = getCheckedValues('year-checkbox');

            updateButtonText('folderBtn', checkedFolders.length, 'كل المجلدات');
            updateButtonText('topicBtn', checkedTopics.length, 'كل المواضيع');
            updateButtonText('modelBtn', checkedModels.length, 'كل النماذج');
            updateButtonText('yearBtn', checkedYears.length, 'كل السنوات');

            let visibleCount = 0;

            for (let i = 0; i < rows.length; i++) {
                let row = rows[i];
                let text = row.innerText.toLowerCase();

                let dFolder = row.getAttribute('data-folder');
                let dTopic = row.getAttribute('data-topic');
                let dModel = row.getAttribute('data-model');
                let dYear = row.getAttribute('data-year');
                let dUsed = row.getAttribute('data-used');

                let matchFolder = (checkedFolders.length === 0) || checkedFolders.includes(dFolder);
                let matchTopic = (checkedTopics.length === 0) || checkedTopics.includes(dTopic);
                let matchModel = (checkedModels.length === 0) || checkedModels.includes(dModel);
                let matchYear = (checkedYears.length === 0) || checkedYears.includes(dYear);

                let matchUsed = (selectedUsed === "") || (dUsed === selectedUsed);
                let matchSearch = text.includes(searchText);

                if (matchSearch && matchUsed && matchFolder && matchTopic && matchModel && matchYear) {
                    row.style.display = "";
                    visibleCount++;
                } else {
                    row.style.display = "none";
                }
            }
            rowCountDisplay.innerText = visibleCount;
        }

        function clearChecks(className) {
            document.querySelectorAll('.' + className).forEach(cb => cb.checked = false);
            filterTable();
        }

        searchInput.addEventListener('keyup', filterTable);
        usedFilter.addEventListener('change', filterTable);

        document.querySelectorAll('.form-check-input').forEach(cb => {
            cb.addEventListener('change', filterTable);
        });

        rowCountDisplay.innerText = rows.length;

        function showImage(src, title) {
            document.getElementById('modalImage').src = src;
            document.getElementById('imgModalLabel').innerText = title;
            var myModal = new bootstrap.Modal(document.getElementById('imgModal'));
            myModal.show();
        }
    </script>
    </body>
    </html>
    """

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

                topic, year, model, qnum = parse_filename(f)

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


if __name__ == "__main__":
    main()
