# coding: utf-8

#Author: Rodrigo Méndez Gamboa

import Tkinter as tk
import ttk
from matplotlib.pyplot import *
import struct
#from pylab import *

'''
// hour and min in dec
typedef struct
{
    BYTE hour;
    BYTE min;
} Time;
  
// date, month and year in dec, year 0-99
typedef struct
{
    BYTE date;
    BYTE month;
    BYTE year;
} Date;

typedef struct
{
    Date date;
    Time time;
    BYTE temp;
} Record;
'''

class Record(struct.Struct):
	def __init__(self, bytes=None):
		struct.Struct.__init__(self, 'BBBBBB')
		self.date = 0
		self.month = 0
		self.year = 0
		self.hour = 0
		self.min = 0
		self.temp = 0

		self.fromRaw(bytes)

	def fromRaw(self, bytes):
		if bytes is None:
			return
		self.date, self.month, self.year, self.hour, self.min, self.temp = self.unpack(bytes)

	def toRaw(self):
		return self.pack(self.date, self.month, self.year, self.hour, self.min, self.temp)

class Database:
	def __init__(self):
		self.nEntries = 0
		self.entries = []

class MainView:
	def __init__(self, window, device):
		self.window = window
		self.device = device
		self.controlFrame = ttk.LabelFrame(self.window, text="Control")
		self.controlFrame.pack(expand="yes", fill="both", padx=10, pady=10)

		self.PingButton = ttk.Button(self.controlFrame, text='Ping', command=device.ping)
		self.PingButton.grid(row=0, column=0)
		self.EraseButton = ttk.Button(self.controlFrame, text='Borrar memoria', command=device.eraseMemory)
		self.EraseButton.grid(row=0, column=1)
		self.GetDataButton = ttk.Button(self.controlFrame, text='Obtener datos', command=self.getData)
		self.GetDataButton.grid(row=0, column=2)
		self.GetTempButton = ttk.Button(self.controlFrame, text='Obtener temperatura actual', command=device.getCurrentTemp)
		self.GetTempButton.grid(row=1, column=0)

		self.PlotButton = ttk.Button(self.controlFrame, text='Graficar datos', command=self.graph)
		self.PlotButton.grid(row=1, column=2)

		self.alarmFrame = ttk.LabelFrame(self.window, text='Alarmas')
		self.alarmFrame.pack(expand="yes", fill="both", padx=10, pady=10)
		self.upTempLabel = ttk.Label(self.alarmFrame, text="Temperatura máxima: ")
		self.upTempSpin = tk.Spinbox(self.alarmFrame, from_=0, to=100)
		self.upTempButton = ttk.Button(self.alarmFrame, text='Configurar máxima', command=self.setHAlarm)
		self.lowTempLabel = ttk.Label(self.alarmFrame, text="Temperatura mínima: ")
		self.lowTempSpin = tk.Spinbox(self.alarmFrame, from_=0, to=100)
		self.lowTempButton = ttk.Button(self.alarmFrame, text='Configurar mínima', command=self.setLAlarm)

		self.upTempLabel.grid(row=0, column=0)
		self.upTempSpin.grid(row=0, column=1)
		self.upTempButton.grid(row=0, column=2)
		self.lowTempLabel.grid(row=1, column=0)
		self.lowTempSpin.grid(row=1, column=1)
		self.lowTempButton.grid(row=1, column=2)

		self.entriesFrame = ttk.LabelFrame(self.window, text='Registros')
		self.entriesFrame.pack(expand="yes", fill="both", padx=10, pady=10)
		self.entriesList = ttk.Treeview(self.entriesFrame, columns=('Fecha', 'Hora', 'Temperatura'), show='headings')
		self.entriesList.pack(expand=True, fill=tk.BOTH)

		self.outputFrame = ttk.LabelFrame(self.window, text="Output")
		self.outputFrame.pack(expand="yes", fill="both", padx=10, pady=10)
		self.scrollbar = ttk.Scrollbar(self.outputFrame)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.output = tk.Text(self.outputFrame, height=8, borderwidth=0, yscrollcommand=self.scrollbar.set)
		self.output.config(font=("consolas", 12), undo=True, wrap='word')
		self.output.pack(side=tk.LEFT, fill=tk.BOTH)
		self.scrollbar.config(command=self.output.yview)

		self.data = []

		self.entries = Database()

		self.device.onGetCurrentTemp.append(self.gotTemp)
		self.device.onGetHAlarm.append(self.gotHAlarm)
		self.device.onGetLAlarm.append(self.gotLAlarm)
		self.device.onNEntries.append(self.gotNEntries)
		self.device.onPing.append(self.gotPing)
		self.device.onEraseMemory.append(self.gotMemErased)

	def setHAlarm(self):
		self.device.setHAlarm(int(self.upTempSpin.get()))

	def setLAlarm(self):
		self.device.setLAlarm(int(self.lowTempSpin.get()))

	def getData(self):
		self.output.insert(tk.END, u'Obteniendo datos...\n')
		# Borrar datos antiguos:
		self.entries.nEntries = 0
		self.entries.entries = []
		self.data = []
		# Get nEntries
		# Get entry1
		# ...
		# Get entry n
		# end
		self.device.getHAlarm()
		self.device.getLAlarm()
		self.device.getNEntries()

	def gotHAlarm(self, temp):
		self.output.insert(tk.End, u'Temperatura máxima: %d\n' % temp)
		self.upTempSpin.set(temp)

	def gotLAlarm(self, temp):
		self.output.insert(tk.End, u'Temperatura mínima: %d\n' % temp)
		self.lowTempSpin.set(temp)

	def gotNEntries(self, entries):
		self.output.insert(tk.End, u'Número de registros: %d\n' % entries)
		self.entries.nEntries = entries
		# Start requesting entries
		index = len(self.entries.entries)
		if lindex < self.entries.nEntries:
			self.device.getEntry(index)

	def gotEntry(self, entry):
		# Save entry
		newEntry = Record(entry)
		self.entries.entries.append(newEntry)
		# Append to plotted data
		self.data.append(newEntry.temp)
		# Request next entry:
		index = len(self.entries.entries)
		if lindex < self.entries.nEntries:
			self.device.getEntry(index)

		self.output.insert(tk.End, u'Entrada %d obtenida.\n' % index)


	def gotPing(self):
		self.output.insert(tk.End, u'Dispositivo encontrado correctamente.\n')

	def gotMemErased(self):
		self.output.insert(tk.End, u'Memoria borrada correctamente.\n')

	def gotTemp(self, temp):
		if temp > 100 or temp < 6:
			return
		self.output.insert(tk.END, 'Temperatura: %d\n' % temp)
		self.data.append(temp)

	def graph(self):
		figure()
		plot(self.data, 'r')
		xlabel('Tiempo')
		ylabel('Temperatura')
		title('Datos')
		show()

