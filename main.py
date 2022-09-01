import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import pyperclip
from jupyterManager import JupyterLabManager
from addLabUI import SubUI


class UI(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master, bg=None)
    self.master = master
    self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
    self.manager = JupyterLabManager()
    self.statusVar = tk.StringVar(value='Unknown')
    self.pathVar = tk.StringVar(value='')
    self.portVar = tk.StringVar(value="Unknown")
    self.startLabel = tk.StringVar(value="Start")
    self.tokenVar = tk.StringVar(value="Unknown")
    self.create_widgets()
    self.put_widgets()
    self.winfo_toplevel().title("Jupyterlab Manager")
    self.master.protocol("WM_DELETE_WINDOW", self.on_closing)


  def on_closing(self):
    stillRunning = False
    for config in self.manager.configs:
      if config["running"]:
        stillRunning = True
    if stillRunning:
      quitMsg = "There are some labs still running, do you want to close all and quit?"
      if tk.messagebox.askokcancel("Quit", quitMsg):
        self.manager.stopAll()
        self.manager.saves()
        self.master.destroy()
      return
    self.manager.saves()
    self.master.destroy()



  def create_widgets(self):
    self.listbox = tk.Listbox(self, height=10, listvariable=self.manager.recall_name)
    self.listbox.bind('<<ListboxSelect>>', self.listBoxChange)
    self.labelStatus1 = ttk.Label(self, text="Status:", width=6)
    self.labelStatus2 = ttk.Label(self, textvariable=self.statusVar, width=10)
    self.labelPort1 = ttk.Label(self, text="Port:", width=6)
    self.labelPort2 = ttk.Label(self, textvariable=self.portVar, width=10)
    self.labelPath = ttk.Label(self, textvariable=self.pathVar, width=50)
    self.addLabBtn = ttk.Button(self, text="Add Lab", command=self.addLab)
    self.startBtn = ttk.Button(self, textvariable=self.startLabel, command=self.startBtnEvt)
    self.stopBtn = ttk.Button(self, text="Stop", command=self.stopBtnEvt)
    self.startBtn.state(["disabled"])
    self.stopBtn.state(["disabled"])
    self.labelToken1 = ttk.Label(self, text="Token:", width=6)
    self.labelToken2 = ttk.Label(self, textvariable=self.tokenVar, width=20)

    for i in range(0,self.manager.n):
      if i % 2 == 0:
        self.listbox.itemconfigure(i, {'bg':'#f0f0ff'})
      self.listbox.itemconfigure(i, {'fg': '#ff0000'})

    self.labelToken2.bind("<Double-1>", self.copyToken)
    self.listbox.bind("<Delete>", self.deleteLab)


  def put_widgets(self):
    self.listbox.grid(column=0, row=0, rowspan=5)
    # self.listbox.selection_set(0)
    # self.listBoxChange(None)
    self.labelStatus1.grid(column=1, row=0, sticky=tk.E, padx=2)
    self.labelStatus2.grid(column=2, row=0, sticky=tk.W, padx=2)
    self.labelPort1.grid(column=1, row=1, sticky=tk.E, padx=2)
    self.labelPort2.grid(column=2, row=1, sticky=tk.W, padx=2)
    self.labelToken1.grid(column=1, row=2, sticky=tk.E, padx=2)
    self.labelToken2.grid(column=2, row=2, columnspan=2, sticky=tk.W, padx=2)
    self.labelPath.grid(column=1, row=5, columnspan=2)
    self.addLabBtn.grid(column=0, row=5)
    self.startBtn.grid(column=1, row=3, rowspan=2, sticky=tk.E, padx=4)
    self.stopBtn.grid(column=2, row=3, rowspan=2, sticky=tk.W, padx=4)


  def listBoxChange(self, e):
    self.selectionUpdate(self.getIndex())


  def getIndex(self):
    idxs = self.listbox.curselection()
    if len(idxs) == 1:
      return idxs[0]


  def selectionUpdate(self, idx):
    if idx is None:
      return
    running = self.manager.configs[idx]["running"]
    self.statusVar.set("Running" if running else "Stopped")
    self.labelStatus2.configure(foreground="green" if running else "red")
    self.pathVar.set(self.manager.labs[idx]["path"])
    self.startBtn.state(["!disabled"])
    port = self.manager.configs[idx]["port"]
    token = self.manager.configs[idx]["token"]
    self.portVar.set("Unknown" if port is None else str(port))
    self.tokenVar.set("Unknown" if token is None else token)
    if running:
      self.stopBtn.state(["!disabled"])
      self.startLabel.set("Open")
    else:
      self.startLabel.set("Start" if port is None else "Restart")
      self.stopBtn.state(["disabled"])


  def startBtnEvt(self, e=None):
    idx = self.getIndex()
    if idx is None:
      return
    if self.manager.configs[idx]["running"]:
      self.manager.open(idx)
    else:
      self.startBtn.state(["disabled"])
      self.manager.start(idx)
      self.startBtn.state(["!disabled"])
      self.stopBtn.state(["!disabled"])
      self.startLabel.set("Open")
      self.listbox.itemconfigure(idx, {'fg': 'green'})
    self.selectionUpdate(idx)


  def stopBtnEvt(self, e=None):
    idx = self.getIndex()
    if idx is None:
      return
    self.stopBtn.state(["disabled"])
    self.manager.stop(idx)
    self.startLabel.set("Restart")
    self.listbox.itemconfigure(idx, {'fg': '#ff0000'})
    self.selectionUpdate(idx)


  def copyToken(self, e):
    idx = self.getIndex()
    if idx is None:
      return
    token = self.manager.configs[idx]["token"]
    if token is None:
      return
    pyperclip.copy(token)
    tk.messagebox.showinfo(title="Jupyterlab Manager info", message="Token copied")


  def addLab(self, e=None):
    self.prompt = tk.Toplevel(self)
    self.prompt.title("Add new lab")
    self.subUI = SubUI(self.prompt, self)


  def deleteLab(self, e=None):
    idx = self.getIndex()
    if idx is None:
      return
    self.manager.delete(idx)


  def submit(self):
    self.manager.add(self.subUI.name, self.subUI.path)
    self.prompt.destroy()
    self.subUI = None
    self.prompt = None
    # self.listbox.listvariable = self.manager.recall_name
    if self.manager.n % 2 == 1:
      self.listbox.itemconfigure(self.manager.n-1, background='#f0f0ff')
    self.listbox.itemconfigure(self.manager.n-1, foreground='#ff0000')


root = tk.Tk()
root.resizable(False,False)
app = UI(root)
app.mainloop()


