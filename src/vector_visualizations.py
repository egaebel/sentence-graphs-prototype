from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pylab


def plot_3d_vectors(vectors, labels=None, output_file_path=None, show_figure=False):
    if labels is not None:
        _plot_3d_vectors_with_labels(vectors, labels, output_file_path, show_figure)
        return
    matrix = np.array(vectors)
    fig = plt.figure()
    axes3d = fig.add_subplot(111, projection='3d')
    print("Matrix:")
    print(matrix)
    axes3d.plot(matrix[:, 0], matrix[:, 1], matrix[:, 2], 'ro')
    if output_file_path is not None:
        plt.savefig(fname=output_file_path)
    if show_figure:
        plt.show()

def _plot_3d_vectors_with_labels(vectors, labels, output_file_path, show_figure):
    matrix = np.array(vectors)
    fig = pylab.figure()
    ax = fig.add_subplot(111, projection = '3d')
    sc = ax.scatter(matrix[:, 0], matrix[:, 1], matrix[:, 2])
    # now try to get the display coordinates of the first point

    x2, y2, _ = proj3d.proj_transform(1, 1, 1, ax.get_proj())

    label = pylab.annotate(
        "this", 
        xy = (x2, y2), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    def update_position(e):
        x2, y2, _ = proj3d.proj_transform(1, 1, 1, ax.get_proj())
        label.xy = x2,y2
        label.update_positions(fig.canvas.renderer)
        fig.canvas.draw()
    fig.canvas.mpl_connect('button_release_event', update_position)
    pylab.show()

if __name__ == '__main__':
    plot_3d_vectors(
        [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])], 
        output_file_path="test-file-for-plot-3d-vectors.png",
        show_figure=True)

"""
import pylab
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
fig = pylab.figure()
ax = fig.add_subplot(111, projection = '3d')
x = y = z = [1, 2, 3]
sc = ax.scatter(x,y,z)
# now try to get the display coordinates of the first point

x2, y2, _ = proj3d.proj_transform(1,1,1, ax.get_proj())

label = pylab.annotate(
    "this", 
    xy = (x2, y2), xytext = (-20, 20),
    textcoords = 'offset points', ha = 'right', va = 'bottom',
    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

def update_position(e):
    x2, y2, _ = proj3d.proj_transform(1,1,1, ax.get_proj())
    label.xy = x2,y2
    label.update_positions(fig.canvas.renderer)
    fig.canvas.draw()
fig.canvas.mpl_connect('button_release_event', update_position)
pylab.show()
"""