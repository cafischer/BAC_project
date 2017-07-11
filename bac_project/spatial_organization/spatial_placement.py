from __future__ import division
import numpy as np
from random import Random

def get_positions(n, sidelength, seed_prng=None):
    """
    Generates 3d points, each randomly placed inside a voxel with side length dist on a nxn grid.
    :param n: Size of the grid (nxn).
    :type n: int
    :param sidelength: side length of the voxel
    :type sidelength: float
    :return: 3D coordinates of the points randomly placed within the voxel
    :rtype: array_like
    """
    prng = Random()
    if seed_prng is None:
        prng.seed(time())
    
    # create the x, y coordinates for the nxn grid
    x_grid, y_grid = np.meshgrid(np.arange(0, n*sidelength,  sidelength), np.arange(0, n*sidelength, sidelength))

    # find random x,y,z coordinates for the position inside the voxel of the specified side length
    x = np.array([prng.uniform(0, sidelength) for i in range(n*n)]).reshape((n, n))
    y = np.array([prng.uniform(0, sidelength) for i in range(n*n)]).reshape((n, n))
    z = np.array([prng.uniform(0, sidelength) for i in range(n*n)]).reshape((n, n))
    
    # add the grid position to the position inside the square 
    x += x_grid
    y += y_grid
    z = z
    
    # turn matrix into flat list
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    return x, y, z


if __name__ == '__main__':
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from random import Random
    from time import time

    seed = time()
    prng = Random()
    prng.seed(seed)
    n = 3
    sidelength = 1
    x, y, z = get_positions(n, sidelength, prng)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='k', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([0, n *sidelength])
    ax.set_ylim([0, n *sidelength])
    ax.set_zlim([0, sidelength])
    plt.show()