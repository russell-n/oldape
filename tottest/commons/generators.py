"""
A module to hold the generators for the concatenator.
"""

# python libraries
import fnmatch
import os

WRITEABLE = 'w'
EOSection = ''

def find(glob, start=None):
    """
    Matches all below cwd or start-directory
    
    :param:

     - `glob`: A file-glob to match interesting files 
     - `start`: The top path (finds files below the top)

    :yield: Matching file name
    """
    if start is None:
        start = os.getcwd()
    for path, dir_list, file_list in os.walk(start):
        for name in fnmatch.filter(file_list, glob):
            yield os.path.join(path, name)
    return

def shallow_find(glob, start = None):
    """
    Matches only in one directory
    
    :param:

     - `glob`: A file-glob to match interesting files in this directory
    """
    if start is None:
        start = os.getcwd()
    names = (name for name in os.listdir(start))
    for name in fnmatch.filter(names, glob):
        yield name
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
