from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, Union

import numpy as np

from fepyio.exceptions import ArrayShapeError
from fepyio.utils.dict_utils import prune_dict

from .feb_base import FebBase, FebEnum


class LoadControllerType(FebEnum):
    """Types of LoadController."""

    LOAD_CURVE = "loadcurve"
    MATH = "math"
    PID = "PID"


@dataclass
class LoadController(FebBase):
    """FEBio > LoadData > LoadController

    Base LoadController class

    Parameters
    ----------
    id : int
        The load controller id.
    type : LoadControllerType
        The type of load controller.

    Attributes
    ----------
    id : int
        The load controller id.
    type : LoadControllerType
        The type of load controller.
    _key = "load_controller"

    Notes
    -----
    See: [FEBio Manual section 3.17](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.17.html).
    """

    id: int
    type: LoadControllerType
    _key: str = "load_controller"


@dataclass
class LoadCurve(LoadController):
    """FEBio > LoadData > LoadController

    Specify a load curve

    Parameters
    ----------
    id : int
        The load controller id.
    points : np.ndarray or list of (float, float)
        Array of (x,y) points to define load curve. Either list of 2-tuple of floats or
        Numpy array of shape (n, 2), where 'n' is the number of points.
    interpolate : {"step", "linear", "smooth"}, optional
        Define how the loadcurve is interpolated between the data points.
    extra : {"constant", "extrapolate", "repeat", "repeat offset"}, optional
        Define how load curve is interpolated past the min/max data points.

    Attributes
    ----------
    id : int
        The load controller id.
    points : np.ndarray or list of (float, float)
        Array of (x,y) points to define load curve. Either list of 2-tuple of floats or
        Numpy array of shape (n, 2), where 'n' is the number of points.
    interpolate : {"step", "linear", "smooth"}, optional
        Define how the loadcurve is interpolated between the data points.
    extra : {"constant", "extrapolate", "repeat", "repeat offset"}, optional
        Define how load curve is interpolated past the min/max data points.
    type = LoadControllerType.LOAD_CURVE
    _key = "LoadCurve"

    Notes
    -----
    See: [FEBio Manual section 3.17.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.17.1.html).
    """

    points: Union[list[tuple[float, float]], np.ndarray] = np.empty(shape=(0, 2))
    interpolate: Optional[Literal["step", "linear", "smooth"]] = None
    extra: Optional[
        Literal["constant", "extrapolate", "repeat", "repeat offset"]
    ] = None
    type: LoadControllerType = field(default=LoadControllerType.LOAD_CURVE, init=False)

    def __post_init__(self):
        # Make sure self.point is the correct shape
        if isinstance(self.points, np.ndarray) and not (
            self.points.ndim == 2
            and self.points.shape[0] >= 2
            and self.points.shape[1] == 2
        ):
            raise ArrayShapeError(
                array_shape=self.points.shape,
                array_name="points",
                expected_shape="(n, 2), where n >= 2",
            )

        if isinstance(self.points, list) and len(self.points) < 2:
            raise ArrayShapeError(
                array_shape=len(self.points),
                array_name="points",
                expected_shape="(n, 2), where n >= 2",
            )

    def to_dict(self):
        def _try_upper(s: Optional[str]) -> Optional[str]:
            """Try to return s.upper() otherwise return s"""
            return s.upper() if s is not None else None

        # Create list of comma-separated (x,y) coordinates from points
        _points = [",".join(map(str, point)) for point in self.points]

        _dict = {
            "@id": self.id,
            "@type": self.type.get_value(),
            "interpolate": _try_upper(self.interpolate),
            "extra": _try_upper(self.extra),
            "points": {"point": _points},
        }

        return prune_dict(_dict)

    @classmethod
    def linear_curve(cls, id: int) -> LoadCurve:
        """Create a linear LoadCurve with id."""
        return cls(id=id, points=[(0, 0), (1, 1)], interpolate="linear")


@dataclass
class LoadData(FebBase):
    """FEBio > LoadData

    The LoadData section is used to define load controllers. A load controller allows
    users to manipulate the value of most model parameters as an explicit of implicit
    function of time.

    Parameters
    ----------
    load_controllers : list of LoadController
        List of `LoadController`s


    Attributes
    ----------
    load_controllers : list of LoadController
        List of LoadControllers
    _key = "LoadData"

    Notes
    -----
    See: [FEBio Manual section 3.17](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.17.html)
    """

    load_controllers: list[LoadController]

    def _convert_key(self, key: str) -> str:
        return key[:-1] if key.endswith("s") else super()._convert_key(key)
