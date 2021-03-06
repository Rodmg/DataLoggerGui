#!/usr/bin/python
# coding: utf-8

#Author: Rodrigo Méndez Gamboa

# PACKET
# BYTE 0 --> [COMM_PACKET_HEADER_1ST]
# BYTE 1 --> [COMM_PACKET_HEADER_2ND]
# BYTE 2 --> { USER CUSTOM COMMAND }
# BYTE 3 --> { USER DATA SIZE = N }
# BYTE 4 --> { USER DATA }
# ...    --> { USER DATA }
# BYTE 4 + (N-1) --> { USER DATA }
# BYTE 4 + (N) --> [CHECKSUM]

import threading
import time
import binascii

HEADER = bytearray([0x55, 0xAA])

class CommPacket:
	def __init__(self, cmd, length, data):
		self.cmd = cmd
		self.length = length
		self.data = data

class Comm(threading.Thread):
	def __init__(self, connection):
		threading.Thread.__init__(self)
		self.setConnection(connection)
		self.rxBuffer = bytearray([])
		self.packetReceived = False
		self.rxCounter = 0
		self.rxCallback = None

	def setConnection(self, connection):
		print "conection changed to" + str(connection)
		self.connection = connection

	def calculateChecksum(self, data):
		sum = 0;
		for byte in data:
			sum += byte

		return sum & 0xFF

	def writeCommand(self, command, data=[]):
		buffer = HEADER + bytearray([command, len(data)]) + bytearray(data)
		buffer = buffer + bytearray([self.calculateChecksum(buffer)])
		if self.connection.isOpen():
			print binascii.hexlify(buffer)
			self.connection.write(buffer)

	def readPacket(self):
		try:
			self.packetReceived = False
			packet = CommPacket(self.rxBuffer[2], self.rxBuffer[3], self.rxBuffer[4:4+self.rxBuffer[3]])
			self.rxCounter = 0
			self.rxBuffer = bytearray([])
			return packet
		except Exception, e:
			self.packetReceived = False
			self.rxCounter = 0
			self.rxBuffer = bytearray([])
			return None

	def rxCheck(self):
		if not self.connection.isOpen() or self.packetReceived:
			time.sleep(1)
			return

		b = ord(self.connection.read())

		# print "received data" + binascii.hexlify(str(b))


		if self.rxCounter == 0:
			if b != HEADER[0]:
				self.rxCounter = 0
				self.rxBuffer = bytearray([])
				return
		elif self.rxCounter == 1:
			if b != HEADER[1]:
				self.rxCounter = 0
				self.rxBuffer = bytearray([])
				return
		elif self.rxCounter == 3:
			pass
		elif self.rxCounter > 3:
			if self.rxCounter == self.rxBuffer[3] + 4:	#Checksum byte
				if self.calculateChecksum(self.rxBuffer) == b:
					self.packetReceived = True
				else:
					self.rxCounter = 0
					self.rxBuffer = bytearray([])
					return

		self.rxBuffer.append(b)
		self.rxCounter += 1


	def run(self):
		print 'thread running'
		while True:
			self.rxCheck()
			if self.packetReceived and self.rxCallback is not None:
				print "Got packet"
				self.rxCallback()





