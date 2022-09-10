import numpy as np

class Frame():
    """Frames are 2d slices

    X : to "right"
    Y : to top
    """

    def __init__(self, *args):
        """Construct a Frame using my_frame = Frame(x1,y1,x2,y2,....)"""
        if not args:
            raise ValueError("Please provide x and y locations for the points")

        if len(args) % 2 != 0:
            raise ValueError("Number of coordinates should be even")

        for a in args:
            if not isinstance(a, (float,int)):
                raise ValueError(f"Only numeric entries are accepted, {a} is not nummeric")

        n = len(args) // 2
        self.xy = [(args[2*i], args[2*i+1]) for i in range(n)]

        if self.xy[0] != self.xy[-1]:
            self.xy.append(self.xy[0])

        self.xy = tuple(self.xy)  # make immutable

    def autocomplete(self):
        """Retruns a copy of self with the frame expanded over the mirror in x=0"""

        frame = self.xy[:-1] # all except the last one (which is the duplicate of 1)

        n = len(frame)
        xs = [f[0] for f in frame]
        ys = [f[1] for f in frame]

        r = [(xs[i], ys[i]) for i in range(n)] # make a new list


        if np.min(xs) >= 0:
            mirror = [(-xs[i], ys[i]) for i in reversed(range(n)) if
                      xs[i] != 0]  # duplicate except points on the centerline
            r = [*r, *mirror]

        # create a new frame and return that
        xy = []
        for pair in r:
            xy.extend(pair)

        return Frame(*xy)

    def center(self):
        xs = [f[0] for f in self.xy]
        ys = [f[1] for f in self.xy]

        return (np.mean(xs), np.mean(ys))

    @property
    def n(self):
        return len(self.xy)

    def as_vertices_at(self, x):
        """Returns 3d points (vertices) if this frame is located in 3d at x=given"""
        return [(x, p[0], p[1]) for p in self.xy]