import logging
import warnings

import netCDF4 # required for saving - fallback to scipy.io.netcdf causes issues

import numpy as np
from numpy import pi

import capytaine as cpt
from capytaine.io.xarray import separate_complex_values

from capytaine.meshes.geometry import xOz_Plane
from capytaine.meshes.symmetric import ReflectionSymmetricMesh

import mafredo
from mafredo import Hyddb1

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s: %(message)s')
bem_solver = cpt.BEMSolver()

# Helper
def make_database(body, omegas, wave_directions, waterdepth=0, water_level=0):
    # SOLVE BEM PROBLEMS
    problems = []
    for wave_direction in wave_directions:
        for omega in omegas:
            problems += [cpt.RadiationProblem(omega=omega, body=body, radiating_dof=dof, water_depth=waterdepth, free_surface=water_level) for dof in body.dofs]
            problems += [cpt.DiffractionProblem(omega=omega, body=body, wave_direction=wave_direction, water_depth=waterdepth, free_surface=water_level)]
    results = [bem_solver.solve(problem) for problem in problems]
    # *radiation_results, diffraction_result = results
    dataset = cpt.assemble_dataset(results)

    # dataset['diffraction_result'] = diffraction_result

    return dataset

def run_capytaine(file_grid : str,  # input file, e.g. grid.stl
                  periods : np.array,  # periods in seconds
                  directions_deg : np.array,
                  waterdepth : float = None,  # waterdepth
                  water_level : float = 0,  # water level
                  grid_symmetry : bool = False,  # symmetry in XZ plane
                  heading_symmetry : bool = False,  # symmetry in YZ plane
                  show_only : bool = False,  # show only the mesh
                  lid : bool = True,  # add a lid
                  outfile : str = None  # output file
                  ):

    name = file_grid[:-4]

    if grid_symmetry and not heading_symmetry:
        warnings.warn('Grid symmetry requires heading symmetry')

    periods = np.array(periods)
    directions = np.array(directions_deg) * pi / 180

    file_out_nc = outfile + '.nc'
    outfile_dhyd = outfile + '.dhyd'


    omega = 2 * np.pi / periods

    # load and create mesh
    hull_mesh = cpt.load_mesh(file_grid, file_format="stl")

    # generate lid
    if lid:
        lid_mesh = hull_mesh.generate_lid(z=-0.01)
    else:
        lid_mesh = None


    if grid_symmetry:
        if lid:
            raise ValueError('Symmetry and lid are not compatible')

        hull_mesh = ReflectionSymmetricMesh(hull_mesh, plane=xOz_Plane, name=f"{name}_mesh")

    boat = cpt.FloatingBody(mesh=hull_mesh, lid_mesh=lid_mesh)

    boat.add_all_rigid_body_dofs()
    boat.keep_immersed_part()
    boat.show()

    if show_only:
        return

    dataset = make_database(body=boat, omegas=omega, wave_directions=directions, waterdepth=waterdepth, water_level=water_level)


    sep = separate_complex_values(dataset)
    # sep.to_netcdf(file_out_nc,
    #               encoding={'radiating_dof': {'dtype': 'U'},
    #                         'influenced_dof': {'dtype': 'U'},
    #                         'diffraction_result': {'dtype': 'U'}})


    # Before saving to NetCDF, convert categorical variables to strings
    for var_name in sep.variables:
        if hasattr(sep[var_name].dtype, 'name') and sep[var_name].dtype.name == 'category':
            sep[var_name] = sep[var_name].astype(str)



    sep.to_netcdf(file_out_nc,
                  encoding={'radiating_dof': {'dtype': 'U'},
                            'influenced_dof': {'dtype': 'U'}})

    print(f'saved NC results as {file_out_nc}')

    hyd = Hyddb1.create_from_capytaine(filename=file_out_nc)
    if heading_symmetry:
        hyd.symmetry = mafredo.Symmetry.XZ
    else:
        hyd.symmetry = mafredo.Symmetry.No

   
    hyd.save_as(outfile_dhyd)
    print(f'Saved as: {outfile_dhyd}')
    hyd.plot(do_show=True)