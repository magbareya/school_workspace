SHELL := /bin/bash

.NOTPARALLEL:
.SUFFIXES:
.PHONY: all pdf printable cs md tex clean soft-clean

# Find all ipynb and md files recursively
NB := $(shell find . -name "*.ipynb")
MD := $(shell find . -name "*.md" ! -iname "README.md")
TEX := $(shell find . -name "*.tex")

# Map input paths (./X.ipynb → out/X.pdf)
IPYNB := $(patsubst ./%.ipynb,out/%.pdf,$(NB))
MDS  := $(patsubst ./%.md,out/%.pdf,$(MD))
TEXS  := $(patsubst ./%.tex,out/%.pdf,$(TEX))

PRINTABLES := $(patsubst ./%.ipynb,out/%_printable.pdf,$(NB))
CSFILES := $(patsubst ./%.ipynb,out/%.cs,$(NB))

all: pdf printable cs md tex soft-clean

pdf: ipynb md tex soft-clean

ipynb: $(IPYNB)

printable: $(PRINTABLES)

md: $(MDS)

cs: $(CSFILES)

tex: $(TEXS)

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

# ipynb → pdf
$(IPYNB): out/%.pdf : %.ipynb
	@mkdir -p $(dir $@)
	jupyter nbconvert $< \
		--to webpdf \
		--template lab \
		--embed-images \
		--HTMLExporter.sanitize_html=False \
		--TemplateExporter.exclude_input_prompt=True \
		--output-dir $(dir $@) \
		--output $(basename $(notdir $<))

# md → pdf
$(MDS): out/%.pdf : %.md
	@mkdir -p $(dir $@)
	pandoc $< \
		--pdf-engine=xelatex \
		--number-sections \
		--toc --toc-depth=2 \
		-V papersize:A4 \
		-V geometry:margin=2.5cm \
		-V mainfont="Amiri" \
		-V lang=ar \
		-V footer-center="\thepage" \
		-o $@

# tex → pdf
$(TEXS): out/%.pdf : %.tex
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) $<

clean:
	rm -rf out

soft-clean:
	# remove empty files
	find out -type f -empty -delete
	# remove .log and .aux files
	find out -type f \( -name "*.log" -o -name "*.aux" \) -delete
	# remove _printable.pdf if same size as main pdf
	for f in out/**/*_printable.pdf; do \
	  [ -f "$$f" ] || continue; \
	  orig="$${f%_printable.pdf}.pdf"; \
	  [ -f "$$orig" ] || continue; \
	  size_orig=$$(stat -c %s "$$orig"); \
	  size_print=$$(stat -c %s "$$f"); \
	  if [ "$$size_orig" -eq "$$size_print" ]; then \
	    echo "Removing duplicate $$f"; \
	    rm -f "$$f"; \
	  fi; \
	done
