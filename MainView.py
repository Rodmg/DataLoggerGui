# coding: utf-8

#Author: Rodrigo Méndez Gamboa

import Tkinter as tk
import ttk
from matplotlib.pyplot import *
#from pylab import *

class Database:
	def __init__(self):
		self.nEntries = 0
		self.entries = []

class MainView:
	def __init__(self, window, device):
		self.window = window
		self.device = device
		self.frame = ttk.Frame(self.window)
		self.frame.pack()
		self.inFrameTop = ttk.Frame(self.frame)
		self.inFrameBottom = ttk.Frame(self.frame)
		self.inFrameTop.pack()
		self.inFrameBottom.pack()

		self.PingButton = ttk.Button(self.inFrameTop, text='Ping', command=device.ping)
		self.PingButton.grid(row=0, column=0)
		self.EraseButton = ttk.Button(self.inFrameTop, text='Borrar memoria', command=device.eraseMemory)
		self.EraseButton.grid(row=1, column=0)
		self.GetDataButton = ttk.Button(self.inFrameTop, text='Obtener datos', command=self.getData)
		self.GetDataButton.grid(row=0, column=1)
		self.GetTempButton = ttk.Button(self.inFrameTop, text='Obtener temperatura', command=device.getCurrentTemp)
		self.GetTempButton.grid(row=1, column=1)

		self.PlotButton = ttk.Button(self.inFrameTop, text='Graficar datos', command=self.graph)
		self.PlotButton.grid(row=2, column=1)

		self.output = tk.Text(self.inFrameBottom, borderwidth=3, relief="sunken")
		self.output.config(font=("consolas", 12), undo=True, wrap='word')
		self.output.pack()

		self.data = []

		self.entries = Database()

		self.device.onGetCurrentTemp.append(self.gotTemp)

	def getData(self):
		self.output.insert(tk.END, 'Hola\n')
		# Get nEntries
		# Get entry1
		# ...
		# Get entry n
		# end

	def gotNEntries(self, entries):
		self.entries.nEntries = entries

	def gotTemp(self, temp):
		if temp > 100 or temp < 6:
			return
		self.output.insert(tk.END, str(temp) + '\n')
		self.data.append(temp)

	def graph(self):
		figure()
		plot(self.data, 'r')
		xlabel('Tiempo')
		ylabel('Temperatura')
		title('Datos')
		show()

