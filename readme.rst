All-in-one Performance Evaluation Tools
=======================================

The `APE` is an attempt at a swiss-army knife style of test-runner, which uses a configuration file (`ini <http://en.wikipedia.org/wiki/INI_file>`_) to declare both the parts of the test to be executed and the parameters those parts need. Additionally, it accepts a `glob <http://en.wikipedia.org/wiki/Glob_(programming)>`_ so that separate configurations can be executed in lexicographic order.

Documentation
-------------

It is currently being converted to a Literate Programming implementation. To build the documentation, make sure you have:

   * sphinx
   * sphinxcontrib-uml

Then run ``make <format>`` in the same director as the `Makefile`. For example, to create html-documentation::

   make html

The documentation should then be in the folder ``build/html``.

Requirements
------------

The ``requirements.txt`` file is built using ``pip freeze``. It may have more than is needed (e.g. `pep8`) since it includes packages to help create the code, but it should have everything that's needed. To install from the file::

   pip install -r requirements.txt


Bugs
----

This code is currently in maintenance mode as the newer ape was meant to take its place. If you find a bug please file it through the bitbucket `issue tracker <https://bitbucket.org/rallion/apetools/issues>`_. If you're not sure what makes a good bug report, `this description <http://quaid.fedorapeople.org/TOS/Practical_Open_Source_Software_Exploration/html/sn-Debugging_the_Code-The_Anatomy_of_a_Good_Bug_Report.html>`_ from fedora might be helpful.
