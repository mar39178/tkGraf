#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from matplotlib import pyplot as plt

# from tkinter import ttk

class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Show graph"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)

        self.entry = tk.Entry()
        self.entry.pack()
        self.btn1 = tk.Button(text="...", command=self.find)
        self.btn1.pack()
        self.btn2 = tk.Button(text="Vykreslit", command=self.show)
        self.btn2.pack()
        self.btn3 = tk.Button(text="Quit", command=quit)
        self.btn3.pack()

    
    def find(self):
        file = filedialog.askopenfile()   
        self.entry.insert(0, file.name)

    def show(self):
        file = self.entry.get()
        f = open(file, "r")
        content = f.readlines()
        x_values = []
        y_values = []
        for line in content:
            lines = line.split()
            x_values.append(float(lines[0]))
            y_values.append(float(lines[1]))
        plt.plot(x_values, y_values)  
        plt.show()          

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()
