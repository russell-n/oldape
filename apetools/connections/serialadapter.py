
# third party libraries
import serial

#apetools libraries
#from apetools.baseclass import BaseClass


EMPTY_STRING = ''
NEWLINE = '\n'


class SerialAdapter(serial.Serial):
    """
    A SerialAdapter adapts pyserial to this librarys' style.
    """
    def __init__(self, *args, **kwargs):
        """
        Takes the same parameters as serial.Serial

        """
        super(SerialAdapter, self).__init__(*args, **kwargs)
        return
    
    def exec_command(self, command, timeout=None):
        """
        Sends the command to the device.
        
        :return: self.client (a file-like object)
        """
        if timeout is None:
            timeout = self.timeout
        else:
            self.timeout = timeout
        self.writeline(command)
        return self

    def writeline(self, message=EMPTY_STRING):
        """
        Adds a newline and sends the message to the device.
        
        :param:

         - `message`: The message to send to the device.
        """
        self.write(message.rstrip(NEWLINE) + NEWLINE)
        return                                   
# end class SerialAdapter
