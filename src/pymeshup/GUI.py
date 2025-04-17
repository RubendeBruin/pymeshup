print("Loading GUI...")

from pymeshup.gui.main import *

import netCDF4

app = QApplication()
gui = Gui()
app.exec()