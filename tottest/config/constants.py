"""
Constants needed to parse the config file.
"""

from string import whitespace
STRIP_LIST = "'\"" + whitespace
TIME_STAMP_FOLDER = "{name}_{stamp}"
TIME_FORMAT = "%Y_%m_%d_%a"


CONFIG_FOLDER = "config"
DEFAULTS = ["tot.ini", 'readme_useme_loveme']
