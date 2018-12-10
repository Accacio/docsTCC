(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("coppe" "grad" "numbers")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "preamble"
    "glossaires_et_symb"
    "frontMatter/dedicatoria"
    "frontMatter/thanks"
    "frontMatter/resumo"
    "frontMatter/abstract"
    "mainMatter/chap01"
    "mainMatter/chap02"
    "mainMatter/chap03"
    "mainMatter/chap04"
    "mainMatter/chap05"
    "appendices/appenA"
    "coppe"
    "coppe10")
   (LaTeX-add-bibliographies
    "thesis"))
 :latex)

