# Builds every paper in this directory to PDF.
# The bibliography of other people's work is the external repository
# davidbarkhuizen/indrajala-literature (library.bib); clone it beside this one, or point
# LITERATURE at your clone: make LITERATURE=/path/to/indrajala-literature
LITERATURE ?= ../indrajala-literature
PAPERS := $(basename $(wildcard *.tex))

all: $(addsuffix .pdf,$(PAPERS))

%.pdf: %.tex extra.bib $(LITERATURE)/library.bib
	@test -f $(LITERATURE)/library.bib || { echo "missing $(LITERATURE)/library.bib: clone git@github.com:davidbarkhuizen/indrajala-literature.git"; exit 1; }
	BIBINPUTS=$(LITERATURE): latexmk -pdf -interaction=nonstopmode -halt-on-error $<

clean:
	latexmk -C

.PHONY: all clean
