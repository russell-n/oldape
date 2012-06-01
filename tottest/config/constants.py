"""
Constants needed to parse the config file.
"""

from string import whitespace
STRIP_LIST = "'\"" + whitespace
TIME_STAMP_FOLDER = "{name}_{stamp}"
TIME_FORMAT = "%Y_%m_%d_%a"


CONFIG_FOLDER = "config"
DEFAULTS = ["ttr.ini", 'source_this_for_sl4a', 'readme_useme_loveme']
