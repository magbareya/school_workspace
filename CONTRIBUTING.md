# Contributing to Computer Science Basics Course Materials

Thank you for your interest in contributing to this educational project! We welcome contributions from educators, students, and anyone passionate about computer science education.

## How Can I Contribute?

### Reporting Issues

If you find any errors, typos, or have suggestions for improvement:

1. Check if the issue already exists in the [Issues](https://github.com/magbareya/school_workspace/issues) section
2. If not, create a new issue with a clear title and description
3. Include relevant details:
   - Which file or section has the issue
   - What you expected vs. what you found
   - Suggestions for improvement (if any)

### Suggesting Enhancements

We welcome suggestions for:
- New topics or lessons
- Additional exercises or examples
- Improved explanations
- Better visualizations or diagrams
- Translation improvements (especially for Arabic content)

### Contributing Content

#### Before You Start

1. Fork the repository
2. Create a new branch for your contribution: `git checkout -b feature/your-feature-name`
3. Familiarize yourself with the project structure (see README.md)

#### Content Guidelines

**For Lesson Notes:**
- Use Jupyter notebooks (`.ipynb`) for interactive content
- Follow existing formatting and structure
- Include clear explanations and examples
- Add comments in both English and Arabic where appropriate
- Test all code examples

**For Exercises and Exams:**
- Use LaTeX (`.tex`) files for exercises
- Follow the existing template structure
- Ensure proper difficulty progression
- Include solutions (marked with appropriate macros)
- Verify that PDFs compile correctly

**For Bagrut Questions:**
- Follow the naming convention: `topic_year_number_question.pdf`
- Create solution files using the provided scripts
- Add appropriate topic tags

#### Technical Requirements

1. **Build and Test:**
   ```bash
   make clean
   make pdf
   ```
   Ensure all files compile without errors

2. **Formatting:**
   - Use consistent indentation (4 spaces for Python, follow LaTeX conventions)
   - Keep line lengths reasonable
   - Use descriptive file names

3. **Documentation:**
   - Update README.md if adding new features or changing structure
   - Add comments to complex code or LaTeX
   - Document any new scripts or utilities

#### Pull Request Process

1. Update your branch with the latest main branch:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add lesson notes for recursion topic"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request with:
   - Clear title describing the change
   - Detailed description of what was added/changed and why
   - Any relevant issue numbers (e.g., "Fixes #123")
   - Screenshots or examples of generated PDFs (if applicable)

5. Wait for review and address any feedback

### Code Review Process

- At least one maintainer will review your PR
- We aim to respond within a week
- Be patient and respectful during the review process
- Address feedback promptly

## Development Setup

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Pandoc
- XeLaTeX (TeX Live or MiKTeX)
- GNU Make

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/school_workspace.git
cd school_workspace

# Install Python dependencies (if any)
pip install jupyter nbconvert

# Test the build
make pdf
```

## Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions

### LaTeX
- Use semantic markup
- Keep consistent formatting
- Use Arabic text with proper RTL support

### Jupyter Notebooks
- Clear cell organization
- Include markdown explanations
- Test all code cells

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Reach out to the maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Creative Commons Attribution-ShareAlike 4.0 International License).

Thank you for helping make computer science education more accessible! 🎓
