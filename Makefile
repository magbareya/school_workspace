SHELL := /bin/bash

.PHONY: all pdf printable sols ipynb md cs tex clean sclean

# -----------------------
# Sources
# -----------------------

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

SOLS_TEX := $(patsubst %.tex,out/%_sols.pdf,$(TEX_REL))

CSFILES := $(patsubst %.ipynb,out/%.cs,$(NB_REL))

export TEXMF_OUTPUT_DIRECTORY=.


# -----------------------
# Targets
# -----------------------

all: pdf printable sols sclean

pdf: ipynb md tex sclean
printable: $(PRINTABLE_NB) $(PRINTABLE_TEX)
sols: $(SOLS_TEX)        # <-- new target

ipynb: $(IPYNB)
md: $(MDS)
tex: $(TEXS)
cs: $(CSFILES)

hclean: sclean dclean
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
	python3 scripts/export_cs.py $< $@

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
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedtrue} \def\setwithsols{\withsolsfalse} \input{$<}"
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedtrue} \def\setwithsols{\withsolsfalse} \input{$<}"

# tex → printable pdf without code
out/%_printable.pdf: src/%.tex
	@echo "Building printable PDF for $< -> $@"
	@mkdir -p $(dir $@)
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedfalse} \def\setwithsols{\withsolsfalse} \input{$<}"
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedfalse} \def\setwithsols{\withsolsfalse} \input{$<}"

# tex → sols pdf (detailed + withsols)
out/%_sols.pdf: src/%.tex
	@echo "Building solutions PDF for $< -> $@"
	@mkdir -p $(dir $@)
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedtrue} \def\setwithsols{\withsolstrue} \input{$<}"
	TEXMF_OUTPUT_DIRECTORY=$(dir $@) xelatex -shell-escape -output-directory=$(dir $@) -jobname=$(basename $(notdir $@)) "\def\setdetailed{\detailedtrue} \def\setwithsols{\withsolstrue} \input{$<}"

# -----------------------
# Cleaning
# -----------------------

clean:
	rm -rf out
	find . -type d -name "_minted*" -exec rm -rf {} +


CLEAN_EXTS := log aux toc fls fdb_latexmk out minted pyg vrb nav snm gz
sclean:
	find out -type f -empty -delete
	@for ext in $(CLEAN_EXTS); do \
		find . -type f -name "*.$$ext" -delete; \
	done
	find . -type d -name "_minted*" -exec rm -rf {} +

dclean:
	python3 scripts/clean.py out
