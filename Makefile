SHELL := /bin/bash

.PHONY: all pdf printable ipynb md cs tex clean soft-clean

# Find all ipynb, md, tex under src
NB  := $(shell find src -name "*.ipynb")
MD  := $(shell find src -name "*.md")
TEX := $(shell find src -name "*.tex")

# Remove the leading src/ so that out/... mirrors structure inside src
NB_REL  := $(patsubst src/%,%,$(NB))
MD_REL  := $(patsubst src/%,%,$(MD))
TEX_REL := $(patsubst src/%,%,$(TEX))

# Map input paths to outputs
IPYNB := $(patsubst %.ipynb,out/%.pdf,$(NB_REL))
MDS   := $(patsubst %.md,out/%.pdf,$(MD_REL))
TEXS  := $(patsubst %.tex,out/%.pdf,$(TEX_REL))

PRINTABLE_NB  := $(patsubst %.ipynb,out/%_printable.pdf,$(NB_REL))
PRINTABLE_TEX := $(patsubst %.tex,out/%_printable.pdf,$(TEX_REL))

CSFILES := $(patsubst %.ipynb,out/%.cs,$(NB_REL))

# -----------------------
# Targets
# -----------------------

all: pdf printable cs md tex

pdf: ipynb md tex

ipynb: $(IPYNB)

printable: $(PRINTABLE_NB) $(PRINTABLE_TEX)

md: $(MDS)

cs: $(CSFILES)

tex: $(TEXS)

# -----------------------
# Rules
# -----------------------

# Jupyter notebooks → printable pdf (only markdown cells)
out/%_printable.pdf: src/%.ipynb
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
out/%.cs: src/%.ipynb
	@mkdir -p $(dir $@)
	python scripts/export_cs.py $< $@

# ipynb → pdf
out/%.pdf: src/%.ipynb
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
out/%.pdf: src/%.md
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

# tex → pdf with code
out/%.pdf: src/%.tex
	@echo "Building regular PDF for $< -> $@"
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setwithcode{\withcodetrue} \input{$<}"
	xelatex -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setwithcode{\withcodetrue} \input{$<}"


# tex → printable pdf without code
out/%_printable.pdf: src/%.tex
	@echo "Building printable PDF for $< -> $@"
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setwithcode{\withcodefalse} \input{$<}"
	xelatex -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setwithcode{\withcodefalse} \input{$<}"



# -----------------------
# Cleaning
# -----------------------

clean:
	rm -rf out

soft-clean:
	# remove empty files
	find out -type f -empty -delete
	# remove .log, .aux, .toc files
	find out -type f \( -name "*.log" -o -name "*.aux" -o -name "*.toc" \) -delete
	# remove _printable.pdf if same size as main pdf
	find out -type f -name '*_printable.pdf' | while read -r f; do \
	  orig="$${f%_printable.pdf}.pdf"; \
	  [ -f "$$orig" ] || continue; \
	  size_orig=$$(stat -c %s "$$orig"); \
	  size_print=$$(stat -c %s "$$f"); \
	  if [ "$$size_orig" -eq "$$size_print" ]; then \
	    echo "Removing duplicate $$f"; \
	    rm -f "$$f"; \
	  fi; \
	done
