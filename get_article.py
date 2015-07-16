#!/usr/bin/env python3
__author__ = 'bernhard'

import sys
import re
import os
import nltk

import wikipedia
wikipedia.set_lang('en')  # set english as default language

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


def __get_content(article_name):
    """
    Writes the content of the given article on the english Wikipedia to file
    with the same name as the given article name.
    The output will be split on sentences with one sentence on each line.

    :param article_name: name of the article
    :type article_name: str
    :return:
    """

    content = ""

    try:
        page = wikipedia.page(title=article_name)
        content = page.content
    except wikipedia.PageError as e:
        raise PageNotFoundException("The page '{}' does not exist.".format(article_name))
    except wikipedia.DisambiguationError as e:
        raise PageNotFoundException("The page '{}' has multiple entries: {}".format(article_name, e.options))

    # clean headings and other useless stuff
    for key in REMOVES:
        content = re.sub(
            pattern=PATTERN[key],
            repl="",
            string=content,
            flags=PATTERN_PARAMS[key]
        )

    if content is "":
        raise PageNotFoundException("The content of the page '{}' is empty.".format(article_name))
    else:
        return '\n'.join(nltk.sent_tokenize(text=content))  # one sentence per line


def get_content(article_name):
    return __get_content(article_name)


def write_to_file(article_name):
    content = get_content(article_name)

    filename = re.sub(r'\W', repl='-', string=article_name) + '.txt'
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, mode='w') as outfile:
        outfile.write(content)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Must give the page name")
    else:
        get_content(sys.argv[1])


class PageNotFoundException(Exception):

    def __init__(self, message=""):
        self.message = message
