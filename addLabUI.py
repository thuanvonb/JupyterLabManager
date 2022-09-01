import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

class SubUI(tk.Frame):
  def __init__(self, master, parent):
    super().__init__(master, bg=None)
    self.parent = parent
    self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
    self.label1 = ttk.Label(self, text="Lab name:")
    self.label2 = ttk.Label(self, text="Path:")
    self.nameVar = tk.StringVar()
    self.pathVar = tk.StringVar()
    self.text = tk.Entry(self, textvariable=self.nameVar, width=20)
    self.button = ttk.Button(self, text="Browse", command=self.browseFolder, width=10)
    self.label3 = ttk.Label(self, textvariable=self.pathVar, width=40)
    self.submitButton = ttk.Button(self, text="Add", width=7, command=self.parent.submit)
    self.submitButton.state(["disabled"])
    self.putsWidgets()
    self.path = ""
    self.name = ""
    self.text.bind("<Key>", self.onInput)
    self.nameVar.trace("w", self.onInput)


  def putsWidgets(self):
    self.label1.grid(column=0, row=0, sticky='e')
    self.label2.grid(column=0, row=1, sticky='e')
    self.text.grid(column=1, row=0, sticky='w', columnspan=2)
    self.button.grid(column=1, row=1, padx=0)
    self.label3.grid(column=2, row=1, sticky='w', padx=0)
    self.submitButton.grid(column=0, row=2, columnspan=3)


  def browseFolder(self, e=None):
    filename = tk.filedialog.askdirectory()
    self.setActive()
    self.pathVar.set(filename)
    self.path = filename
    if self.name != "" and self.path != "":
      self.submitButton.state(["!disabled"])
    else:
      self.submitButton.state(["disabled"])


  def onInput(self, *args, **kwargs):
    self.name = self.nameVar.get()
    if self.name != "" and self.path != "":
      self.submitButton.state(["!disabled"])
    else:
      self.submitButton.state(["disabled"])


  def setActive(self):
    self.lift()
    self.focus_force()
    self.grab_set()
    self.grab_release()