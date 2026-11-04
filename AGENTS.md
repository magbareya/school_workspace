# Authoring & Teaching Style Guide (AGENTS.md)

This document defines the authoring conventions, pedagogical style, LaTeX architecture, build system, and coding standards used across all course materials in this repository.

**Any AI assistant or contributor generating or editing worksheets, booklets, homeworks, lesson notes, summaries, Bagrut solutions, or exams in this workspace MUST follow the rules in this document.** When a rule here conflicts with an older file in the repository, this document wins.

---

## 0. Quick Checklist (Read First)

Before finishing any task, verify that every item below holds. Each item links to its detailed section.

1. **Compile with `make`, never with `xelatex` directly**, and confirm the PDF builds without errors ([Section 2.2](#22-build--mandatory-compilation-check)).
2. **Terminology:** use the mandatory Arabic terms (`عملية` not `دالة`, `نمط` not `نوع`, `حد` not `عنصر`, `مؤشر`, `مسح`, `تعريف`, ...) and keep code identifiers in `\textenglish{...}` ([Section 3](#3-strict-pedagogical-terminology-arabic--cs-concepts)).
3. **Math mode `$...$` for numbers, single-letter variables & operators; never `\textenglish` inside `$...$`:** wrap inline numbers (`$0$`, `$10$`, `$-5$`), single-letter variables/labels (`$x$`, `$a$`, `$A$`), and operators in `$...$`, **never** in `\textenglish{...}`. Inside math mode `$...$`, **never** use `\textenglish` — use `\text{...}` for multi-letter identifiers ([Section 3.1](#31-language-policy-technical-concepts-vs-code-identifiers)).
4. **No Arabic in code (strictly forbidden without any exception)** — never write any Arabic text anywhere inside code (`minted` blocks, `.cs` files, `.py` files, etc.), neither in print/console commands (`Console.WriteLine`, `print`) nor in comments ([Sections 2.1](#21-engine-fonts--document-skeleton) and [7](#7-solution--code-standards)).
5. **Boxes never split across pages** — keep every `tcolorbox` short; split long solutions into several boxes ([Section 4.1](#41-critical-rule-tcolorbox-environments-do-not-split-across-pages)).
6. **Pagination:** `\filbreak` after every `\item` (outside any `\fi`), `\clearpage` before every `\section*` ([Section 8](#8-pagination--spacing-rules)).
7. **Use `longtable` for tables with long text, code cells, or many rows**, and put class descriptions in the standard two-column `longtable`; adding a single method is plain text ([Section 5.7](#57-standard-latex-table-patterns)).
8. **Solutions** go in `\ifwithsols \begin{boxSolution} ... \end{boxSolution} \fi`, or — for OOP booklets — in standalone `.cs` files ([Sections 5.2](#52-progressive-multi-stage-oop-booklets--standalone-c-solutions) and [7](#7-solution--code-standards)).
9. **Every C# `if`/`else`/`for`/`while` has braces**, and fields are accessed with `this.` ([Section 7](#7-solution--code-standards)).
10. **Never put worksheet/exercise solutions as examples in lesson notes or summaries** — all examples in summaries/lesson notes must be different from the questions in the practice worksheets ([Section 5.4](#54-lesson-notes--student-summaries)).

---

## 1. Overview, Context & Repository Layout

- **Course:** High School Computer Science (Grades 10–12, Israeli Bagrut matriculation curriculum — 899371 / 899222 / 899205).
- **Core Subjects & Languages:**
  - **C# Fundamentals (`src/basics/`, `history_src/2025_26/basics/`):** Variables, I/O, math/division/modulo, conditionals (`if`/`else`), loops (`while`, `for`, nested loops), helper methods, strings, 1D/2D arrays, and introduction to classes.
  - **C# Object-Oriented Programming (`src/oop/`):** Encapsulation (`Get`/`Set`), constructors (default, parameterized, copy), composition & defensive copying, arrays of objects, inheritance (`: base(...)`, `protected`), polymorphism (upcasting, `virtual`/`override`, downcasting with `is`/`as`, `Object.Equals`), abstract classes (`abstract`), and interfaces (`IComparable`).
  - **Python (`src/python/pythonA/`):** Variables, I/O, conditionals, `for`/`while` loops, strings (indexing & slicing), and lists.
  - **Computational Models & Automata (`history_src/2025_26/computational_models/`):** Formal languages, regular operations, DFA, NFA, product automaton, closure properties, PDA, and Turing Machines.
- **Language of Instruction:** Formal, clear Arabic for explanations and requirements, combined seamlessly with English (`\textenglish{...}`) for code tokens, keywords, identifiers, and console I/O.
- **School & Instructor Identity:** The page headers are already set by the preamble — do NOT redefine them in individual files:
  - Header Right: `\fancyhead[R]{الأستاذ محمود اغبارية}`
  - Header Left: `\fancyhead[L]{مدرسة التسامح الشاملة}`
- **Standard Document Closing** (end every student-facing document with it):

  ```latex
  \vspace{1cm}
  \begin{flushleft}
  أرجو لكم وقتًا ممتعًا.

  الأستاذ محمود اغبارية.
  \end{flushleft}
  ```

### 1.1. Repository Directory Structure
- [`src/`](file:///c:/dev/workspace/school_workspace/src): Current active teaching materials (`basics/`, `oop/`, `python/pythonA/`). Inside each subject: `exs/` (worksheets, booklets, homework), `lessonNotes/` (lesson notes and summaries), `exams/`, and `topicPlans/` (teacher-facing guides).
- [`history_src/2025_26/`](file:///c:/dev/workspace/school_workspace/history_src/2025_26): Full archive of previous year materials (`basics/`, `computational_models/`). *Authoring conventions evolved over that year; when an archive file contradicts this document, follow this document.*
- [`bagrut_questions/`](file:///c:/dev/workspace/school_workspace/bagrut_questions): Cropped Bagrut exam question images (`.png`/`.pdf`) and their modular `.tex` solution fragments.
- [`scripts/`](file:///c:/dev/workspace/school_workspace/scripts): Shared LaTeX preambles ([`tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex), [`beamer_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/beamer_preamble.tex)) and Python automation utilities (`scripts/bagrut_questions/`).
- `out/`: Compiled PDFs mirroring the `src/` directory structure (generated by the [`Makefile`](file:///c:/dev/workspace/school_workspace/Makefile)). Never edit files in `out/` by hand.

---

## 2. LaTeX Technical Architecture & Build System

### 2.1. Engine, Fonts & Document Skeleton
- **Engine:** `XeLaTeX` with `-shell-escape` (required for `minted` v3) and `polyglossia`.
  - Main language: Arabic (`\setmainlanguage[numerals=western]{arabic}`); second language: English (`\setotherlanguage{english}`).
  - Fonts: `Calibri` (Arabic), `Courier New` (monospace/code), `Segoe UI Emoji` (`\emoji` for box icons).
- **CRITICAL Rule — Arabic in Code is Strictly Forbidden (Without Any Exception):** It is **totally forbidden** to write any Arabic text anywhere inside code (`\begin{minted}{csharp}`, `\begin{minted}{python}`, standalone `.cs` / `.py` files, etc.) — **neither in print/output commands (`Console.WriteLine`, `Console.Write`, `print`, `input`) nor in comments (`//`, `/* ... */`, `#`) nor in string literals**. Apart from the Latin monospace font lacking Arabic glyphs in `minted` (rendering them as blank spaces), all code, console messages, string literals, and comments MUST be 100% in English without any exception. Even if a question in Arabic asks to print a message (e.g., "اطبع أنّ العدد زوجي"), the code MUST print it in English (`Console.WriteLine("Even");`).
- **Document Skeleton:**
  ```latex
  \documentclass[14pt]{extarticle}
  \input{../../../scripts/tex_preamble.tex}  % adjust ../ depth to the file's location

  \title{...}

  \begin{document}
  \maketitle
  ...
  \end{document}
  ```

### 2.2. Build & Mandatory Compilation Check
- **Every `.tex` file you create or modify MUST be compiled to PDF and the build must succeed without errors.**
- **Always compile with `make` — NEVER run `xelatex` manually.** The [`Makefile`](file:///c:/dev/workspace/school_workspace/Makefile) sets `TEXMF_OUTPUT_DIRECTORY`, runs two passes, and passes the conditional flags (Section 2.3).
- **Targets** (path under `out/` mirrors the path under `src/`):

  | Command | Output | Flags |
  | :--- | :--- | :--- |
  | `make out/<path>/<name>.pdf` | Regular PDF | `detailed=true`, `withsols=false` |
  | `make out/<path>/<name>_printable.pdf` | Compact student handout | `detailed=false`, `withsols=false` |
  | `make out/<path>/<name>_sols.pdf` | Solutions | `detailed=true`, `withsols=true` |
  | `make out/<path>/<name>_wb.pdf` | Black-and-white landscape | `whiteblack=true` |
  | `make out/<path>/<name>_wb_sols.pdf` | Black-and-white landscape + solutions | `whiteblack=true`, `withsols=true` |

  Example: `make out/oop/exs/ex02-Company.pdf`, then `make sclean` to remove temporary files. Bulk targets: `make tex`, `make pdf`, `make printable`, `make sols`, `make wb`, `make wbsols`, `make all`.
- **If a file contains `\ifwithsols` or `\ifdetailed` blocks, also build the `_sols` / `_printable` variant** to make sure both branches compile.
- **A build that hangs is a LaTeX error:** `xelatex` is not run in non-stop mode, so on an error it waits for input. Stop it and read the end of `out/<path>/<name>.log` (look for lines starting with `!`).

### 2.3. Conditional Compilation Flags
- `\ifdetailed` — sample console runs (`boxExample`) and visual hints. `true` in regular builds, `false` in `_printable` handouts (keeps them short and paper-efficient).
- `\ifwithsols` — reference solution boxes (`boxSolution`). `true` only in `_sols` builds.
- `\ifwhiteblack` — black-and-white A4 landscape presentation mode (`\LARGE` font, `bw` minted style, black borders). Use `\ifwhiteblack \clearpage \fi` (right after an item's `\filbreak`) only when an exercise must get its own landscape page (see Section 8).

### 2.4. Helper Macros & Global Defaults (in [`tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex))
- `\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}` — centered fixed-width table column (`|C{2.5cm}|`).
- `\importpdfpage{filepath}{pagenum}` — imports a full-page PDF graphic.
- `\insertFullImg{filepath}` — centers an image at `0.9\paperwidth`.
- `\begin{pycell} ... \end{pycell}` — frameless, full-width cell for putting `minted` code inside an RTL table cell (see Section 5.7).
- **Global `minted` look:** `\setminted{fontsize=\small, breaklines=true}` (not applied in `\ifwhiteblack` mode, which uses `\LARGE`).
- **Compact `boxCode`:** the `simplecode` style is extended with `fontupper=\setstretch{0.95}, top=4pt, bottom=4pt, before skip=6pt, after skip=6pt`, so code boxes stay compact despite the global `onehalfspacing`.
- **Do NOT redefine any of the above** (`pycell`, `\setminted`, `\tcbset{simplecode...}`) in individual `.tex` files. Add a per-file override only when a specific document genuinely needs a different value.
- **List Spacing (`itemsep`):**
  - When the questions in a section/list are **short** (1–2 lines each), use `\begin{enumerate}[itemsep=1em]` (or `[resume, itemsep=1em]`).
  - When the questions are **longer** (multi-line descriptions, sub-questions, or examples), use `\begin{enumerate}[itemsep=2em]` (or `[itemsep=2.2em]` in multi-stage booklets).
  - To continue numbering across sections, use `\begin{enumerate}[resume, ...]`.

---

## 3. Strict Pedagogical Terminology (Arabic ↔ CS Concepts)

In high school CS and Bagrut exams, verb and noun choices convey exact technical specifications. **Never interchange these terms:**

| Arabic Term | Exact Technical Meaning | Code Equivalent |
| :--- | :--- | :--- |
| **تستقبل** | Reads input from the user via keyboard/console | `Console.ReadLine()` / `input()` |
| **تتلقى** | Receives values as method/function parameters | `public static void Foo(int x)` |
| **تطبع** | Outputs text/data directly to the console | `Console.WriteLine(...)` / `print(...)` |
| **تعيد** | Returns a value to the caller | `return value;` |
| **برنامج** | A full runnable program | Code executed inside `Main()` |
| **مقطع برنامج** | A focused code snippet | Logic lines without class/method boilerplate |
| **عملية خارجية** / **عملية** | Method / function (static or instance) | `public static ...` / `public ...` |
| **عملية داخلية** | Instance method belonging to a class | `public double GetSalary()` |
| **عملية مساعدة** | Private helper method (`private`) | `private int Clamp(int val)` |
| **فئة** | Class | `class ...` |
| **كائن** | Object / instance | `new ClassName(...)` |
| **عملية بنائية** | Constructor | `public Point(...)` |
| **صفات** | Fields / attributes of a class | `private double x;` |
| **مُعطى / معطيات** | Parameter(s) passed to a method | `(int amount, ScoutShip target)` |
| **جدول متابعة** | Tracing / dry-run table | Table tracking variables, conditions, outputs |

### 3.1. Language Policy: Technical Concepts vs. Code Identifiers
- **Technical Concepts (المصطلحات التقنية):** If an established Arabic term exists (e.g. `الوراثة` for Inheritance, `تعدد الأشكال` for Polymorphism, `مخطط الهرمية` for Hierarchy, `البرمجة كائنية التوجه` for OOP, `العمليات البنائية` for Constructors, `التحميل الزائد` for Overloading, `التحويل لأعلى` for Upcasting, `التحويل لأسفل` for Downcasting, `إعادة تعريف العمليات` for Overriding, `الفئة المجردة` for Abstract Class, `الواجهة` for Interface), **write the Arabic term only**. Do NOT append English translations in parentheses (avoid: `الوراثة (Inheritance)`, `البرمجة كائنية التوجه (OOP)`).
- **Code Identifiers, Keywords & Console Strings (أسماء الفئات والعمليات والمتغيرات والكلمات المحجوزة):** Keep multi-letter English identifiers, keywords, and strings wrapped in `\textenglish{...}` in questions, headings, tables, and prompts (e.g. `\textenglish{Employee}`, `\textenglish{ToString}`, `\textenglish{GetScore}`, `\textenglish{AddEmployee}`, `\textenglish{Get}` / `\textenglish{Set}`, `\textenglish{MAX}`, `\textenglish{virtual}`, `\textenglish{override}`, `\textenglish{protected}`, `\textenglish{base}`, `\textenglish{is}`, `\textenglish{as}`). This makes students implement the exact, unified identifiers. Escape underscores and `#` in text mode (`\textenglish{student\_name}`, `\textenglish{C\#}`).
- **Inline Numbers, Single-Letter Variables & Math Expressions Wrapped in `$` (كتابة الأرقام والمتغيرات أحادية الحرف داخل `$`):**
  - Every time a number appears inline with text (in questions, requirements, explanations, headings, grade allocations, constraints, ranges, loops, or indices), **wrap it in math mode with `$` (e.g. `$0$`, `$1$`, `$10$`, `$100$`, `$-5$`, `$3.14$`), and NEVER with `\textenglish{...}`**.
  - **Do NOT use `\textenglish{...}` when `$...$` can be used instead** — such as for single-letter variable names (`$a$`, `$b$`, `$c$`, `$i$`, `$k$`, `$n$`, `$x$`, `$y$`), single-letter option labels (`$A$`, `$B$`, `$C$`, `$D$`), arithmetic/comparison operators (`$+$`, `$-$`, `$/$`, `$//$`, `$\%$`, `$>$`, `$<$`), or simple mathematical assignments (`$a = 10$`, `$i = 0$`).
  - **NEVER use `\textenglish{...}` inside math mode `$...$`** (this is invalid in LaTeX). Whenever a multi-letter identifier must appear inside `$...$`, use `\text{...}` (e.g. `$\text{num1} = 9$`, `$\text{num1} \geq \text{num2}$`).

### 3.2. Mandatory Word Choices (تفضيلات المصطلحات الإلزامية)
1. **استخدام "تعريف" بدلاً من "ترويسة":** عند الإشارة إلى توقيع أو رأس الفئة أو العملية البرمجية (Header / Signature / Definition)، استخدم دائمًا مصطلح **"تعريف"** (مثل: `تعريف الفئة`، `تعريف العملية`) وتجنّب استخدام كلمة "ترويسة".
2. **استخدام "عملية" بدلاً من "دالة":** في جميع الأسئلة والملاحظات والحلول، اعتمد دائمًا مصطلح **"عملية"** (أو `عملية خارجية`، `عملية بنائية`، `عملية بنائية ناسخة`، `عملية بنائية افتراضية`، `عملية مساعدة`، `عمليات`) وتجنّب استخدام لفظ "دالة" أو "دوال".
3. **استخدام "نمط" بدلاً من "نوع" (Type):** عند الإشارة إلى نمط المعطيات أو الكائنات (`int`، `string`، `Employee`، `object`)، استخدم **"نمط"** (`من نمط`، `نمط الإرجاع`، `النمط الساكن`، `النمط الفعلي`، `فحص النمط`).
4. **استخدام "مؤشر" بدلاً من "مرجع" أو "فهرس" (Reference / Pointer & Index):** استخدم **"مؤشر"** (وجمعه `مؤشرات`) للإشارة إلى عنوان الكائن في الذاكرة (Reference) وكذلك للإشارة إلى رقم المكان في المصفوفة (Index).
5. **استخدام "حد / حدود" بدلاً من "عنصر / عناصر" (Array Element):** عند الحديث عن عناصر المصفوفة، استخدم **"حد"** و**"حدود المصفوفة"** (`الحدود الفارغة`، `الحدود المطابقة`).
6. **استخدام "مسح" بدلاً من "مرور" (Scan):** عند المرور على حدود مصفوفة أو مبنى معطيات، استخدم **"مسح المصفوفة"** (`نمسح المصفوفة`، `تمسح العملية`).
7. **استخدام "عامل" بدلاً من "معامل" (Operator):** مثل `العامل is`، `العامل as`، `العوامل المنطقية`.
8. **استخدام "أذونات الوصول" بدلاً من "الصلاحية" (Access Modifiers):** مثل `أذونات الوصول protected`، `بإذن وصول private`.
9. **استخدام "تطبيق" (Implementation):** عند الحديث عن كتابة كود الفئة أو العملية أو الواجهة (`تطبيق الفئة`، `تطبيق العملية`، `تطبّق الواجهة`).

### 3.3. Trilingual Terminology Glossary (عربي – עברית – English)

المصطلحات المعتمدة ثلاثية اللغة (عربية / عبرية / إنجليزية) كما ترد في ورقة المصطلحات الرسمية. عند صياغة الأسئلة والملاحظات والحلول استخدم هذه المصطلحات حصرًا:

| المصطلح بالعربية | המונח בעברית | Term in English |
| :--- | :--- | :--- |
| مصفوفة | מערך | Array |
| فئة | מחלקה | class |
| عملية | פעולה | function/method |
| كائن / كائنات | עצם\עצמים | Object/s |
| صفات | תכונות | property/attribute |
| عملية بنائية | פעולה בונה | constructor |
| عملية بنائية ناسخة | — | Copy constructor |
| عملية بنائية افتراضية | — | Default constructor |
| نمط | טיפוס | type |
| مباني معطيات | מבני נתונים | data structure |
| دور | תור | Queue |
| راصة | מחסנית | Stack |
| شجرة بينارية | עץ בינארי | Binary Tree |
| عقدة | חוליה | Node |
| سلسلة عُقَد | שרשרת חוליות | Node list |
| قائمة مترابطة | רשימה מקושרת | Node list |
| حد | איבר | element |
| ليست فارغة | לא ריקה | not empty |
| عملية تراجعية | פעולה רקורסיבית | recursive operation |
| حل تراجعي | פתרון רקורסיבי | recursive solution |
| حلقة | לולאה | loop |
| مسح | סריקה | scan |
| ادعاء الدخول | טענת כניסה | Precondition |
| ادعاء الخروج | טענת יציאה | Postcondition |
| عامل | אופרטור | operator |
| تعبير منطقي | ביטוי לוגי | logical expression |
| تعبير بولياني | ביטוי בוליאני | boolean expression |
| مؤشر | אינדקס | Index |
| مؤشر | הפניה | Reference / Pointer |
| ظهور | מופע | Instance |
| هدف العملية | מטרת הפעולה | Function Purpose |
| تعقيدات زمن التشغيل | סיבוכיות זמן ריצה | Complexity |
| عقدة في الشجرة | צומת בעץ | Node (Vertex) |
| جذر | שורש | Root |
| تفرعات في الشجرة | הסתעפות בעץ | Branch |
| ورقة | עלה | Leaf |
| مستوى | רמה | Level |
| مسار | מסלול | Path |
| شجرة فرعية | תת עץ | Sub-Tree |
| ابن أيسر | בן שמאלי | Left-Child |
| ابن أيمن | בן ימני | Right-Child |
| المسح الأولي | סריקה תחילית | Pre-Order |
| المسح الداخلي | סריקה תוכית | In-Order |
| المسح النهائي | סריקה סופית | Post-Order |
| المسح العرضي | חיפוש לרוחב | BFS: Breadth-First-Search |
| المسح للعمق | חיפוש לעומק | DFS: Depth-First-Search |
| أذونات الوصول | הרשאות הגישה | — |
| تطبيق | מימוש | Implementation |

**ملاحظات:**
- الخلايا المعلّمة بـ (—) فارغة في ورقة المصطلحات الرسمية.
- المصطلحان "مؤشر" و"ابن أيسر" مكتوبان في الورقة الرسمية بصيغة ناقصة ("مؤش"، "أيس")؛ الصيغة المعتمدة هنا هي الصيغة الكاملة.

---

## 4. Semantic Callout Boxes (`tcolorbox`)

All callout boxes are defined in [`tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex) with colored borders and emoji icons. The optional argument is appended to the title; pass a leading dash for a subtitle (`\begin{boxNote}[- عنوان فرعي]`).

| Environment | Title / Icon | Primary Pedagogical Use |
| :--- | :--- | :--- |
| `\begin{boxDef}[#]` | `📘 تعريف # :` | Formal concept definitions or project story/domain framing (`[قصة السلسلة: ...]`). |
| `\begin{boxExercise}[#]` | `🧩 تمرين # :` | Standalone exercise blocks inside lesson notes. |
| `\begin{boxExample}[#]` | `📝 مثال # :` | Sample console input/output runs and illustrative scenarios (wrapped in `\ifdetailed`). |
| `\begin{boxNote}[#]` | `✨ ملاحظة # :` | Helpful hints, type selection reminders, or rules tables. |
| `\begin{boxAttention}[#]` | `🔔 تنبيه # :` | Important pedagogical reflections (`[- نقطة للتفكير]`), pre-submission checklists, or key distinctions. |
| `\begin{boxWarning}[#]` | `⚡ ملاحظة هامة # :` | Common pitfalls (e.g. integer division truncation) or mandatory workflow instructions (testing in `Main`). |
| `\begin{boxSolution}[#]` | `✅ حل # :` | Reference solutions wrapped inside `\ifwithsols ... \fi`. Labels like `[1]`, `[بديل]`, `[فرع أ]`. |
| `\begin{boxSymbol}[#]` | `🔣 رمز # :` | Mathematical or formal notation (Automata / Computational Models). |
| `\begin{boxHint}[#]` | `💡 تلميح # :` | Guided hints for challenging problems. |
| `\begin{boxCode}` | *(No title bar)* | Compact gray box for method signatures, localized code snippets, or exam cover instructions. |

### 4.1. Critical Rule: `tcolorbox` Environments Do NOT Split Across Pages
None of the boxes above can break across pages. A box taller than the remaining space jumps to the next page (leaving a large gap), and a box taller than a whole page overflows the bottom margin and is **clipped in print**.
- **Keep code boxes short and localized:** In summaries and lesson notes, avoid full-program listings in one `boxCode`. Write focused 8–15 line snippets showing the exact concept, plus 2–3 lines of `// Usage in Main:`.
- **Split long solutions** into several consecutive `boxSolution`s (see Section 7).
- **Keep tables inside boxes short** — a table row cannot break either.

---

## 5. Document Types, Templates & Subject Conventions

### 5.1. Standard Worksheets & Practice Sheets (`exs/exXX-*.tex`)
- **Location:** `src/<subject>/exs/exXX-<TopicName>.tex`
- **Title Scheme** (adjust the sheet number, grade, and topic):
  ```latex
  \ifwithsols
  \title{حل ورقة تمرن X للصف العاشر $10$ - [الموضوع]}
  \else
  \title{ورقة تمرن X للصف العاشر $10$ - [الموضوع]}
  \fi
  ```
- **Reference Examples:**
  - C# Basics: [src/basics/exs/ex05-ifStatement.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/ex05-ifStatement.tex)
  - C# OOP Single Class: [src/oop/exs/ex01-PointClass.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex01-PointClass.tex)
  - C# Arrays & Classes Archive: [history_src/2025_26/basics/exs/ex10D-classes2-classesWithArrays.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exs/ex10D-classes2-classesWithArrays.tex)

### 5.2. Progressive Multi-Stage OOP Booklets & Standalone C# Solutions
Progressive booklets (`كراس تمارين متدرج`) in `src/oop/exs/` teach object-oriented design, inheritance, polymorphism, abstract classes, and interfaces step by step through one domain story.

- **Files:** Each booklet exists as one full file (`exXX-<Name>.tex`) and as one file per stage (`exXX-<Name>_part1.tex`, `_part2.tex`, ...). Each stage's reference solution is in its own folder `exXX-<Name>_sol/partN/` (or `exXX_<name>_sol/partN/`).
- **Reference Examples:**
  - Employees & Company (5 stages): [ex02-Company.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex02-Company.tex), parts `ex02-Company_part1..5.tex`, solutions in [`ex02-Company_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex02-Company_sol)
  - Galactic Fleet (4 stages): [ex03-galacticFleet.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex03-galacticFleet.tex), solutions in [`ex03_galactic_fleet_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex03_galactic_fleet_sol)
  - Dragon Riders Academy (4 stages): [ex04-dragonRiders.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex04-dragonRiders.tex), solutions in [`ex04_dragon_riders_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex04_dragon_riders_sol)
- **Required Architectural Pattern:**
  1. **Header Boxes:** Open with `\begin{boxDef}[قصة السلسلة: ...]` introducing the narrative, followed by `\begin{boxWarning}` instructing students to update and run `Main` in every exercise.
  2. **Continuous Exercise Numbering:** `\begin{enumerate}[label=\textbf{تمرين \arabic*:}, wide=0pt, itemsep=2.2em]`, continued in later stages with `\begin{enumerate}[resume, ...]`.
  3. **Stage Progression** (one `\section*{المرحلة ...}` per stage):
     - **مقدمة للوراثة:** Build 2 sibling classes *without* inheritance (some identical fields/methods, some unique), then extract only the identical members into a common base class, followed by `\begin{boxAttention}[- نقطة للتفكير]` motivating inheritance.
     - **تطبيق الوراثة بين الفئات:** Refactor the base class (`protected` fields) and derived classes (`: base(...)`, `override ToString()` calling `base.ToString()`), and add a third derived class holding an array of objects (e.g. `Supervisor`, `MotherShip`, `AlphaDragon`).
     - **تعدد الأشكال وإدارة المجموعة:** A management/registry class holding a polymorphic array of the base type; `virtual`/`override` methods; downcasting with `is` and `as`; overriding `Equals(object obj)`.
     - **الفئات المجردة والواجهات:** Convert the base class to `abstract class` with an `abstract` method taking `object`, implement `IComparable` (`CompareTo(object obj)`), build `SortServices`, and write methods that filter by type (`is`) and return sorted sub-arrays.
     - A booklet may split one of these stages into two (e.g. the Company booklet has 5 stages).
  4. **Mandatory `Main` Verification in Every Exercise:** Every exercise MUST end with `\textbf{الفحص في \textenglish{Main}:}` specifying which objects to create, which methods to call (both valid and edge/failure cases), and what to print.
  5. **Standalone C# Solution Files:** Do NOT embed the evolving C# code inside `boxSolution` in the booklet. Put compilable C# classes (one `.cs` file per class + `Program.cs`) in the stage's solution folder; the full booklet's final solution equals the last stage's solution.

### 5.3. Homework (`exs/hwXX-*.tex`)
- **Location:** `src/<subject>/exs/hwXX-<TopicName>.tex`
- **Title Scheme:** `\title{وظيفة بيتية X للصف العاشر $10$: [الموضوع]}`
- **Header Boxes:** An imperative `boxWarning` reminding students to run and test their code before submission, followed by a `boxNote` about choosing proper types (`int` vs `double`).
- **Reference Examples:** [src/basics/exs/hw01-VariablesMathOperations.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/hw01-VariablesMathOperations.tex), [src/oop/exs/hw00-DateClass.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/hw00-DateClass.tex).

### 5.4. Lesson Notes & Student Summaries (`lessonNotes/`)
- **Location:** `src/<subject>/lessonNotes/`
- **Title Scheme:** `\title{ملخص: [الموضوع]}` or `\title{ملخص شامل للطلاب: [الموضوع]}` with `\author{أ. محمود اغبارية}`.
- **CRITICAL Rule — Never Use Worksheet Questions as Examples:** It is **strictly forbidden** for lesson notes, summaries, or slides to include code examples that are solutions to the questions in the worksheets (`exs/`). Always invent distinct, parallel examples (different numbers, conditions, or scenarios) that teach the same concept without giving away the answers to the exercises.
- **Two Formats:**
  1. **Detailed Lesson Notes:** Formal syntax in `boxCode`, rules tables, memory/TikZ diagrams, and in-class `boxExercise` blocks. Examples: [src/basics/lessonNotes/01-variables_math_string_operations_new.tex](file:///c:/dev/workspace/school_workspace/src/basics/lessonNotes/01-variables_math_string_operations_new.tex), [history_src/2025_26/basics/lessonNotes/12-classes.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/lessonNotes/12-classes.tex).
  2. **Compact Printable Student Summaries:** Each numbered topic (`\subsection*{1. ...}`, preceded by `\filbreak`) has a strict 3-part structure:
     - `\textbf{الفكرة:}` — concise 1–2 sentence explanation using exact terminology.
     - `\begin{boxCode} ... \end{boxCode}` — short, localized, self-contained example + `// Usage in Main:`.
     - `\textbf{تنبيه:}` — a common exam mistake to avoid (optional when there is no typical mistake).
     - Reference examples: [src/oop/lessonNotes/student_summary_csharp_oop.tex](file:///c:/dev/workspace/school_workspace/src/oop/lessonNotes/student_summary_csharp_oop.tex), [src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex](file:///c:/dev/workspace/school_workspace/src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex).

### 5.5. Exams & Quizzes (`exams/`)
- **Title Scheme:** `\title{اختبار شهري للصف $10$-$10$}` or `\title{امتحان فصلي ...}`
- **Exam Rules Header Box:** Inside `\ifwithsols \else \begin{boxCode} ... \end{boxCode} \fi`: exam duration, ink-only requirement, external answer sheet instructions, and allowed materials.
- **Point Allocations:** Next to question headers as `\item \textbf{السؤال الأوّل} ($25$ علامة)`, and next to sub-questions as `($10$ علامات)` or `\textbf{(بونوس $+5$ علامات)}`.
- **Detached Student Tear-Off Answer Sheet (`ورقة تسليم للطالب`):** When students must hand in tracing tables (`جدول متابعة`) or fill-in tables, duplicate those tables at the very end of the document inside `\ifwithsols \else ... \fi`, preceded by an empty spacer page (`\clearpage \thispagestyle{empty} \mbox{} \clearpage`), so in double-sided printing the tear-off sheet is on its own physical sheet.
- **Reference Examples:** [history_src/2025_26/basics/exams/exam01-BasicsMathIf1.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exams/exam01-BasicsMathIf1.tex), [history_src/2025_26/basics/exams/exam04-final_untilClasses2.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exams/exam04-final_untilClasses2.tex).

### 5.6. Bagrut Question Fragments (`bagrut_questions/`)
- **Architecture:** Each Bagrut question file `bagrut_questions/<subject>/<topic>_<year>_<examId>_<qNum>.tex` is a **document fragment** (no `\documentclass`, no `\begin{document}`) that is `\input{...}` into topic compilations or full exam booklets (e.g. [src/oop/review_basics/bagrut371-2026.tex](file:///c:/dev/workspace/school_workspace/src/oop/review_basics/bagrut371-2026.tex)). Verify a fragment by building the document that includes it.
- **Bullet Alignment Inside `boxSolution`:** When an `\item` inside `\begin{enumerate}` is immediately followed by a `\begin{boxCode}` or a table, write `\item .` (with a period) so `polyglossia`/`bidi` does not misalign the bullet vertically.
- **Reference Example:** [bagrut_questions/basics/classes2_2026_899371_5.tex](file:///c:/dev/workspace/school_workspace/bagrut_questions/basics/classes2_2026_899371_5.tex).

### 5.7. Standard LaTeX Table Patterns

- **Mandatory Rule — Use `longtable` Whenever Relevant (Tables With Long Text, Code Cells, or Many Rows):**
  - Always use `\begin{longtable}{...} ... \end{longtable}` instead of `\begin{tabular}{...} ... \end{tabular}` for any table that contains long/multi-line text, `pycell` code blocks, TikZ figures, or many rows (including class specification tables, code-output tables, loop-matching tables, boolean-expression tables, and multi-row fill-in tables). Unlike `tabular`, `longtable` splits cleanly across page boundaries and prevents large vertical gaps or bottom-margin overflows.
  - Note: `longtable` centers itself automatically (`\LTleft=\fill`, `\LTright=\fill`), so do not wrap it in `\begin{center}`; wrap it in a group `{\renewcommand{\arraystretch}{...} \begin{longtable}{...} ... \end{longtable}}` when adjusting row spacing.
  - **Exception:** `longtable` cannot be used inside a `tcolorbox` (`boxSolution`, `boxNote`, etc.) or inside another table cell; keep tables that are inside a `tcolorbox` or tiny 1–2 row diagrams (like 1D array visuals) as `tabular`.

1. **Two-Column RTL Class Specification Table (واجهة الفئة / ملخص الفئة):**
   - **When to use:** Every time a question describes a class (its attributes and/or several methods), present it in this table. If a question only asks to add **a single method** to an existing class, write it as regular text instead.
   - **Exact style:** use `longtable` with the columns `|>{\raggedleft\arraybackslash}p{0.4\textwidth}|>{\raggedright\arraybackslash}p{0.5\textwidth}|` (Arabic description on the right, English definition on the left):
   ```latex
   {\renewcommand{\arraystretch}{1.2}
   \small
   \begin{longtable}{|>{\raggedleft\arraybackslash}p{0.4\textwidth}|>{\raggedright\arraybackslash}p{0.5\textwidth}|}
   \hline
   \multicolumn{2}{|c|}{\textbf{الفئة الأساسية: \textenglish{Employee}}} \\
   \hline
   صفات محمية: رقم الهوية، الاسم، وسنوات الأقدمية. & \textenglish{protected string id, name;} \newline \textenglish{protected int seniority;} \\
   \hline
   عمليتان بنائيتان لتهيئة صفات الموظف. & \textenglish{public Employee(string id, string name, int seniority)} \newline \textenglish{public Employee(string id, string name)} \\
   \hline
   عمليات \textenglish{Get}، \textenglish{SetName}، \textenglish{AddSeniorityYear}، و \textenglish{ToString}. & \textenglish{GetId(), GetName(), GetSeniority(), SetName(...), AddSeniorityYear(), ToString()} \\
   \hline
   \end{longtable}}

   \vspace{1em}
   ```
2. **Left-to-Right Tracing Table (`جدول متابعة`):** Always wrap tracing tables in `\begin{english}` so columns flow left-to-right like code execution. Use `longtable` when the tracing table is outside a `tcolorbox` and has many rows, or `tabular` when inside `boxSolution`:
   ```latex
   {\begin{english}
   \renewcommand{\arraystretch}{1.6}
   \begin{longtable}{|C{2cm}|C{2cm}|C{3cm}|C{3.5cm}|}
   \hline
   \textbf{a} & \textbf{b} & \textbf{a > b} & \textarabic{\textbf{المخرجات}} \\
   \hline
    & & & \\ \hline
   \end{longtable}
   \end{english}}
   ```
3. **Visual 1D Array Diagram (رسم مصفوفة مع مؤشراتها):**
   ```latex
   \begin{center}
   \begin{english}
   \begin{tabular}{c|c|c|c|c|}
   \multicolumn{1}{c}{} & \multicolumn{1}{c}{\small 0} & \multicolumn{1}{c}{\small 1} & \multicolumn{1}{c}{\small 2} & \multicolumn{1}{c}{\small 3} \\ \cline{2-5}
   \textbf{arr} & 14 & 7 & 22 & 5 \\ \cline{2-5}
   \end{tabular}
   \end{english}
   \end{center}
   ```
4. **Table With Code Cells (جدول يحوي مقاطع برنامج):** When a cell must contain code (e.g. a "what does each method print" table with columns *البند / العملية / المُخرج* or a two-column loop matching table), use `longtable` and put the code in a `pycell` inside a **fixed-width `p{...}` column**, so it stays left-to-right inside the RTL table and the table can break across pages between rows:
   ```latex
   {\renewcommand{\arraystretch}{1.3}
   \begin{longtable}{|C{1.2cm}|p{8cm}|C{3.5cm}|}
   \hline
   \textbf{البند} & \textbf{العملية} & \textbf{المُخرج} \\
   \hline
   أ &
   \begin{pycell}
   \begin{english}
   \begin{minted}{python}
   def ex1():
       a = 5
       print(a * 2)

   ex1()
   \end{minted}
   \end{english}
   \end{pycell}
   & \\
   \hline
   \end{longtable}}
   ```

### 5.8. Python (`src/python/pythonA/`) & Computational Models (`computational_models/`)
- **Python Conventions:**
  - Wrap code in `\begin{english} \begin{minted}{python} ... \end{minted} \end{english}`.
  - Use `snake_case` for all Python variable and function identifiers (`sum_even`, `user_age`).
  - Reference example: [src/python/pythonA/pythonA_review2.tex](file:///c:/dev/workspace/school_workspace/src/python/pythonA/pythonA_review2.tex).
- **Computational Models / Automata Conventions:**
  - Formal notation: alphabet $\Sigma$, stack alphabet $\Gamma$, word length $|w|$, character count $\#_a(w)$, concatenation $w_1 \cdot w_2$ / $L_1 \bullet L_2$, reversal $w^R$ or $R(w)$, complement $\overline{L}$, Turing left-end marker $\vdash$, blank symbol $\triangle$.
  - State diagrams use TikZ `automata` (`\begin{tikzpicture}[shorten >=1pt, node distance=2.8cm, on grid, auto, >={Stealth[round]}]`) wrapped inside `\begin{english}`.
  - Reference examples: [history_src/2025_26/computational_models/lessonNotes/01-DFA.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/lessonNotes/01-DFA.tex), [history_src/2025_26/computational_models/lessonNotes/03-TuringMachine.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/lessonNotes/03-TuringMachine.tex), [history_src/2025_26/computational_models/exams/diplomme2026.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/exams/diplomme2026.tex).

---

## 6. Question Formulation & Pedagogical Guidelines

### 6.1. Scaffolding & Section Structure
- Group questions into clear thematic sections (`\section*{القسم الأول: ...}` or `\section*{المرحلة الأولى: ...}`). Each section starts on a new page and every `\item` ends with `\filbreak` (see Section 8).
- Questions must be graduated:
  - Start with direct, single-variable or single-concept questions.
  - Progress through compound conditions and multi-variable logic.
  - Continue with real-world application scenarios (tax tiers, cinema pricing, date validation, company management).
  - Only the final general section includes 1–2 challenging multi-step questions.

### 6.2. When to Include `boxExample` Blocks
- **Do NOT add `boxExample` to easy, clear questions** (positive/negative, even/odd, pass/fail, password match, simple comparisons). Text-only questions let several fit on one page of the student handout.
- **Add `boxExample` (always wrapped in `\ifdetailed ... \fi`) ONLY for:**
  1. Non-obvious output formatting (e.g. `3 < 9 < 15`, `Result = 15`).
  2. Multi-input or conditional pricing/tier calculations (e.g. cinema discounts, electricity brackets).
  3. Boundary and error cases (e.g. division by zero, invalid dates, leap years).
- **Arithmetic Breakdown Rule:** When an example involves a multi-step calculation, write the step-by-step arithmetic in Arabic right below the example box:

  ```latex
  \begin{boxExample}
  ...
  \end{boxExample}
  لأنّ $30 + 0.18 \cdot 30 = 35.4$
  ```

### 6.3. Formatting Prompts
- **Class Descriptions Use a Table:** Whenever a question describes a class's attributes and/or methods, use the class table from Section 5.7. A request to add a **single method** is written as regular text.
- **Inline Numbers Wrapped in `$:`** Always wrap inline numbers in math mode (e.g. `$0$`, `$5$`, `$10$`, `$-1$`, `$100$`) instead of `\textenglish{...}` or bare digits.
- **Bold Key Terms:** Bold critical words to prevent misreading, e.g. `الراتب \textbf{الشهري}`, `الضريبة \textbf{السنوية}`, `\textbf{موجب}`, `\textbf{سالب}`, `\textbf{غير سالب}`.
- **Explicit Assumptions:** State domain constraints in parentheses, e.g. `(افترض أنّ الرقمين ليسا صفرًا.)`, `(عدد صحيح موجب)`.

---

## 7. Solution & Code Standards

- **Strict Bracing Rule:** Every `if`, `else if`, `else`, `for`, and `while` block in C# solutions and examples MUST have curly braces `{ }`, even for a single statement:

  ```csharp
  // CORRECT:
  if (num > 0)
  {
      Console.WriteLine("Positive");
  }
  else
  {
      Console.WriteLine("Negative");
  }

  // FORBIDDEN:
  if (num > 0) Console.WriteLine("Positive");
  ```

- **Solution Wrapping:** Code always goes in `english` + `minted`; in worksheets, solutions go in `\ifwithsols` + `boxSolution`:

  ```latex
  \ifwithsols
  \begin{boxSolution}
  \begin{english}
  \begin{minted}{csharp}
  ...
  \end{minted}
  \end{english}
  \end{boxSolution}
  \fi
  ```

- **Identifier Naming & `this.` in C#:**
  - Fields (`private` or `protected`), local variables, and parameters: meaningful `camelCase` (`temperature`, `birthYear`, `totalCost`, `seniority`).
  - Methods and classes: `PascalCase` (`GetSalary`, `AddEmployee`, `Technician`).
  - Inside constructors and methods, access fields with `this.` (`this.name = name;`, `return this.score;`).
- **Zero Arabic in Code (Console Messages, String Literals & Comments):** It is **strictly and totally forbidden (without any exception)** to write any Arabic characters inside code — neither in print/output commands (`Console.WriteLine(...)`, `print(...)`) nor in inline/block comments (`// ...`, `# ...`) nor in string literals. Always write all console prompts, outputs, and code comments in English (`Console.WriteLine("Enter temperature:");`, `// Reject negative values`), even when the Arabic question prompt phrases the output requirement in Arabic.
- **Alternative Solutions:** When showing two valid approaches (e.g. nested `if` vs. `&&`), use consecutive boxes labeled `\begin{boxSolution}[1]` and `\begin{boxSolution}[2]` (or `[بديل]`).
- **Partitioning Long Solutions:** A single `boxSolution` cannot break across pages, so a long solution (a full class, several helper methods, a long decision tree) would be clipped. **Long solutions MUST be split into several consecutive boxes:**
  - Split at logical points (e.g. Part 1: fields & constructors, Part 2: methods & `Main`; or `[فرع أ]` / `[فرع ب]`).
  - Label each box: `\begin{boxSolution}[الجزء الأول: ...]`, `\begin{boxSolution}[الجزء الثاني: ...]`.
  - Put `\filbreak` (not `\clearpage`) between the boxes, so the next box moves to a new page only if it does not fit:
    ```latex
    \ifwithsols
    \begin{boxSolution}[الجزء الأول: تعريف الفئة والعمليات البنائية]
    \begin{english}
    \begin{minted}{csharp}
    // ... Part 1 code ...
    \end{minted}
    \end{english}
    \end{boxSolution}

    \filbreak

    \begin{boxSolution}[الجزء الثاني: العمليات الإضافية والعمليات المساعدة]
    \begin{english}
    \begin{minted}{csharp}
    // ... Part 2 code ...
    \end{minted}
    \end{english}
    \end{boxSolution}
    \fi
    ```

---

## 8. Pagination & Spacing Rules

These two rules are **mandatory** in every document. Any older pattern that contradicts them (e.g. `\clearpage` every 2–3 questions) is obsolete.

1. **`\filbreak` after every `\item` (always, outside any `\fi`):**
   At the end of each `\item` block — after the question text and after any `\ifdetailed ... \fi` / `\ifwithsols ... \fi` blocks belonging to it — put `\filbreak` on its own line, **outside** the conditional, so it applies in every build (regular, printable, solutions, white/black). The next item stays on the current page if it fits and moves to a new page only if it does not, so a question is never separated from its example/solution box.
   ```latex
   \begin{enumerate}[label=\textbf{تمرين \arabic*:}, wide=0pt, itemsep=2.2em]
   \item اكتب برنامجًا يستقبل ...
   \ifdetailed
   \begin{boxExample}
   ...
   \end{boxExample}
   \fi
   \ifwithsols
   \begin{boxSolution}
   ...
   \end{boxSolution}
   \fi
   \filbreak

   \item ...
   \filbreak
   \end{enumerate}
   ```
   - Applies to items at every nesting level of question/exercise lists (including sub-questions `أ.`, `ب.`).
   - Does NOT apply to short lists inside a `tcolorbox` (`boxNote`, `boxAttention` checklists, ...) or inside tables, since a box cannot break anyway.
2. **`\clearpage` before every `\section` / `\section*`:**
   Every new section (`القسم ...`, `المرحلة ...`, `الجزء ...`) starts on a new page. Put `\clearpage` on its own line directly before `\section*{...}`.
   - **Only exception:** the first section of the document (it follows the title and any opening boxes directly) — do not push it to a new page.
   - If an `enumerate` list continues across sections, close it before `\clearpage \section*{...}` and reopen it with `\begin{enumerate}[resume, ...]`.

**Other pagination & spacing rules (consistent with the two rules above):**
- **Question list spacing (`itemsep`):** Use `\begin{enumerate}[itemsep=1em]` when questions are short (1–2 lines each), and `\begin{enumerate}[itemsep=2em]` when questions are longer (see Section 2.4).
- **Subsections:** Use `\filbreak` (not `\clearpage`) before each `\subsection*`, so a topic heading and its code box stay together on the same page.
- **Between partitioned solution boxes** inside one item: use `\filbreak` (Section 7).
- **No other `\clearpage`:** Do not add `\clearpage` between questions or inside `\ifwithsols`; the `\filbreak` after each `\item` already handles it. The only other allowed forced breaks are the exam tear-off spacer page (`\clearpage \thispagestyle{empty} \mbox{} \clearpage`, Section 5.5) and `\ifwhiteblack \clearpage \fi` right after an item's `\filbreak` when an exercise must get its own page in landscape presentation mode.
