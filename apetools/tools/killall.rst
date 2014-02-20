Kill All
========

A module to kill processes.

.. currentmodule:: apetools.tools.killall



KillAllError
------------

The `KillAllError` is raised if an error specific to the command is detected.

.. uml::

   KillAllError -|> CommandError



KillAll
-------

The `KillAll` command (it probably should not be in the `tools`) kills processes.

.. autosummary::
   :toctree: api

   KillAll

.. uml::

   KillAll -|> BaseClass
   KillAll : name
   KillAll : time_to_sleep
   KillAll : expression
   KillAll : run(connection, name, time_to_sleep)
   KillAll : __call__(connection, name, time_to_sleep)

* The `name` parameter is the name of a process to kill.

* The `time_to_sleep` parameter is an amount of time to wait before checking that the process was successfully killed.

* The `connection` is a connection to the device.

* all the constructor parameters can be passed in to the call instead

* The expected ``ps`` output currently matches the standard GNU output (a la *Ubuntu*), android, and Cygwin

.. todo:: Implement the Cygwin expression (need a windows machine)

Example Use::

    connection = SSHConnection(hostname='elin', username='tester',
                               operating_system=OperatingSystem.android)
    connection_2 = SSHConnection(hostname='bob', username='tester',
                               operating_system=OperatingSystem.linux)

    killer = KillAll(connection, 'spotify')
    killer()
    killer.connection = connection_2
    try:
        killer('emacs')
    except KillAllError:
        killer.level = 9
        killer('emacs')



Testing the KillAll
-------------------

.. autosummary::
   :toctree: api

   TestKillAll.test_set_connection
   TestKillAll.test_kill_command
   TestKillAll.test_failed_kill
   TestKillAll.test_call
   TestKillAll.test_set_level
   TestKillAll.test_reset_level




