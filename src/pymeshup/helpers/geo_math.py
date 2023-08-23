import math

import numpy as np


def points_on_circle(p1, p2, radius, max_angle_deg):
    """Given two points on a circle (p1 and p2) and the radius of that circle (radius),
    returns a list of points on that circle between p1 and p2."""

    # https://math.stackexchange.com/questions/496070/finding-the-equation-of-a-circle-given-two-points-and-the-radius

    A = np.array(p1)
    B = np.array(p2)

    p0 = 0.5 * (B+A)
    v = 0.5 * (B-A)

    AB = B-A
    n = np.array([-AB[1], AB[0]])

    t = np.sqrt((radius**2-np.linalg.norm(v)**2) / np.linalg.norm(n)**2)

    M = p0 + t * n


    points = []

    a0 = np.arctan2(p1[1]-M[1], p1[0]-M[0])
    a1 = np.arctan2(p2[1]-M[1], p2[0]-M[0])

    angle_change = abs(a1-a0)
    max_angle_rad = max_angle_deg * np.pi / 180

    for a in np.linspace(a0, a1, num = math.ceil(angle_change / max_angle_rad)):
        points.append(M + radius * np.array([np.cos(a), np.sin(a)]))

    return points

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    p1 = [0.3,0]
    p2 = [1,1]
    radius = 2
    max_angle_deg = 2

    points = points_on_circle(p1, p2, radius, max_angle_deg)

    plt.plot(p1[0], p1[1],'b*')
    plt.plot(p2[0], p2[1],'b*')

    for point in points:
        plt.plot(point[0], point[1],'r.')
    plt.show()