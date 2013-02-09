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
#   limitations under the License.
"""
The entry point for stand-alone invocation (runs the argumentbureau).

"""
# python Libraries

# testrunner Libraries
from proletarians.argumentparser import ArgumentParser
from proletarians.enabledebugging import enable_debugging
from log_setter import set_logger


def main():
    """
    The main entrance point. Relies on functions being defined in argparser.

    1. parse the args
    2. set the logger
    3. enable debugging
    4. start the watcher
    5. execute the strategy
    """
    parser = ArgumentParser()
    args = parser.args
    if args is None:
        raise Exception("Something's wrong with the ArgumentParser")
        return
    set_logger(args)
    enable_debugging(args)    

    args.function(args)
    return


if __name__ == "__main__":
    import pudb;pudb.set_trace()
    main()
