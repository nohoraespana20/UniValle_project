import tkinter as tk
from tkinter import ttk
from tkinter import *

# bind the selected value changes
def currency_changed(event):
    _currency = selected_currency.get()
    etiqueta.config(text = _currency)

root = tk.Tk()

# config the root window
root.geometry('600x400')
root.resizable(True, True)
root.title('APP test')

# Currency label
label1 = ttk.Label(text = "Please select a currency: ")
label1.grid(row=0, column=0)

# Currency combobox
selected_currency = tk.StringVar()
currency_cb = ttk.Combobox(root, textvariable = selected_currency)
currency_cb['values'] = ['COP', 'USD']
currency_cb['state'] = 'readonly'
currency_cb.grid(row=0, column=1)

currency_cb.bind('<<ComboboxSelected>>', currency_changed)

# etiqueta = ttk.Label(root, text = " Valor ")
# etiqueta.grid(row=1, column=0)

# Cost label
label2 = ttk.Label(text = "CONVENTIONAL VEHICLE")
label2.grid(row=2, column=0)

# Cost label
label3 = ttk.Label(text = "ELECTRIC VEHICLE")
label3.grid(row=2, column=3)

# Cost label
label4 = ttk.Label(text = "Total vehicle cost: ")
label4.grid(row=3, column=0)

valor1 = ""
entrada_texto = Entry(root, width=10, textvariable=valor1)
entrada_texto.grid(row=3, column=1)

# Cost label
label4 = ttk.Label(text = "Total vehicle cost: ")
label4.grid(row=3, column=3)

valor2 = ""
entrada_texto = Entry(root, width=10, textvariable=valor2)
entrada_texto.grid(row=3, column=4)

root.mainloop()