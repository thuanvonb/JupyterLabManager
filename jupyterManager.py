import tkinter as tk
import os
import json
import socket
import subprocess
import re
from random import randint
import webbrowser

def is_port_in_use(port: int) -> bool:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    return s.connect_ex(('localhost', port)) == 0

regex = re.compile(r'token=([0-9a-z]+)')

class JupyterLabManager:
  def __init__(self):
    self.labs = []
    self.loads()
    self.names = [lab["name"] for lab in self.labs]
    self.recall_name = tk.StringVar(value=self.names)
    self.configs = []
    for i in range(len(self.labs)):
      config = dict()
      config["running"] = False
      config["process"] = None
      config["port"] = None
      config["token"] = None
      self.configs.append(config)
    self.n = len(self.labs)


  def loads(self):
    if not os.path.exists("labs.json"):
      return
    with open("labs.json", "r") as f:
      dat = f.read()
      self.labs = json.loads(dat)


  def saves(self):
    with open("labs.json", "w") as f:
      data = json.dumps(self.labs)
      f.write(data)


  def start(self, idx):
    config = self.configs[idx]
    if config["running"]:
      return
    while config["port"] is None or is_port_in_use(config["port"]):
      config["port"] = randint(1000, 65535)

    port = config["port"]
    config["process"] = proc = subprocess.Popen(["jupyter-lab", "--no-browser", "--notebook-dir=\"%s\"" % self.labs[idx]["path"], "--port=%d" % port],stderr=subprocess.PIPE)
    token = None
    for line in iter(proc.stderr.readline, b''):
      line = proc.stderr.readline().decode()
      match = re.search(regex, line)
      if match is not None:
        token = match.groups()[0]
        break
    config["token"] = token
    config["running"] = True


  def stop(self, idx):
    config = self.configs[idx]
    if not config["running"]:
      return
    config["process"].terminate()
    config["process"] = None
    config["token"] = None
    config["running"] = False


  def open(self, idx):
    port = self.configs[idx]["port"]
    token = self.configs[idx]["token"]
    url = f"http://localhost:{port}/lab?token={token}"
    webbrowser.open(url, new=0, autoraise=True)


  def stopAll(self):
    for i in range(self.n):
      self.stop(i)


  def add(self, name, path):
    self.labs.append({
      "name": name, 
      "path": path
    })
    self.configs.append({
      "running": False,
      "process": None,
      "port": None,
      "token": None
    })
    self.n += 1
    self.names.append(name)
    self.recall_name.set(self.names)


  def delete(self, idx):
    if idx >= self.n or idx < 0:
      return
    del self.labs[idx]
    del self.configs[idx]
    del self.names[idx]
    self.recall_name.set(self.names)
