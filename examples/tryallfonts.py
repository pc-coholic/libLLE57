import time
import sys
sys.path.append('../')
from libLLE57 import LLE57

slave = 3

treppe = LLE57(serialport = '/dev/ttyUSB3', slave = slave, lineheight = 63)
treppe.cmd_set_text(text = "", output = '0x04')
treppe.cmd_set_text(text = "", output = '0x01')
treppe.send(True)
treppe.flush()

time.sleep(1)

treppe.cmd_set_text(text = "", output = '0x00')
treppe.send(True)
treppe.flush()

time.sleep(20)

for fontid in range(0, 256):
	treppe.cmd_set_charset(font = hex(fontid))
	treppe.cmd_set_text(text = "Font " + hex(fontid) + " / " + str(fontid))
	treppe.send(True)
	treppe.flush()
	print "Sent FontId " + hex(fontid) + " / " + str(fontid)
	time.sleep(2)
