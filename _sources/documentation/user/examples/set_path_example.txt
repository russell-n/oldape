Read-Only Device, Non-Interactive PATH Not Complete
===================================================

Contents:

   * :ref:`What's Unique About This Example <no-path-unique-features>`

   * :ref:`Assumptions Made for a Concrete Example <no-path-example-assumptions>`

   * :ref:`Setting Up the Configuration to Add the Path <no-path-adding-the-path>`

   * :ref:`Some Notes About the Notation <no-path-notes-on-notation>`

.. _no-path-unique-features:

Unique Features
---------------

Devices that meet the following conditions should find this example applicable:

   * Commands needed aren't on the PATH

   * Device is read-only (or you lack permissions to move, link, or edit files to locations set in its ``PATH`` variable)

.. _no-path-example-assumptions:

Example Assumptions
-------------------

To make the example concrete, we'll assume that the device has an ssh-connection, is linux-based, and is missing the following directories on its PATH:

   * /sbin

   * /opt/wifi

.. _no-path-adding-the-path:

Adding the PATH
---------------

To add the ``PATH`` to the DUT's commands you would add a ``path`` sub-option to the Node information in the configuration file::

   [NODES]
   hr44 = hostname:hr44, login:root, password:happy2code, operating_system:linux, connection:ssh, test_interface:eth1, path:/opt/wifi /sbin

.. csv-table:: Example Notes
   :header: Item,Explanation
   :delim: ;

   hr44; A user-created identifier used to name the files and log-entries
   hostname; IP address or hostname of the node's network interface to send control commands to
   login; Login user-name for the node
   password; Password (if needed) to log into the node
   operating_system; OS used to interpret the output of command-line commands
   connection; Type of connection (serial, local, ssh, adbssh, etc.) **Use SSH whenever possible**
   test_interface; The name of the network interface on the node to use for test-traffic
   path; Space-separated directories to add to the node's PATH

.. _no-path-notes-on-notation:

Notes on the notation
---------------------

The basic format for a line in an ``ini`` file is::

   <option> = <value>

Because it uses an equal sign (``=``) to separate options and values you can't use it within a value. This, for example won't work:

   hr44 = hostname:hr44, login:root, connection:ssh, test_interface:eth1, path = /opt/wifi /sbin

The second equal-sign confuses the parser, which is why I used a ``<sub-option>:<value>`` format. Additionally, I had already decided to use comma-separated lists to bundle sub-options with options so adding a list as a sub-option (in this case a list of `path` directories) couldn't use commas so I went with space-separated lists for lists within option lists.

You don't really need to know this, but because the ``ini`` format is so free, when errors do occur they are hard to interpret, so I thought I'd emphasize that the format for the `NODE` options isn't necessarily what you might expect.
