Getting Help
============

The obvious thing would be to say - *What do you think this document is for?* but I would like to also mention the command-line help that is available.

The -h Flag
-----------

The -h flag is an auto-generated help message created by the argument-parser. It is meant to help remind you of the options you can pass in when running the program. If you can remember that the program is called `ttr`, then you just have to remember the help flag::

    ttr -h

This will produce the following::

    usage: ttr [-h] [-d] [--pdb] [-s] {run,fetch,test,help} ...
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Display debugging messages.
      --pdb                 Enable interactive debugging.
      -s, --silent          Turn off screen output.
    
    Test Subcommands Help:
      Available Subcommands
    
      {run,fetch,test,help}
                            test subcommands
        run                 Run a Test
        fetch               Fetch a sample config file.
        test                Test your setup.
        help                Show more help

The notation seems to be a variant of Backus-Naur Form - what you see in square brackets is optional, what you see in curly-braces are alternatives (i.e. you can choose only one).

The first line shows you what you can enter at the command line to run the program. An abstract of what it's telling you is::

    ttr <options> {<sub-commands>}

The sections below them explain what they are for. In most cases you won't need the options, they're more helpful when debugging the program than when running a test. The sub-commands are what you really need. As you can see there are four of them (`run, fetch, test, help`). These are sub-commands, not positional arguments (they are the names of functions to be called by the `ttr`) and so they can also take arguments. Typing `ttr help -h`, for instance, brings up this::

    usage: ttr help [-h] [topic]
    
    positional arguments:
      topic       A specific subject to inquire about.
    
    optional arguments:
      -h, --help  show this help message and exit

If you need prompts to remind you how to use the program, use the `-h` flag.

The Help Subcommand
-------------------

If you noticed, there is a subcommand called `help`. This pulls up some documentation created to be sort of a secondary step between the `-h` flag and this document. It hopefully covers enough to remind you of what the sub-commands do. To see the config-file help, for instance, you'd type::

    ttr help config


pydoc
-----

Python provides auto-generated documentation for installed libraries. This is primarily intended to be used by developers who want to use the code, but if you want to get some kind of idea of what the stack-traces mean without reading the code, you could try and explore this tool. The way to use it is to refer to sub-packages by dot notation. if you wanted to see what the :ref:`errorsvscrashing` examples were referring to when the SL4AConnection was mentioned, you could first enter::

    pydoc timetorecovertest

You use `timetorecovertest` not `ttr` since that's the name of the actual library, `ttr` is a python-file that executest the `main()` function in the library. The pydoc output should end with a listing of **Package Contents** one of which is *connections (package)*. You could then enter::

    pydoc timetorecovertest.connections

Which would reveal that its **Package Contents** include something called `sl4aconnection`. Looking at its pydoc output::

    pydoc timetorecovertest.connections.sl4aconnection

Reveals that it has a class called Sl4aConnection which is a sub-class of android.Android - a module and class provided by the `SL4A` developers, which if you didn't install you will realize came with my installation and maybe shouldn't be there... I'm not a lawyer, what do I know.

This probably is the least helpful to you when running the tests, but if you're interested in python at all, it's a very helpful tool to get to know.
