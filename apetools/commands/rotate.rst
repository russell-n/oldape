The Rotate
==========

A command-line interface to run the rotate command remotely.

::

    SIGKILL = 9
    PROCESS = 'rotate'
    
    



RotateError
-----------

.. uml::

   CommandError <|-- RotateError
   
::

    class RotateError(CommandError):
        """
        An error in the rotation
        """
    # end class RotateError
    
    



RotateParameters
----------------

This is a class intended for the RotateCommand.__call__. It generates arguments based on what settings it gets.

.. module:: apetools.commands.rotate
.. autosummary::
   :toctree: api

   RotateParameters
   RotateParameters.configuration
   RotateParameters.section
   RotateParameters.angles
   RotateParameters.argument_strings
   RotateParameters.values_string
   RotateParameters.booleans_string
   RotateParameters.base_arguments



RotateCommand
-------------

.. module:: apetools.commands.rotate
.. autosummary::
   :toctree: api

   RotateCommand
   RotateCommand.kill
   RotateCommand.kill_process
   RotateCommand.__call__
   RotateCommand.check_errors
   
::

    if __name__ == "__main__":
        from apetools.connections.sshconnection import SSHConnection
        c = SSHConnection("pogo2", "root")
        r = RotateCommand(c)
        print "Rotate to 90 degrees"
        r(90)
        time.sleep(1)
        print "Rotate to 180 Degrees"
        r(180)
        time.sleep(1)
        print "Rotate to 0 degrees"
        r()
    
    

