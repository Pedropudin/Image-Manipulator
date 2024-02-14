from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Conversor de Imagem para PDF")

mainframe = ttk.Frame(root, padding="300 3 12 12") #padding é a distância vazia que vai ter em cada parede
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

meters = StringVar()

ttk.Button(mainframe, text="Converter").grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Imagem e PDF").grid(column=0, row=1, sticky=N)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()