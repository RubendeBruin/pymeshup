from pathlib import Path
from random import random

from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QCheckBox, QMainWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer

from pymeshup import STEP
from pymeshup.gui.forms.step_mesher import Ui_MainWindow
from pymeshup.gui.helpers.vtkBlenderLikeInteractionStyle import BlenderStyle
from pymeshup.gui.main import CreateVTKActor, CreateVTKLineActor


class StepMesherGui:
    def __init__(self):

        self.MainWindow = QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.pbBrowse.clicked.connect(self.browse)

        self.ui.leFilename.textChanged.connect(self.load_step_file)

        self.ui.dsAngTol.valueChanged.connect(self.changed)
        self.ui.dsLinTol.valueChanged.connect(self.changed)
        self.ui.pbApply.clicked.connect(self.update_mesh)

        self.ui.pbSave.clicked.connect(self.save_stl)

        self.ui.pbBatch.clicked.connect(self.process_all_files_in_folder)

        self.step_file : STEP | None = None

        self.MainWindow.show()

        self.setup_3d()

        self.iren.Initialize()
        self.style = BlenderStyle()
        self.iren.SetInteractorStyle(self.style)

        self.MainWindow.closeEvent = self.on_dialog_closed

        self.ui.leFilename.setText(r"Drop or enter your file here or press ...")



    def setup_3d(self):
        self.vtkWidget = QVTKRenderWindowInteractor()
        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)
        self.ui.view3d.setLayout(layout)

        self.renderer = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()



        self.renderer.SetBackground((254, 254, 254))
        self.create3Dorigin()





    def browse(self):
        """Open the standard Qt file open dialog to choose a STEP file and
        set the chosen path into the output line edit.
        """
        # Use the standard Open dialog (not Save) as requested.
        filename, _ = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Select STEP File",
            "",
            "STEP Files (*.step *.stp);;All Files (*)",
        )

        if not filename:
            return

        self.ui.leFilename.setText(filename)

    def load_step_file(self):
        filename = self.ui.leFilename.text()

        if Path(filename).exists():
            print(f"Loading STEP file: {filename}")

        else:
            self.ui.leFilename.setStyleSheet("color: red")
            return

        self.ui.leFilename.setStyleSheet("")

        scale = 1.0
        if self.ui.leScale.text():
            try:
                scale = float(self.ui.leScale.text())
            except:
                self.ui.lbFeedback.setText("Scale must be a number")
                return

        try:
            self.step_file = STEP(filename, scale = scale)
        except Exception as e:
            self.ui.lbFeedback.setText(str(e))
            return

        self.ui.lbFeedback.setText(f"Loaded: {filename}")

    def changed(self):
        if not self.ui.chAutoApply.isChecked():
            return

        self.update_mesh()

    def update_mesh(self, *args, filename : Path | None = None):

        lintol = self.ui.dsLinTol.value()
        angtol = self.ui.dsAngTol.value()

        mesh = self.step_file.to_volume(
            linear_tolerance=lintol,
            angular_tolerance=angtol,
            filename = filename
        )

        self.ui.lbFeedback.setText(
            f"Generated mesh with {len(mesh.vertices)} using lin.tol={lintol}, ang.tol={angtol}"
        )


        cm = mesh.ms.current_mesh()

        vertices = cm.vertex_matrix()
        faces = cm.face_matrix()
        actor = CreateVTKActor(vertices, faces)

        # use a random color
        red = random()
        green = random()
        blue = 0.5*random()


        actor.GetProperty().SetColor(red, green, blue)
        actor.GetProperty().SetRepresentationToWireframe()

        self.renderer.RemoveAllViewProps()

        self.renderer.AddActor(actor)
        self.renderer.Render()

        self.vtkWidget.update()

    def create3Dorigin(self):
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (10, 0, 0), (254, 0, 0)))
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (0, 10, 0), (0, 254, 0)))
        self.renderer.AddActor(CreateVTKLineActor((0, 0, 0), (0, 0, 10), (0, 0, 254)))

    def save_stl(self):
        file = Path(self.ui.leFilename.text())

        self.ui.leFilename.setText(str(file))
        self.load_step_file()

        # output file is same as input only with .stl extension
        filename = file.with_suffix(".stl")

        self.update_mesh(filename = filename)
        self.ui.lbFeedback.setText("Saved as: " + str(filename))



    def process_all_files_in_folder(self):
        path = Path(self.ui.leFilename.text()).parent

        for file in path.glob("*.step"):
            self.ui.leFilename.setText(str(file))
            self.load_step_file()

            # output file is same as input only with .stl extension
            filename = file.with_suffix(".stl")

            self.update_mesh(filename = filename)
            self.ui.lbFeedback.setText("Saved as: " + str(filename))

            QApplication.instance().processEvents()



    def on_dialog_closed(self, event):
        pass
        # self.vtkWidget.GetRenderWindow().Finalize()



if __name__ == '__main__':
    app = QApplication([])
    window = StepMesherGui()
    window.MainWindow.show()

    app.exec()

