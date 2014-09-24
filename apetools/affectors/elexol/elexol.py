
# python standard library
import socket


class elexol24(object):
    """
    A class for UDP socket communication with the Elexol24 Ethernet I/O board. 
    
    The class must be instantiated using the IP address as an argument, for example::
        a = elexol.elexol24("192.168.20.68")
        
    The UDP port is set at 2424 (the Elexol default).  After connecting with the device all pins are set to output mode and cleared (set to zero).
    The most useful methods are probably ``setpin24()``, ``setxpin24()``, and ``getpin24()``, as they don't require any messing with the ports on the Elexol board.
     
    
    """

    UDP_PORT = 2424
    HOST = ''
    
    def __init__(self, IP, clear = True, retry=5, ports="ABC", pins=8):
    
        """
        Constructor - Establishes communication with the Elexol24 and by default sets all pins to output mode.
        
        :param:
            - 'IP' : a string containing the IP address of the Elexol24.  Connection is made on port 2424.
            - `ports`: The Identifier for the serial port on the elexol
            - `pins`: The number of pins per port
        """
        self.closed = False
        self.IP = IP
        self.MAX_RETRY = retry
        self.ports = ports
        self.pins = pins
        self.clear = clear
        self._socket = None
        return

    @property
    def socket(self):
        """
        :return: UPD socket
        """
        if self._socket is None:
            try:
            # set up socket
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # bind to port
                self._socket.bind((self.HOST, self.UDP_PORT))
                self._socket.settimeout(0.5)
            
            # set port directions to output by default
                for port in self.ports:
                    self.setportdirection(port, 0)
            
            # set all output to zero
                if self.clear:
                    self.clearall()

            except socket.error:
                print "elexol24: ", socket.error
        return self._socket
    
    def tryrecv(self, message):
        try_num = 0
        msg = None
        while (try_num < self.MAX_RETRY):
            self.trysend(message)
            try_num = try_num + 1
            try:
                msg = self.socket.recv(2)
                break
            except socket.timeout:
                print "elexol24.getport: socket timeout"
            except socket.error:
                print "elexol24.getport: ", socket.error
        return msg

    def trysend(self, message):
        try_num = 0
        while (try_num < self.MAX_RETRY):
            try_num = try_num + 1
            try:
                self.socket.sendto(message, (self.IP, self.UDP_PORT))
                break
            except socket.timeout:
                print "elexol24.trysend: socket timeout"
            except socket.error:
                print "elexol24.trysend: ", socket.error
                
            
    # set port direction
    def setportdirection(self, port, direction):
        """
        Set the desired I/O pin direction for a particular Elexol24 port
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C' to indicate the desired port.
            - 'direction' : A byte containing binary pin direction settings for that particular port, where binary 0 is input and binary 1 is output.  ex: setting direction to 255 will set all pins to '1' and thus set the entire port to input.
            
        """
        
        self.trysend("!" + port + chr(direction))
        
        
    # set entire port at once
    def setport(self, port, value):
        """ 
        Writes values to a single port
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C' to indicate desired port.
            - 'value' : A byte containing binary values to write to the port.  ex: 255 will write all 1's to the port.
        """
        self.trysend(port.upper()+chr(value))

    # get port value
    def getport(self, port):
        """
        Gets current values on a particular port.
        
        :param: 
            - 'port' : A string containing either 'A', 'B', or 'C'.
        
        :rtype: Byte
        :return: A byte containing the current status of the desired port.
        
        """
        #self.trysend(port.lower())
        msg = self.tryrecv(port.lower())
        # return the value from the device
        return ord(msg[1])
            
    # clear all values of individual port
    def clearport(self, port):
        """
        Clears all values on given port
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C'.
            
        """        
        self.setport(port, 0)
        
    
    # clear entire device
    def clearall(self):
        """ 
        Clears all pins on the device.
        """
        for port in self.ports:
            self.clearport(port)
        return
        
                        
    # set individual pin value, keeping existing values (logical OR)
    def setpin(self, port, pin):
        """ 
        Sets an individual pin value, but leaves all other pins untouched.
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C'.
            - 'pin' : A zero-indexed value specifying the desired pin. Valid range is 0-7.

        :raise: AssertionError if pin is out of range.
        """        
        assert(pin < 8 and pin >= 0), "elexol24.setpin: pin out of range"
        
        # get existing port status and OR the result
        a = self.getport(port)
        b = a | (1 << pin)
            
        # write it back to device
        self.trysend(port.upper()+chr(b)) 
            
    # set individual pin value, with all else zero
    def setxpin(self, port, pin):
        """
        Sets an individual pin on a specified port, and clears the rest.
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C'.
            - 'pin' : A zero-indexed value specifying the desired pin. Valid range is 0-7.
            
        """
        
        self.trysend(port.upper()+chr(1 << pin))
            
    # get status of individual pin
    def getpin(self, port, pin):
        """
        Gets the status of an individual pin on a specified port. 
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C'.
            - 'pin' : A zero-indexed value specifying the desired pin. Valid range is 0-7.
        
        :rtype: Boolean
        :return: The value of the specified pin.
        
        """
    
        # get current port value and AND with desired bit
        assert(pin < 8 and pin >= 0), "elexol24.getpin: pin out of range"
        a = self.getport(port)
        return bool(a & (1 << pin))
            
            
    # clear one individual pin, keeping existing values
    def clearpin(self, port, pin):
        """ 
        Clears an individual pin on a specified port.
        
        :param:
            - 'port' : A string containing either 'A', 'B', or 'C'.
            - 'pin' : A zero-indexed value specifying the desired pin. Valid range is 0-7.          
        """
        
        assert(pin < 8 and pin >= 0), "elexol24.clearpin: pin out of range"
        # get port status, AND with inverted pin value
        a = self.getport(port)
        b = a & ~(1 << pin)
        
        # write back to device
        self.trysend(port.upper()+chr(b))
        
    # set one pin in entire 24 pin bank 
    def setpin24(self, pin):
        """
        Sets an individual pin across the entire device, and leaves all other untouched.
        
        :param:
            - 'pin' : A zero-indexed value specifying the desired pin.  Valid range is 0-23
        """
        assert (pin < 24 and pin >= 0), "elexol24.setpin24: Pin input outside of range."
        
        # determine port
        port, pin = self.ports[pin/self.pins], pin % self.pins
        # perform operation
        self.setpin(port, pin)
        return
        
    
    # set one pin in entire 24 pin bank, keeping all else zero
    def setxpin24(self, pin):
        """
        Sets an individual pin across the entire device. All other pins are cleared.
        
        :param:
            - `pin` : A zero-indexed value specifying the desired pin. Valid range is 0-23.

        :raise: AssertionError if pin out of range.
        """        
        assert (pin < 24 and pin >= 0), "elexol24.setxpin24: Pin input outside of range."
        
        # determine port
        port, pin = self.ports[pin/self.pins], pin % self.pins
        
        # perform operation
        self.clearall()
        self.setpin(port, pin)
        return

    def getpin24(self, pin):
        """
        Gets the value of an individual pin across the entire device.
        
        :param:
            - 'pin' : A zero-indexed value specifying the desired pin. Valid range is 0-23.
        
        :rtype: Boolean
        :return: The value of the specified pin.

        :raise: AssertionError if ping out of range
        """
        
        assert (pin < 24 and pin >= 0), "elexol24.getpin24: Pin input outside of range."
        
        # determine port
        port, pin = self.ports[pin/self.pins], pin % self.pins
            
        # perform operation
        return(self.getpin(port, pin))
        
        
    # clear one individual pin in entire 24 pin bank, keeping existing values
    def clearpin24(self, pin):
        """
        Clears an individual pin across the entire device, leaving all other untouched.
        
        :param:
            - `pin` : A zero-indexed value specifying the desired pin. Valid range is 0-23.

        :raise: AssertionError if `pin` out of range.
        """
        assert (pin < 24 and pin >= 0), "elexol24.clearpin24: Pin input outside of range."
        
        # determine port
        port, pin = self.ports[pin/self.pins], pin % self.pins
            
        # perform operation
        self.clearpin(port, pin)
        return
    
    # cleanup
    def close(self):
        """
        Closes open sockets. Automatically called by destructor.
        """
        if not self.closed:
            self.socket.close()
    
    # destructor
    def __del__(self):
        """
        Calls self.close
        """
        self.close()
# end elexol24        
