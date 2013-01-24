# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.'
"""
A place to hold the set_logger function. This has to be at the top-level so that modules in sub-folders can use it.
"""
# Python Libraries
import logging
import logging.handlers
import os

logger = logging.getLogger(__package__)
SMALL_TIMESTAMP = "%H:%M:%S"
SCREEN_FORMAT = "%(levelname)s: %(name)s.%(funcName)s, Line: %(lineno)d [%(asctime)s] -- %(message)s"
SCREEN_FORMAT_QUIET = "%(levelname)s: [%(asctime)s] -- %(message)s"
DATA_FRIENDLY_FORMAT = "%(levelname)s,%(asctime)s,%(message)s"
LOG_FORMAT = "%(levelname)s,%(module)s,%(threadName)s,%(funcName)s,Line: %(lineno)d,%(asctime)s,%(message)s" 
LOG_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

GIGABYTE = 1073741824
BACKUP_LOGS = 5

LOGNAME = "{0}.log".format(__package__)

def cleanup(log_directory="last_log"):
    """
    Saves the last log to sub-directory

    :param:

     - `log_directory`: sub-directory to save old file to

    :postconditions:

     - `log_directory` is a sub-directory of the current directory (if log exists)
     - log-file is moved to the log-directory (if log existed)
    """
    if not os.path.isfile(LOGNAME):
        return
    if not os.path.isdir(log_directory):
        os.makedirs(log_directory)
    os.rename(LOGNAME, os.path.join(log_directory, LOGNAME))
    return

def set_logger(args):
    """
    Creates a logger and sets the level based on args.

    :param:

     - `args`: args with debug and silent attributes
    """
    cleanup()
    stderr = logging.StreamHandler()
    if args.debug:
        screen_format = SCREEN_FORMAT
    else:
        screen_format = SCREEN_FORMAT_QUIET
        
    screen_format = logging.Formatter(screen_format, datefmt=SMALL_TIMESTAMP)
    stderr.setFormatter(screen_format)

    log_file = logging.handlers.RotatingFileHandler(LOGNAME,
                                           maxBytes=GIGABYTE, backupCount=BACKUP_LOGS)
    file_format = logging.Formatter(LOG_FORMAT, datefmt=LOG_TIMESTAMP)
    log_file.setFormatter(file_format)
    
    logger.setLevel(logging.DEBUG)
    log_file.setLevel(logging.DEBUG)

    if args.debug:
        stderr.setLevel(logging.DEBUG)
    elif args.silent:
        stderr.setLevel(logging.ERROR)
    else:
        stderr.setLevel(logging.INFO)

    logger.addHandler(stderr)
    logger.addHandler(log_file)
    return 

