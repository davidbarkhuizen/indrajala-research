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

# arXiv source packages (docs/workplans/arxiv-posting-workplan.md, D5), built from the release tags with
# scripts/arxiv_package.py into ARXIV_OUT, which must not exist. Each package's text is compared with its
# released PDF from Zenodo, fetched into ARXIV_OUT/released.
ARXIV_OUT ?= arxiv-packages
PAPER1_PDF := https://zenodo.org/api/records/23826655/files/learning-transducers-with-proof.pdf/content
CERTNOTE_PDF := https://zenodo.org/api/records/23972277/files/proving-a-trained-network-is-a-finite-state-machine.pdf/content

arxiv:
	@test ! -e $(ARXIV_OUT) || { echo "$(ARXIV_OUT) exists; set ARXIV_OUT to a new directory"; exit 1; }
	mkdir -p $(ARXIV_OUT)/released
	curl -sSfL -o $(ARXIV_OUT)/released/paper1.pdf $(PAPER1_PDF)
	curl -sSfL -o $(ARXIV_OUT)/released/certnote.pdf $(CERTNOTE_PDF)
	python3 -I -B scripts/arxiv_package.py --literature $(LITERATURE) --compare $(ARXIV_OUT)/released/paper1.pdf \
		paper1-v1.2 papers/learning-transducers-with-proof.tex $(ARXIV_OUT)/paper1
	python3 -I -B scripts/arxiv_package.py --literature $(LITERATURE) --compare $(ARXIV_OUT)/released/certnote.pdf \
		certnote-v1 research-notes/certificate-method.tex $(ARXIV_OUT)/certnote

clean:
	for f in $(SOURCES); do latexmk -cd -C $$f; done

.PHONY: all clean arxiv
