from mpl_toolkits.mplot3d import Axes3D
from pylab import show

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def plot_3d_vectors(vectors, labels=None, output_file_path=None, show_figure=False):
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

if __name__ == '__main__':
    plot_3d_vectors(
        [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])], 
        output_file_path="test-file-for-plot-3d-vectors.png",
        show_figure=True)