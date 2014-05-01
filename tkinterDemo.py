import Tkinter as tk

def pressed():
	print 'You pressed me!'

root = tk.Tk()
tk.Label(root, text="Hello, world").pack()

tk.Button(root, text='Press me!', command=pressed).pack()

entry = tk.Entry(root)
entry.pack()
entry.insert(0, 'some text')

value = tk.IntVar()
tk.Checkbutton(root, text='Checked?', variable=value).pack()

value = tk.IntVar()
for n in range(4):
	tk.Radiobutton(root, value=n, text="Selection %d"%(n+1), variable=value).pack()

value = tk.StringVar(value='One')
tk.OptionMenu(root, value, 'One', 'Two', 'Three').pack()

listbox = tk.Listbox(root)
listbox.pack()
listbox.insert(tk.END, 'a list entry')
for item in 'one two three four'.split():
	listbox.insert(tk.END, item)

text = tk.Text(root)
text.pack()
text.insert(tk.END, '''some text
		more text''')

scale = tk.Scale(root, from_=0, to=100)
scale.pack()

root.mainloop()

