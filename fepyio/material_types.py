from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Type


class MaterialType(Enum):
    """Types of FEBio materials."""

    NEO_HOOKEAN = "neo-Hookean"
    COUPLED_MOONEY_RIVLIN = "coupled Mooney-Rivlin"


@dataclass
class BaseMaterial:
    """Base class for FEBio materials.

    Attributes
    ----------
    name : str
        Material name.
    id : int
        Material id.
    type : MaterialType
        Material type.

    Notes
    -----
    Additional FEBio materials exist but are not currently supported.
    """

    name: str
    id: int
    type: MaterialType


@dataclass
class NeoHookean(BaseMaterial):
    """Neo-Hookean FEBio material.

    Attributes
    ----------
    name : str
        Material name.
    id : int
        Material id.
    density : float
        Material density.
    E : float
        Young's modulus [P].
    v : float
        Poisson's ratio.
    type = MaterialType.NEO_HOOKEAN

    Notes
    -----
    See: [FEBio Manual section 4.1.3.16](https://help.febio.org/FebioUser/FEBio_um_3-4-4.1.3.16.html).
    """

    density: float
    E: float
    v: float
    type: MaterialType = field(default=MaterialType.NEO_HOOKEAN, init=False)


@dataclass
class CoupledMooneyRivlin(BaseMaterial):
    """Coupled Mooney-Rivlin FEBio material.

    Parameters
    ----------
    name : str
        Material name.
    id : int
        Material id.
    density : float
        Material density.
    c1 : float
        Mooney-Rivlin c1 parameter [P].
    c2 : float
        Mooney-Rivlin c2 parameter [P].
    k : float
        Bulk-modulus [P].

    Attributes
    ----------
    name : str
        Material name.
    id : int
        Material id.
    density : float
        Material density.
    c1 : float
        Mooney-Rivlin c1 parameter [P].
    c2 : float
        Mooney-Rivlin c2 parameter [P].
    k : float
        Bulk-modulus [P].
    type = MaterialType.COUPLED_MOONEY_RIVLIN

    Notes
    -----
    See: [FEBio Manual section 4.1.3.17](https://help.febio.org/FebioUser/FEBio_um_3-4-4.1.3.17.html).
    """

    density: float
    c1: float
    c2: float
    k: float
    type: MaterialType = field(default=MaterialType.COUPLED_MOONEY_RIVLIN, init=False)


material_dict: dict[str, Type[BaseMaterial]] = {
    material.type.value: material for material in BaseMaterial.__subclasses__()
}
"""Dictionary of FEBio material classes.

keys are the material type as a string and values are the material class (not instance)
"""
