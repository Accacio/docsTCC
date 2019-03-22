all:  notes clean
	cp *.pdf ../

clean:
	cleanLatex

notes:
	pdflatex -jobname presentation presentation.tex

fr: 
	pdflatex -jobname cv-Rafael_Accacio_NOGUEIRA-fr "\AtBeginDocument{\french}\input{curriculum-multilingual.tex}"

