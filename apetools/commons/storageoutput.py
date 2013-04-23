
#python libraries
import os
import time
import copy
#from types import StringType
import shutil


# apetools libraries
from apetools.baseclass import BaseClass
#from assertions import assert_is
from errors import StorageError


WRITEABLE = 'w'
APPEND = 'a'
NEWLINE_ADD = '{l}\n'
TIMESTAMP_FLAG = "{t}"
NEWLINE = "\n"
IPERF_TIMESTAMP = "%Y%m%d%H%M%S"
FOLDER_TIMESTAMP = "%Y_%m_%d"


class StorageOutput(BaseClass):
    """
    A StorageOutput maintains an output file.
    """
    def __init__(self, output_folder, timestamp_format=IPERF_TIMESTAMP, *args, **kwargs):
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
                self.output_folder = self.timestamp(self.output_folder, FOLDER_TIMESTAMP)
            if not os.path.isdir(self.output_folder):
                os.makedirs(self.output_folder)
            self._path = self.output_folder
        return self._path

    def extend_path(self, subdirectory):
        """
        Extends the current path with the given sub-directory.
        
        :param:

         - `subdirectory`: a path to add to the current path

        :postcondition:

         -`self.output_folder` extended with subdirectory
         - `self._path` is None
        """
        self._path = None
        self.output_folder = os.path.join(self.output_folder, subdirectory)
        return

    def is_file(self, filename, subdir=None):
        """
        Checks if the file exists within the known path
        
        :param:

         - `filename`: The name of the file to open 
         - `subdir`: A subdirectory whithin the output folder to put the file in.
         
        :return: True if file exists, False otherwise
        """
        if subdir is not None:
            dirname = os.path.join(self.path, subdir)
        else:
            dirname = self.path
        return os.path.isfile(os.path.join(dirname, filename))

    def get_full_path(self, filename):
        """
        Returns the filename with the (relative) path 
        
        :param:

         - `filename`: name of file

        :return: path to filename in output folder
        :postcondition: output folder exists
        """
        return os.path.join(self.output_folder, filename)
    
    def open(self, filename, subdir=None, mode=WRITEABLE):
        """
        Opens a writeable file using the stored path information 
        
        :param:

         - `filename`: The name of the file to open 
         - `subdir`: A subdirectory whithin the output folder to put the file in.
         
        :return: A clone of this object with a new file opened.
        """
        self.filename = self.get_filename(filename, subdir, mode)
        #self.logger.debug("Opening File: {0}".format(self.filename))
        clone = copy.deepcopy(self)
        clone.output_file = open(self.filename, mode)
        return clone

    def get_filename(self, filename, subdir=None, mode=WRITEABLE):
        """
        Builds a super-filename with the path and numbering

         * This was broken out so that other file-related classes can use it

        :param:

         - `filename`: a filename around which to build the new name
         - `subdir`: A sub-directory of self.path
         - `mode`: file-mode (writeable or appendable)

        :return: the path to the output file
        """
        filename, extension = os.path.splitext(filename)
        directory = self.path
        if subdir is not None:
            directory = os.path.join(self.path, subdir)
            if not os.path.isdir(directory):
                os.makedirs(directory)
        if mode != APPEND:
            filename = self.timestamp(filename)
            filename = self._fix_duplicate_names(filename, extension, subdir)
        filename += extension
        return os.path.join(directory, filename)


    def timestamp(self, name, timestamp_format=None):
        """
        Checks for a '{t}' in the string for a placeholder
        
        :return: name with timestamp
        """
        if timestamp_format is None:
            timestamp_format = self.timestamp_format
        timestamp = time.strftime(timestamp_format)
        if timestamp in name or TIMESTAMP_FLAG not in name:
            return name
        return name.format(t=timestamp)
        
    def _fix_duplicate_names(self, name, extension, subdir=None):
        """
        Checks if the name exists as a prefix and adds a number if it does.

        :return: uniqued name
        """
        if subdir is not None:
            dirname = os.path.join(self.path, subdir)
        else:
            dirname = self.path
        count = sum((1 for filename in os.listdir(dirname) if filename.startswith(name)
                     and filename.endswith(extension)))
        if count > 0:
            name = "{0}_{1}".format(name, str(count+1).zfill(3))
        return name

    def write(self, line):
        """
        Write a line to the file
        
        :param:

         - `line`: A string to send to the output_file
        """
        try:
            #assert_is(type(line), StringType)
            self.output_file.write(line)
            self.output_file.flush()
            os.fsync(self.output_file.fileno())
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

         - `line`: string to add to (if it doesn't have one) then send to output 
        """
        if not line.endswith(NEWLINE):
            line = NEWLINE_ADD.format(l=line)
        self.write(line)
        return

    def writelines(self, lines):
        """
        Write all the lines to the output file
        
        :param:

         - `lines`: iterable of strings to send to the file
        """
        for line in lines:
            self.write(line)
        return

    def copy(self, source, subdir=None):
        """
        Copy the file to a subdirectory
        
        :param:

         - `source`: The path to a file.
         - `subdir`: subfolder in the output folder

        :postcondition: file in path is copied to output folder.
        """
        directory = self.path
        if subdir is not None:
            directory = os.path.join(self.path, subdir)
            if not os.path.isdir(directory):
                os.makedirs(directory)
        filename = os.path.basename(source)
        root, ext = os.path.splitext(filename)
        filename = self._fix_duplicate_names(root, ext) + ext
        target = os.path.join(directory, filename)
        try:
            shutil.copy(source, target)
        except IOError as error:
            self.logger.error(error)
        return

    def move(self, source, subdir=None):
        """
        Move the file to a subdirectory.
        :param:

         - `source`: The path to a file or directory to move to the output folder.
         - `subdir`: a subdirectory to make within the output folder.
        """
        directory = self.path
        if subdir is not None:
            directory = os.path.join(self.path, subdir)
            if not os.path.isdir(directory):
                os.path.makedirs(directory)
        filename = os.path.basename(source)
        root, ext = os.path.splitext(filename)
        filename = self._fix_duplicate_names(root, ext) + ext
        target = os.path.join(directory, filename)
        try:
            shutil.move(source, target)
        except IOError as error:
            self.logger.error(error)
        return

    def close(self):
        """
        Close the output filen
        :postcondition:

         - self.output_file is flushed
         - self.output_file is closed
        """
        if self.output_file is not None:
            try:
                self.output_file.flush()
                os.fsync(self.output_file.fileno())
                self.output_file.close()
            except ValueError as error:
                self.logger.debug("File already closed?: {0}".format(error))
        return

    def __del__(self):
        """
        Destructor
        
        :postcondition: self.close called
        """
        self.close()
        return
# end class StorageOutput
