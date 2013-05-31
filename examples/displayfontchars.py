import time
import sys
sys.path.append('../')
from libLLE57 import LLE57

textslave = LLE57(serialport = '/dev/ttyUSB3', slave = 2)
fontslave = LLE57(serialport = '/dev/ttyUSB3', slave = 3, lineheight = 63)
fontstotry = range(10, 11)
textfont = 8

textslave.cmd_set_text(text = "", output = '0x04')
textslave.cmd_set_text(text = "", output = '0x01')
textslave.send(True)
textslave.flush()
fontslave.cmd_set_text(text = "", output = '0x04')
fontslave.cmd_set_text(text = "", output = '0x01')
fontslave.send(True)
fontslave.flush()

time.sleep(1)

textslave.cmd_set_text(text = "", output = '0x00')
textslave.send(True)
textslave.flush()
fontslave.cmd_set_text(text = "", output = '0x00')
fontslave.send(True)
fontslave.flush()

for fontid in fontstotry:
	for char in range(160, 256):
		textslave.cmd_set_charset(font = hex(textfont))
		textslave.cmd_set_text(text = "FontId " + hex(fontid) + "  " + str(fontid), starty = 56, startx = 50)
		textslave.cmd_set_text(text = "Char " + hex(char) + "  " + chr(char), starty = 63, startx = 50, output = '0x01')
		textslave.send(True)
		textslave.flush()

		fontslave.cmd_set_charset(font = hex(fontid))
		fontslave.cmd_set_text(text = chr(char))
		fontslave.send(True)
		fontslave.flush()
		print "FontId " + hex(fontid) + "  " + str(fontid)
		print "Char " + hex(char) + "  " + chr(char)
		time.sleep(1)
		#sys.stdin.readline()
