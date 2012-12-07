#!/usr/bin/python

import elexol
import time
import nps
# test routine for elexol24

print "Initializing..."
# init communications
el = nps.nps("192.168.20.68", clear = False)

# cycle through all pins on device, once per second
for i in range(24):
	#el.setxpin24(i)
	print "Pin status: {:08b}{:08b}{:08b}".format(el.getport('C'), el.getport('B'), el.getport('A'))
	time.sleep(1)

