all: clean
	cp *.pdf ../

tables: table/initial table/metal table/plastic table/armBeltToPress table/press table/armPressToStorage table/storageY table/storageX table/storePiece table/complete

table/initial:
	@emacs ../../tables/1-initialization/initial.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables ../../tables/1-initialization/initial.tex

table/metal:
	@emacs ../../tables/2-metalv/metalv.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables ../../tables/2-metalv/metalv.tex

table/plastic:
	@emacs ../../tables/3-plastic^/plastic.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables ../../tables/3-plastic^/plastic.tex

table/armBeltToPress:
	@emacs ../../tables/4-armBeltToPress/armBeltToPress.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/4-armBeltToPress/armBeltToPress.tex

table/press:
	@emacs ../../tables/5-press/press.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/5-press/press.tex

table/armPressToStorage:
	@emacs ../../tables/6-armPressToStorage/armPressToStorage.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/6-armPressToStorage/armPressToStorage.tex

table/storageY:
	@emacs ../../tables/7-storageY/storageY.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/7-storageY/storageY.tex

table/storageX:
	@emacs ../../tables/8-storageX/storageX.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/8-storageX/storageX.tex

table/storePiece:
	@emacs ../../tables/9-storePiece/storePiece.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;
	linkTables	../../tables/9-storePiece/storePiece.tex

table/complete:
	@emacs ../../tables/completo/completo.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

petriNets: petriNet/initial petriNet/metal petriNet/plastic petriNet/armBeltToPress petriNet/press petriNet/armPressToStorage petriNet/storageY petriNet/storageX petriNet/storePiece 

petriNet/initial:
	dot2petri ../../figures/petriNets/dot/1-initialization/initial.dot -py
	linkPetriNets ../../figures/petriNets/dot/1-initialization/initial.tex

petriNet/metal:
	dot2petri ../../figures/petriNets/dot/2-metalv/metalv.dot -py
	linkPetriNets ../../figures/petriNets/dot/2-metalv/metalv.tex

petriNet/plastic:
	dot2petri ../../figures/petriNets/dot/3-plastic^/plastic.dot -py
	linkPetriNets ../../figures/petriNets/dot/3-plastic^/plastic.tex

petriNet/armBeltToPress:
	dot2petri ../../figures/petriNets/dot/4-armBeltToPress/armBeltToPress.dot -py
	linkPetriNets ../../figures/petriNets/dot/4-armBeltToPress/armBeltToPress.tex

petriNet/press:
	dot2petri ../../figures/petriNets/dot/5-press/press.dot -py
	linkPetriNets ../../figures/petriNets/dot/5-press/press.tex

petriNet/armPressToStorage:
	dot2petri ../../figures/petriNets/dot/6-armPressToStorage/armPressToStorage.dot -py
	linkPetriNets ../../figures/petriNets/dot/6-armPressToStorage/armPressToStorage.tex

petriNet/storageY:
	dot2petri ../../figures/petriNets/dot/7-storageY/storageY.dot -py
	linkPetriNets ../../figures/petriNets/dot/7-storageY/storageY.tex

petriNet/storageX:
	dot2petri ../../figures/petriNets/dot/8-storageX/storageX.dot -py
	linkPetriNets ../../figures/petriNets/dot/8-storageX/storageX.tex

petriNet/storePiece:
	dot2petri ../../figures/petriNets/dot/9-storePiece/storePiece.dot -py
	linkPetriNets ../../figures/petriNets/dot/9-storePiece/storePiece.tex

petriNet/complete:
	dot2petri ../../figures/petriNets/dot/completo/completo.dot  -py

clean:
	@cleanLatex
