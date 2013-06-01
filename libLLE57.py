import serial
from datetime import datetime

class LLE57(object):
	def __init__(self, slave = 255, internaladdress = 1, lineheight = 7, linewidth = 112, lines = 10, serialport = '/dev/ttyUSB0'):
		self.__ser = serial.Serial(port = serialport,
					   baudrate=9600,
					   parity=serial.PARITY_NONE,
					   stopbits=serial.STOPBITS_ONE,
					   bytesize=serial.EIGHTBITS)
		self.__slave = hex(slave)
		self.__internaladdress = hex(internaladdress)
		self.__lineheight = hex(lineheight)
		self.__linewidth = hex(linewidth)
		self.__lines = lines
		self.__datasets = []

	def add_hex(self, hex1, hex2):
		# Add two hexadeimal numbers and return the result in hex
		return hex(int(hex1, 16) + int(hex2, 16))

	def make_checksum(self, command):
		# Calculate the checksum and return it
		# The checksum is the sum of all bytes starting from and including
		# the Control-Byte (0x43) until, excluding, the checksum-byte.
		# Then modulo everything 0x100.
		checksum = '0x00'
		for i in command:
			checksum = self.add_hex(checksum, i)
	
		return hex(int(checksum, 16) % int('0x100', 16))

	def cmd_set_time(self, timestamp = datetime.now()):
		# Generate command to set the date and time of the device
		# By default, the current time and day is set
		command = []
		command.append('0x09') # length
		command.append(self.__internaladdress) # internal address
		command.append('0x50') # Dataset-identifier (set date and time)
		command.append(hex(timestamp.year))
		command.append(hex(timestamp.month))
		command.append(hex(timestamp.day))
		command.append(hex(timestamp.hour))
		command.append(hex(timestamp.minute))
		command.append(hex(timestamp.second))

		self.__datasets.append(command)

	def cmd_set_conserve_font(self):
		# Set a conserved font-dump
		self.__datasets.append(['0x03', '0x01', '0x32', '0x87'])
		
	def cmd_set_conserve_text(self):
		# Set a conserved text-dump
		self.__datasets.append(['0x11', '0x01', '0x30', '0x13', '0x00', '0x00','0x00', '0x00',
			 '0x1C', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x31'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x07', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x32'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x0E', '0x00',
			 '0x1D', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x33'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x15', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x34'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x1C', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x35'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x23', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x36'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x2A', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x37'])
		self.__datasets.append(['0x11', '0x01', '0x30', '0x12', '0x00', '0x00', '0x31', '0x00',
			 '0x1E', '0x00', '0x07', '0x00', '0x05', '0x6F', '0x62', '0x65', '0x6E', '0x38'])
		self.__datasets.append(['0x0C', '0x01', '0x30', '0x11', '0x00', '0x00', '0x00', '0x00',
			 '0x00', '0x00', '0x00', '0x00', '0x00'])

	def cmd_set_text(self, text, memory = '0x01', output = '0x00', attrib = '0x00', startx = 0, starty = 0):
		# Write the desired text
		command = []
		command.append(self.__internaladdress) # internal address
		command.append('0x30') # Dataset-identifier (Text)
		command.append(hex(int( "%04d" % int(bin(int(memory, 16))[2:]) + 
					"%04d" % int(bin(int(output, 16))[2:]), 2))) # Textcontrol-byte
		command.append(hex(startx)) # Horizontal position
		command.append('0x00') # Horizontal position 2 TODO
		command.append(hex(starty)) # Vertical position
		command.append('0x00') # Vertical position 2 TODO
		command.append(self.__linewidth) # Width of the line
		command.append('0x00') # Width of the line 2 TODO
		command.append(self.__lineheight) # Height of the line
		command.append(attrib) # Text-Attribute
		command.append(hex(len(text))) # Lenght of the text to display
		for i in text:
			command.append(i.encode('hex'))

		command.insert(0, hex(len(command))) # insert length of dataset at the beginning

		self.__datasets.append(command)
	
	def cmd_set_charset(self, font = '0x07', transparency = '1', spacing = '0x00'):
		#Set the desired font, transparency and spacing
		command = []
		command.append('0x03') # length
		command.append(self.__internaladdress) # internal address
		command.append('0x32') # Dataset-identifier (set charset)
		command.append(hex(int( str(transparency) +
					"%02d" % int(bin(int(spacing, 16))[2:]) + 
					"%05d" % int(bin(int(font, 16))[2:]), 2)))

		self.__datasets.append(command)

	def cmd_set_graphics(self, pixels, height, width, startx = 0, starty = 0, memory = '0x01', output = '0x00'):
		command = []
		command.append(self.__internaladdress) # internal address
		command.append('0x31') # Dataset-identifier (Graphics)
		command.append(hex(int( "%04d" % int(bin(int(memory, 16))[2:]) + 
					"%04d" % int(bin(int(output, 16))[2:]), 2))) # Textcontrol-byte
		command.append(hex(startx)) # Horizontal position
		command.append('0x00') # Horizontal position 2 TODO
		command.append(hex(starty)) # Vertical position
		command.append('0x00') # Vertical position 2 TODO
		command.append(hex(height)) # Height of the graphic
		command.append('0x00') # Height of the graphic 2 TODO
		command.append(hex(width)) # Weight of the graphic
		command.append('0x00') # Weight of the graphic 2 TODO

		for line in pixels:
			# Extend to be a multiple of 8 Bits
			for i in range(0, 8 - (len(line) % 8)):
				line.append(0)
			
			for i in range (1, (len(line) / 8)):
				bits = ""
				for j in range(0, 8):
					bits += str(line[j])
				
				command.append(hex(int(bits, 2)))
				

		command.insert(0, hex(len(command))) # insert length of dataset at the beginning
		self.__datasets.append(command)

	def flush(self):
		# Remove all datasets
		self.__datasets = []

	def make_datasets(self):
		# Create a list with all datasets and the needed Information-bytes
		payload = []
		payload.append(hex(len(self.__datasets))) # Information-Byte, number of datasets
		payload.append('0xB9') # Function group Text/Chars/Graphics

		for dataset in self.__datasets:
			for byte in dataset:
				payload.append(byte)

		return payload
	
	def escape_payload(self, payload):
		# All occurances of 0x7D and 0x7E need to be replaced.
		escaped = []
		for byte in payload:
			escaped.append(byte)
			if (byte == '0x7D'):
				escaped.append('0x5D')
			if (byte == '0x7E'):
				escaped.append('0x5E')
				
		return escaped

	def send(self, showpayload = False):
		# Construct the telegram and send it
		if len(self.__datasets) == 0:
			return

		payload = []
		payload.append('0x43') # Control-byte
		payload.append(self.__slave) # Slave-address
		payload.append('0x00') # OSI3-byte
		payload.extend(self.make_datasets()) # append the datasets

		payload.append(self.make_checksum(payload)) # append the checksum
		allfields = hex(len(payload) - 1) # insert the field-count at the start
						  # substract one for checksum
		payload.insert(0, '0x68') # insert Start-sentinel
		payload.insert(0, allfields) # insert total field count
		payload.insert(0, allfields) # insert another time!
		payload.insert(0, '0x68') # insert another Start-sentinel
		payload.append('0x16') # insert Stop-sentinel at the end

		payload = self.escape_payload(payload) # escape special control sequences

		payload.append('0x7E') # Add end of telegram
		payload.insert(0, '0x7E') # Add start of telegram

		preped = ""
		for byte in payload:
			byte = int(byte, 16)

			# 0x00 is ignored by the function below, therefore this hack
			if byte == 0:
				preped += chr(0)
			while byte:
				preped += chr(byte & 0xFF)
				byte >>= 8

		if showpayload:
			print payload
			#print preped

		return self.__ser.write(preped)
