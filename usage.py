#!/usr/bin/env python3

__author__ = 'bernhard'

from wikipedia_wrapper.get_article import write_to_file, get_content

write_to_file('Jupiter')
write_to_file('Obama')
write_to_file('Paris')

# for internal use, use get_content('Jupiter')
