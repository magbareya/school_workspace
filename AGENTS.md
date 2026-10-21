# Authoring & Teaching Style Guide (AGENTS.md)

This document defines the authoring conventions, pedagogical style, LaTeX architecture, build system, and coding standards used across all course materials in this repository.

**Any AI assistant or contributor generating or editing worksheets, booklets, homeworks, lesson notes, summaries, Bagrut solutions, or exams in this workspace MUST follow the rules in this document.**

---

## 1. Overview, Context & Repository Layout

- **Course:** High School Computer Science (Grades 10–12, Israeli Bagrut matriculation curriculum — 899371 / 899222 / 899205).
- **Core Subjects & Languages:**
  - **C# Fundamentals (`src/basics/`, `history_src/2025_26/basics/`):** Variables, I/O, math/division/modulo, conditionals (`if`/`else`), loops (`while`, `for`, nested loops), helper methods, strings, 1D/2D arrays, and introduction to classes.
  - **C# Object-Oriented Programming (`src/oop/`):** Encapsulation (`Get`/`Set`), constructors (default, parameterized, copy), composition & defensive copying, arrays of objects, inheritance (`: base(...)`, `protected`), polymorphism (upcasting, `virtual`/`override`, downcasting with `is`/`as`, `Object.Equals`), abstract classes (`abstract`), and interfaces (`IComparable`).
  - **Python (`src/python/pythonA/`):** Variables, I/O, conditionals, `for`/`while` loops, strings (indexing & slicing), and lists.
  - **Computational Models & Automata (`history_src/2025_26/computational_models/`):** Formal languages, regular operations, DFA, NFA, product automaton, closure properties, PDA, and Turing Machines.
- **Language of Instruction:** Formal, clear Arabic for explanations and requirements, combined seamlessly with English (`\textenglish{...}`) for code tokens, keywords, identifiers, and console I/O.
- **School & Instructor Identity:**
  - Header Right: `\fancyhead[R]{الأستاذ محمود اغبارية}`
  - Header Left: `\fancyhead[L]{مدرسة التسامح الشاملة}`
  - Standard Document Closing:

    ```latex
    \vspace{1cm}
    \begin{flushleft}
    أرجو لكم وقتًا ممتعًا.

    الأستاذ محمود اغبارية.
    \end{flushleft}
    ```

