The PS Command
==============

This implements a ``ps`` command caller.

.. currentmodule:: apetools.commands.pscommand




The PS Command
---------------

.. autosummary::
   :toctree: api

   PsCommand
   PsCommandEnum

.. uml::

   PsCommand -|> BaseProcessCommand
   PsCommand : connection
   PsCommand : __call__()

.. uml::

   PsCommandEnum : top
   PsCommandEnum : missing
   PsCommandEnum : bad_arg

   
Subclasses
~~~~~~~~~~

 * None

Responsibilities
~~~~~~~~~~~~~~~~

 * Sends ``ps`` command to a connection to a device

 * Checks for error-messages specific to the ``ps`` command.

 * Generates output from the ``ps`` command

Collaborators
~~~~~~~~~~~~~

 * Connection


Example Use::

    connection = SSHConnection(hostname='elin', username='tester')
    ps = PsCommand(connection)
    for line in ps():
        print line

The Error Expression
--------------------

The errors have been tested on an Ubuntu system, a Nexus 7, and a Motorola Triumph.



The PsGrep
-----------

.. autosummary::
   :toctree: api

   PsGrep

.. uml::

   PsGrep -|> BaseProcessGrep
   PsGrep : process
   PsGrep : expression

Subclasses
~~~~~~~~~~

 * None

Responsibilities
~~~~~~~~~~~~~~~~

 * Calls the PsCommand and traverses its output

 * Extracts fields from lines that match the indicated process-names

 * Yields all extracted fields

Collaborators
~~~~~~~~~~~~~

 * `PsCommand`

Example Use::

    connection = SSHConnection(hostname='elin', username='tester')
    grep = PsGrep(connection, 'iperf')
    for pid in grep():
        print pid

.. note:: Since the `PsGrep` is implemented in this case to directly use the `PsCommand` it acts as a `Builder` for it, making the collaboration with the `PsCommand` somewhat obscure.

The advantage in having this relationship is that you can change the `PsCommand` by changing the `PsGrep` connection::

   connection_1 = SSHConnection(hostname='elin', username='tester')
   connection_2 = SSHConnection(hostname='bob', username='tester')
   grep = PsGrep(connection)
   for pid in grep():
       print pid

   grep.connection = connection_2
   for pid in grep():
       print pid


    
Testing the PS
--------------

.. autosummary::
   :toctree: api

   TestPs.test_constructor
   TestPs.test_wrong_command
   TestPs.test_wrong_command_nexus
   TestPs.test_bad_argument
   TestPs.test_bad_argument_android
   TestPs.test_standard_error
   TestPs.test_no_processes_found

.. autosummary::
   :toctree: api

   TestPsGrep.test_constructor
   TestPsGrep.test_call
   TestPsGrep.test_expression
   TestPsGrep.test_unmatched
   TestPsGrep.test_call_parameter
   TestPsGrep.test_cpu_field
   TestPsGrep.test_change_connection




[call.debug('Calling: ps '),
 call.debug('USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME'),
 call.warning('No processes found, check `ps `')]


