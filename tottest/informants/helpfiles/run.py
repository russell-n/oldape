from timetorecovertest.info.constants import TEMPLATE, BOLD, RESET, NAME_TEMPLATE, BLUE

name = NAME_TEMPLATE.format(name="ttr run",
                            description="(run the test)").center(80)

synopsis = """
The {bold}run{reset} ({blue}ttr run{reset}) runs the TTR test.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

description = """
The {bold}ttr run{reset} runs the test based on the config file (default {blue}ttr.ini{reset})
""".format(bold=BOLD, reset=RESET, blue=BLUE)

examples="""
To run any file that ends with {bold}.ini{reset}:

    {blue}ttr run{reset}

to run a specific file or files that match a glob:

    {blue}ttr run [name | glob]{reset}
""".format(blue=BLUE, reset=RESET, bold=BOLD)

see_also = """
    RFKill
"""

output = TEMPLATE.format(name=name, synopsis=synopsis, description=description,
                         examples=examples, see_also=see_also)
