#!/usr/bin/python
# coding: utf-8

#Author: Rodrigo Méndez Gamboa

'''
Comandos:
0 - Ping
	responde con el mismo mensaje
1 - Borrar memoria
	responde con el mismo mensaje
2 - Obtener número de entradas
	responde con un byte en datos del número de entradas
3 - Obtener entrada N (n en datos)
	responde con todos los bytes de la entrada en datos
4 - Obtener hora
5 - Configurar hora
6 - Obtener alarma 1
7 - Configurar alarma 1
8 - Obtener alarma 2
9 - Configurar alarma 2
10 - Leer temperatura actual
	responde con un byte en datos de la temperatura

'''

from Comm import Comm
import datetime

class DevControl(Comm):
	def __init__(self, connection):
		Comm.__init__(self, connection)
		self.rxCallback = self.responseCallback

	def ping(self):
		self.writeCommand(0)

	def eraseMemory(self):
		self.writeCommand(1)

	def getNEntries(self):
		self.writeCommand(2)

	def getEntry(self, n):
		self.writeCommand(3, [n])

	def getTime(self):
		self.writeCommand(4)

	def setTime(self):
		now = datetime.datetime.now()
		self.writeCommand(5, [now.second, now.minute, now.hour, now.day, now.month, now.year])

	def getTimeAlarm(self):
		self.writeCommand(6)

	def setTimeAlarm(self, t):
		self.writeCommand(7, [t.minute, t.hour])

	def getTempAlarm(self):
		self.writeCommand(8)

	def setTempAlarm(self, min, max):
		self.writeCommand(9, [min, max])

	def getCurrentTemp(self):
		self.writeCommand(10)

	def responseCallback(self):
		if not self.packetReceived:
			return
		packet = self.readPacket()

		if packet.cmd == 0:
			#Ping response
			print 'Device present'
		elif packet.cmd == 1:
			#Erase memory response
			print 'Memory erased ok'
		elif packet.cmd == 2:
			#GetNEntries response
			try:
				print 'Entries: ' + packet.data[0]
			except:
				pass
		elif packet.cmd == 3:
			#getEntry response
			pass
		elif packet.cmd == 4:
			#getTime response
			pass
		elif packet.cmd == 5:
			#setTime response
			pass
		elif packet.cmd == 6:
			#getTimeAlarm response
			pass
		elif packet.cmd == 7:
			#setTimeAlarm response
			pass
		elif packet.cmd == 8:
			#getTempAlarm response
			pass
		elif packet.cmd == 9:
			#setTempAlarm response
			pass
		elif packet.cmd == 9:
			#getCurrentTemp response
			try:
				print 'Temp: ' + packet.data[0]
			except:
				pass
