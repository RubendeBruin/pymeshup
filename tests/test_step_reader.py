from pymeshup import STEP, Plot

def test_read_step(assets_dir):
    s = STEP(assets_dir / 'sphere_r1.step')
    v = s.to_volume()
    Plot(v)