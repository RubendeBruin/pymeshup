from copy import copy

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

        if len(args) == 1:
            if isinstance(args[0], Frame):
                self.xy = tuple(args[0].xy)
                return

        if len(args) % 2 != 0:
            raise ValueError("Number of coordinates should be even")

        for a in args:
            if not isinstance(a, (float,int)):
                raise ValueError(f"Only numeric entries are accepted, {a} is not nummeric")

        n = len(args) // 2

        if n==0:
            raise ValueError("Please provide coordinates")

        self.xy = [(args[2*i], args[2*i+1]) for i in range(n)]

        if self.xy[0] != self.xy[-1]:
            self.xy.append(self.xy[0])

        self.xy = tuple(self.xy)  # make immutable

    def copy(self):
        f = Frame(0,0)  # use dummy data
        f.xy = copy(self.xy)

        return f

    def autocomplete(self):
        """Returns a copy of self with the frame expanded over the mirror in x=0"""

        frame = self.xy[:-1] # all except the last one (which is the duplicate of 1)

        n = len(frame)

        if n==0:  # Only a single point, nothing to auto-complete
            # return a copy of self
            return self.copy()

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

    def is_identical_to(self, other):
        """Returns True if this frame is identical to other"""
        if self.n != other.n:
            return False

        for i in range(self.n):
            if self.xy[i] != other.xy[i]:
                return False

        return True