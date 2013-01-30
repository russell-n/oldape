from apetools.info.constants import TEMPLATE, BOLD, RESET, NAME_TEMPLATE, BLUE

name = NAME_TEMPLATE.format(name="apetools",
                            description="(nee' RFKill)").center(80)

synopsis = """
The {bold}time-to-recover-test{reset} ({blue}ttr{reset}) characterizes the time a device's connection takes to recover after its WiFi radio is re-enabled.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

description = """
Although the {bold}apetools{reset} is a python library, it is intended to be used as a command-line tool ({blue}ttr{reset}). There are four main sub-commands:

    1. help (which is how you got here)
    2. fetch (which gathers userful files)
    3. test (which tests the ADB, SL4A, and network connections for the DUT)
    4. run (which runs the test)
""".format(bold=BOLD, reset=RESET, blue=BLUE)

examples="""
    To get more help, pass the {bold}help{reset} command a sub-command:

    fetch
    test
    run
    config

    e.g:

        {blue}ttr help fetch{reset}
""".format(blue=BLUE, reset=RESET, bold=BOLD)

see_also = """
    RFKill
"""

output = TEMPLATE.format(name=name, synopsis=synopsis, description=description,
                         examples=examples, see_also=see_also)
