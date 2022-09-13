from PySide6.QtGui import QBrush, QColor, QFont, QFontMetricsF
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt

from pymeshup import *
from pymeshup.gui.forms.main_form import Ui_MainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


from matplotlib.backends.backend_qtagg import (FigureCanvas,
     NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import cm

from pymeshup.gui.helpers.highlighter import PythonHighlighter

HELP = """
<html><body><b>PyMeshUp</b>
PyMeshUp is a simple script-based application to generate meshes.<br><br>
Primitive volumes can be created using:
- Box(xmin, xmax, ymin, ymax, zmin, zmax)
- Cylinder(radius, height, resolution)

Or load them from a file
- Load('filename') 

Meshes can be combined and modified using:
- add(other)
- remove(other)
- rotate(x,y,z)
- move(x,y,z)
- scale(x,y,z)
- crop(xmin, xmax, ymin, ymax, zmin, zmax)

Hulls can be constructed using Frames
- First construct a Frame using
  f1 =  Frame(x1,y1,x2,y2,...)
  f2 =  Frame(x1,y1,x2,y2,...)
- then construct a hull from frames and their positions using
  h = Hull(0,f1, 20, f2, 30, f2, ...)

Creating a panel distribution:
- regrid(iterations=10, pct=5)

Deleting
- del(what) removes what

Other
- The script is vanilla Python with pymeshup imported.
- print('hello world') will work

</body></html>

"""


import vedo

example_code = """
c = Cylinder()
b = Box(xmin=0, zmax=3, ymin=-3, ymax=3)
e = c.inside_of(b)

frame2 = (0, 0,
          0.1, 0,
          0.9, 0,
          1.0, 0.1,
          1, 1)

frame1 = (0, -0.1,
          0.1, -0.1,
          0.1, 0.3,
          1, 0.3,
          1, 1)

f1 = Frame(*frame1).autocomplete()
f2 = Frame(*frame2).autocomplete()
fb = Frame(0, 1  # bow

h = Hull(0, f1,
         5, f2,
         15, f2,
         20, fb)

h = h.remove(c)  # cut cylinder from hull

hg = h.regrid()
"""

COLORMAP = cm.tab20

class Gui():

    def __init__(self):
        # Main Window
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.label.setText(HELP.replace('\n','<br>'))

        # ---- Volumes

        self._actors = []

        self.panel3d = QVTKRenderWindowInteractor()
        layout = QVBoxLayout()
        layout.addWidget(self.panel3d)
        self.ui.widgetGraphics.setLayout(layout)

        self.plotter = vedo.Plotter(qtWidget=self.panel3d)

        self.ui.teCode.setPlainText(example_code)

        self.ui.pushButton.pressed.connect(self.run)
        self.ui.listVolumes.itemChanged.connect(self.update_visibility)

        # ---- Frames

        # See: https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html

        layout = QVBoxLayout()

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax = self.static_canvas.figure.subplots()

        # Ideally one would use self.addToolBar here, but it is slightly
        # incompatible between PyQt6 and other bindings, so we just add the
        # toolbar as a plain widget instead.
        layout.addWidget(NavigationToolbar(self.static_canvas, self.MainWindow))
        layout.addWidget(self.static_canvas)

        self.ui.widgetPlot.setLayout(layout)

        self.ui.listFrames.currentRowChanged.connect(self.select_frame)

        self.ui.splitter.setStretchFactor(1,60)

        # ---- Code formatting

        font = QFont()
        font.setPointSize(12)
        font.setFamily('Segou UI')
        self.ui.teCode.setFont(font)
        self.ui.teCode.setTabStopDistance(QFontMetricsF(self.ui.teCode.font()).horizontalAdvance(' ') * 4)

        highlight = PythonHighlighter(self.ui.teCode.document())

        # ---- Finalize

        self.MainWindow.show()

    def run(self):
        code = self.ui.teCode.toPlainText()
        self.ui.teFeedback.clear()

        key_before = [v for v in locals().keys()]

        try:
            exec(code)
            self.ui.teFeedback.setPlainText("Done!")

        except Exception as E:

            print(f'Error {E.msg} in {E.text}')
            print(f'Error on line {E.lineno} to {E.end_lineno}')
            print(f'Error from {E.offset} to {E.end_offset}')

            self.ui.teFeedback.setPlainText(str(E))


        key_after = [v for v in locals().keys()]
        local_vars = [v for v in locals().values()]
        items_after = [i for i in locals().items()]

        volumes = dict()
        frames = dict()

        for key, value in items_after:
            if key not in key_before:
                print(f'New variable found: {key}')

                if isinstance(value, Volume):
                    volumes[key] = value
                elif isinstance(value, Frame):
                    frames[key] = value

        self.frames = frames
        self.volumes = volumes

        self.update_3dplotter()
        self.update_3d_listbox()
        self.update_visibility()

        self.update_frames_listbox()
        self.plot_frames()

    # --- Frame plot

    def update_frames_listbox(self):
        self.ui.listFrames.blockSignals(True)
        self.ui.listFrames.clear()

        self.ui.listFrames.addItems(self.frames.keys())
        self.ui.listFrames.blockSignals(False)

    def select_frame(self):
        name = self.ui.listFrames.currentItem().text()
        self.plot_frames(active_key=name)

    def plot_frames(self, active_key = None):

        self.static_ax.clear()

        for key, frame in self.frames.items():

            xx = [p[0] for p in frame.xy]
            yy = [p[1] for p in frame.xy]

            self.static_ax.plot(xx,yy,'k-', linewidth = 0.5)

        if active_key is not None:
            frame = self.frames[active_key]

            xx = [p[0] for p in frame.xy]
            yy = [p[1] for p in frame.xy]

            self.static_ax.plot(xx, yy, 'b-', linewidth=1)

            for i, point in enumerate(frame.xy):
                self.static_ax.plot(point[0], point[1], 'k.' )
                self.static_ax.text(point[0], point[1], str(i))

        self.static_canvas.figure.canvas.draw()

    # --- 3D

    def update_3d_listbox(self):

        self.ui.listVolumes.blockSignals(True)

        # remember currently unchecked items
        unchecked = []
        for irow in range(self.ui.listVolumes.count()):
            item = self.ui.listVolumes.item(irow)
            key = item.text()
            visible = item.checkState() == Qt.CheckState.Checked
            if not visible:
                unchecked.append(key)



        self.ui.listVolumes.clear()

        icol = 0
        for key, value in self.volumes.items():
            item = QListWidgetItem(str(key))
            if key in unchecked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

            rgb = COLORMAP(icol)
            brush = QBrush(QColor.fromRgb(254*rgb[0], 254*rgb[1], 254*rgb[2]))
            item.setBackground(brush)
            self.ui.listVolumes.addItem(item)
            icol += 1

        self.ui.listVolumes.blockSignals(False)

    def update_visibility(self):
        for irow in range(self.ui.listVolumes.count()):
            item = self.ui.listVolumes.item(irow)
            key = item.text()
            visible = item.checkState() == Qt.CheckState.Checked
            self.volumes[key].actor.SetVisibility(visible)


        self.plotter.render()
        self.panel3d.update()

    def update_3dplotter(self):

        # add volumes to plotter
        self.plotter.clear(self._actors)
        self._actors.clear()


        icol = 0

        for key, m in self.volumes.items():
            vertices = m.ms.current_mesh().vertex_matrix()
            faces = m.ms.current_mesh().face_matrix()
            actor = vedo.Mesh([vertices, faces])
            self._actors.append(actor)
            self.plotter.add(actor, render=False)
            actor.SetVisibility(False)
            actor.c(COLORMAP(icol)[:3])
            m.actor = actor
            icol +=1

        self.plotter.show(axes=1, viewup='z')



if __name__ == '__main__':

    app = QApplication()
    gui = Gui()




    app.exec()