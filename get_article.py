#!/usr/bin/env python3
__author__ = 'bernhard'

import sys
import re
import os
import logging
import nltk

import wikipedia
wikipedia.set_lang('en')  # set english as default language

log = logging.getLogger()
log.setLevel(logging.INFO)

# The keys which PATTERN is removed from the content.
# Note, that the order is important.
REMOVES = [
    'see_also',
    'headings',
    'newlines'
]

PATTERN = {
    'newlines': r'^\n*',  # removes all blank lines
    'see_also': r'^== See also ==(.*)',  # removes everything after "See Also" (no content sentences after this)
    'headings': r'[=]+.+[=]+'  # removes all headings
}

# corresponding parameters for removing
PATTERN_PARAMS = {
    'newlines': re.UNICODE | re.MULTILINE,
    'see_also': re.UNICODE | re.MULTILINE | re.DOTALL,
    'headings': re.UNICODE
}


def get_content(article_name):
    """
    Writes the content of the given article on the english Wikipedia to file
    with the same name as the given article name.
    The output will be split on sentences with one sentence on each line.

    :param article_name: name of the article
    :type article_name: str
    :return:
    """

    article_name = article_name.lower()

    content = ""

    try:
        page = wikipedia.page(title=article_name)
        content = page.content
    except wikipedia.PageError as e:
        log.error("The page '{}' does not exist: {}".format(article_name, e.error))
        sys.exit(1)
    except wikipedia.DisambiguationError as e:
        log.error("The page '{}' has multiple entries: {}".format(article_name, e.options))

    # clean headings and other useless stuff
    for key in REMOVES:
        content = re.sub(
            pattern=PATTERN[key],
            repl="",
            string=content,
            flags=PATTERN_PARAMS[key]
        )

    if content is "":
        log.error("The content of this page is empty.")
    else:
        filename = re.sub(r'\W', repl='-', string=article_name) + '.txt'
        if os.path.isfile(filename):
            log.info("The file '{}' for the article '{}' already exists, it will be overwritten.".format(filename, article_name))
            os.remove(filename)
        with open(filename, mode='w') as outfile:
            sentences = nltk.sent_tokenize(text=content)  # tokenize sentences
            outfile.write('\n'.join(sentences))
            log.info("The content of the article '{}' was written to the file '{}'".format(article_name, filename))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Must give the page name")
    else:
        get_content(sys.argv[1])