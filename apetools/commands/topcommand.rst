The Top Command
===============

This is a substitute for the `ps` command in the cases where it is not available. The device for which it is intially being built is an `iPad`. 

.. currentmodule:: apetools.commands.topcommand

Top Requirements
----------------

The `top` command on the iPad does not behave exactly like the GNU top and so anyone using this must make sure that:

    * The syntax for getting a single (non-interactive) output (the flag below is an 'l' as in 'larry')::

        top -l 1

    * The `top` command outputs all the processes (some versions of `top` will only output what fits on the screen)

    * The `top` command does not need the ``TERM`` variable set when run via non-interactive ssh

    * The first two columns of output are *PID* and *COMMAND*



The Top Command
---------------

.. autosummary::
   :toctree: api

   TopCommand
   TopCommandError

.. uml::

   TopCommand -|> BaseClass
   TopCommand : connection
   TopCommand : __call__()

.. uml::

   TopCommandError -|> CommandError
   
Subclasses
~~~~~~~~~~

 * None

Responsibilities
~~~~~~~~~~~~~~~~

 * Sends ``top`` command to a connection to a device

 * Checks for error-messages specific to the ``top`` command.

 * Generates output from the ``top`` command

Collaborators
~~~~~~~~~~~~~

 * Connection




Example Use::

    connection = SSHConnection(hostname='elin', username='tester')
    top = TopCommand(connection)
    for line in top():
        print line



The TopGrep
-----------

.. autosummary::
   :toctree: api

   TopGrep
   TopGrepError

.. uml::

   TopGrep -|> BaseClass
   TopGrep : process
   TopGrep : expression

Subclasses
~~~~~~~~~~

 * None

Responsibilities
~~~~~~~~~~~~~~~~

 * Calls the TopCommand and traverses its output

 * Extracts fields from lines that match the indicated process-names

 * Yields all extracted fields

Collaborators
~~~~~~~~~~~~~

 * `TopCommand`

Example Use::

    connection = SSHConnection(hostname='elin', username='tester')
    grep = TopGrep(connection, 'iperf')
    for pid in grep():
        print pid

.. note:: Since the `TopGrep` is implemented in this case to directly use the `TopCommand` it acts as a `Builder` for it, making the collaboration with the `TopCommand` somewhat obscure.

The advantage in having this relationship is that you can change the `TopCommand` by changing the `TopGrep` connection::

   connection_1 = SSHConnection(hostname='elin', username='tester')
   connection_2 = SSHConnection(hostname='bob', username='tester')
   grep = TopGrep(connection)
   for pid in grep():
       print pid

   grep.connection = connection_2
   for pid in grep():
       print pid
                 



    
Testing the Top
---------------

.. autosummary::
   :toctree: api

   TestTop.test_constructor
   TestTop.test_wrong_command
   TestTop.test_bad_argument
   TestTop.test_standard_error

.. autosummary::
   :toctree: api

   TestTopGrep.test_constructor
   TestTopGrep.test_call
   TestTopGrep.test_expression
   TestTopGrep.test_unmatched
   TestTopGrep.test_call_parameter
   TestTopGrep.test_cpu_field
   TestTopGrep.test_change_connection






