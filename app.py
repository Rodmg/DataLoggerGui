#!/usr/bin/python
# coding: utf-8

#Author: Rodrigo Méndez Gamboa

import serial
from serial.tools import list_ports
import Tkinter as tk
from DevControl import DevControl
from Event import Event
from MainView import MainView

BAUDRATE = 9600

class SerialSelector:
	def __init__(self):
		self.connection = serial.Serial()
		self.ports = ['No hay puertos']
		self.selectedPort = tk.StringVar()
		self.select = tk.OptionMenu(window, self.selectedPort, *self.ports)
		self.select.pack()
		self.reloadButton = tk.Button(window, text='Recargar', command=self.loadPorts)
		self.reloadButton.pack(side=tk.LEFT)
		self.connectButton = tk.Button(window, text='Conectar', command=self.connect)
		self.connectButton.pack(side=tk.RIGHT)
		self.disconnectButton = tk.Button(window, text='Desconectar', command=self.disconnect)
		self.disconnectButton.pack()
		self.loadPorts()

		self.onPortChanged = Event()

	def loadPorts(self):
		self.ports = []
		for port in list_ports.comports():
			self.ports.append(port[0])
		
		if len(self.ports) <= 0:
			self.ports = ['No hay puertos']

		self.selectedPort.set(self.ports[0])
		self.select['menu'].delete(0, 'end')

		for port in self.ports:
			self.select['menu'].add_command(label=port, command=tk._setit(self.selectedPort, port))

	def connect(self):
		self.connection.close()
		if self.selectedPort.get() != 'No hay puertos':
			self.connection.baudrate = BAUDRATE
			self.connection.port = self.selectedPort.get()
			self.connection.open()
			self.onPortChanged(self.connection)

	def disconnect(self):
		self.connection.close()




if __name__ == '__main__':
	window = tk.Tk()
	selector = SerialSelector()
	device = DevControl(selector.connection)
	mainView = MainView(window, device)
	selector.onPortChanged.append(device.setConnection)
	device.daemon = True
	device.start()
	window.mainloop()
