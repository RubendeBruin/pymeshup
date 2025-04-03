from PySide6.QtWidgets import QDialog


def GHS_to_DAVE_conversion_dialog():
    from PySide6.QtWidgets import QApplication

    from pymeshup.DAVE.GHS_to_DAVE_form import Ui_ConversionDialog

    if QApplication.instance() is None:
        app = QApplication()
    else:
        app = QApplication.instance()

    dialog = QDialog()
    dialog.ui = Ui_ConversionDialog()
    dialog.ui.setupUi(dialog)

    def go(*args):
        filename = dialog.ui.tbFilename.text()
        output_folder = dialog.ui.tbOutputDir.text()
        name = dialog.ui.tbVesselName.text()
        resolution_deg = dialog.ui.sbDeg.value()

        from pymeshup.DAVE.GHS_to_DAVE import GHS_to_DAVE

        dialog.ui.tbOutput.setPlainText("Running")
        dialog.update()
        app.processEvents()

        output = []

        try:
            GHS_to_DAVE(
                filename_gf1=filename,
                outdir=output_folder,
                vessel_name=name,
                circular_segments_step=resolution_deg,
                output=output,
            )
        except Exception as E:
            output.append("-- There was an error :-(")
            output.append(str(E))

        dialog.ui.tbOutput.setPlainText("\n".join(output))


    def browse():
        from PySide6.QtWidgets import QFileDialog

        filename, _ = QFileDialog.getOpenFileName(dialog, "Select GHS file", "", "GHS files (*.gf; *.gf1);;All files (*)")
        if filename:
            dialog.ui.tbFilename.setText(filename)

    dialog.ui.pbGo.clicked.connect(go)
    dialog.ui.pbBrowse.clicked.connect(browse)

    dialog.ui.tbFilename.setFocus()

    dialog.exec()


if __name__ == "__main__":
    GHS_to_DAVE_conversion_dialog()
