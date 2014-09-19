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
    
    

