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
from Event import Event
import datetime

class DevControl(Comm):
	def __init__(self, connection):
		Comm.__init__(self, connection)
		self.rxCallback = self.responseCallback

		self.onPing = Event()
		self.onEraseMemory = Event()
		self.onNEntries = Event()
		self.onEntry = Event()
		self.onGetTime = Event()
		self.onSetTime = Event()
		self.onGetHAlarm = Event()
		self.onSetHAlarm = Event()
		self.onGetLAlarm = Event()
		self.onSetLAlarm = Event()
		self.onGetCurrentTemp = Event()

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
		# TODO: Implement correctly
		now = datetime.datetime.now()
		self.writeCommand(5, [now.second, now.minute, now.hour, now.day, now.month, now.year])

	def getHAlarm(self):
		self.writeCommand(6)

	def setHAlarm(self, temp):
		print temp
		self.writeCommand(7, [temp])

	def getLAlarm(self):
		self.writeCommand(8)

	def setLAlarm(self, temp):
		print temp
		self.writeCommand(9, [temp])

	def getCurrentTemp(self):
		self.writeCommand(10)

	def responseCallback(self):
		if not self.packetReceived:
			return
		packet = self.readPacket()
		if packet is None:
			return

		if packet.cmd == 0:
			#Ping response
			self.onPing()
			print 'Device present'
		elif packet.cmd == 1:
			#Erase memory response
			self.onEraseMemory()
			print 'Memory erased ok'
		elif packet.cmd == 2:
			#GetNEntries response
			try:
				print 'Entries: ' + packet.data[0]
				self.onNEntries(packet.data[0])
			except:
				pass
		elif packet.cmd == 3:
			#getEntry response
			try:
				self.onEntry(packet.data)
			except:
				pass
		elif packet.cmd == 4:
			#getTime response
			try:
				self.onGetTime(packet.data)
			except:
				pass
		elif packet.cmd == 5:
			#setTime response
			self.onSetTime()
		elif packet.cmd == 6:
			#getHAlarm response
			self.onGetHAlarm(packet.data)
		elif packet.cmd == 7:
			#setHAlarm response
			self.onSetHAlarm()
		elif packet.cmd == 8:
			#getLAlarm response
			self.onGetLAlarm(packet.data)
		elif packet.cmd == 9:
			#setLAlarm response
			self.onSetLAlarm()
		elif packet.cmd == 10:
			#getCurrentTemp response
			try:
				print 'Temp: ' + str(packet.data[0])
				self.onGetCurrentTemp(packet.data[0])
			except:
				pass
