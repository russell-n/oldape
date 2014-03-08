All-in-one Performance Evaluation Tools
=======================================

The `APE` is an attempt at a swiss-army knife style of test-runner, which uses a configuration file (`ini <http://en.wikipedia.org/wiki/INI_file>`_) to declare both the parts of the test to be executed and the parameters those parts need. Additionally, it accepts a `glob <http://en.wikipedia.org/wiki/Glob_(programming)>`_ so that separate configurations can be executed in lexicographic order.

It is currently being converted to a Literate Programming implementation. To build the documentation, make sure you have:

   * sphinx
   * sphinxcontrib-uml

The tests have been combined with the code so to run it you also need:

   * mock

   * nose