### 1.1. Repository Directory Structure
- [`src/`](file:///c:/dev/workspace/school_workspace/src): Current active teaching materials (`basics/`, `oop/`, `python/pythonA/`).
- [`history_src/2025_26/`](file:///c:/dev/workspace/school_workspace/history_src/2025_26): Full archive of previous year materials (`basics/`, `computational_models/`). *Note: Authoring conventions evolved over that year; always follow the latest settled conventions documented below.*
- [`bagrut_questions/`](file:///c:/dev/workspace/school_workspace/bagrut_questions): Cropped Bagrut exam question images (`.png`/`.pdf`) and their modular `.tex` solution fragments.
- [`scripts/`](file:///c:/dev/workspace/school_workspace/scripts): Shared LaTeX preambles ([`scripts/tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex), [`scripts/beamer_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/beamer_preamble.tex)) and Python automation utilities (`scripts/bagrut_questions/`).
- `out/`: Compiled PDFs mirroring the `src/` directory structure (generated via [`Makefile`](file:///c:/dev/workspace/school_workspace/Makefile)).

---

## 2. LaTeX Technical Architecture & Build System

- **Engine:** `XeLaTeX` with `-shell-escape` (required for `minted` v3) and `polyglossia`.
  - Main language: Arabic (`\setmainlanguage[numerals=western]{arabic}`).
  - Second language: English (`\setotherlanguage{english}`).
  - Fonts: `Calibri` (Arabic), `Courier New` (monospace/code), `Segoe UI Emoji` (`\emoji` for box icons).
  - **CRITICAL Font Rule for `minted`:** Never write Arabic text or Arabic comments inside `\begin{minted}{csharp}` or `\begin{minted}{python}` because the default Latin monospace font lacks Arabic glyphs (they will render as blank spaces). All inline comments inside `minted` blocks MUST be in English.
- **Document Class:** Always `\documentclass[14pt]{extarticle}`.
- **Preamble Import:** Always `\input{../../../scripts/tex_preamble.tex}` (adjust relative path based on directory depth).
- **Mandatory PDF Compilation Verification via `make`:**
  - Every `.tex` file created or modified MUST be verified by compiling it to PDF and checking that compilation succeeds without errors.
  - **Always compile using `make` — NEVER run `xelatex` manually.** The [`Makefile`](file:///c:/dev/workspace/school_workspace/Makefile) automatically handles `TEXMF_OUTPUT_DIRECTORY`, two-pass compilation, conditional flags (`\ifdetailed`, `\ifwithsols`, `\ifwhiteblack`), and cleanup (`make sclean`).
  - Examples of `make` commands:
    - Build a specific target PDF: `make out/oop/exs/ex02-inheritanceAndPolymorphism.pdf` (or `_printable.pdf`, `_sols.pdf`, `_wb.pdf`) and then run `make sclean`.
    - Build all `.tex` PDFs: `make tex` or `make pdf`, `make printable`, `make sols`, or `make all`.
- **Conditional Compilation Flags (driven by [`Makefile`](file:///c:/dev/workspace/school_workspace/Makefile)):**
  - `\ifdetailed`: Controls sample console interactions (`boxExample`) and visual hints.
    - Set to `true` in regular builds (`make pdf` $\rightarrow$ `out/.../<name>.pdf`).
    - Set to `false` in printable student handouts (`make printable` $\rightarrow$ `out/.../<name>_printable.pdf`) to keep the handout compact and paper-efficient.
  - `\ifwithsols`: Controls inclusion of reference solution boxes (`\begin{boxSolution} ... \end{boxSolution}`).
    - Set to `true` in solutions builds (`make sols` $\rightarrow$ `out/.../<name>_sols.pdf`).
  - `\ifwhiteblack`: Controls black-and-white A4 landscape presentation mode (`make wb` $\rightarrow$ `out/.../<name>_wb.pdf` and `make wbsols`). Sets `\LARGE` font, `bw` minted style, and black-and-white borders. Use `\ifwhiteblack \clearpage \fi` where needed for landscape page breaks.
- **Helper Macros & Global Defaults in [`scripts/tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex):**
  - `\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}`: Centered fixed-width column for tables (`|C{2.5cm}|`).
  - `\importpdfpage{filepath}{pagenum}`: Imports a full-page PDF graphic.
  - `\insertFullImg{filepath}`: Centers an image at `0.9\paperwidth`.
  - `\begin{pycell} ... \end{pycell}`: Frameless, full-width code cell used to put `minted` code inside a table cell while keeping it left-to-right inside an RTL table (see Section 5.7). Do NOT redefine it inside individual `.tex` files.
  - **Default `minted` look:** `\setminted{fontsize=\footnotesize, breaklines=true}` is set globally by the preamble in regular builds (it is intentionally NOT applied in `\ifwhiteblack` mode, which uses `\LARGE`). Do NOT repeat it in individual files.
  - **Compact `boxCode`:** the preamble also appends `fontupper=\setstretch{0.95}, top=4pt, bottom=4pt, before skip=6pt, after skip=6pt` to the `simplecode` style, so code boxes stay compact despite the global `onehalfspacing`. Do NOT repeat it in individual files.
- **List Spacing:** Standardize item separation with `[itemsep=2em]` or `[itemsep=2.2em]`. When resuming lists across sections or pages, use `\begin{enumerate}[resume, ...]`.

---

## 3. Strict Pedagogical Terminology (Arabic $\leftrightarrow$ CS Concepts)

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
- **Code Identifiers, Keywords & Console Strings (أسماء الفئات والعمليات والمتغيرات والكلمات المحجوزة):** Keep these in English wrapped in `\textenglish{...}` in questions, headings, tables, and prompts (e.g. `\textenglish{Employee}`, `\textenglish{Technician}`, `\textenglish{ToString}`, `\textenglish{GetScore}`, `\textenglish{AddEmployee}`, `\textenglish{YearlyBonus}`, `\textenglish{IsAccepted}`, `\textenglish{Get}` / `\textenglish{Set}`, `\textenglish{current}`, `\textenglish{MAX}`, `\textenglish{virtual}`, `\textenglish{override}`, `\textenglish{protected}`, `\textenglish{base}`, `\textenglish{is}`, `\textenglish{as}`). This ensures students define and implement unified, specific identifiers in their code. Remember to escape underscores in text mode (`\textenglish{student\_name}`).

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
- الخلايا المعلّمة بـ (—) فارغة في ورقة المصطلحات المصدرية (`tmp/translate.pdf`).
- المصطلحان "مؤشر" و"ابن أيسر" مكتوبان في الورقة المصدرية بصيغة ناقصة ("مؤش"، "أيس")؛ الصيغة المعتمدة هنا هي الصيغة الكاملة.

---

## 4. Semantic Callout Boxes (`tcolorbox`) & Non-Splitting Rules

All callout boxes are defined in [`scripts/tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex) with colored borders and emoji icons:

| Environment | Title / Icon | Primary Pedagogical Use |
| :--- | :--- | :--- |
| `\begin{boxDef}[#]` | `📘 تعريف # :` | Formal concept definitions or project story/domain framing (`[قصة السلسلة: ...]`). |
| `\begin{boxExercise}[#]` | `🧩 تمرين # :` | Standalone exercise blocks inside lesson notes. |
| `\begin{boxExample}[#]` | `📝 مثال # :` | Sample console input/output runs and illustrative scenarios (wrapped in `\ifdetailed`). |
| `\begin{boxNote}[#]` | `✨ ملاحظة # :` | Helpful hints, type selection reminders, or rules tables. Pass a leading dash for subtitles: `\begin{boxNote}[- عنوان فرعي]`. |
| `\begin{boxAttention}[#]` | `🔔 تنبيه # :` | Important pedagogical reflections (`\begin{boxAttention}[- نقطة للتفكير]`), pre-submission checklists, or key distinctions. |
| `\begin{boxWarning}[#]` | `⚡ ملاحظة هامة # :` | Common pitfalls (e.g. integer division truncation) or mandatory workflow instructions (testing in `Main`). |
| `\begin{boxSolution}[#]` | `✅ حل # :` | Reference solutions wrapped inside `\ifwithsols ... \fi`. Supports labels like `[1]`, `[بديل]`, `[فرع أ]`. |
| `\begin{boxSymbol}[#]` | `🔣 رمز # :` | Mathematical or formal notation boxes (used in Automata / Computational Models). |
| `\begin{boxHint}[#]` | `💡 تلميح # :` | Guided hints for challenging problems. |
| `\begin{boxCode}` | *(No title bar)* | Compact gray box (`simplecode`) for method signatures, localized code snippets, or exam cover instructions. |

### 4.1. Critical Rule: `tcolorbox` Environments Do NOT Split Across Pages
None of the boxes above (`boxCode`, `boxSolution`, `boxNote`, etc.) are breakable across pages. If a box is too tall for the remaining space on a page, it will jump to the next page (leaving large whitespace) or overflow the bottom margin and get clipped in print.
- **Keep `boxCode` Examples Localized & Short:** In summaries and lesson notes, avoid long full-program listings inside a single `boxCode`. Write focused 8–15 line snippets illustrating the exact concept + 2–3 lines of `// Usage in Main:`.
- **Compact Code Boxes Are Configured Globally:** [`scripts/tex_preamble.tex`](file:///c:/dev/workspace/school_workspace/scripts/tex_preamble.tex) loads `\usepackage[onehalfspacing]{setspace}`, and therefore it also sets (in regular, non-`\ifwhiteblack` builds) `\setminted{fontsize=\footnotesize, breaklines=true}` and appends `fontupper=\setstretch{0.95}, top=4pt, bottom=4pt, before skip=6pt, after skip=6pt` to the `simplecode` style. **Do NOT copy these `\setminted` / `\tcbset` lines into individual `.tex` files** — they are already in effect for every document. Only add a per-file override when a specific document genuinely needs a different value.
- **Use `\filbreak` Between Topics in Summaries:** Place `\filbreak` before each `\subsection*` in summary sheets so a topic heading and its explanation never sit at the bottom of a page while its `boxCode` jumps to the next page.

---

## 5. Document Types, Templates & Subject Conventions

### 5.1. Standard Worksheets & Practice Sheets (`exs/exXX-*.tex`)
- **Location:** `src/<subject>/exs/exXX-<TopicName>.tex`
- **Title Scheme:**
  ```latex
  \ifwithsols
  \title{حل ورقة تمرن X للصف العاشر 10 - [الموضوع]}
  \else
  \title{ورقة تمرن X للصف العاشر 10 - [الموضوع]}
  \fi
  ```
- **Reference Examples:**
  - C# Basics: [src/basics/exs/ex05-ifStatement.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/ex05-ifStatement.tex)
  - C# OOP Single Class: [src/oop/exs/ex01-PointClass.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex01-PointClass.tex)
  - C# Arrays & Classes Archive: [history_src/2025_26/basics/exs/ex10D-classes2-classesWithArrays.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exs/ex10D-classes2-classesWithArrays.tex)

### 5.2. Progressive Multi-Stage OOP Booklets (`كراس تمارين متدرج`) & Standalone C# Solutions
Used in `src/oop/exs/` to teach object-oriented design, inheritance, polymorphism, abstract classes, and interfaces step-by-step through a unified domain story:
- **Reference Examples:**
  - Employees & Company Project: [src/oop/exs/ex02-inheritanceAndPolymorphism.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex02-inheritanceAndPolymorphism.tex) (Solutions in [`src/oop/exs/ex02_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex02_sol))
  - Galactic Fleet Project: [src/oop/exs/ex03-galacticFleet.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex03-galacticFleet.tex) (Solutions in [`src/oop/exs/ex03_galactic_fleet_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex03_galactic_fleet_sol))
  - Dragon Riders Academy Project: [src/oop/exs/ex04-dragonRiders.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex04-dragonRiders.tex) (Solutions in [`src/oop/exs/ex04_dragon_riders_sol/`](file:///c:/dev/workspace/school_workspace/src/oop/exs/ex04_dragon_riders_sol))
- **Required Architectural Pattern:**
  1. **Header Boxes:** Open with `\begin{boxDef}[قصة السلسلة: ...]` introducing the narrative, followed by `\begin{boxWarning}` instructing students to update and run `Main` in every exercise.
  2. **Continuous Exercise Numbering:** Use `\begin{enumerate}[label=\textbf{تمرين \arabic*:}, wide=0pt, leftmargin=*, itemsep=2.2em]` and `\begin{enumerate}[resume, ...]` across stages.
  3. **Four-Stage Pedagogical Progression:**
     - **المرحلة الأولى (مقدمة للوراثة):** Build 2 sibling classes *without* inheritance (having some identical fields/methods and some unique ones), then extract only the identical members into a common base class, followed by `\begin{boxAttention}[- نقطة للتفكير]` motivating inheritance.
     - **المرحلة الثانية (تطبيق الوراثة بين الفئات):** Refactor the base class (`protected` fields) and derived classes (`: base(...)`, `override ToString()` calling `base.ToString()`), and add a third derived class containing an array of objects (e.g. `Supervisor`, `MotherShip`, `AlphaDragon`).
     - **المرحلة الثالثة (تعدد الأشكال وإدارة المجموعة):** Build a management/registry class holding a polymorphic array of the base type, implement `virtual` and `override` methods, practice downcasting with `is` and `as`, and override `Equals(object obj)`.
     - **المرحلة الرابعة (الفئات المجردة والواجهات):** Convert the base class to `abstract class` with an `abstract` method taking `object`, implement `IComparable` (`CompareTo(object obj)`), build `SortServices`, and write methods that filter by type (`is`) and return sorted sub-arrays.
  4. **Mandatory `Main` Verification in Every Exercise:** Every single exercise MUST end with `\textbf{الفحص في \textenglish{Main}:}` specifying what objects to instantiate, which methods to call (both valid and edge/failure cases), and what to print.
  5. **Standalone C# Solution Files:** Do NOT embed 1,000+ lines of evolving C# inside `boxSolution` in the `.tex` booklet. Instead, place the final, compilable C# classes (`.cs` file per class + `Program.cs`) in a dedicated folder `src/oop/exs/exXX_..._sol/`.

### 5.3. Homework (`exs/hwXX-*.tex`)
- **Location:** `src/<subject>/exs/hwXX-<TopicName>.tex`
- **Title Scheme:** `\title{وظيفة بيتية X للصف العاشر 10: [الموضوع]}`
- **Header Boxes:** Opens with an imperative `boxWarning` reminding students to run and test their code before submission, followed by a `boxNote` regarding proper types (`int` vs `double`).
- **Reference Examples:** [src/basics/exs/hw01-VariablesMathOperations.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/hw01-VariablesMathOperations.tex), [src/oop/exs/hw00-DateClass.tex](file:///c:/dev/workspace/school_workspace/src/oop/exs/hw00-DateClass.tex).

### 5.4. Lesson Notes & Student Summaries (`lessonNotes/`)
- **Location:** `src/<subject>/lessonNotes/`
- **Title Scheme:** `\title{ملخص: [الموضوع]}` or `\title{ملخص شامل للطلاب: [الموضوع]}` with `\author{أ. محمود اغبارية}`.
- **Two Formats:**
  1. **Detailed Lesson Notes:** Include formal syntax in `boxCode`, rules tables, memory/TikZ diagrams, and in-class `boxExercise` blocks. Examples: [src/basics/lessonNotes/01-variables_math_string_operations_new.tex](file:///c:/dev/workspace/school_workspace/src/basics/lessonNotes/01-variables_math_string_operations_new.tex), [history_src/2025_26/basics/lessonNotes/12-classes.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/lessonNotes/12-classes.tex).
  2. **Compact Printable Student Summaries:** Each numbered topic (`\subsection*{1. ...}`) preceded by `\filbreak` follows a strict 3-part localized structure:
     - `\textbf{الفكرة:}` Concise 1–2 sentence explanation using exact terminology.
     - `\begin{boxCode} ... \end{boxCode}` Short, localized, self-contained example + `// Usage in Main:`.
     - `\textbf{تنبيه:}` Common exam mistake to avoid.
     - **Reference Examples:** [src/oop/lessonNotes/student_summary_csharp_oop.tex](file:///c:/dev/workspace/school_workspace/src/oop/lessonNotes/student_summary_csharp_oop.tex), [src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex](file:///c:/dev/workspace/school_workspace/src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex).

### 5.5. Exams & Quizzes (`exams/`)
- **Title Scheme:** `\title{اختبار شهري للصف 10-10}` or `\title{امتحان فصلي ...}`
- **Exam Rules Header Box:** Enclosed inside `\ifwithsols \else \begin{boxCode} ... \end{boxCode} \fi` containing exam duration, ink-only requirement, external answer sheet instructions, and allowed materials.
- **Point Allocations:** Displayed next to question headers as `\item \textbf{السؤال الأوّل} (25 علامة)` and sub-questions as `(10 علامات)` or `\textbf{(بونوس +5 علامات)}`.
- **Detached Student Tear-Off Answer Sheet (`ورقة تسليم للطالب`):**
  When an exam contains tracing tables (`جدول متابعة`) or fill-in-the-blank tables that students must hand in inside the exam packet, duplicate those tables at the very end of the document inside `\ifwithsols \else ... \fi`, preceded by an empty spacer page (`\clearpage \thispagestyle{empty} \mbox{} \clearpage`) so that in double-sided printing the tear-off sheet is on a separate physical page.
- **Reference Examples:** [history_src/2025_26/basics/exams/exam01-BasicsMathIf1.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exams/exam01-BasicsMathIf1.tex), [history_src/2025_26/basics/exams/exam04-final_untilClasses2.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/basics/exams/exam04-final_untilClasses2.tex).

### 5.6. Bagrut Question Fragments (`bagrut_questions/`)
- **Architecture:** Individual Bagrut question `.tex` files in `bagrut_questions/<subject>/<topic>_<year>_<examId>_<qNum>.tex` are **document fragments** (they do NOT contain `\documentclass` or `\begin{document}`) designed to be `\input{...}` into topic compilations or full exam booklets (such as [src/oop/review_basics/bagrut371-2026.tex](file:///c:/dev/workspace/school_workspace/src/oop/review_basics/bagrut371-2026.tex)).
- **Formatting Rule Inside Bagrut `boxSolution`:** When an `\item` inside `\begin{enumerate}` is immediately followed by a `\begin{boxCode}` or table, place a period after `\item` (`\item .`) so `polyglossia`/`bidi` does not misalign the bullet vertically.
- **Reference Example:** [bagrut_questions/basics/classes2_2026_899371_5.tex](file:///c:/dev/workspace/school_workspace/bagrut_questions/basics/classes2_2026_899371_5.tex).

### 5.7. Standard LaTeX Table Patterns

1. **Two-Column RTL Class Specification Table (واجهة الفئة / ملخص الفئة):**
   - **Mandatory Usage Rule:** Every time a question or exercise describes a class (its attributes and/or multiple methods), it **MUST** be presented in a two-column table using the exact style below. However, if a question asks to add **only a single method** to an existing class, write it as regular text (do NOT use a table).
   - **Mandatory Table Style (`{\centering ... \par} %` + `\vspace{2em}`):** Always wrap the table in `{\centering ... \par} %` followed by `\vspace{2em}`, and use `|>{\raggedleft\arraybackslash}p{0.4\textwidth}|>{\raggedright\arraybackslash}p{0.5\textwidth}|` for the columns:
   ```latex
   {\centering
   \renewcommand{\arraystretch}{1.2}
   \small
   \begin{tabular}{|>{\raggedleft\arraybackslash}p{0.4\textwidth}|>{\raggedright\arraybackslash}p{0.5\textwidth}|}
   \hline
   \multicolumn{2}{|c|}{\textbf{الفئة الأساسية: \textenglish{Employee}}} \\
   \hline
   صفات محمية: رقم الهوية، الاسم، وسنوات الأقدمية. & \textenglish{protected string id, name;} \newline \textenglish{protected int seniority;} \\
   \hline
   عمليتان بنائيتان لتهيئة صفات الموظف. & \textenglish{public Employee(string id, string name, int seniority)} \newline \textenglish{public Employee(string id, string name)} \\
   \hline
   عمليات \textenglish{Get}، \textenglish{SetName}، \textenglish{AddSeniorityYear}، و \textenglish{ToString}. & \textenglish{GetId(), GetName(), GetSeniority(), SetName(...), AddSeniorityYear(), ToString()} \\
   \hline
   \end{tabular}
   \par} %

   \vspace{2em}
   ```
2. **Left-to-Right Tracing Table (`جدول متابعة`):**
   Always wrap tracing tables in `\begin{english}` so columns flow left-to-right matching code execution:
   ```latex
   \begin{center}
   \begin{english}
   \renewcommand{\arraystretch}{1.6}
   \begin{tabular}{|C{2cm}|C{2cm}|C{3cm}|C{3.5cm}|}
   \hline
   \textbf{a} & \textbf{b} & \textbf{a > b} & \textarabic{\textbf{المخرجات}} \\
   \hline
    & & & \\ \hline
   \end{tabular}
   \end{english}
   \end{center}
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
4. **Table With Code Cells (جدول يحوي مقاطع برنامج):**
   When a table cell must contain a code snippet (e.g. a "what is the output of each method" table with columns *البند / العملية / المُخرج*), put the code in a `pycell` (defined in the preamble) inside a **fixed-width `p{...}` column**, so the code stays left-to-right inside the RTL table. Keep each cell's snippet short (the table row cannot split across pages). If a snippet is long, use a separate `boxCode` per item instead of a table.
   ```latex
   {\centering
   \renewcommand{\arraystretch}{1.3}
   \begin{tabular}{|C{1.2cm}|p{8cm}|C{3.5cm}|}
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
   \end{tabular}
   \par} %
   ```
   Always compile with `make` and check the result visually when using this pattern for the first time in a document.

### 5.8. Python (`src/python/pythonA/`) & Computational Models (`computational_models/`)
- **Python Conventions:**
  - Wrap code in `\begin{english} \begin{minted}{python} ... \end{minted} \end{english}`.
  - Use `snake_case` for all Python variable and function identifiers (`sum_even`, `user_age`).
  - Reference example: [src/python/pythonA/pythonA_review2.tex](file:///c:/dev/workspace/school_workspace/src/python/pythonA/pythonA_review2.tex).
- **Computational Models / Automata Conventions:**
  - Formal notation: Alphabet $\Sigma$, stack alphabet $\Gamma$, word length $|w|$, character count $\#_a(w)$, concatenation $w_1 \cdot w_2$ / $L_1 \bullet L_2$, reversal $w^R$ or $R(w)$, complement $\overline{L}$, Turing left-end marker $\vdash$, blank symbol $\triangle$.
  - State diagrams use TikZ `automata` (`\begin{tikzpicture}[shorten >=1pt, node distance=2.8cm, on grid, auto, >={Stealth[round]}]`) wrapped inside `\begin{english}`.
  - Reference examples: [history_src/2025_26/computational_models/lessonNotes/01-DFA.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/lessonNotes/01-DFA.tex), [history_src/2025_26/computational_models/lessonNotes/03-TuringMachine.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/lessonNotes/03-TuringMachine.tex), [history_src/2025_26/computational_models/exams/diplomme2026.tex](file:///c:/dev/workspace/school_workspace/history_src/2025_26/computational_models/exams/diplomme2026.tex).

---

## 6. Question Formulation & Pedagogical Guidelines

### 6.1. Scaffolding & Section Structure
- Group questions into clear thematic sections (`\section*{القسم الأول: ...}` or `\section*{المرحلة الأولى: ...}`).
- Questions must be graduated:
  - Start with direct, single-variable or single-concept questions.
  - Progress through compound conditions and multi-variable logic.
  - Real-world application scenarios (tax tiers, cinema pricing, date validation, company management).
  - Only in the final general section include 1–2 challenging multi-step questions.

### 6.2. When to Include vs. Delete `boxExample` Blocks
- **DO NOT include `boxExample` for easy/clear questions:**
  Direct questions (e.g., positive/negative, even/odd, pass/fail, checking password match, simple comparisons) should have **no** bulky example boxes. Keeping them text-only allows several questions to fit per page in student handouts.
- **INCLUDE `boxExample` (wrapped in `\ifdetailed`) ONLY for:**
  1. Questions with non-obvious output formatting (e.g. `3 < 9 < 15`, `Result = 15`).
  2. Multi-input or conditional pricing/tier calculations (e.g. cinema discount rules, electricity consumption brackets).
  3. Boundary and error test cases (e.g. division by zero, invalid dates, leap year test years).
- **Arithmetic Breakdown Rule:**
  Whenever an example involves a multi-step calculation, write an explicit step-by-step arithmetic breakdown in Arabic immediately below the example box:

  ```latex
  \begin{boxExample}
  ...
  \end{boxExample}
  لأنّ $30 + 0.18 \cdot 30 = 35.4$
  ```

### 6.3. Formatting Prompts
- **Class Descriptions Must Use a Table (Unless Adding Only 1 Method):** Whenever a question describes the attributes and/or methods of a class, present the class specification in the standard two-column table defined in Section 5.7 (`{\centering ... \par} %` + `\vspace{2em}`). If a question asks to add only a **single method** to an existing class, write the requirement as regular text instead of a table.
- **Bold Key Terms:** Always bold critical operational words to prevent misreading:
  e.g., `الراتب \textbf{الشهري}`, `الضريبة \textbf{السنوية}`, `\textbf{موجب}`, `\textbf{سالب}`, `\textbf{غير سالب}`.
- **Explicit Assumptions:** Enclose domain constraints in parentheses:
  e.g., `(افترض أنّ الرقمين ليسا صفرًا.)`, `(عدد صحيح موجب)`.

---

## 7. Solution & Code Standards

- **Strict Bracing Rule:** Every `if`, `else if`, `else`, `for`, and `while` block in C# solutions and examples MUST have curly braces `{ }`, even if the body is a single statement:

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

- **Language Wrapping:** Always wrap code blocks with `english` and `minted`:

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

- **Identifier Naming & `this.` Qualification in C#:**
  - Fields (`private` or `protected`) and local variables/parameters: meaningful `camelCase` (`temperature`, `birthYear`, `totalCost`, `seniority`).
  - Methods and classes: `PascalCase` (`GetSalary`, `AddEmployee`, `Technician`).
  - Inside class constructors and methods, qualify field accesses with `this.` (`this.name = name;`, `return this.score;`).
- **Console Messages & Inline Comments:** Always write console prompts/outputs and code comments in English (`Console.WriteLine("Enter temperature:");`, `// Reject negative values`).
- **Alternative Solutions:** When demonstrating two valid pedagogical approaches (e.g., nested `if` vs. `&&`), provide both in consecutive boxes labeled `\begin{boxSolution}[1]` and `\begin{boxSolution}[2]` (or `\begin{boxSolution}[بديل]`).
- **Partitioning Long Solutions (Multiple Solution Boxes):**
  A single `boxSolution` (`tcolorbox`) will not break cleanly across pages; if a solution is long (e.g., a full class implementation, multiple helper methods, or a lengthy multi-branch decision tree), a single box will run off the bottom of the page and its contents will be clipped and disappear.
  **Therefore, long solutions MUST be partitioned into multiple sequential solution boxes:**
  - Break the code into logical segments (e.g. Part 1: Fields & Constructors, Part 2: Methods & `Main`; or `[فرع أ]` and `[فرع ب]`).
  - Label each box clearly: `\begin{boxSolution}[الجزء الأول]` and `\begin{boxSolution}[الجزء الثاني]`.
  - Place `\clearpage` between the boxes so each box renders fully on its own page without vertical overflow:
    ```latex
    \ifwithsols
    \begin{boxSolution}[الجزء الأول: تعريف الفئة والعمليات البنائية]
    \begin{english}
    \begin{minted}{csharp}
    // ... Part 1 code ...
    \end{minted}
    \end{english}
    \end{boxSolution}

    \clearpage

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

- **Compact Handouts:** Do NOT place `\clearpage` unconditionally after simple questions in worksheets.
- **Clean Solutions:** Put `\clearpage` inside `\ifwithsols` every 2–3 questions (or between partitioned solution boxes) so solution boxes never overflow across pages.
- **Summary Subsections:** Use `\filbreak` before each `\subsection*` in summary sheets so a topic heading and its code box stay together on the same page.
- **White/Black Breaks:** Use `\ifwhiteblack \clearpage \fi` when an exercise or solution requires its own slide/page in presentation/landscape mode.
