from dataclasses import dataclass, field
from typing import Optional

from fepyio.utils.dict_utils import prune_dict

from ._base import FebBase
from ._feb_enum import FebEnum


class SurfaceLoadType(FebEnum):
    """Types of SurfaceLoads."""

    PRESSURE = "pressure"


@dataclass
class SurfaceLoad(FebBase):
    """FEBio > Loads > Surface Loads.

    Currently only supports pressure surface loads.

    Attributes
    ----------
    name : str
        The name of the surface load.
    surface : str
        The name of the surface that the load will be applied to.
    type : SurfaceLoadType
        The type of surface load

    Notes
    -----
    See: [FEBio Manual section 3.12.2](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.12.2.html)
    """

    name: str
    surface: str
    type: SurfaceLoadType
    _key: str = field(default="surface_load", init=False)


@dataclass
class PressureLoad(SurfaceLoad):
    """FEBio > Loads > Surface Load > Pressure Load

    Parameters
    ----------
    name : str
        The name of the surface load.
    surface : str
        The name of the surface that the load will be applied to.
    pressure : float
        The applied pressure value [P].
    load_curve : int
        The id of the load curve used for pressure. Defaults to constant load.
    symmetric_stiffness : bool, optional
        Symmetric stiffness flag. Defaults to True.
    linear : bool, optional
        Linear flag. Defaults to False.
    shell_bottom : bool, optional
        Shell bottom flag. Defaults to False.

    Attributes
    ----------
    name : str
        The name of the surface load.
    surface : str
        The name of the surface that the load will be applied to.
    pressure : float
        The applied pressure value [P].
    load_curve : int
        The id of the load curve used for pressure. Defaults to constant load.
    symmetric_stiffness : bool
        Symmetric stiffness flag. Defaults to True.
    linear : bool
        Linear flag. Defaults to False.
    shell_bottom : bool
        Shell bottom flag. Defaults to False.
    type = SurfaceLoadType.PRESSURE
    _key = "surface_load"

    Notes
    -----
    See: [FEBio Manual section 3.12.2.1](https://help.febio.org/FebioUser/FEBio_um_3-4-3.12.2.1.html).
    """

    pressure: float
    load_curve: Optional[int] = None
    symmetric_stiffness: Optional[bool] = None
    linear: Optional[bool] = None
    shell_bottom: Optional[bool] = None
    type: SurfaceLoadType = field(default=SurfaceLoadType.PRESSURE, init=False)

    def to_dict(self):
        def _bint(b: Optional[bool]) -> Optional[int]:
            return int(b) if b is not None else None

        # Create dictionary for pressure if custom load curve is specified
        _pressure = (
            {"@lc": self.load_curve, "#text": str(self.pressure)}
            if self.load_curve is not None
            else self.pressure
        )

        _dict = {
            "@name": self.name,
            "@surface": self.surface,
            "@type": self.type.get_value(),
            "pressure": _pressure,
            "symmetric_stiffness": _bint(self.symmetric_stiffness),
            "linear": _bint(self.linear),
            "shell_bottom": _bint(self.shell_bottom),
        }

        # Prune None values
        return prune_dict(_dict)


@dataclass
class Loads(FebBase):
    """FEBio > Loads

    The Loads section defines all nodal, edges, surface, and body loads that can be
    applied to the model.

    Parameters
    ----------
    surface_loads : list of SurfaceLoad
        Surface loads

    Attributes
    ----------
    surface_loads : list of SurfaceLoad
        Surface loads
    _key = "Loads"

    Notes
    -----
    See: [FEBio Manual section 3.12](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.12.html).
    """

    surface_loads: list[SurfaceLoad]

    def _convert_key(self, key: str) -> str:
        return key[:-1] if key.endswith("s") else super()._convert_key(key)
