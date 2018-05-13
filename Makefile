FILENAME = HSF_ML_CWP

date = $(shell date +%Y-%m-%d)
output_file = draft_$(date).pdf

figure_src = $(wildcard images/*.tex images/*/*.tex)
figure_list = $(figure_src:.tex=.pdf)

# LATEX = pdflatex
# LATEX = xelatex
LATEX = lualatex

BIBTEX = bibtex
# BIBTEX = biber

default: document copy_draft

all: default

figures: $(figure_list)

# Target assumes figure source is in same directory as expected figure path
images/%.pdf: images/%.tex
	latexmk -$(LATEX) -interaction=nonstopmode -halt-on-error $(basename $@)
	mv $(notdir $(basename $@)).pdf $(basename $@).pdf
	rm $(notdir $(basename $@)).*

text:
	latexmk -$(LATEX) -logfilewarnings -halt-on-error $(FILENAME)

document: clear_screen figures text

copy_draft:
	rsync $(FILENAME).pdf $(output_file)

clear_screen:
	clear

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.idx *.lof *.log *.lot *.toc \
		*.glg *.gls *.glo *.xdy *.nav *.out *.snm *.vrb *.mp \
		*.synctex.gz *.run.xml *.bcf *.brf *.fls *.fdb_latexmk

clean_figures:
	rm -f $(figure_list)

realclean: clean clean_figures
	rm -f *.ps *.pdf

final:
	if [ -f *.aux ]; \
		then make clean; \
	fi
	make figures
	make text
	make clean
