import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy
)
from PySide6.QtGui import QGuiApplication, QImage # QImageReader is not used

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DraggablePoint:
    def __init__(self, point, ax, on_update):
        self.point = point
        self.ax = ax
        self.on_update = on_update
        self.press = None
        self.background = None
        self.connect()

    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = self.point.get_offsets().flatten(), event.xdata, event.ydata
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        axes.draw_artist(self.point)
        canvas.blit(axes.bbox)


    def on_motion(self, event):
        if self.press is None or event.inaxes != self.point.axes: return
        offsets, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.set_offsets([[offsets[0] + dx, offsets[1] + dy]])

        canvas = self.point.figure.canvas
        axes = self.point.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.point)
        canvas.blit(axes.bbox)


    def on_release(self, event):
        if self.press is None: return
        self.press = None
        self.point.set_animated(False)
        self.background = None
        self.point.figure.canvas.draw()
        self.on_update()

    def disconnect(self):
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

class DigitizerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Digitizer")
        self.setMinimumSize(800, 600)

        self.points_data = []
        self.draggable_points = []
        self.background_image_artist = None # Matplotlib artist for the background image
        self._stored_qimage = None # To store the QImage from clipboard

        # Main layout
        main_layout = QVBoxLayout(self)

        # Controls layout
        controls_layout = QHBoxLayout()
        self.x_min_edit = QLineEdit("0")
        self.x_max_edit = QLineEdit("10")
        self.y_min_edit = QLineEdit("0")
        self.y_max_edit = QLineEdit("10")
        apply_limits_button = QPushButton("Apply Limits")
        paste_image_button = QPushButton("Paste Background Image")

        controls_layout.addWidget(QLabel("X Min:"))
        controls_layout.addWidget(self.x_min_edit)
        controls_layout.addWidget(QLabel("X Max:"))
        controls_layout.addWidget(self.x_max_edit)
        controls_layout.addWidget(QLabel("Y Min:"))
        controls_layout.addWidget(self.y_min_edit)
        controls_layout.addWidget(QLabel("Y Max:"))
        controls_layout.addWidget(self.y_max_edit)
        controls_layout.addWidget(apply_limits_button)
        controls_layout.addWidget(paste_image_button)

        # Add clear button
        clear_button = QPushButton("Clear All")
        controls_layout.addWidget(clear_button)

        main_layout.addLayout(controls_layout)

        # Matplotlib Figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.canvas)

        # Coordinates display
        self.coordinates_edit = QTextEdit()
        self.coordinates_edit.setReadOnly(True)
        main_layout.addWidget(QLabel("Coordinates:"))
        main_layout.addWidget(self.coordinates_edit)

        # Add OK button at the bottom
        bottom_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # QDialog's reject method
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # QDialog's accept method
        bottom_layout.addStretch()
        bottom_layout.addWidget(cancel_button)
        bottom_layout.addWidget(ok_button)
        main_layout.addLayout(bottom_layout)

        # Connections
        apply_limits_button.clicked.connect(self.apply_axis_limits)
        paste_image_button.clicked.connect(self.paste_background_image)
        clear_button.clicked.connect(self.clear_all_points)  # Connect clear button
        self.canvas.mpl_connect('button_press_event', self.on_plot_click)

        self.apply_axis_limits() # Initial setup

    def apply_axis_limits(self):
        try:
            x_min = float(self.x_min_edit.text())
            x_max = float(self.x_max_edit.text())
            y_min = float(self.y_min_edit.text())
            y_max = float(self.y_max_edit.text())
        except ValueError:
            print("Invalid input for axis limits.")
            # Consider showing a QMessageBox to the user
            return

        # These limits will be used by redraw_plot when it re-reads from edits
        # or when it calls self.ax.get_xlim/ylim after setting them.
        self.ax.set_aspect('auto') # Or 'equal' if you prefer
        self.redraw_plot()

    def paste_background_image(self):
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            qimage = clipboard.image()
            if not qimage.isNull():
                # Create a deep copy of the image to avoid issues with clipboard ownership
                self._stored_qimage = QImage(qimage)
                # Print debug info
                print(f"Image info - Format: {self._stored_qimage.format()}, Size: {self._stored_qimage.width()}x{self._stored_qimage.height()}")
                self.redraw_plot()  # Let redraw_plot handle displaying it
            else:
                print("Pasted image is null.")
        else:
            print("No image found on clipboard.")

    def on_plot_click(self, event):
        if event.inaxes == self.ax and event.button == 1: # Left click
            # Check if click is on an existing point (handled by DraggablePoint)
            for dp in self.draggable_points:
                contains, _ = dp.point.contains(event)
                if contains:
                    return # Let DraggablePoint handle it

            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                self.add_point(x, y)

    def add_point(self, x, y):
        # self.points_data is updated by update_coordinates_display from draggable_points
        point_plot = self.ax.scatter([x], [y], c='red', picker=True)
        dp = DraggablePoint(point_plot, self.ax, self.update_coordinates_display)
        self.draggable_points.append(dp)
        self.update_coordinates_display() # This will also add the new point to self.points_data
        self.canvas.draw_idle()

    def update_coordinates_display(self):
        new_points_data = []
        for dp in self.draggable_points:
            offsets = dp.point.get_offsets()
            if offsets.any():
                 new_points_data.append(list(offsets[0]))
        self.points_data = new_points_data

        text = ""
        for i, (x, y) in enumerate(self.points_data):
            text += f"Point {i+1}: {x:.2f}, {y:.2f}\n"
        self.coordinates_edit.setText(text)

    def redraw_plot(self):
        try:
            x_min_val = float(self.x_min_edit.text())
            x_max_val = float(self.x_max_edit.text())
            y_min_val = float(self.y_min_edit.text())
            y_max_val = float(self.y_max_edit.text())
        except ValueError:
            print("Invalid axis limits in text boxes. Using previous limits or default 0,10 for redraw.")
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            x_min_val = current_xlim[0] if current_xlim[0] < current_xlim[1] else 0.0
            x_max_val = current_xlim[1] if current_xlim[1] > current_xlim[0] else 10.0
            y_min_val = current_ylim[0] if current_ylim[0] < current_ylim[1] else 0.0
            y_max_val = current_ylim[1] if current_ylim[1] > current_ylim[0] else 10.0
            self.x_min_edit.setText(str(x_min_val))
            self.x_max_edit.setText(str(x_max_val))
            self.y_min_edit.setText(str(y_min_val))
            self.y_max_edit.setText(str(y_max_val))

        self.ax.clear() # Clear previous plot elements

        self.ax.set_xlim(x_min_val, x_max_val)
        self.ax.set_ylim(y_min_val, y_max_val)
        # Aspect was set in apply_axis_limits, self.ax.get_aspect() will use it.

        # Redraw background image if it's stored
        self.background_image_artist = None # Clear old artist reference
        if self._stored_qimage and not self._stored_qimage.isNull():
            try:
                # Get image dimensions and format
                width = self._stored_qimage.width()
                height = self._stored_qimage.height()

                if width > 0 and height > 0:
                    # Convert QImage to numpy array directly using a simpler approach
                    # First convert to RGBA format to ensure consistency
                    qimage_rgba = self._stored_qimage.convertToFormat(QImage.Format.Format_RGBA8888)

                    # Method 1: Using the bits() method which returns a Python bytes object
                    ptr = qimage_rgba.bits()
                    if ptr:
                        # Create contiguous copy of the data
                        img_data = np.frombuffer(ptr, dtype=np.uint8).reshape(height, width, 4).copy()

                        # Plot the image
                        ax_xlim = self.ax.get_xlim()
                        ax_ylim = self.ax.get_ylim()
                        self.background_image_artist = self.ax.imshow(
                            img_data,
                            extent=[ax_xlim[0], ax_xlim[1], ax_ylim[0], ax_ylim[1]],
                            aspect=self.ax.get_aspect()
                        )
                        print(f"Successfully displayed image: {width}x{height}")
                    else:
                        print("Failed to get image data from QImage")
                else:
                    print(f"Image has invalid dimensions: {width}x{height}")
            except Exception as e:
                print(f"Error processing image for display: {e}")
                # Don't clear self._stored_qimage here to allow retrying
                import traceback
                traceback.print_exc()

        # Re-plot points
        old_points_data = list(self.points_data)
        self.draggable_points.clear()
        self.points_data.clear()

        for x, y in old_points_data:
            point_plot = self.ax.scatter([x], [y], c='red', picker=True)
            dp = DraggablePoint(point_plot, self.ax, self.update_coordinates_display)
            self.draggable_points.append(dp)

        self.update_coordinates_display() # Sync self.points_data and text edit
        self.canvas.draw_idle()

    def clear_all_points(self):
        # Disconnect draggable points first
        for dp in self.draggable_points:
            dp.disconnect()

        # Clear points from the plot and internal data structures
        self.points_data.clear()
        self.draggable_points.clear()
        self.coordinates_edit.clear()

        # Clear background image
        self._stored_qimage = None
        self.background_image_artist = None

        # Clear the plot and reset limits
        self.ax.clear()
        self.canvas.draw_idle()

        # Reapply axis limits to restore the grid
        self.apply_axis_limits()

    def closeEvent(self, event):
        for dp in self.draggable_points:
            dp.disconnect()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DigitizerDialog()
    dialog.exec()
    # app.exec()

    print(dialog.points_data)