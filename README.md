# translation4tru: Translation for the rest of us
## Word-level translation for automated text analysis

Automated machine translation has been improving in quality rapidly for some years, and now approaches that of professional human translation. However, for large volume translations, these methods remain costly, in terms of money, computational resources, or time. In contrast, word-level translation is both free and fast, simply mapping each word in a source language deterministically to a target language. While the resulting translations are ungainly, for many text analysis methods this is not a problem.

This repository makes available translation dictionaries for a number languages (at the moment, 10 European languages). For each language pair, there is a dictionary file (with lines of the form `<source word>,<target word>`) and an associated translation code file (with lines of the form `<source word> <translation code>`). The translation dictionaries are generated from a combination of 1) individual word translation using DeepL and 2) aligned embeddings, applying a number of heuristics to improve the translation quality. The translation codes indicate which heuristics were used to generate the translation. 
  
A simple Jupyter notebook is supplied to translate texts from a source to a target language using one of these dictionaries, but using the notebook is not a requirement to use the dictionaries. 
  
Current languages included:
- For translation into English: French, Italian, Portuguese, Spanish, Danish, Dutch, German, Finnish, Greek, Polish
- For translation into French: Italian, Portuguese, Spanish, Dutch, English, German (these are currently created using aligned embeddings only, and are of somewhat lower quality than those for translation itno English)

The accompanying paper provides more infornation about the process generating the dictionaries, their current size, and validation tests establishing their suitability for standard text analysis purposes (including comparisons to neural machine translation output).

  
## Attribution and citation
  
These dictionaries are © A. Maurits van der Veen, 2022, and are made available under the MIT license.

If you use the dictionaries for research resulting in an academic paper/publication, please cite the accompanying paper:

        van der Veen, A. Maurits. 2022. "Translation for the rest of us: Word-level translation for automated text analysis." Williamsburg, VA: William & Mary.
  
_Last updated June 14, 2022._
