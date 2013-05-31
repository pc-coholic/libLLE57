import time
import sys
sys.path.append('../')
from libLLE57 import LLE57

treppe = LLE57(serialport = '/dev/ttyUSB3')

treppe.cmd_set_text(text = "", output = '0x04')
treppe.cmd_set_text(text = "", output = '0x01')
treppe.send()
treppe.flush()

time.sleep(1)

treppe.cmd_set_text(text = "", output = '0x00')
treppe.send()
treppe.flush()

graphics = [
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
]

treppe.cmd_set_graphics(pixels = graphics, height = 8, width = 8, startx = 50)
treppe.send(True)
treppe.flush()

time.sleep(5)

smiley = [
			[0, 1, 1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 1, 0, 0, 1, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 1, 0, 0, 1, 0, 1],
			[1, 0, 0, 1, 1, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1, 1, 0],
]

treppe.cmd_set_graphics(pixels = smiley, height = 8, width = 8, startx = 50)
treppe.send(True)