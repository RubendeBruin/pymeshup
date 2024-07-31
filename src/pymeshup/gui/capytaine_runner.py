import logging

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
def make_database(body, omegas, wave_directions, waterdepth=0):
    # SOLVE BEM PROBLEMS
    problems = []
    for wave_direction in wave_directions:
        for omega in omegas:
            problems += [cpt.RadiationProblem(omega=omega, body=body, radiating_dof=dof, water_depth=waterdepth) for dof in body.dofs]
            problems += [cpt.DiffractionProblem(omega=omega, body=body, wave_direction=wave_direction, water_depth=waterdepth)]
    results = [bem_solver.solve(problem) for problem in problems]
    # *radiation_results, diffraction_result = results
    dataset = cpt.assemble_dataset(results)

    # dataset['diffraction_result'] = diffraction_result

    return dataset

def run_capytaine(name: str,  # name of the body eg "boat"
                  file_grid : str,   # input file, e.g. grid.stl
                  periods : np.array, # periods in seconds
                  directions_deg : np.array,
                  waterdepth : float = None, # waterdepth
                  symmetry : bool = False, # symmetry in XZ plane
                  show_only : bool = False # show only the mesh
                  ):

    periods = np.array(periods)
    directions = np.array(directions_deg) * pi / 180

    file_out_nc = file_grid[:-4] + '.nc'
    outfile = "{}.dhyd".format(file_grid[:-4])


    omega = 2 * np.pi / periods

    boat = cpt.FloatingBody.from_file(file_grid, file_format="stl", name=name)

    if symmetry:
        mesh = ReflectionSymmetricMesh(boat.mesh, plane=xOz_Plane, name=f"{name}_mesh")
        boat = cpt.FloatingBody(mesh=mesh)

    boat.add_all_rigid_body_dofs()
    boat.keep_immersed_part()
    boat.show()

    if show_only:
        return

    dataset = make_database(body=boat, omegas=omega, wave_directions=directions, waterdepth=waterdepth)


    sep = separate_complex_values(dataset)
    # sep.to_netcdf(file_out_nc,
    #               encoding={'radiating_dof': {'dtype': 'U'},
    #                         'influenced_dof': {'dtype': 'U'},
    #                         'diffraction_result': {'dtype': 'U'}})
    sep.to_netcdf(file_out_nc,
                  encoding={'radiating_dof': {'dtype': 'U'},
                            'influenced_dof': {'dtype': 'U'}})

    print(f'saved NC results as {file_out_nc}')

    hyd = Hyddb1.create_from_capytaine(filename=file_out_nc)
    if symmetry:
        hyd.symmetry = mafredo.Symmetry.XZ
    else:
        hyd.symmetry = mafredo.Symmetry.No

   
    hyd.save_as(outfile)
    print(f'Saved as: {outfile}')
    hyd.plot(do_show=True)
