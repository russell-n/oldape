from elexol import elexol24
import time

# Total number of AC ports device can control
MAX_PINS = 24
# Total number of AC devices per port (A, B, C)
PINS_PER_PORT = 8
# Time, in seconds, to delay between turning a device on/off
TOGGLE_DELAY = 0.05
# Maximum number of devices that are allowed to be on at a time.
MAX_ON = 6

class nps (object):
    """
    This class allows access to the Network Power Supply (NPS). 
    It prevents electrically unsafe use.

    The most important commands to use are:

       * `TurnOn()`
       * `TurnOff()`
       * `TurnOffList()`
       * `TurnOnList()`

    * `TurnOn/Off()` accepts an integer to specify which AC port to turn on/off.
    * `TurnOff/OnList()` accepts a list of devices to turn on or off.  
    * `TurnOnList()`'s keyword 'clear' indicates whether to disable devices already on.

    Error checking is done to ensure that devices do indeed turn on/off when desired.
    """
    def __init__ (self, IP, clear=True, retry=5):
        """
        Initializes an elexol24 object to talk to the NPS device.
     
        :param:
         - `IP`    : String containing the IP address of the Elexol device.
         - `clear` : Bool indicating whether or not NPS will disable all plugs at start
         - `retry` : Number of times to retry if communication with Elexol fails.
        """
        self.el = elexol24(IP, clear, retry)
        self.ports = ['A', 'B', 'C']
        self.port_status = {}
        for port in self.ports:
            self.port_status[port] = []
            for idx in range(PINS_PER_PORT):
                self.port_status[port].append(False)
        self.num_retry = retry
	#self.onCnt = self.OnCnt()

    def GetPortStatus(self):
        """
        Queries Elexol  to get current ON/OFF status for all pins.
        This information is populated in the self.port_status dict.
        
        Example retrieval of status::

            status = np.port_status[port][pin]
            
            for example,
            
            np = nps.nps()
            np.GetPortStatus()
            if np.port_status['B'][4] == True:
                print 'Port B4 is on!'
 
        See `ToPortPin()` to convert pin (i.e. 23) to  port/pin (i.e., 'C', 7)
        """
        for port in self.ports:
            raw_int = self.el.getport(port)
            for pin in range(PINS_PER_PORT):
                self.port_status[port][pin] = bool(raw_int & (1 << pin))

    def OnCnt(self):
        """
        Queries Elexol to determine how many devices are currently on.

        :rtype: int
        :return: Number of devices currently ON.

        """
        count = 0
        self.GetPortStatus()
        for port in self.ports:
            for idx in range(PINS_PER_PORT):
                if self.port_status[port][idx]:
                    count = count + 1
        return count

    def ToPortPin(self, number):
        """
        Converts AC device number to its equivalent Port/Pin pair
        
        :param:
         - `number` : AC device number
        
        :rtype: string, int
        :return: tuple (Port number, Pin number) matching AC device number requested.
        """
        if self.CheckBounds(number):
            return None
        port_id = number / PINS_PER_PORT
        port = self.ports[port_id]
        pin = number % PINS_PER_PORT
        return port, pin

    def DisplayError(self, msg):
        """
        Helper function to display error message to the screen.

        :param:
         - `msg` : String message to include in error.
        """
        print "!!!!!!!!!!!!!!!!!    You're blowin' it!     !!!!!!!!!!!!!"
        print
        print msg
        print
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'        

    def CheckBounds(self, number):
        """
        Ensures that device number requested is out of bounds.
        
        :param:
        - `number` : int device number to check

        :rtype: Boolean
        :return: Flag indicating if device number is valid. (True=Invalid, False=Valid)
        """
        if number >= MAX_PINS:
            self.DisplayError("Port # {0} does not exist!".format(number))
            return True
        return False

    def TurnOnList(self, on_list, clear=False):
        """
        Turn on all devices whose numbers are included in a provided list.

        :param:

         - `on_list`: List containing integer device numbers                
         - `clear`  : If *True* turn *Off* all other devices. If *False* leave *On*.
        """
        if clear:
            self.AllOff(on_list)
        for item in on_list:
            self.TurnOn(item)

    def TurnOffList(self, off_list):
        """
        Turn off all devices whose numbers are included in a provided list.

        :param:
         - `off_list` : List that contains the integer device numbers
 
        """
        for item in off_list:
            self.TurnOff(item)

    def TurnOn(self, number):
        """
        Turn ON device listed by number

        :param:
         - `number` : Device number to turn on   
        """
        if self.CheckBounds(number):
            return
        self.GetPortStatus()
        port, pin = self.ToPortPin(number)
        if self.port_status[port][pin]:
            return
        count = self.OnCnt()
        if count >= MAX_ON:
            self.DisplayError(('ERROR: Maximum number of ON devices exceeded'
                               ' ({0})--device {1} was not turned on').format(MAX_ON, number))
            return
        try_num = 0
        while try_num < self.num_retry:
            self.el.setpin24(number)
            time.sleep(TOGGLE_DELAY)
            self.GetPortStatus()
            if self.port_status[port][pin]:
                break
            try_num = try_num + 1
       
        if try_num == self.num_retry:
            self.DisplayError("Could not turn on pin #{0}".format(number))

    def TurnOff(self, number):
        """
        Turn OFF device listed by number

        :param:
         - `number` : Device number to turn off
        """
        if self.CheckBounds(number):
            return
        self.GetPortStatus()
        port, pin = self.ToPortPin(number)
        if self.port_status[port][pin]:
            return

        try_num = 0
        while try_num < self.num_retry:
            self.el.clearpin24(number)
            time.sleep(TOGGLE_DELAY)
            self.GetPortStatus()
            if self.port_status[port][pin]:
                break
            try_num = try_num + 1
 
        if try_num == self.num_retry:
            self.DisplayError("Could not turn off pin #{0}".format(number))
    
    def AllOff(self, exception = []):
        """
        Turns off all devices on the Elexol NPS not listed in `exception` list

        :param: 
        - `exception` : list of device numbers (int) to leave on. (Default=all off))
        """
        for i in xrange(MAX_PINS):
            if i not in exception: 
                self.TurnOff(i)
