"""
Constants needed to parse the config file.
"""

from string import whitespace
STRIP_LIST = "'\"" + whitespace
TIME_STAMP_FOLDER = "{name}_{stamp}"
TIME_FORMAT = "%Y_%m_%d_%a"


CONFIG_FOLDER = "lexicographers/configfiles"
DEFAULTS = ["throughputovertime.ini"]
