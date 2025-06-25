PyMeshUp
========

PyMeshUp aims to provide an easy way to make simple volume meshes using a script.

This is done by wrapping some of the features of pymeshlab and adding an gui.

<img width="645" alt="image" src="https://user-images.githubusercontent.com/34062862/194708772-63d63df1-6ee7-4806-865c-52180e1e42df.png">


To run the gui you can simple run:

`python -m pymeshup.GUI`

*or* activate the environment with

`./.venv/Scripts/activate`

and then run:

`pymeshup.exe`.

Install a desktop launcher
--------------------------

Create a desktop launcher of the package by running

`python.exe make_desktop_launcher.py`

Installation as package
------------------------

`pip install pymeshup`

Pre-build executable
--------------------

https://www.open-ocean.org/pymeshup/


Building the executable using pyinstaller
-----------------------------------------
pyinstaller PyMeshupGUI.spec
