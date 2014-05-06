#!/usr/bin/python
# coding: utf-8

#Author: Rodrigo Méndez Gamboa

import serial
from serial.tools import list_ports
import Tkinter as tk
import ttk
from DevControl import DevControl
from Event import Event
from MainView import MainView

BAUDRATE = 19200

class SerialSelector:
	def __init__(self):
		self.frame = ttk.LabelFrame(window, text='Conectar')
		self.frame.pack(expand="yes", fill="both", padx=10, pady=10)
		self.inFrameTop = ttk.Frame(self.frame)
		self.inFrameBottom = ttk.Frame(self.frame)
		self.inFrameTop.pack()
		self.inFrameBottom.pack()
		self.connection = serial.Serial()
		self.ports = ['No hay puertos']
		self.selectedPort = tk.StringVar()
		self.portsLabel = ttk.Label(self.inFrameTop, text='Puerto: ')
		self.portsLabel.pack(side=tk.LEFT)
		self.select = ttk.OptionMenu(self.inFrameTop, self.selectedPort, *self.ports)
		self.select.pack(side=tk.LEFT)
		self.reloadButton = ttk.Button(self.inFrameBottom, text='Recargar puertos', command=self.loadPorts)
		self.reloadButton.pack(side=tk.LEFT)
		self.connectButton = ttk.Button(self.inFrameBottom, text='Conectar', command=self.connect)
		self.connectButton.pack(side=tk.LEFT)
		self.disconnectButton = ttk.Button(self.inFrameBottom, text='Desconectar', command=self.disconnect)
		self.disconnectButton.pack(side=tk.LEFT)
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
	window.wm_title('Control DataLogger')
	window.configure(background='#E8E9E8')
	selector = SerialSelector()
	device = DevControl(selector.connection)
	mainView = MainView(window, device)
	selector.onPortChanged.append(device.setConnection)
	device.daemon = True
	device.start()
	window.mainloop()
