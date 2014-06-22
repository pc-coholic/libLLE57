import time
import sys
sys.path.append('../')
from libLLE57 import LLE57
import feedparser
import textwrap
import math

textslave = LLE57(serialport = '/dev/ttyUSB0', slave = 255)

textslave.cmd_set_text(text = "", output = '0x04')
textslave.cmd_set_text(text = "", output = '0x01')
textslave.send()
textslave.flush()

time.sleep(1)

feed = feedparser.parse(r'rss.xml')
while True:
	for entry in feed['entries']:
		text = textwrap.wrap(entry['title'].encode('ascii', 'ignore'), 24)

		print "Lines of text: " + str(len(text))
		pages = int(math.ceil(len(text) / 8.0))
		print "Pages: " + str(pages)
		print text
		for page in range(1, pages + 1):
			print "Page " + str(page)
			textslave.cmd_set_charset(font = hex(7)) # 16
			#textslave.cmd_set_text(text = "       Fefes Blog", output = '0x3', starty = 0)
			textslave.cmd_set_text(text = "      Fpletz' Blog", output = '0x3', starty = 0)
			textslave.send()
			textslave.flush()

			y = 1
			#for line in text:
			for i in range((page-1) * 8, page * 8):
				textslave.cmd_set_charset(font = hex(8)) # 23
				if (i < len(text)):
					textslave.cmd_set_text(text = text[i], output = '0x1', starty = y * 7)
					print text[i]
				else:
					textslave.cmd_set_text(text = "", output = '0x1', starty = y * 7)
					print ""
				textslave.send()
				textslave.flush()
				time.sleep(1)
				y += 1
		
			if ( (pages != 1) and (page != pages) ):
				textslave.cmd_set_charset(font = hex(8)) # 23
				textslave.cmd_set_text(text = "                                 (...)", output = '0x1', starty = y * 7)
				print "(...)"
				textslave.send()
				textslave.flush()
				time.sleep(5)
				print "---- Next Page ----"

		print "---- Next Entry ----"
		time.sleep(5)
		textslave.cmd_set_text(text = "", output = '0x05')
		textslave.cmd_set_text(text = "", output = '0x01')
		textslave.send()
		textslave.flush()
		time.sleep(1)
