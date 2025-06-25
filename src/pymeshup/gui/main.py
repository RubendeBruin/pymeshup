import os
import sys
import ast
import math
import pathlib
import json  # Add import for JSON


import vtkmodules.vtkRenderingOpenGL2   # Needed to initialize VTK !

from io import StringIO
from contextlib import redirect_stdout

from PySide6.QtGui import QBrush, QColor, QFont, QFontMetricsF, QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QListWidgetItem,
    QMessageBox,
    QFileDialog,
    QMenu,
)
from PySide6.QtCore import Qt, QSettings

import numpy as np
from vedo import camera_to_dict, camera_from_dict
from vtkmodules.vtkFiltersSources import vtkLineSource

from pymeshup import *
from pymeshup.gui.forms.main_form import Ui_MainWindow


from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


from matplotlib.backends.backend_qtagg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib import cm

from pymeshup.gui.helpers.vtkBlenderLikeInteractionStyle import BlenderStyle

from pymeshup.syntaxedit.core import SyntaxEdit

HELP = """
<html><body><b>PyMeshUp</b>
PyMeshUp is a simple script-based application to generate meshes.<br><br>
<b>Primitive volumes can be created using:</b>
- Box(xmin, xmax, ymin, ymax, zmin, zmax)
- Cylinder(radius, height, resolution)


Or load them from a <b>mesh file</b> (eg stl, obj)
- Load('filename') 

Or load from a <b>GHS geometry file</b>
- g = GHSgeo(filename)
and then:
- volume = g['HULL']


<b>Loading from STEP (.stp)</b> files is supported using an additional step:
- step_model = STEP(filename, scale=1.0)
- volume = step_model.to_volume(angular_tolerance=5, linear_tolerance=0.1)

<b>Combining meshes</b>

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

<b>Creating frames and hulls</b>

Hulls can be constructed using Frames
- First construct a Frame using
  f1 =  Frame(x1,y1,x2,y2,...)
  f2 =  Frame(x1,y1,x2,y2,...)
- frames can be scaled using new_f = f1.scaled(x=2, y=2)
- then construct a hull from frames and their positions using
  h = Hull(0,f1, 20, f2, 30, f2, ...)

<b>Creating a panel distribution</b>
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


def CreateVTKLineActor(start, end, color=(0, 0, 0)):
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


class Gui:
    def __init__(self):
        # private variables

        self._digitizer_dialog = None  # Digitizer dialog instance
        self._first_run = True  # Flag to check if this is the first run

        self._user_functions = {}  # allow to register user functions

        self._global_scope_base = {
            "Load": Load,
            "Frame": Frame,
            "Volume": Volume,
            "GHSgeo": GHSgeo,
            "Hull": Hull,
            "Box": Box,
            "Cylinder": Cylinder,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
        }
        self._global_scope = self._global_scope_base.copy()



        # Main Window

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.teHelp.setHtml(HELP.replace("\n", "<br>"))

        # ---- Volumes

        self._actors = []

        self.vtkWidget = QVTKRenderWindowInteractor()
        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)
        self.ui.widgetGraphics.setLayout(layout)

        self.renderer = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.renderer.SetBackground((254, 254, 254))
        self.create3Dorigin()

        self.ui.teCode = SyntaxEdit(example_code, syntax="Python", use_smart_indentation=True)
        self.ui.teCode.setTheme("pastie")

        self.ui.verticalLayout_3.addWidget(self.ui.teCode)

        self.ui.pushButton.pressed.connect(self.run)
        self.ui.listVolumes.itemChanged.connect(self.update_visibility)

        self.ui.actionOpen_GSH_to_DAVE_conversion_tool.triggered.connect(
            self.ghs_to_dave
        )

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

        self.ui.splitter.setStretchFactor(1, 60)



        # Add context menu to teCode
        self.ui.teCode.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.teCode.customContextMenuRequested.connect(self.show_code_context_menu)

        # --- Save , open

        self.ui.actionOpen.triggered.connect(self.fileOpenMenu)

        self.ui.actionReopen.triggered.connect(self.reopen_last_file)


        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSave_as.triggered.connect(self.fileSaveAs)
        self.ui.actionSet_work_folder.triggered.connect(self.openFolder)
        self.ui.actionOpen_work_folder_in_explorer.triggered.connect(self.openWorkFolder)

        self.ui.actionLoad_Capytaine_settings.triggered.connect(self.load_capytaine_settings)
        self.ui.actionSave_Capytaine_settings.triggered.connect(self.save_capytaine_settings)

        self.settings = QSettings("pymeshup", "gui")

        self.filename = self.settings.value("lastfile")
        if self.filename:
            try:
                self.open(self.filename)
            except:
                self.filename = None

        if self.filename is None:
            curdir = self.settings.value("last_workdir")
            if curdir:
                self.curdir = curdir
            else:
                self.curdir = str(pathlib.Path(__file__).parent)

            self.ui.label_3.setText(self.curdir)

        self.ui.pushButton_3.clicked.connect(self.save_volumes)

        self.ui.actionOpen_2.triggered.connect(self.open_examples)
        self.ui.actionHelp_visible.triggered.connect(
            lambda: self.ui.dockWidget.setVisible(not self.ui.dockWidget.isVisible())
        )

        self.ui.pbWorkFolder.clicked.connect(self.openFolder)

        # ---- capytaine part

        self.ui.tePeriods.textChanged.connect(self.update_period)
        self.ui.teHeading.textChanged.connect(self.update_heading)
        self.ui.pbShowMesh.pressed.connect(lambda: self.run_captyaine(dryrun=True))
        self.ui.pbRunCapytaine.pressed.connect(lambda: self.run_captyaine(dryrun=False))

        self.ui.cbInf.toggled.connect(self.update_inf)
        self.ui.cbInf.setChecked(True)

        self.update_period()
        self.update_heading()

        # ---- Finalize
        self.ui.tabWidget.setCurrentIndex(0)

        self.MainWindow.show()
        self.MainWindow.setWindowTitle("PyMeshUp + Capytaine")
        self.iren.Initialize()

        self.MainWindow.closeEvent = self.closeEvent

        self.style = BlenderStyle()
        self.iren.SetInteractorStyle(self.style)
        self.style.callbackSelect = self.select_3d_actor

        self.update_period()
        self.update_heading()

    def open_examples(self):
        import os, sys

        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            self.fileOpen(path=application_path + "/examples")
        else:
            self.fileOpen(path=str(pathlib.Path(__file__).parent / "examples"))

    def ghs_to_dave(self, *args):
        from pymeshup.DAVE.GHS_to_DAVE_dialog import GHS_to_DAVE_conversion_dialog

        GHS_to_DAVE_conversion_dialog()

    def update_inf(self):
        self.ui.teWaterdepth.setEnabled(not self.ui.cbInf.isChecked())

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
        file_grid = str(pathlib.Path(self.curdir) / self.ui.teMeshFile.text())
        symmetry_m = self.ui.cbSymmetryMesh.isChecked()
        symmetry_h = self.ui.cbSymmetryHeadings.isChecked()

        if symmetry_m and not symmetry_h:
            msg_box = QMessageBox()
            msg_box.setText("Symmetry in grid but not in headings, are you sure? Continue?")
            msg_box.setWindowTitle("Confirmation")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg_box.exec() == QMessageBox.No:
                return

        if self.ui.cbInf.isChecked():
            waterdepth = float("inf")
        else:
            waterdepth = self.ui.teWaterdepth.value()

        do_lid = self.ui.cbLid.isChecked()

        run_capytaine(
            file_grid=file_grid,
            periods=periods,
            directions_deg=heading,
            waterdepth=waterdepth,
            grid_symmetry=symmetry_m,
            heading_symmetry=symmetry_h,
            show_only=dryrun,
            lid=do_lid,
            outfile=self.ui.teOutputFile.text()
        )

    def run(self):
        code = self.ui.teCode.toPlainText()
        self.ui.teFeedback.clear()
        self.ui.teFeedback.append("Running...")
        self.ui.teFeedback.update()

        local_scope = {}
    
        # ── First pass: only if function definitions exist ──
        parsed_ast = ast.parse(code)
        has_functions = any(isinstance(node, ast.FunctionDef) for node in parsed_ast.body)

        if has_functions:
            # register user functions in the global scope
            local_def_scope = {}
            try:
                exec(code, self._global_scope_base.copy(), local_def_scope)
            except Exception:
                pass  # Only extracting function definitions

            self._user_functions.update({
                name: obj
                for name, obj in local_def_scope.items()
                if callable(obj) and obj.__class__.__name__ == "function"
            })

        # ── Second pass: rebuild global scope with base + user functions ──
        self._global_scope = self._global_scope_base.copy()
        self._global_scope.update(self._user_functions)

        try:
            _output_redirect = StringIO()
            with redirect_stdout(_output_redirect):
                exec(code, self._global_scope, local_scope)

            output = _output_redirect.getvalue()
            self.ui.teFeedback.setPlainText(output)
            self.ui.teFeedback.append("..Done!")

        except SyntaxError as E:
            print(f"Error {E.msg} in {E.text}")
            try:
                print(f"Error on line {E.lineno} to {E.end_lineno}")
                print(f"Error from {E.offset} to {E.end_offset}")
            except Exception:
                pass

            for i, line in enumerate(code.splitlines(), 1):
                self.ui.teFeedback.append(f"{i}: {line}")

            self.ui.teFeedback.setPlainText("\n\n" + str(E))
            self.setErrorPos(E.lineno, E.offset)
            return

        except (NameError, AttributeError) as E:
            self.ui.teFeedback.setPlainText(str(E))
            return

        except Exception as E:
            self.ui.teFeedback.setPlainText(str(E))
            return

        # ── Collect Volumes and Frames from local variables ──
        volumes = dict()
        frames = dict()

        for key, value in local_scope.items():
            # If the value is a dict, unpack and use subkeys
            if isinstance(value, dict):
                for subkey, val in value.items():
                    dict_key = f"{key}{subkey}"
                    if isinstance(val, Volume):
                        volumes[dict_key] = val
                    elif isinstance(val, Frame):
                        frames[dict_key] = val
                    elif isinstance(val, GHSgeo):
                        for name, part in val.parts.items():
                            if "volume" in part:
                                vol: Volume = part["volume"]
                                volumes[name] = vol
            else:
                values = value if isinstance(value, list) else [value]
                for cnt, val in enumerate(values):
                    new_key = f"{key}_{cnt}" if len(values) > 1 else key
                    if isinstance(val, Volume):
                        volumes[new_key] = val
                    elif isinstance(val, Frame):
                        frames[new_key] = val
                    elif isinstance(val, GHSgeo):
                        for name, part in val.parts.items():
                            if "volume" in part:
                                vol: Volume = part["volume"]
                                volumes[name] = vol

        # ── Update UI and render state ──
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

    def plot_frames(self, active_key=None):
        self.static_ax.clear()

        for key, frame in self.frames.items():
            xx = [p[0] for p in frame.xy]
            yy = [p[1] for p in frame.xy]

            self.static_ax.plot(xx, yy, "k-", linewidth=0.5)

        if active_key is not None:
            frame = self.frames[active_key]

            xx = [p[0] for p in frame.xy]
            yy = [p[1] for p in frame.xy]

            self.static_ax.plot(xx, yy, "b-", linewidth=1)

            for i, point in enumerate(frame.xy):
                self.static_ax.plot(point[0], point[1], "k.")
                self.static_ax.text(
                    point[0], point[1], f"{point[0]:.3f} , {point[1]:.3f}"
                )

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
            brush = QBrush(QColor.fromRgb(254 * rgb[0], 254 * rgb[1], 254 * rgb[2]))
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
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (10, 0, 0), (254, 0, 0)))
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (0, 10, 0), (0, 254, 0)))
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (0, 0, 10), (0, 0, 254)))

    def update_3dplotter(self):
        # add volumes to plotter

        # try to capture the current state of the renderer,
        # so that we can restore it later

        camera_dict = None
        try:
            if not self._first_run:
                camera_dict = camera_to_dict(self.renderer.active_camera)
        except:
            pass




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
            actor.GetProperty().SetColor(COLORMAP(icol % 20)[:3])
            m.actor = actor
            icol += 1

        self.renderer.Render()
        try:
            self.renderer.ResetCamera() # zoom all
        except:
            pass

        if camera_dict:
            camera_from_dict(modify_inplace = self.renderer.active_camera, camera=camera_dict)

        self._first_run = False

    def select_3d_actor(self, actors):
        name = getattr(actors[0], "name")
        self.ui.teFeedback.append(f"Clicked on {name}")

    # === file operations

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

        self.vtkWidget.GetRenderWindow().Finalize()


    def isModified(self):
        return self.ui.teCode.document().isModified()

        ### ask to save

    def maybeSave(self):
        if not self.isModified():
            return True

        ret = QMessageBox.question(
            self.MainWindow,
            "Message",
            "<h4><p>The script was modified.</p>\n"
            "<p>Do you want to save changes?</p></h4>",
            QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Cancel,
        )

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
            with open(self.filename, "w") as file:
                file.write(self.ui.teCode.toPlainText())

            self.ui.teCode.document().setModified(False)
            self.MainWindow.setWindowTitle(self.filename + "[*]")

            self.settings.setValue("lastfile", self.filename)

        else:
            self.fileSaveAs()

            ### save File

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(
            self.MainWindow, "Save as...", self.filename, "PyMeshUp files (*.pym)"
        )

        if not fn:
            print("Error saving")
            return False

        lfn = fn.lower()
        if not lfn.endswith(".pym"):
            fn += ".pym"

        self.filename = fn

        self.curdir = str(pathlib.Path(fn).parent)
        os.chdir(self.curdir)
        self.ui.label_3.setText(f"Workfolder = {self.curdir}")

        return self.fileSave()

    def fileOpenMenu(self):
        self.fileOpen()

    def fileOpen(self, path=None):
        if path is None:
            path = str(self.curdir)

        if self.maybeSave():
            path, _ = QFileDialog.getOpenFileName(
                self.MainWindow,
                "Open File",
                path,
                "Python Files (*.pym);; all Files (*)",
            )
            if path:
                self.open(path)

    def openFolder(self, *args):
        path = QFileDialog.getExistingDirectory()
        if path:
            self.setWorkPath(path)

    def open(self, path):
        with open(path, "r") as f:
            self.ui.teCode.setPlainText(f.read())
            self.settings.setValue("lastfile", path)

            self.filename = path

            path = pathlib.Path(path).parent
            self.setWorkPath(str(path))

    def reopen_last_file(self):
        if self.filename:
            self.open(self.filename)
        else:
            QMessageBox.information(
                self.MainWindow,
                "No file",
                "No previous file found to reopen."
            )

    def setWorkPath(self, path):
        self.curdir = path

        os.chdir(self.curdir)
        self.ui.label_3.setText(f"Workfolder = {self.curdir}")
        self.settings.setValue("last_workdir", path)

    def openWorkFolder(self):
        if self.curdir is not None:
            os.startfile(self.curdir)
        else:
            QMessageBox.warning(
                self.MainWindow,
                "Warning",
                "No work folder set. Please set a work folder first.",
            )
    
    def load_capytaine_settings(self):
        """Load Capytaine settings from a JSON file."""
        path, _ = QFileDialog.getOpenFileName(
            self.MainWindow, "Load Capytaine Settings", "", "JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return

        try:
            with open(path, "r") as file:
                settings = json.load(file)

            self.ui.tePeriods.setText(settings.get("periods", ""))
            self.ui.teHeading.setText(settings.get("heading", ""))
            self.ui.teMeshFile.setText(settings.get("mesh_file", ""))
            self.ui.teOutputFile.setText(settings.get("output_file", ""))
            self.ui.cbSymmetryMesh.setChecked(settings.get("symmetry_mesh", False))
            self.ui.cbSymmetryHeadings.setChecked(settings.get("symmetry_headings", False))
            self.ui.cbInf.setChecked(settings.get("infinite_waterdepth", False))
            self.ui.teWaterdepth.setValue(settings.get("waterdepth", 100.0))
            self.ui.cbLid.setChecked(settings.get("lid", False))
            self.setWorkPath(settings.get("work_folder", self.curdir))

            QMessageBox.information(self.MainWindow, "Success", "Settings loaded successfully.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Failed to load settings: {e}")

    def save_capytaine_settings(self):
        """Save Capytaine settings to a JSON file."""
        path, _ = QFileDialog.getSaveFileName(
            self.MainWindow, "Save Capytaine Settings", "", "JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return

        if not path.endswith(".json"):
            path += ".json"

        settings = {
            "periods": self.ui.tePeriods.text(),
            "heading": self.ui.teHeading.text(),
            "mesh_file": self.ui.teMeshFile.text(),
            "output_file": self.ui.teOutputFile.text(),
            "symmetry_mesh": self.ui.cbSymmetryMesh.isChecked(),
            "symmetry_headings": self.ui.cbSymmetryHeadings.isChecked(),
            "infinite_waterdepth": self.ui.cbInf.isChecked(),
            "waterdepth": self.ui.teWaterdepth.value(),
            "lid": self.ui.cbLid.isChecked(),
            "work_folder": self.curdir,
        }

        try:
            with open(path, "w") as file:
                json.dump(settings, file, indent=4)

            QMessageBox.information(self.MainWindow, "Success", "Settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Failed to save settings: {e}")

    # -------- save volumes

    def save_volumes(self):
        for irow in range(self.ui.listVolumes.count()):
            item = self.ui.listVolumes.item(irow)
            key = item.text()
            visible = item.checkState() == Qt.CheckState.Checked

            if visible:
                fname = str(self.curdir) + "/" + key + self.ui.comboBox.currentText()
                self.volumes[key].save(fname)
                self.ui.teFeedback.append(f"Saved: {fname}")

    # ---- frame digitizer

    def add_frame_using_digitizer(self):
        from pymeshup.gui.digitizer.digitizer import DigitizerDialog

        if self._digitizer_dialog is None:
            self._digitizer_dialog = DigitizerDialog()

        dialog = self._digitizer_dialog # alias

        if dialog.exec():
            points = dialog.points_data

            code = "\nf = Frame("
            for x,y in points:
                code += f"{x:.3f}, {y:.3f},\n    "
            code += ").autocomplete()\n"

            # Insert the code into the text editor at the current cursor position
            cursor = self.ui.teCode.textCursor()
            cursor.insertText(code)
            self.ui.teCode.document().setModified(True)

    def show_code_context_menu(self, position):
        """Show context menu for the code editor."""
        context_menu = QMenu(self.ui.teCode)

        # Add a menu action for the digitizer
        add_frame_action = QAction("Add Frame Using Digitizer", self.ui.teCode)
        add_frame_action.triggered.connect(self.add_frame_using_digitizer)
        context_menu.addAction(add_frame_action)

        # Add standard editing actions
        context_menu.addSeparator()
        if hasattr(self.ui.teCode, 'actions'):
            for action in self.ui.teCode.actions():
                if action.text() in ('Cut', 'Copy', 'Paste', 'Select All'):
                    context_menu.addAction(action)

        # Show the context menu at the cursor position
        context_menu.exec(self.ui.teCode.mapToGlobal(position))

def main():
    app = QApplication(sys.argv)


    icon_path = pathlib.Path(__file__).parent.parent / "resources" / "pymeshup_logo.ico"
    app.setWindowIcon(QIcon(str(icon_path)))

    Gui()
    sys.exit(app.exec())

def run():
    main()

if __name__ == "__main__":
    main()