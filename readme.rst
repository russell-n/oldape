All-in-one Performance Evaluation Tools (Read Me)
=================================================


The `APE` is an attempt at a swiss-army knife style of test-runner, which uses a configuration file (`ini <http://en.wikipedia.org/wiki/INI_file>`_) to declare both the parts of the test to be executed and the parameters those parts need. Additionally, it accepts a `glob <http://en.wikipedia.org/wiki/Glob_(programming)>`_ so that separate configurations can be executed in lexicographic order.


Installation
------------

The APE isn't on `PyPi` so you have to pull the repository and change into the top directory, then install it:

    python setup.py install

.. '    

Command Line Help
-----------------

You Can Check out the help:

   ape -h

::

    usage: apetools [-h] [-d] [--pudb] [--pdb] [-s] {run,fetch,test} ...
    
    optional arguments:
      -h, --help        show this help message and exit
      -d, --debug       Display debugging messages.
      --pudb            Enable pudb interactive debugging.
      --pdb             Enable python's debugger
      -s, --silent      Turn off screen output.
    
    Test Subcommands Help:
      Available Subcommands
    
      {run,fetch,test}  test subcommands
        run             Run a Test
        fetch           Fetch a sample config file.
        test            Test your setup.
    
    



There are three sub-commands -- `run`, `fetch`, and `test`.

The Run Sub-command
-------------------

::

    usage: apetools run [-h] [<config-file glob>]
    
    positional arguments:
      <config-file glob>  A file glob to match config files (default='*.ini').
    
    optional arguments:
      -h, --help          show this help message and exit
    
    
    



The run sub-command will read in the configuration and attempt to run the tests.

The Fetch Sub-Command
---------------------

::

    usage: apetools fetch [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
    
    



The fetch sub-command will retrieve a sample configuration.

.. warning:: This will retrieve a file named ``ape.ini``. If there is already a file there by that name it will be replaced by the fresh copy.

The Test Sub-Command
--------------------

::

    usage: apetools test [-h] [<config-file glob>]
    
    positional arguments:
      <config-file glob>  A file glob to match config files (e.g. *.ini -
                          default='*.ini').
    
    optional arguments:
      -h, --help          show this help message and exit
    
    
    



The intention is for the test sub-command to test your configuration but right now it is broken.

Documentation
-------------

The built documentation is `online at GitHub <https://rsnakamura.github.io/oldape/>. To build the documentation, make sure you have:

   * sphinx
   * sphinxcontrib-uml
   * sphinx_bootstrap_theme

Then run ``make <format>`` in the same director as the `Makefile`. For example, to create html-documentation::

   make html

The documentation should then be in the folder ``build/html``.

Requirements
------------

The ``requirements.txt`` file is built using ``pip freeze``. It may have more than is needed (e.g. `pep8`) since it includes packages to help create the code, but it should have everything that's needed. To install from the file::

   pip install -r requirements.txt

.. '

Bugs
----

This code is currently in maintenance mode as the newer ape was meant to take its place. If you find a bug please file it through the GitHub `issue tracker <https://github.com/rsnakamura/oldape/issues>`_. 
