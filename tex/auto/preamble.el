(TeX-add-style-hook
 "preamble"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("babel" "brazil") ("fontenc" "T1")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "inputenc"
    "babel"
    "fontenc"
    "graphicx"
    "subcaption"
    "hyperref"
    "amsmath"
    "amssymb"
    "indentfirst"
    "mathptmx"
    "pdfpages"
    "multirow"
    "color"
    "blindtext"
    "float"
    "nameref"
    "multicol"
    "listings"
    "enumerate"
    "tikz"
    "ladder")
   (TeX-add-symbols
    '("todo" ["argument"] 1)
    '("note" 1)
    '("warning" 1)
    '("doing" 1)
    '("figplaceholder" 2)
    '("symbl" 3)
    '("acr" 3)
    "draft"
    "final"
    "oldsection"
    "oldsubsection"
    "oldsubsubsection"
    "oldtoc")
   (LaTeX-add-labels
    "tocsection"
    "fig:#2")
   (LaTeX-add-environments
    "example"
    "theorem"
    "observation"))
 :latex)

