from libLLE57 import LLE57
import time

treppen = []
for i in range(0, 3):
	treppen.append(LLE57(serialport = '/dev/ttyUSB3', slave = i + 1))
	treppen[i].cmd_set_conserve_font()
	treppen[i].cmd_set_text(text = "", output = '0x04')
	treppen[i].cmd_set_text(text = "", output = '0x01')
	treppen[i].send(True)
	treppen[i].flush()

time.sleep(1)

for i in range(0, 3):
	treppen[i].cmd_set_text(text = "", output = '0x00')
	treppen[i].send(True)
	treppen[i].flush()

for i in range(0, 11):
	for j in range (0, len(treppen)):
		treppen[j].cmd_set_text(text = "Slave " + str(j + 1) + "/Line " + str(i + 1),
					starty = i * 7, output = '0x01', attrib = '0x10')
		treppen[j].send(True)
		treppen[j].flush()

