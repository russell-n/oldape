from apetools.info.constants import TEMPLATE, BOLD, RESET, NAME_TEMPLATE, BLUE

name = NAME_TEMPLATE.format(name="ttr fetch",
                            description="(fetch needed files)").center(80)

synopsis = """
The {bold}fetch{reset} ({blue}ttr fetch{reset}) copies necessary files to the current directory.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

description = """
The {bold}ttr fetch{reset} sub-command fetches three(3) files:

    1. ttr.ini
    2. source_this_for_sl4a
    3. readme_useme_loveme

The {blue}ttr.ini{reset} file is the configuration file for the tests (see `ttr help config`). The {blue}source_this_for_sl4a{reset} file can start the `SL4A` server for you. {blue}readme_useme_loveme{reset} is a help file to remind you of what the files are for.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

examples="""
    To start the {bold}SL4a Server{reset}:

        {blue}source source_this_for_sl4a{reset}

    To test it:

        {blue}ttr test{reset}
""".format(blue=BLUE, reset=RESET, bold=BOLD)

see_also = """
    RFKill
"""

output = TEMPLATE.format(name=name, synopsis=synopsis, description=description,
                         examples=examples, see_also=see_also)
