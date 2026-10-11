# Authoring & Teaching Style Guide (AGENTS.md)

This document defines the authoring conventions, pedagogical style, LaTeX architecture, and coding standards used across all course materials in this repository.

**Any AI assistant or contributor generating or editing worksheets, homeworks, lesson notes, or exams in this workspace MUST follow the rules in this document.**

---

## 1. Overview & Context

- **Course:** High School Computer Science (Grades 10–12, Israeli Bagrut matriculation curriculum).
- **Core Languages:** C# (`basics`, `oop`), Python (`pythonA`, `pythonB`), and Computational Models / Automata.
- **Language of Instruction:** Formal, clear Arabic for explanations and requirements, combined seamlessly with English for code tokens, keywords, and console I/O.
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

---

## 2. LaTeX Technical Architecture

- **Engine:** `XeLaTeX` with `polyglossia`.
  - Main language: Arabic (`\setmainlanguage[numerals=western]{arabic}`).
  - Second language: English (`\setotherlanguage{english}`).
  - Fonts: `Calibri` (Arabic), `Courier New` (monospace/code).
- **Document Class:** Always `\documentclass[14pt]{extarticle}`.
- **Preamble Import:** Always `\input{../../../scripts/tex_preamble.tex}` (adjust relative path based on directory depth).
- **Conditional Compilation Flags (driven by Makefile):**
  - `\ifdetailed`: Controls sample console interactions (`boxExample`) and visual hints.
    - Set to `true` in regular builds (`make pdf`).
    - Set to `false` in printable student handouts (`make printable`) to keep the handout clean and paper-efficient.
  - `\ifwithsols`: Controls inclusion of reference solution boxes (`\begin{boxSolution} ... \end{boxSolution}`).
    - Set to `true` in solutions builds (`make sols`).
  - `\ifwhiteblack`: Controls black-and-white landscape mode (`make wb`). Use `\ifwhiteblack \clearpage \fi` where needed for landscape page breaks.
- **List Spacing:** Standardize item separation with `[itemsep=2em]` or `[itemsep=3em]`. When resuming lists across sections, use `\begin{enumerate}[resume, itemsep=2em]`.

---

## 3. Strict Pedagogical Terminology (Arabic $\leftrightarrow$ CS Concepts)

In high school CS and Bagrut exams, verb choices convey exact technical specifications. **Never interchange these verbs:**

| Arabic Term | Exact Technical Meaning | Code Equivalent |
| :--- | :--- | :--- |
| **تستقبل** | Reads input from the user via keyboard/console | `Console.ReadLine()` / `input()` |
| **تتلقى** | Receives values as function/method parameters | `public static void Foo(int x)` |
| **تطبع** | Outputs text/data directly to the console | `Console.WriteLine(...)` / `print(...)` |
| **تعيد** | Returns a value to the caller | `return value;` |
| **برنامج** | A full runnable program | Code executed inside `Main()` |
| **مقطع برنامج** | A focused code snippet | Logic lines without class/method boilerplate |
| **عملية خارجية** / **عملية** | Method / function | `public static ...` |
| **فئة** | Class | `class ...` |
| **كائن** | Object / instance | `new ClassName(...)` |
| **عملية بنائية** | Constructor | `public Point(...)` |
| **صفات** / **خصائص** | Fields / attributes | `private double x;` |
| **جدول متابعة** | Tracing / dry-run table | Table tracking variables, conditions, outputs |

### 3.1. Language Policy: Technical Concepts vs. Code Identifiers
- **Technical Concepts (المصطلحات التقنية):** If an established Arabic term exists (e.g. `الوراثة` for Inheritance, `تعدد الأشكال` for Polymorphism, `مخطط الهرمية` for Hierarchy, `البرمجة كائنية التوجه` for OOP, `العمليات البنائية` for Constructors), **write the Arabic term only**. Do NOT append English translations in parentheses (avoid: `الوراثة (Inheritance)`, `البرمجة كائنية التوجه (OOP)`).
- **Code Identifiers & Entities (أسماء الفئات والعمليات والمتغيرات):** Keep these in English in questions, headings, tables, and prompts (e.g. `Employee`, `Technician`, `ToString`, `GetScore`, `AddEmployee`, `YearlyBonus`, `IsAccepted`, `Get / Set`, `current`, `MAX`). This ensures students define and implement unified, specific identifiers in their code.

### 3.2. Mandatory Word Choices (تفضيلات المصطلحات الإلزامية)
1. **استخدام "تعريف" بدلاً من "ترويسة":** عند الإشارة إلى توقيع أو رأس الفئة أو العملية البرمجية (Header / Signature / Definition)، استخدم دائمًا مصطلح **"تعريف"** (مثل: `تعريف الفئة`، `تعريف العملية`) وتجنّب استخدام كلمة "ترويسة".
2. **استخدام "عملية" بدلاً من "دالة":** في جميع الأسئلة والملاحظات والحلول، اعتمد دائمًا مصطلح **"عملية"** (أو "عملية خارجية"، "عملية بنائية"، "عمليات") وتجنّب استخدام لفظ "دالة" أو "دوال".

---

## 4. Semantic Callout Boxes (`tcolorbox`)

Defined in `scripts/tex_preamble.tex`, with colored icons and borders:

