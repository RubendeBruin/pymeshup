import cadquery as cq
import os
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

    def to_volume(
        self, angular_tolerance: float = 5, linear_tolerance: float = 1, filename: str | None = None
    ) -> Volume:
        """
        Convert the loaded STEP file to a Volume object.

        Args:
            angular_tolerance: Angular tolerance for mesh generation in degrees
            linear_tolerance: Linear tolerance for mesh generation
            filename : optional filename to save the STL mesh to

        Returns:
            Volume object containing the mesh
        """

        import tempfile

        # Create temporary file if needed
        if filename is not None:
            temp_filename = str(filename)
        else:
            temp_file = tempfile.NamedTemporaryFile(suffix=".stl", delete=False)
            temp_filename = temp_file.name
            temp_file.close()

        # Create a deep copy of the workplane to avoid modifying the original
        # when exporting (cq.exporters.export modifies the passed object)
        # We need to use OCCT's BRepBuilderAPI_Copy for a true deep copy
        from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy

        copied_solids = []
        for solid in self._workplane.solids().vals():
            # Create a true deep copy using OCCT's copy builder
            copy_builder = BRepBuilderAPI_Copy(solid.wrapped)
            copied_solid = cq.Shape.cast(copy_builder.Shape())
            copied_solids.append(copied_solid)

        workplane_copy = cq.Workplane("XY").newObject(copied_solids)

        # Export to STL with the specified tolerances
        cq.exporters.export(
            workplane_copy,
            temp_filename,
            tolerance=linear_tolerance,
            angularTolerance=angular_tolerance,
        )

        # Load the STL using pymeshup
        volume = Load(temp_filename)

        # Clean up temporary file
        if filename is None:
            os.unlink(temp_filename)

        return volume


# Example usage
if __name__ == "__main__":
    filename = r"C:\data\gpsh0055rov.stp"

    stp = STEP(filename, scale=0.001)
    volume = stp.to_volume()

    Plot(volume)
