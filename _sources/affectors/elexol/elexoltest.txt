Testing the Elexol
==================


A test routine for the elexol24.

::

    if __name__ == '__main__':
        print "Initializing..."
        
        # init communications
        elexol = elexol.elexol24("192.168.20.68", clear = False)
        
        # cycle through all pins on device, once per second
        for i in range(24):
            print "Pin status: {:08b}{:08b}{:08b}".format(elexol.getport('C'),
                                                          elexol.getport('B'),
                                                          elexol.getport('A'))
        	time.sleep(1)
    
    

