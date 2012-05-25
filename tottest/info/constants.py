BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0;0m"

TEMPLATE="""
{bold}Name{reset}
{{name}}

{bold}Synopsis{reset}
{{synopsis}}

{bold}Description{reset}
{{description}}

{bold}Examples{reset}
{{examples}}

{bold}See Also{reset}
{{see_also}}
""".format(bold=BOLD, reset=RESET)

NAME_TEMPLATE="{0}{{name}}{1} - {{description}}".format(BOLD, RESET)
HELP_FOLDER = "timetorecovertest.info.helpfiles"
OUTPUT_VARIABLE = "output"
HELP_BASE = "helpmain"

