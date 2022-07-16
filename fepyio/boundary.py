from dataclasses import dataclass, field
from typing import Literal

from fepyio.utils.dict_utils import prune_dict

from ._base import FebBase
from ._feb_enum import FebEnum


class BoundaryType(FebEnum):
    """Types of BoundaryCondition."""

    FIX = "fix"
    PRESCRIBE = "prescribe"
    RIGID = "rigid"
    LINEAR_CONSTRAINT = "linear constraint"


@dataclass
class BoundaryCondition(FebBase):
    """FEBio > Boundary > Boundary Condition

    Define individual boundary condition.

    Parameters
    ----------
    name : str
        The name of the boundary condition.
    type : BoundaryType
        Type of boundary condition.
    node_set : str
        The name of the node set the boundary condition is applied to.

    Attributes
    ----------
    name : str
        The name of the boundary condition.
    type : BoundaryType
        Type of boundary condition.
    node_set : str
        The name of the node set the boundary condition is applied to.
    _key = "bc"

    Notes
    -----
    See: [FEBio manual section 3.10](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.10.html)
    """

    name: str
    node_set: str
    type: BoundaryType
    _key: str = field(default="bc", init=False)


@dataclass
class FixedBoundary(BoundaryCondition):
    """FEBio > Boundary > Boundary Condition > Fix

    Parameters
    ----------
    name : str
        The name of the boundary condition.
    node_set : str
        The name of the node set the boundary condition is applied to.
    dofs : tuple of ({"x", "y", "z"}, ...)
        Which axis the boundary condition is applied to.

    Attributes
    ----------
    name : str
        The name of the boundary condition.
    node_set : str
        The name of the node set the boundary condition is applied to.
    dofs : tuple of ({"x", "y", "z"}, ...)
        Which axis the boundary condition is applied to.
    type = BoundaryType.FIX
    _key = "bc"

    Notes
    -----
    See: [FEBio manual section 3.10.2](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.10.2.html)
    """

    dofs: tuple[Literal["x", "y", "z"], ...]
    type: BoundaryType = field(default=BoundaryType.FIX, init=False)

    def to_dict(self) -> dict:
        return {
            "@name": self.name,
            "@type": self.type.get_value(),
            "@node_set": self.node_set,
            "dofs": ",".join(map(str, self.dofs)),
        }


@dataclass
class Boundary(FebBase):
    """FEBio > Boundary

    The Boundary section defines all fixed and prescribed boundary conditions that may
    be applied to the geometry.

    Parameters
    ----------
    boundary_conditions : Listable of BoundaryCondition
        Single or list of BoundaryCondition objects.

    Attributes
    ----------
    boundary_conditions : Listable of BoundaryCondition
        Single or list of BoundaryCondition objects.
    _key = "Boundary"

    Notes
    -----
    See: [FEBio manual section 3.10](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.10.html)
    """

    boundary_conditions: list[BoundaryCondition]

    def to_dict(self):
        _dict = {
            "bc": [bc.to_dict() for bc in self.boundary_conditions],
        }

        return prune_dict(_dict)
