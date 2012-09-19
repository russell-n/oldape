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

class ShallowFind(object):
    """
    A finder of files that doesn't traverse directories
    """
    def __init__(self, glob, path=None):
        """
        :param:

         - `glob`: a file glob to match
         - `path`: an alternate to the current directory
        """
        self.glob = glob
        self._path = path
        self._filenames = None
        return

    @property
    def path(self):
        """
        :return: the path to the directory to search
        """
        if self._path is None:
            self._path = os.getcwd()
        return self._path

    @property
    def filenames(self):
        """
        :return: all files found in the path
        """
        if self._filenames is None:
            self._filenames = os.listdir(self.path)
        return self._filenames

    def reset(self):
        """
        Sets all properties to None
        """
        self._filenames = None
        self._path = None
        return

    def __iter__(self):
        """
        :yield: the matching filenames
        """
        for name in fnmatch.filter(self.filenames, self.glob):
            yield name    
        return 
# end class ShallowFind
    
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
