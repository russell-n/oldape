"""
A module to hold the generators for the concatenator.
"""

# python libraries
import fnmatch
import os
import re

WRITEABLE = 'w'
EOSection = ''

def find(glob, start=None):
    """
    :param:

     - `glob`: A file-glob to match interesting files.
     - `start`: The top path (finds files below the top)

    :yield: Matching file name
    """
    if start is None:
        start = os.getcwd()
    for path, dir_list, file_list in os.walk(start):
        for name in fnmatch.filter(file_list, glob):
            yield os.path.join(path, name)
    return

def concatenate(glob, start=None):
    """
    :param:

     - `glob`: A file-glob to match interesting files.
     - `start`: The top path (finds files below the top)

    :yield: lines in matching files.
    """
    for name in find(glob, start):
        for line in open(name):
            yield line
    return

def sections(glob, start, end, top=None):
    """
    :param:

     - `glob`: A file glob that matches source files
     - `start`: A regular expression to match the start of a section.
     - `end`: A regular expression to match the end of a section.
     - `top`: The starting path to search for files

    :yield: section generator of lines
    """
    start, end = re.compile(start), re.compile(end)
    concatenator = concatenate(glob, top)
    for line in concatenator:
        if start.search(line):
            yield section(concatenator, end, line)
    return

def section(iterator, end, firstline=None):
    """
    :param:

     - `iterator`: An iterator of lines
     - `end`: A regular expression to match the last line in the section

    :yield: lines up to and including the end match
    """
    ended = False
    if firstline is not None:
        yield firstline
    # uses next instead of iterator so it doesn't consume the last line
    while not ended:
        try:
            line = iterator.next()
            if end.search(line):
                ended = True
            yield line
        except StopIteration:
            return
            
def line_counter(glob, start, end, interesting):
    """
    Counts interesting lines within sections

    :param:

     - `glob`: the glob for the source files.
     - `start`: regular expression that defines the start of a section
     - `end`: end of section regular expression
     - `interesting`: interesting line regular expression

    :yield: count of interesting lines in each section
    """
    start, end, interesting = re.compile(start), re.compile(end), re.compile(interesting)
    for section in sections(glob, start, end):
        counter = 0
        for line in section:
            if interesting.search(line):
                counter += 1
        yield counter
