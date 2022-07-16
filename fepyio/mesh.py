from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from fepyio.exceptions import ArrayShapeError
from fepyio.utils.dict_utils import prune_dict, unlist_dict

from ._base import FebBase
from ._feb_enum import FebEnum


@dataclass
class Nodes(FebBase):
    """FEBio > Mesh > Nodes

    Parameters
    ----------
    name : str
        Set name.
    coords : np.ndarray
        Numpy array of node coordinates (x,y,z). Same length as `ids`. Should be shape
        (n, 3), where 'n' is the number of nodes.
    ids : np.ndarray
        Numpy array of node ids. Same length as `coords`. Should be shape (n, ), where
        'n' is the number of nodes.

    Attributes
    ----------
    name : str
        Set name.
    coords : np.ndarray
        Numpy array of node coordinates (x,y,z). Same length as `ids`. Should be shape
        (n, 3), where 'n' is the number of nodes.
    ids : np.ndarray
        Numpy array of node ids. Same length as `coords`. Should be shape (n, ), where
        'n' is the number of nodes.
    _key = "Nodes"

    Notes
    -----
    See: [FEBio Manual section 3.6.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.6.1.html).
    """

    name: str
    coords: np.ndarray
    ids: np.ndarray

    def __post_init__(self):
        # Check numpy array shape
        if self.coords.ndim != 2 or self.coords.shape[1] != 3:
            raise ArrayShapeError(
                array_shape=self.coords.shape,
                array_name="coords",
                expected_shape="(n, 3)",
            )
        if self.ids.ndim != 1 or self.ids.shape[0] != self.coords.shape[0]:
            raise ArrayShapeError(
                array_shape=self.ids.shape,
                array_name="ids",
                expected_shape=f"({self.coords.shape[0],},)",
            )

    def to_dict(self):
        _dict = {
            "@name": self.name,
            "node": [
                {
                    "@id": _id,
                    "#text": ",".join(map(str, coord)),
                }
                for _id, coord in zip(self.ids, self.coords)
            ],
        }

        return unlist_dict(_dict)


class ElementType(FebEnum):
    """Type of FEBio elements"""

    HEX8 = "hex8"
    HEX20 = "hex20"
    HEX27 = "hex27"
    PENTA6 = "penta6"
    PENTA15 = "penta15"
    PYRA5 = "pyra5"
    TET4 = "tet4"
    TET10 = "tet10"
    TET15 = "tet15"


@dataclass
class Elements(FebBase):
    """FEBio > Mesh > Elements

    Parameters
    ----------
    name : str
        Set name.
    type : ElementType
        Type of elements. Determines expected length of 'nodes' 2nd dimension.
    elements : np.ndarray
        (n, t) Numpy array of node indices, where 'n' is the number of elements and 't' is
        the number of nodes per element specified by 'type'.
    ids : np.ndarray
        (n,) Numpy array of element ids, where 'n' is the number of elements.

    Attributes
    ----------
    name : str
        Set name.
    type : ElementType
        Type of elements. Determines expected length of 'nodes' 2nd dimension.
    elements : np.ndarray
        (n, t) Numpy array of node indices, where 'n' is the number of elements and 't' is
        the number of nodes per element specified by 'type'.
    ids : np.ndarray
        (n,) Numpy array of element ids, where 'n' is the number of elements.
    _key = "Elements"

    Notes
    -----
    See: [FEBio Manual section 3.6.2](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.6.2.html).
    """

    name: str
    type: ElementType
    elements: np.ndarray
    ids: np.ndarray

    def __post_init__(self):
        # Extract digits from string and cast to int
        num_elements = int(
            "".join([ch for ch in self.type.get_value() if ch.isnumeric()])
        )

        # Check to make sure 'num_elements' == elements.shape
        if self.elements.ndim != 2 or self.elements.shape[1] != num_elements:
            raise ArrayShapeError(
                array_shape=self.elements.shape,
                array_name="elements",
                expected_shape=f"(n, {num_elements},)",
                extra=f"for type '{self.type}'",
            )
        if self.ids.ndim != 1 or self.ids.shape[0] != self.elements.shape[0]:
            raise ArrayShapeError(
                array_shape=self.ids.shape,
                array_name="ids",
                expected_shape=f"({self.elements.shape[0]},)",
            )

    def to_dict(self):
        _dict = {
            "@type": self.type.get_value(),
            "@name": self.name,
            "elem": [
                {
                    "@id": _id,
                    "#text": ",".join(map(str, node)),
                }
                for _id, node in zip(self.ids, self.elements)
            ],
        }

        return unlist_dict(_dict)


