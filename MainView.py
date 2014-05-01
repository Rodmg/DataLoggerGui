# coding: utf-8

#Author: Rodrigo Méndez Gamboa

import Tkinter as tk
from matplotlib.pyplot import *
#from pylab import *

class MainView:
	def __init__(self, window, device):
		self.window = window
		self.device = device
		self.PingButton = tk.Button(self.window, text='Ping', command=device.ping)
		self.PingButton.pack()
		self.EraseButton = tk.Button(self.window, text='Borrar memoria', command=device.eraseMemory)
		self.EraseButton.pack()
		self.GetDataButton = tk.Button(self.window, text='Obtener datos', command=self.getData)
		self.GetDataButton.pack()
		self.GetTempButton = tk.Button(self.window, text='Obtener temperatura', command=device.getCurrentTemp)
		self.GetTempButton.pack()

		self.PlotButton = tk.Button(self.window, text='Graficar datos', command=self.graph)
		self.PlotButton.pack()

		self.output = tk.Text(self.window, borderwidth=3, relief="sunken")
		self.output.config(font=("consolas", 12), undo=True, wrap='word')
		self.output.pack()

		self.data = [1,2,34,5,6,76,3,24,3,45,46,7,65,4,54,645,4,43,56,35,34,5,6,34,4,34,6,156,5]

	def getData(self):
		self.output.insert(tk.END, 'Holaaaa\n')

	def graph(self):
		figure()
		plot(self.data, 'r')
		xlabel('Tiempo')
		ylabel('Temperatura')
		title('Datos')
		show()

