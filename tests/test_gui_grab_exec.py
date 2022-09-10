from pymeshup import *


code = """
c = Cylinder()
b = Box(xmin=0, zmax = 3, ymin=-3, ymax=3)
d = 23
e = c.inside_of(b)
del c
"""

def test_grab_newly_created_volumes():

    key_before = [v for v in locals().keys()]

    exec(code)

    key_after = [v for v in locals().keys()]
    local_vars = [v for v in locals().values()]
    items_after = [i for i in locals().items()]
    volumes = dict()

    for key, value in items_after:
        if key not in key_before:
            print(f'New variable found: {key}')

            if isinstance(value, Volume):
                volumes[key] = value


    assert 'b' in volumes
    assert 'e' in volumes
    assert 'c' not in volumes
    assert 'd' not in volumes