@dataclass
class NodeSet(FebBase):
    """FEBio > Mesh > NodeSet

    Parameters
    ----------
    name : str
        Set name.
    node_ids : np.ndarray, optional
        Numpy array of node ids to include in the set.
    node_sets : Listable of NodeSet, optional
        Other NodeSets to include in the set.

    Attributes
    ----------
    name : str
        Set name.
    node_ids : np.ndarray, optional
        Numpy array of node ids to include in the set.
    node_sets : Listable of NodeSet, optional
        Other NodeSets to include in the set.

    Notes
    -----
    See: [FEBio Manual section 3.6.3](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.6.3.html).
    """

    name: str
    node_ids: Optional[np.ndarray] = None
    node_sets: Optional[list[NodeSet]] = None

    def __post_init__(self):
        if self.node_ids is not None and self.node_ids.ndim != 1:
            raise ArrayShapeError(
                array_shape=self.node_ids.shape,
                array_name="ids",
                expected_shape="(n,)",
            )

    def to_dict(self):
        return prune_dict(
            {
                "@name": self.name,
                "node": self.node_ids,
                "node_sets": self.node_sets,
            }
        )


class FaceType(FebEnum):
    QUAD4 = "quad4"
    QUAD8 = "quad8"
    TRI3 = "tri3"
    TRI6 = "tri6"
    TRI7 = "tri7"


@dataclass
class Face(FebBase):
    """FEBio > Mesh > Surface > Face

    Parameters
    ----------
    type : FaceType
        Face type. Describes how many nodes.
    id : int
        Face id.
    nodes : np.ndarray
        (t,) Numpy array of node indices, where 't' is the number in 'type'.

    Attributes
    ----------
    type : FaceType
        Face type. Describes how many nodes.
    id : int
        Face id.
    nodes : np.ndarray
        (t,) Numpy array of node indices, where 't' is the number in 'type'.
    _key : str, optional
        Defaults to `type`.
    """

    type: FaceType
    id: int
    nodes: np.ndarray
    # Ok to ignore type because we assign default value in __post_init__
    _key: Optional[str] = None  # type: ignore

    def __post_init__(self):
        # Extract digits from string and cast to int
        num_elements = int(
            "".join([ch for ch in self.type.get_value() if ch.isnumeric()])
        )

        # Check to make sure 'num_elements' == nodes.shape
        if self.nodes.ndim != 1 or self.nodes.shape != (num_elements,):
            raise ArrayShapeError(
                array_shape=self.nodes.shape,
                array_name="nodes",
                expected_shape=f"({num_elements},)",
                extra=f"for type '{self.type}'",
            )

        # Auto-assign _key if it hasn't been manually assigned
        if self._key is None:
            self._key = self.type.get_value()


@dataclass
class Surface(FebBase):
    """FEBio > Mesh > Surface

    Parameters
    ----------
    name : str
        Name of surface.
    faces : list of Face
        List of faces.

    Attributes
    ----------
    name : str
        Name of surface.
    faces : list of Face
        List of faces.
    _key = "Surface"

    Notes
    -----
    See: [FEBio Manual section 3.6.5](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.6.5.html).
    """

    name: str
    faces: list[Face]

    def _group_faces(self) -> dict[str, list[Face]]:
        """Return dictionary of faces grouped by type.

        Return:
            Dictionary with key = face types and value = list of faces of that type.
        """
        # Uncomment if self.faces becomes a listable. Unused if self.faces is a list.
        # if isinstance(self.faces, Face):
        #     return {self.faces.type: [self.faces]}

        grouped_faces: dict[str, list[Face]] = {}

        # Group faces
        for face in self.faces:
            if face.type.get_value() not in grouped_faces:
                grouped_faces[face.type.get_value()] = [face]
            else:
                grouped_faces[face.type.get_value()].append(face)

        # Un-list types containing a single face
        return grouped_faces

    def to_dict(self):
        grouped_faces = {
            key: [
                {
                    "@id": face.id,
                    "#text": ",".join(map(str, face.nodes)),
                }
                for face in faces
            ]
            for (key, faces) in self._group_faces().items()
        }

        unlist_grouped_faces = unlist_dict(grouped_faces)

        _dict = {"@name": self.name}
        _dict.update(**unlist_grouped_faces)
        return _dict


@dataclass
class Mesh(FebBase):
    """FEBio > Mesh

    Note: All attributes default to None

    Parameters
    ----------
    nodes : Listable of Nodes, optional
        Single or list of Nodes.
    elements : Listable of Elements, optional
        Single or list of Elements.
    node_sets : Listable of NodeSet, optional
        Single or list of NodeSet.
    surface : Listable of surface, optional
        Single or list of Surface.

    Attributes
    ----------
    nodes : Listable of Nodes
        Single or list of Nodes.
    elements : Listable of Elements
        Single or list of Elements.
    node_sets : Listable of NodeSet
        Single or list of NodeSet.
    surfaces : Listable of surface
        Single or list of Surface.
    _key = "Mesh"

    Notes
    -----
    See: [FEBio Manual section 3.6](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.6.html).
    """

    nodes: list[Nodes] = field(default_factory=lambda: [])
    elements: list[Elements] = field(default_factory=lambda: [])
    node_sets: list[NodeSet] = field(default_factory=lambda: [])
    surfaces: list[Surface] = field(default_factory=lambda: [])

    def to_dict(self) -> dict:
        return prune_dict(
            {
                "Nodes": [node.to_dict() for node in self.nodes],
                "Elements": [element.to_dict() for element in self.elements],
                "NodeSet": [node_set.to_dict() for node_set in self.node_sets],
                "Surface": [surface.to_dict() for surface in self.surfaces],
            }
        )
