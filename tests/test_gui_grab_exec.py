from pymeshup import Volume, Cylinder, Box  # noqa: F401


code = """
c = Cylinder()
b = Box(xmin=0, zmax = 3, ymin=-3, ymax=3)
d = 23
e = c.inside_of(b)
del c
"""


def test_grab_newly_created_volumes():
    # Run the user code in its own namespace. Do not rely on the locals() of this
    # function: since python 3.13 (PEP 667) locals() returns a snapshot, so anything
    # exec() defines in it would be discarded.
    namespace = dict()

    exec(code, globals(), namespace)

    volumes = dict()

    for key, value in namespace.items():
        if isinstance(value, Volume):
            print(f"New volume found: {key}")
            volumes[key] = value

    assert "b" in volumes
    assert "e" in volumes
    assert "c" not in volumes
    assert "d" not in volumes
