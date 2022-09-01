# Jupyter Lab Manager
#### A small program to manage multiple jupyter labs without multiple command lines/terminals.

After working with many jupyter labs in different directories and opening a bunch of terminals, I decide to write this tiny little program to help me manage which labs I am working on, and its status (running/stopped).

This repo requires only `tkintertable`, `pyperclip` for utilities, and `jupyterlab`, of course.

#### How to use:

- Use "Add Lab" button to add the directory you are working on
- Select the lab in the list, then click the "Start" button to start the lab.
- On the info panel on the left side, there's the status, the port, and the token of the running lab. Double click on the token field will copy the token to your clipboard.
- Click on the "Open" button (it was the "Start" button before starting the lab) will open the lab in your default browser without having to input the token.
- To stop the lab, simple click on the "Stop" button.
- To remove any labs you no longer work on it, click on the lab in the list and press Delete.