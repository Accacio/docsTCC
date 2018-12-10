(TeX-add-style-hook
 "coppe"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("book" "12pt" "a4paper" "oneside")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("natbib" "sort&compress") ("babel" "english" "brazil") ("geometry" "a4paper" "bindingoffset=0.0cm" "vcentering=true" "top=2.5cm" "bottom=2.5cm" "left=3.0cm" "right=3.0cm")))
   (TeX-run-style-hooks
    "latex2e"
    "book"
    "bk12"
    "natbib"
    "hyphenat"
    "lastpage"
    "babel"
    "ifthen"
    "graphicx"
    "setspace"
    "tabularx"
    "eqparbox"
    "ltxcmds"
    "geometry")
   (TeX-add-symbols
    '("dedication" 1)
    '("keyword" 1)
    '("examiner" 3)
    '("advisor" 4)
    '("foreigntitle" 1)
    '("department" 1)
    "local"
    "foreign"
    "makefrontpage"
    "makecatalog"
    "printlosymbols"
    "printloabbreviations"
    "bibindent"
    "glossaryname"
    "listabbreviationname"
    "listsymbolname"
    "frontcover"
    "frontpage"
    "abstract"
    "foreignabstract"
    "filename"
    "CoppeTeX"
    "maketitle"
    "and"
    "author"
    "date"
    "symbl"
    "makelosymbols"
    "abbrev"
    "makeloabbreviations"
    "item")
   (LaTeX-add-environments
    "abstract"
    "foreignabstract"
    "theglossary")
   (LaTeX-add-counters
    "keywords"))
 :latex)

