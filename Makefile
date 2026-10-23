# Builds every LaTeX document in papers/ and research-notes/ to PDF, each in its own directory.
# The bibliography of other people's work is the external repository
# davidbarkhuizen/indrajala-literature (library.bib); clone it beside this one, or point
# LITERATURE at your clone: make LITERATURE=/path/to/indrajala-literature
# A build fails on a LaTeX error and on any undefined reference or citation.
LITERATURE ?= ../indrajala-literature
SOURCES := $(wildcard papers/*.tex research-notes/*.tex)
BIBINPUTS := $(abspath $(LITERATURE)):$(CURDIR):

all: $(SOURCES:.tex=.pdf)

%.pdf: %.tex extra.bib $(LITERATURE)/library.bib
	@test -f $(LITERATURE)/library.bib || { echo "missing $(LITERATURE)/library.bib: clone git@github.com:davidbarkhuizen/indrajala-literature.git"; exit 1; }
	BIBINPUTS=$(BIBINPUTS) latexmk -cd -pdf -interaction=nonstopmode -halt-on-error $<
	@! grep -E "There were undefined (references|citations)|Citation .* undefined" $*.log || { echo "$<: undefined references"; exit 1; }

clean:
	for f in $(SOURCES); do latexmk -cd -C $$f; done

.PHONY: all clean
