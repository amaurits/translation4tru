# coding=utf-8

# translation4tru.py

# by A. Maurits van der Veen

# Modification history:
# - 2022-05-05: extract from other code files, to provide standalone translation
#               for the translation4tru repository on Github

# Functions to perform word-level translation across multiple languages.

# *****************************************************************************

def load_cleanpairs(infile, reverse=False, usecsv=False):
    """Load set of source-target word pairs. Assume no duplicates.

    1 pair per line, separated by space.
    Source comes first, unless reverse=True.
    """
    import os
    import csv

    pairs = {}
    if os.path.exists(infile):
        with open(infile, 'r', errors='ignore') as inf:
            if usecsv:
                for row in csv.reader(inf):
                    if len(row) != 2:
                        continue
                    if reverse:
                        pairs[row[1]] = row[0]
                    else:
                        pairs[row[0]] = row[1]
            else:  # pairs are separated by space
                for line in inf:
                    row = line.split()
                    if len(row) != 2:
                        continue
                    if reverse:
                        pairs[row[1]] = row[0]
                    else:
                        pairs[row[0]] = row[1]
    return pairs


def translate_text(text, translation_dict, oov_marker='*oov*', keeplines=True):
    """Translate a text using dictionary. Return translated text & list of oov words.

    To do a line-by-line translation, set keeplines to True

    Note: because we only translate words, and not non-words (i.e. punctuation),
    the translation will not have those non-words in it!!
    """
    import re
    word_def = "(?u)\\b[\\w-]+\\b"

    linejoiner = '\n' if keeplines else ' '
    translatedlines, unknownwords = [], []

    for line in text.split('\n'):
        translatedwords = []
        for word in re.findall(word_def, line):
            if word in translation_dict:
                translatedwords.append(translation_dict[word])
            elif '-' in word:  # might be hyphenated
                hyphtrans = []
                for subword in word.split('-'):
                    if subword in translation_dict:
                        hyphtrans.append(translation_dict[subword])
                    else:  # pre-pend oov-marker and copy to translated text
                        hyphtrans.append(oov_marker + subword)
                        unknownwords.append(subword)
                translatedwords.append('-'.join(hyphtrans))
            else:  # pre-pend oov-marker and copy to translated text
                translatedwords.append(oov_marker + word)
                unknownwords.append(word)
        translatedlines.append(' '.join(translatedwords))
    return linejoiner.join(translatedlines), unknownwords


def translate_corpus(corpusfile, outputfile, translation_dict,
                     oov_marker='*oov*', header=False, textcol=1, keeplines=True,
                     update_interval=1000, show_unknown=True, track_unknown=True):
    """Translate corpus using translation_dict.

    Any oov words get copied over, with oov marker pre-pended.
    (To copy over cleanly, just set oov_marker to empty string.)

    Optionally track, display info about, and return unknown words as FD

    Note: To be sure to translate all words, first generate a wordlist/freqdict for the corpus,
    call new_wordlist on it, and then generate translations for the unknown words.
    """
    from datetime import datetime
    import csv

    csv.field_size_limit(1000000000)

    allunknownwords = set()
    unknownFD = {}

    with open(corpusfile, 'r', encoding='utf-8') as inf, \
            open(outputfile, 'w', encoding='utf-8', newline='') as outf:
        inreader = csv.reader(inf)
        outwriter = csv.writer(outf)

        rows2write = []
        if header:
            rows2write.append(next(inreader))

        for counter, row in enumerate(inreader):
            transl_text, unknownwords = translate_text(row[textcol], translation_dict,
                                                       oov_marker=oov_marker, keeplines=keeplines)
            if len(unknownwords) > 0:
                unknownset = set(unknownwords)
                allunknownwords |= unknownset
                if show_unknown:
                    print('Unknown words in row {}: {}'.format(counter, unknownset))
                if track_unknown:
                    for word in unknownwords:
                        if word in unknownFD:
                            unknownFD[word] += 1
                        else:
                            unknownFD[word] = 1
            row[textcol] = transl_text
            rows2write.append(row)

            if (counter + 1) % update_interval == 0:
                outwriter.writerows(rows2write)
                rows2write = []
                print('processed {} texts'.format(counter + 1))

        # Write out remaining translated rows
        outwriter.writerows(rows2write)
        print('processed {} texts'.format(counter + 1))

    print("\nFinished at {}".format(datetime.now()))

    if track_unknown:
        return counter + 1, allunknownwords, unknownFD
    else:
        return counter + 1, allunknownwords


# ************************ testing/displaying translations **********************


def display_translation_byrow(sourcefile, targetfile, rows2check,
                              textcol=1):
    """Display source text and target text below one another, for visual comparison.

    Do this for each row in rows2check.
    """
    import csv

    csv.field_size_limit(1000000000)

    rows2check = set(rows2check)
    with open(sourcefile, 'r', encoding='utf-8') as sourcef, \
            open(targetfile, 'r', encoding='utf-8') as targetf:
        sourcereader = csv.reader(sourcef)
        targetreader = csv.reader(targetf)

        for rownr, (sourcerow, targetrow) in enumerate(zip(sourcereader, targetreader)):
            if rownr in rows2check:
                print('\n*** text row {} ***'.format(rownr))
                print('\nSource:')
                print(sourcerow[textcol])
                print('\nTarget:')
                print(targetrow[textcol])
                rows2check.remove(rownr)
                if len(rows2check) == 0:
                    break  # end for loop


def display_translation_bycontent(sourcefile, targetfile, source_searchstring, firstN,
                                  textcol=1):
    """Display source text and target text below one another, for visual comparison.

    Do this for the firstN hits found for the source language searchstring provided.
    """
    import csv

    csv.field_size_limit(1000000000)

    nrfound = 0

    with open(sourcefile, 'r', encoding='utf-8') as sourcef, \
            open(targetfile, 'r', encoding='utf-8') as targetf:
        sourcereader = csv.reader(sourcef)
        targetreader = csv.reader(targetf)

        for rownr, (sourcerow, targetrow) in enumerate(zip(sourcereader, targetreader)):
            sourcetext = sourcerow[textcol]
            if source_searchstring in sourcetext:
                print('\n*** text row {} ***'.format(rownr))
                print('\nSource:')
                print(sourcerow[textcol])
                print('\nTarget:')
                print(targetrow[textcol])
                nrfound += 1
                if nrfound >= firstN:
                    break  # end for loop
