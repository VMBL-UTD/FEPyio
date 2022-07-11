from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimpleMesh:
    """Simple mesh containing faces and vertices.

    Parameters
    ----------
    vertices : np.ndarray
        (n, 3) Numpy array of (x,y,z) coordinates of 'n' vertices. Values are `float`s.
    faces : np.ndarray
        (m, p) Numpy array of 'm' faces, with 'p' number of vertices. Values are `int`s
        and correspond to the indices of `vertices`.

    Attributes
    ----------
    vertices : np.ndarray
        (n, 3) Numpy array of (x,y,z) coordinates of 'n' vertices. Values are `float`s.
    faces : np.ndarray
        (m, p) Numpy array of 'm' faces, with 'p' number of vertices. Values are `int`s
        and correspond to the indices of `vertices`.
    """

    vertices: np.ndarray
    faces: np.ndarray


@dataclass
class ArterySurface:
    """Artery surfaces

    Parameters
    ----------
    lumen : SimpleMesh
        SimpleMesh for lumen surface.
    outer : SimpleMesh
        SimpleMesh for outer artery surface.
    endcaps : list[SimpleMesh]
        List of simple meshes for artery endcaps.

    Attributes
    ----------
    lumen : SimpleMesh
        SimpleMesh for lumen surface.
    outer : SimpleMesh
        SimpleMesh for outer artery surface.
    endcaps : list[SimpleMesh]
        List of simple meshes for artery endcaps.
    """

    lumen: SimpleMesh
    outer: SimpleMesh
    endcaps: SimpleMesh


@dataclass
class TetMesh:
    """Tetrahedral elements mesh

    Parameters
    ----------
    vertices : np.ndarray
        (n, 3) Numpy array of vertices.
    elements : np.ndarray
        (m, 4) Numpy array of tetrahedral elements.
    surfaces : SurfaceTypes
        Collection of surfaces, including lumen and endcaps.

    Attributes
    ----------
    vertices : np.ndarray
        (n, 3) Numpy array of vertices.
    elements : np.ndarray
        (m, 4) Numpy array of tetrahedral elements.
    surfaces : SurfaceTypes
        Collection of surfaces, including lumen and endcaps.
    element_centroids : np.ndarray
        (m, 3) Numpy array of element centroids.
    element_materials : np.ndarray
        (m,) Numpy array of element material types
    """

    vertices: np.ndarray
    elements: np.ndarray
    surfaces: ArterySurface
    element_centroids: np.ndarray = field(init=False)
    element_materials: np.ndarray = field(init=False)

    def __post_init__(self):
        self.element_centroids = np.array(
            [np.mean(self.vertices[element], axis=0) for element in self.elements]
        )
