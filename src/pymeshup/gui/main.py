import os
import pathlib

from io import StringIO
from contextlib import redirect_stdout

from PySide6.QtGui import QBrush, QColor, QFont, QFontMetricsF, QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, QSettings

import numpy as np
from vtkmodules.vtkFiltersSources import vtkLineSource

from pymeshup import *
from pymeshup.gui.forms.main_form import Ui_MainWindow


from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer
)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


from matplotlib.backends.backend_qtagg import (FigureCanvas,
     NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import cm

from pymeshup.gui.helpers.highlighter import PythonHighlighter
from pymeshup.gui.helpers.vtkBlenderLikeInteractionStyle import BlenderStyle

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
- cut_at_waterline()
- cut_at_xz()
- merge_close_vertices(pct)
- invert_normals()

! These modifiers return a modified copy. They do not modify the volume itself:
- b.rotate(90) # does not do anything
- b = b.rotate(90) # works

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
fb = Frame(0, 1)  # bow

h = Hull(0, f1,
         5, f2,
         15, f2,
         20, fb)

h = h.remove(c)  # cut cylinder from hull

hg = h.regrid()
"""

COLORMAP = cm.tab20

def CreateVTKActor(vertices, faces):

    # create data
    poly = vtkPolyData()
    points = vtkPoints()

    arr = np.ascontiguousarray(vertices)
    varr = numpy_to_vtk(arr.astype(float), deep=True)

    points.SetData(varr)
    poly.SetPoints(points)

    sourcePolygons = vtkCellArray()

    ast = np.int64

    nf, nc = faces.shape
    hs = np.hstack((np.zeros(nf)[:, None] + nc, faces)).astype(ast).ravel()
    arr = numpy_to_vtkIdTypeArray(hs, deep=True)
    sourcePolygons.SetCells(nf, arr)

    poly.SetPolys(sourcePolygons)

    # mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(poly)

    # actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    return actor

def CreateVTKLineActor(start, end, color=(0,0,0)):
    # create data
    lineSource = vtkLineSource()
    lineSource.SetPoint1(start)
    lineSource.SetPoint2(end)

    # mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())

    # actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(color)

    return actor



class Gui():

    def __init__(self):
        # Main Window

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.label.setText(HELP.replace('\n','<br>'))

        # ---- Volumes

        self._actors = []

        self.vtkWidget  = QVTKRenderWindowInteractor()
        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)
        self.ui.widgetGraphics.setLayout(layout)

        self.renderer = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.renderer.SetBackground((254,254,254))
        self.create3Dorigin()

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

        # --- Save , open

        self.ui.actionOpen.triggered.connect(self.fileOpenMenu)
        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSave_as.triggered.connect(self.fileSaveAs)
        self.ui.actionSet_work_folder.triggered.connect(self.openFolder)

        self.settings = QSettings('pymeshup','gui')

        self.filename = self.settings.value('lastfile')
        if self.filename:
            try:
                self.open(self.filename)
            except:
                self.filename = None

        if self.filename is None:
            curdir = self.settings.value('last_workdir')
            if curdir:
                self.curdir = curdir
            else:
                self.curdir = str(pathlib.Path(__file__).parent)

            self.ui.label_3.setText(self.curdir)

        self.ui.pushButton_3.clicked.connect(self.save_volumes)

        self.ui.actionOpen_2.triggered.connect(lambda : self.fileOpen(path = str(pathlib.Path(__file__).parent / 'examples')))
        self.ui.actionHelp_visible.triggered.connect(lambda: self.ui.dockWidget.setVisible(not self.ui.dockWidget.isVisible()))

        # ---- capytaine part

        self.ui.tePeriods.textChanged.connect(self.update_period)
        self.ui.teHeading.textChanged.connect(self.update_heading)
        self.ui.pbShowMesh.pressed.connect(lambda : self.run_captyaine(dryrun=True))
        self.ui.pbRunCapytaine.pressed.connect(lambda : self.run_captyaine(dryrun=False))

        # ---- Finalize

        self.MainWindow.show()
        self.MainWindow.setWindowTitle("PyMeshUp")
        self.iren.Initialize()

        self.MainWindow.closeEvent = self.closeEvent

        self.style = BlenderStyle()
        self.iren.SetInteractorStyle(self.style)
        self.style.callbackSelect = self.select_3d_actor


    def update_period(self):
        try:
            T = eval(self.ui.tePeriods.text())
        except Exception as E:
            self.ui.lblPeriods.setText(str(E))
            return

        self.ui.lblPeriods.setText(str(T))

        return T

    def update_heading(self):
        try:
            T = eval(self.ui.teHeading.text())
        except Exception as E:
            self.ui.lblHeading.setText(str(E))
            return

        self.ui.lblHeading.setText(str(T))

        return T

    def run_captyaine(self, dryrun=False):
        try:
            from pymeshup.gui.capytaine_runner import run_capytaine
        except Exception as E:
            print(self.ui.teFeedback.append(str(E)))
            return

        periods = self.update_period()
        heading = self.update_heading()
        name = self.ui.teName.text()
        file_grid = str(pathlib.Path(self.curdir) / self.ui.teMeshFile.text())
        symmetry = self.ui.cbSymmetry.isChecked()
        waterdepth = float(self.ui.teWaterdepth.text())

        run_capytaine(name=name,
                      file_grid=file_grid,
                      periods=periods,
                      directions_deg=heading,
                      waterdepth=waterdepth,
                      symmetry=symmetry,
                      show_only=dryrun)



    def run(self):
        code = self.ui.teCode.toPlainText()
        self.ui.teFeedback.clear()
        self.ui.teFeedback.append("Running...")
        self.ui.teFeedback.update()

        key_before = [v for v in locals().keys()]

        try:
            f = StringIO()
            with redirect_stdout(f):
                exec(code)

            s = f.getvalue()
            self.ui.teFeedback.setPlainText(s)
            self.ui.teFeedback.append('..Done!')

        except SyntaxError as E:

            print(f'Error {E.msg} in {E.text}')

            try:
                print(f'Error on line {E.lineno} to {E.end_lineno}')
                print(f'Error from {E.offset} to {E.end_offset}')
            except:
                pass

            for i, line in enumerate(self.ui.teCode.toPlainText()):
                self.ui.teFeedback.append(f'{i} : {line}')

            self.ui.teFeedback.setPlainText('\n\n' + str(E))


            self.setErrorPos(E.lineno, E.offset)


        except (NameError, AttributeError) as E:

            # print(f'Error NameError in {E.msg}')
            # print(f'Error on line {E.lineno} to {E.end_lineno}')
            # print(f'Error from {E.offset} to {E.end_offset}')

            self.ui.teFeedback.setPlainText(str(E))
            # self.setErrorPos(E.lineno, E.offset)


        except Exception as E:

            self.ui.teFeedback.setPlainText(str(E))




        key_after = [v for v in locals().keys()]
        local_vars = [v for v in locals().values()]
        items_after = [i for i in locals().items()]

        volumes = dict()
        frames = dict()

        for key, value in items_after:
            if key not in key_before:
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

    def setErrorPos(self, line, offset):
        pass

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
                self.static_ax.text(point[0], point[1], f'{point[0]:.3f} , {point[1]:.3f}')

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

            rgb = COLORMAP(icol % 20)
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


        self.renderer.Render()
        self.vtkWidget.update()

    def create3Dorigin(self):
        self.renderer.AddActor(CreateVTKLineActor((0,0,0),(10,0,0),(254,0,0)))
        self.renderer.AddActor(CreateVTKLineActor((0,0,0),(0,10,0),(0,254,0)))
        self.renderer.AddActor(CreateVTKLineActor((0,0,0),(0,0,10),(0,0,254)))


    def update_3dplotter(self):

        # add volumes to plotter
        self.renderer.RemoveAllViewProps()
        self._actors.clear()
        self.create3Dorigin()


        icol = 0

        for key, m in self.volumes.items():
            vertices = m.ms.current_mesh().vertex_matrix()
            faces = m.ms.current_mesh().face_matrix()
            actor = CreateVTKActor(vertices, faces)
            actor.name = key
            self._actors.append(actor)
            self.renderer.AddActor(actor)
            actor.SetVisibility(False)
            actor.GetProperty().SetColor(COLORMAP(icol %20)[:3])
            m.actor = actor
            icol +=1

        self.renderer.Render()
        try:
            self.style.ZoomFit()
        except:
            pass

    def select_3d_actor(self, actors):
        name = getattr(actors[0],'name')
        self.ui.teFeedback.append(f"Clicked on {name}")


# === file operations

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.ui.teCode.document().isModified()

        ### ask to save
    def maybeSave(self):
        if not self.isModified():
            return True

        ret = QMessageBox.question(self.MainWindow, "Message",
                "<h4><p>The script was modified.</p>\n" 
                "<p>Do you want to save changes?</p></h4>",
                QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            if self.filename == "":
                self.fileSaveAs()
                return False
            else:
                self.fileSave()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True

    def fileSave(self):
        if self.filename is not None:

            with open(self.filename, 'w') as file:
                file.write(self.ui.teCode.toPlainText())

            self.ui.teCode.document().setModified(False)
            self.MainWindow.setWindowTitle(self.filename + "[*]")

            self.settings.setValue('lastfile',self.filename)

        else:
            self.fileSaveAs()

            ### save File

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self.MainWindow, "Save as...", self.filename, "PyMeshUp files (*.pym)")

        if not fn:
            print("Error saving")
            return False

        lfn = fn.lower()
        if not lfn.endswith('.pym'):
            fn += '.pym'

        self.filename = fn

        self.curdir = str(pathlib.Path(fn).parent)
        os.chdir(self.curdir)
        self.ui.label_3.setText(f'Workfolder = {self.curdir}')

        return self.fileSave()

    def fileOpenMenu(self):
        self.fileOpen()

    def fileOpen(self, path=None):
        if path is None:
            path = str(self.curdir)

        if self.maybeSave():
            path, _ = QFileDialog.getOpenFileName(self.MainWindow, "Open File", path, "Python Files (*.pym);; all Files (*)")
            if path:
                self.open(path)

    def openFolder(self):
        path = QFileDialog.getExistingDirectory()
        if path:
            self.setWorkPath(path)


    def open(self, path):
        with open(path, 'r') as f:
            self.ui.teCode.setPlainText(f.read())
            self.settings.setValue('lastfile',path)

            path = pathlib.Path(path).parent
            self.setWorkPath(str(path))



    def setWorkPath(self, path):

        self.curdir = path

        os.chdir(self.curdir)
        self.ui.label_3.setText(f'Workfolder = {self.curdir}')
        self.settings.setValue('last_workdir',path)

    # -------- save volumes

    def save_volumes(self):
        for irow in range(self.ui.listVolumes.count()):
            item = self.ui.listVolumes.item(irow)
            key = item.text()
            visible = item.checkState() == Qt.CheckState.Checked

            if visible:
                fname = str(self.curdir) + '/' + key + self.ui.comboBox.currentText()
                self.volumes[key].save(fname)
                self.ui.teFeedback.append(f'Saved: {fname}')


if __name__ == '__main__':

    app = QApplication()
    gui = Gui()
    app.exec()