import sys
sys.path.append(r"C:\data\DAVE\public\pymeshup\src")
sys.path.append(r"C:\data\DAVE\public\mafredo\src")

from pymeshup.gui.main import *

app = QApplication()
gui = Gui()
app.exec()
