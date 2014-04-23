Path Additions To the DUT
=========================

Narrative
---------

The **user** specifies directories not in the default *PATH* variable of the **DUT**. 
The DUT **Sub-Lexicographer** reads in any list of paths and adds it to the DUT's parameters.
The **Builder** builds a **connection** to the DUT and impels the connection to add the paths to the DUT's path.

.. uml::

   APE -> (Add Directories To The DUT's PATH)

Main Path
---------

#. Map paths in config-file to a list.
#. Add the list to the DUT's parameters.
#. Build a connection to the DUT.
#. Get the existing *PATH* values.
#. Prepend the new paths to the existing path-values.
#. Set the DUT's *PATH* variable to the new path.

Alternative
-----------

6.1. The connection is unable to create a persistent change to the *PATH*.

6.2. Add the path addition to the connection's *command-prefix*.

Players
-------

* Configuration Map
* Device Lexicographer
* Device Parameters
* Connection Builders
* Connections

