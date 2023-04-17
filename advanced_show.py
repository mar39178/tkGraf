from os.path import basename, splitext
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
import tkinter.ttk as ttk
import os.path

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
    name = "Graf"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5, fill="x")
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(fill="x")
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.selectFile)
        self.fileBtn.pack(anchor="e")
        
        self.dataFormatVar = tk.IntVar(value=1)
        self.rowRadio = tk.Radiobutton(self.fileFrame, text="Data v řádcích", variable=self.dataFormatVar, value=1)
        self.rowRadio.pack(anchor="w")
        self.columnRadio = tk.Radiobutton(self.fileFrame, text="Data ve sloupcích", variable=self.dataFormatVar, value=2)
        self.columnRadio.pack(anchor="w")

        self.graphFrame = tk.LabelFrame(self, text="Graf")
        self.graphFrame.pack(fill="x")
        tk.Label(self.graphFrame, text='Title').grid(row=0, column=0)
        self.titleEntry = MyEntry(self.graphFrame)
        self.titleEntry.grid(row=0, column=1)
        tk.Label(self.graphFrame, text='Osa X').grid(row=1, column=0)
        self.xEntry = MyEntry(self.graphFrame)
        self.xEntry.grid(row=1, column=1)
        tk.Label(self.graphFrame, text='Osa Y').grid(row=2, column=0)
        self.yEntry = MyEntry(self.graphFrame)
        self.yEntry.grid(row=2, column=1)
        tk.Label(self.graphFrame, text='Mřížka').grid(row=3, column=0)
        self.gridVar = tk.BooleanVar(value=True)
        self.gridOpt = tk.Checkbutton(self.graphFrame, variable=self.gridVar)
        self.gridOpt.grid(row=3, column=1, sticky=tk.W)
        tk.Label(self.graphFrame, text='Aproximace').grid(row=4, column=0)
        self.aproxOpt = tk.Checkbutton(self.graphFrame)
        self.aproxOpt.grid(row=4, column=1, sticky=tk.W)
        tk.Label(self.graphFrame, text='Čára').grid(row=5, column=0)
        self.lineVar = tk.StringVar(value="-")
        self.lineCBox = ttk.Combobox(self.graphFrame, values=("-", "--", "-.", ":"), textvariable=self.lineVar)
        self.lineCBox.grid(row=5, column=1)

        self.makeBtn = tk.Button(self, text="Vykreslit", command=self.plot)
        self.makeBtn.pack(pady="5", anchor="w")

        # -------------------------------
        self.quitBtn = tk.Button(self, text="Quit", command=quit)
        self.quitBtn.pack()

    def quit(self, event=None):
        super().quit()

    def selectFile(self):
        self.fileEntry.value = tk.filedialog.askopenfilename()

    def plot(self):
        if not os.path.isfile(self.fileEntry.value):
            return
        with open(self.fileEntry.value, "r") as f:
            if self.dataFormatVar.get() == 1:
                x = f.readline().split(";")
                x = [float(i.replace(",", ".")) for i in x]

                y = f.readline().split(";")
                y = [float(i.replace(",", ".")) for i in y]
            elif self.dataFormatVar.get() == 2:
                q = f.readlines()
                x = []
                y = []
                for line in q:
                    if line != '':
                        w = line.split(";")
                        x.append(float(w[0].replace(",", ".")))
                        y.append(float(w[1].replace(",", ".")))

        plt.plot(x, y, linestyle=self.lineVar.get())
        plt.title(self.titleEntry.value)
        plt.xlabel(self.xEntry.value)
        plt.ylabel(self.yEntry.value)
        plt.grid(self.gridVar.get())
        plt.show()



app = Application()
app.mainloop()