- `\begin{boxExample}[#]`: Used for console input/output runs and illustrative scenarios.
- `\begin{boxSolution}[#]`: Used exclusively inside `\ifwithsols` for reference solutions.
- `\begin{boxWarning}`: Used for common pitfalls (e.g. integer division truncation, code submission verification).
- `\begin{boxAttention}`: Used for important pedagogical definitions (e.g. difference between تستقبل and تتلقى).
- `\begin{boxNote}`: Helpful hints, type selection reminders, or naming rules.
- `\begin{boxCode}`: Compact box for template code or exam instruction rules.
- `\begin{boxDef}`: Formal concept definitions.

---

## 5. Document Types & Conventions

### 5.1. Worksheets & Practice Sheets (`exs/`)

- **Location:** `src/<subject>/exs/exXX-<TopicName>.tex`
- **Title Scheme:** `\title{ورقة تمرن X للصف العاشر 10 [الموضوع]}` or `\title{ورقة عمل X - [الموضوع]}`
- **Solutions Title Variant:**

  ```latex
  \ifwithsols
  \title{حل ورقة تمرن X ...}
  \else
  \title{ورقة تمرن X ...}
  \fi
  ```

- **Reference Example:** [src/basics/exs/ex05-ifStatement.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/ex05-ifStatement.tex)

### 5.2. Homework (`hw/`)

- **Location:** `src/<subject>/exs/hwXX-<TopicName>.tex`
- **Title Scheme:** `\title{وظيفة بيتية X للصف العاشر 10: [الموضوع]}`
- **Header Boxes:** Usually opens with an imperative `boxWarning` reminding students to run and test their code before submission, followed by a `boxNote` regarding proper data types (`int` vs `double`).
- **Reference Example:** [src/basics/exs/hw01-VariablesMathOperations.tex](file:///c:/dev/workspace/school_workspace/src/basics/exs/hw01-VariablesMathOperations.tex)

### 5.3. Lesson Notes & Summaries (`lessonNotes/`)

- **Location:** `src/<subject>/lessonNotes/XX-<topic_name>.tex` or `XX-<topic_name>_summary.tex`
- **Title Scheme:** `\title{ملخص: [الموضوع]}` or `\title{ورقة تلخيصية: [الموضوع]}` with `\author{أ. محمود اغبارية}`.
- **Structure:**
  1. Formal syntax pattern in `boxCode`.
  2. Summary table of data types / operators / valid names.
  3. Code snippet with English inline comments explaining what each line prints.
  4. Visual diagrams where appropriate (e.g. memory representations).
- **Reference Example:** [src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex](file:///c:/dev/workspace/school_workspace/src/basics/lessonNotes/01-variables_math_string_operations_new_summary.tex)

### 5.4. Exams (`exams/`)

- **Title Scheme:** `\title{اختبار شهري للصف 10-10}`
- **Header Box:** Enclosed inside `\ifwithsols \else \begin{boxCode} ... \end{boxCode} \fi` containing exam rules (duration, ink only, external answer sheet, materials allowed).
- **Reference Example:** `history_src/2025_26/basics/exams/exam01-BasicsMathIf1.tex`

---

## 6. Question Formulation & Pedagogical Guidelines

### 6.1. Scaffolding & Section Structure

- Group questions into clear thematic sections (`\section*{القسم الأول: ...}`).
- Questions must be graduated:
  - Start with direct, single-variable or single-concept questions.
  - Progress through compound conditions and multi-variable logic.
  - Real-world application scenarios (tax tiers, cinema pricing, date validation).
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

- **Bold Key Terms:** Always bold critical operational words to prevent misreading:
  e.g., `الراتب \textbf{الشهري}`, `الضريبة \textbf{السنوية}`, `\textbf{موجب}`, `\textbf{سالب}`.
- **Explicit Assumptions:** Enclose domain constraints in parentheses:
  e.g., `(افترض أنّ الرقمين ليسا صفرًا.)`, `(عدد صحيح موجب)`.

---

## 7. Solution & Code Standards

- **Strict Bracing Rule:** Every `if` and `else` block in solutions MUST have curly braces `{ }`, even if the body is a single statement:

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

- **Variable Naming in Code:** Meaningful `camelCase` identifiers in English (`temperature`, `birthYear`, `totalCost`, `isExempt`).
- **Console Messages:** English prompts and outputs (e.g., `Console.WriteLine("Enter temperature:");`).
- **Partitioning Long Solutions (Multiple Solution Boxes):**
  A single `boxSolution` (`tcolorbox`) will not break cleanly across pages; if a solution is long (e.g., a full class implementation, multiple helper methods, or a lengthy multi-branch decision tree), a single box will run off the bottom of the page and its contents will be clipped and disappear.
  **Therefore, long solutions MUST be partitioned into multiple sequential solution boxes:**
  - Break the code into logical segments (e.g. Part 1: Input & Setup, Part 2: Calculation & Output; or Methods 1–2 in the first box, Methods 3–4 in the next).
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

- **Compact Handouts:** Do NOT place `\clearpage` unconditionally after simple questions.
- **Clean Solutions:** Put `\clearpage` inside `\ifwithsols` every 2–3 questions (or between partitioned solution boxes) so solution boxes never overflow across pages.
- **White/Black Breaks:** Use `\ifwhiteblack \clearpage \fi` when an exercise or solution requires its own slide/page in presentation/landscape mode.
