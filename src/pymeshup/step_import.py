import cadquery as cq
import os
from typing import Union, Optional
from pymeshup.volumes import Volume, Load, Plot


class STEP:

    def __init__(self, filename: str, scale: float = 1.0):
        """
        Initialize STEP file loader with optional scaling.

        Args:
            filename: Path to the STEP file
            scale: Scale factor to apply to the imported model (default: 1.0)
        """
        self.filename = filename
        self.scale = scale
        self._workplane = self.load()

    def load(self) -> cq.Workplane:
        """
        Load a STEP file using CadQuery.

        Args:
            filename: Path to the STEP file

        Returns:
            CadQuery Workplane object containing the imported model
        """
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"STEP file not found: {self.filename}")

        # Import the STEP file
        workplane = cq.importers.importStep(self.filename)

        # Apply scaling if needed
        if self.scale != 1.0:
            # Scale all solids in the workplane
            scaled_solids = [solid.val().scale(self.scale) for solid in workplane.all()]
            # Create a new workplane from the scaled solids
            workplane = cq.Workplane("XY").newObject(scaled_solids)

        return workplane


    def to_volume(self, angular_tolerance: float = 5, linear_tolerance: float = 1) -> Volume:
        """
        Convert the loaded STEP file to a Volume object.

        Args:
            angular_tolerance: Angular tolerance for mesh generation in degrees
            linear_tolerance: Linear tolerance for mesh generation

        Returns:
            Volume object containing the mesh
        """

        import tempfile

        # Create temporary file if needed

        temp_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        temp_filename = temp_file.name
        temp_file.close()

        # Export to STL with the specified tolerances
        cq.exporters.export(
            self._workplane,
            temp_filename,
            tolerance=linear_tolerance,
            angularTolerance=angular_tolerance
        )

        # Load the STL using pymeshup
        volume = Load(temp_filename)

        # Clean up temporary file
        os.unlink(temp_filename)

        return volume


# Example usage
if __name__ == "__main__":
    filename = r"C:\data\gpsh0055rov.stp"

    stp = STEP(filename, scale = 0.001)
    volume = stp.to_volume()

    Plot(volume)