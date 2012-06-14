"""
This module holds (a) class(es) to send lines to files.
"""

#python libraries
import os
import time
import copy
#from types import StringType
import shutil


# tottest libraries
from tottest.baseclass import BaseClass
#from assertions import assert_is
from errors import StorageError

WRITEABLE = 'w'
NEWLINE_ADD = '{l}\n'
TIMESTAMP_FLAG = "{t}"


class StorageOutput(BaseClass):
    """
    A WriteOutput maintains an output file.
    """
    def __init__(self, output_folder, timestamp_format="%Y_%m_%d", *args, **kwargs):
        """
        :param:

         - `output_folder`: name of (path to) the output folder to use.
         - `timestamp_format`: strftime timestamp format
        """
        super(StorageOutput, self).__init__(*args, **kwargs)
        self.output_folder = output_folder
        self.timestamp_format = timestamp_format
        self._path = None
        self.filename = None
        self.output_file = None
        return

    @property
    def path(self):
        """
        Adds a timestamp if there's a {t} in the name.
        
        :precondition: self.output_folder is a valid file name
        :postcondition: there exists a folder with the name in self.path
        :rtype: StringType
        :return: the path-prefix for the file output.
        """
        if self._path is None:
            if TIMESTAMP_FLAG in self.output_folder:
                self.output_folder = self._timestamp(self.output_folder)
            if not os.path.isdir(self.output_folder):
                os.makedirs(self.output_folder)
            self._path = self.output_folder
        return self._path

    def open(self, filename, extension='.csv'):
        """
        :param:

         - `filename`: The name of the file to open (minux extension)
         - `extension`: The extension to use.
         
        :return: A clone of this object with a new file opened.
        """
        filename = self._timestamp(filename)
        filename = self._fix_duplicate_names(filename, extension)
        filename += extension
        self.filename = os.path.join(self.path, filename)
        #self.logger.debug("Opening File: {0}".format(self.filename))
        clone = copy.deepcopy(self)
        clone.output_file = open(self.filename, WRITEABLE)
        return clone

    def _timestamp(self, name):
        """
        Checks for a '{t}' in the string for a placeholder
        
        :return: name with timestamp
        """
        timestamp = time.strftime(self.timestamp_format)
        if timestamp in name or TIMESTAMP_FLAG not in name:
            return name
        return name.format(t=timestamp)
        
    def _fix_duplicate_names(self, name, extension):
        """
        Checks if the name exists as a prefix and adds a number if it does.

        :return: uniqued name
        """
        count = sum((1 for filename in os.listdir(self.path) if filename.startswith(name)
                     and filename.endswith(extension)))
        if count > 0:
            name = "{0}_{1}".format(name, count+1)
        return name

    def write(self, line):
        """
        :param:

         - `line`: A string to send to the output_file
        """
        try:
            #assert_is(type(line), StringType)
            self.output_file.write(line)
            #self.output_file.flush()
            #os.fsync(self.output_file.fileno())
        except AssertionError as error:
            self.logger.error(error)
        except AttributeError as error:
            self.logger.error(error)
            raise StorageError("Unable to write to file: {0}".format(self.output_file))
        return

    def writeline(self, line):
        """
        Coerces the line to a string and adds a newline.
        
        :param:

         - `line`: A string to add a newline before sending to the output file.
        """
        self.write(NEWLINE_ADD.format(l=line))
        return

    def writelines(self, lines):
        """
        :param:

         - `lines`: iterable of strings to send to the file
        """
        for line in lines:
            self.write(line)
        return

    def copy(self, source):
        """
        :param:

         - `source`: The path to a file.

        :postcondition: file in path is copied to output folder.
        """
        filename = os.path.basename(source)
        root, ext = os.path.splitext(filename)
        filename = self._fix_duplicate_names(root, ext) + ext
        target = os.path.join(self.path, filename)
        shutil.copy(source, target)
        return

    def move(self, source):
        """
        :param:

         - `source`: The path to a file or directory to move to the output folder.
        """
        filename = os.path.basename(source)
        root, ext = os.path.splitext(filename)
        filename = self._fix_duplicate_names(root, ext) + ext
        target = os.path.join(self.path, filename)
        shutil.move(source, target)
        return

    def __del__(self):
        self.output_file.flush()
        os.fsync(self.output_file.fileno())
        self.output_file.close()
        return
# end class StorageOutput
