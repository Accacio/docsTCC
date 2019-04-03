all: clean
	cp *.pdf ../

tables: table/initial table/metal table/plastic table/armBeltToPress table/press table/armPressToStorage table/storageY table/storageX table/storePiece table/complete

table/initial:
	@emacs ../../tables/1-initialization/initial.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/metal:
	@emacs ../../tables/2-metalv/metalv.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/plastic:
	@emacs ../../tables/3-plastic^/plastic.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/armBeltToPress:
	@emacs ../../tables/4-armBeltToPress/armBeltToPress.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;\

table/press:
	@emacs ../../tables/5-press/press.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;\

table/armPressToStorage:
	@emacs ../../tables/6-armPressToStorage/armPressToStorage.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/storageY:
	@emacs ../../tables/7-storageY/storageY.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/storageX:
	@emacs ../../tables/8-storageX/storageX.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/storePiece:
	@emacs ../../tables/9-storePiece/storePiece.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

table/complete:
	@emacs ../../tables/completo/completo.org --batch --eval="(org-latex-export-to-latex nil nil nil t)" --kill;

petriNets: petriNet/initial petriNet/metal petriNet/plastic petriNet/armBeltToPress petriNet/press petriNet/armPressToStorage petriNet/storageY petriNet/storageX petriNet/storePiece petriNet/complete

petriNet/initial:
	dot2petri ../../figures/petriNets/dot/1-initialization/initial.dot -y

petriNet/metal:
	dot2petri ../../figures/petriNets/dot/2-metalv/metalv.dot -y

petriNet/plastic:
	dot2petri ../../figures/petriNets/dot/3-plastic^/plastic.dot -y

petriNet/armBeltToPress:
	dot2petri ../../figures/petriNets/dot/4-armBeltToPress/armBeltToPress.dot -y

petriNet/press:
	dot2petri ../../figures/petriNets/dot/5-press/press.dot -y

petriNet/armPressToStorage:
	dot2petri ../../figures/petriNets/dot/6-armPressToStorage/armPressToStorage.dot -y

petriNet/storageY:
	dot2petri ../../figures/petriNets/dot/7-storageY/storageY.dot -y

petriNet/storageX:
	dot2petri ../../figures/petriNets/dot/8-storageX/storageX.dot -y

petriNet/storePiece:
	dot2petri ../../figures/petriNets/dot/9-storePiece/storePiece.dot -y

petriNet/complete:
	dot2petri ../../figures/petriNets/dot/completo/completo.dot  -y

clean:
	@cleanLatex
