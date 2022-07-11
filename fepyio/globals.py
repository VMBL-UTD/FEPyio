from dataclasses import asdict, dataclass

from ._base import FebBase


@dataclass
class Globals(FebBase):
    """FEBio global variables. Only supports constants.

    Parameters
    ----------
    R : float, default=0
        Universal gas constant, R [F*L/n*T].
    T : float, default=0
        Absolute temperature, theta [T].
    Fc : float, default=0
        Farady constant, Fc [Q/n].

    Attributes
    ----------
    R : float, default=0
        Universal gas constant, R [F*L/n*T].
    T : float, default=0
        Absolute temperature, theta [T].
    Fc : float, default=0
        Farady constant, Fc [Q/n].
    _key = "Globals"

    Notes
    -----
    See: [FEBio manual section 3.4](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.4.html)
    """

    R: float = 0
    T: float = 0
    Fc: float = 0

    def to_dict(self):
        return {"Constants": asdict(self)}
