from pymeshup.gui.main import *
import netCDF4

def main():
    print("Loading GUI...")

    app = QApplication()
    gui = Gui()
    app.exec()

def run():
    main()

if __name__ == "__main__":
    main()