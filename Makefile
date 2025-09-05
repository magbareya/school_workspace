SHELL := /bin/bash

# Find all ipynb files recursively
NB := $(shell find . -name "*.ipynb")
PDFS := $(patsubst ./%.ipynb,out/%.pdf,$(NB))
PRINTABLES := $(patsubst ./%.ipynb,out/%_printable.pdf,$(NB))
CSFILES := $(patsubst ./%.ipynb,out/%.cs,$(NB))

all: pdf printable cs

pdf: $(PDFS)

printable: $(PRINTABLES)

cs: $(CSFILES)

out/%.pdf: %.ipynb
	@mkdir -p $(dir $@)
	jupyter nbconvert $< \
		--to webpdf \
		--template lab \
		--HTMLExporter.sanitize_html=False \
		--HTMLExporter.embed_mathjax=True \
		--TemplateExporter.exclude_input_prompt=True \
		--output-dir out \
		--output $(basename $(notdir $<))

out/%_printable.pdf: %.ipynb
	@mkdir -p $(dir $@)
	jupyter nbconvert $< \
		--to webpdf \
		--template lab \
		--HTMLExporter.exclude_input=True \
		--HTMLExporter.exclude_output=True \
		--HTMLExporter.sanitize_html=False \
		--TemplateExporter.exclude_input_prompt=True \
		--output-dir out \
		--output $(basename $(notdir $<))_printable

out/%.cs: %.ipynb
	@mkdir -p $(dir $@)
	python scripts/export_cs.py $< $@

clean:
	rm -rf out
