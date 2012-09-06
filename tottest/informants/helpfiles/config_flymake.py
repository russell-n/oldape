from tottest.info.constants import TEMPLATE, BOLD, RESET, NAME_TEMPLATE, BLUE

name = NAME_TEMPLATE.format(name="The config file",
                            description="(Configuring the ttr)").center(80)

synopsis = """
The {bold}config file{reset} ({blue}ttr.ini{reset}) configures the TTR test.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

description = """
The {bold}config file{reset} (default {blue}ttr.ini{reset}) is a declarative specification of the test that the program uses to configure the program at run-time.

It uses the microsoft .ini format which has the following conventions:

{bold}Sections{reset} are indicated by square-brackets (e.g. [SECTION])
{bold}Options{reset} are located below sections and follw the  `<name> = <value>` syntax.

Things to remember:

    * although it looks kind of like a programming language, it's a config file, everything to the right of the equal-sign is read in as a string
    * this means you can put a comment on its own line (with a '#' prefix), but you can't put it on an option line (it will be picked up as part of the value)
    * although it isn't a programming language, it is case-sensitive.
    * it does allow the use of variable-expansion. Any value can be extracted by its name {bold}after{reset} it's been declared using %(<name>)s

{bold}The Sections{reset}

    * [TEST] : holds the test-settings
    * [DUT] : holds DUT-specific information
    * [LOGWATCHER] : specifies logs to watch (only really meant for /proc/kmsg right now)
    * [LOGCATWATCHER] : specifies logcat buffers to watch (default is to watch them all)
""".format(bold=BOLD, reset=RESET, blue=BLUE)

examples="""
To include a timestamp in the output_folder, place it with {{t}}:

   [TEST]
   output_folder = folder_name_{{t}}_more_stuff

To use the output_folder value somewhere else (here it's being re-used in the data-file name):

   data_file = %(output_folder)s_extra_text

Times can be specified by the use of the keywords (Hours, Seconds (the default), Minutes, Days):

   timeout = 4 Days
""".format(blue=BLUE, reset=RESET, bold=BOLD)

see_also = """
    RFKill
"""

output = TEMPLATE.format(name=name, synopsis=synopsis, description=description,
                         examples=examples, see_also=see_also)
