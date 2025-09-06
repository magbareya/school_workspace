SHELL := /bin/bash

# Find all ipynb and md files recursively
NB := $(shell find . -name "*.ipynb")
MD := $(shell find . -name "*.md")

# Map input paths (./X.ipynb → out/X.pdf)
PDFS := $(patsubst ./%.ipynb,out/%.pdf,$(NB)) \
        $(patsubst ./%.md,out/%.pdf,$(MD))

PRINTABLES := $(patsubst ./%.ipynb,out/%_printable.pdf,$(NB))
CSFILES := $(patsubst ./%.ipynb,out/%.cs,$(NB))

all: pdf printable cs

pdf: $(PDFS)

printable: $(PRINTABLES)

cs: $(CSFILES)

# Jupyter notebooks → pdf
out/%.pdf: %.ipynb
	@mkdir -p $(dir $@)
	jupyter nbconvert $< \
		--to webpdf \
		--template lab \
		--embed-images \
		--HTMLExporter.sanitize_html=False \
		--HTMLExporter.embed_mathjax=True \
		--TemplateExporter.exclude_input_prompt=True \
		--output-dir $(dir $@) \
		--output $(basename $(notdir $<))

# Markdown files → pdf (A4 + footer + page numbers + Arabic font)
out/%.pdf: %.md
	@mkdir -p $(dir $@)
	pandoc $< \
		--pdf-engine=xelatex \
		-V papersize:A4 \
		-V geometry:margin=2.5cm \
		-V mainfont="Amiri" \
		-V footer-right="الأستاذ محمود اغبارية" \
		-V footer-left="مدرسة التسامح الشاملة" \
		-V footer-center="\thepage" \
		-o $@

# Jupyter notebooks → printable pdf (only markdown cells)
out/%_printable.pdf: %.ipynb
	@mkdir -p $(dir $@)
	jupyter nbconvert $< \
		--to webpdf \
		--template lab \
		--embed-images \
		--HTMLExporter.exclude_input=True \
		--HTMLExporter.exclude_output=True \
		--HTMLExporter.sanitize_html=False \
		--TemplateExporter.exclude_input_prompt=True \
		--output-dir $(dir $@) \
		--output $(basename $(notdir $<))_printable

# Jupyter notebooks → C# source file (only code cells)
out/%.cs: %.ipynb
	@mkdir -p $(dir $@)
	python scripts/export_cs.py $< $@

clean:
	rm -rf out
