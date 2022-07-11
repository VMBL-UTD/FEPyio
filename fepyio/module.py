from dataclasses import dataclass
from typing import Literal

from ._base import FebBase


@dataclass
class Module(FebBase):
    """Specify type of FEBio analysis.

    Parameters
    ----------
    type : {"solid", "biphasic", "solute", "multiphasic", "heat", "fluid", "fluid-FSI"}
        Type of FEBio analysis

    Attributes
    ----------
    type : {"solid", "biphasic", "solute", "multiphasic", "heat", "fluid", "fluid-FSI"}
        Type of FEBio analysis
    _key = "Analysis"

    Notes
    -----
    See: [FEBio manual section 3.2](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.2.html).
    """

    type: Literal[
        "solid",
        "biphasic",
        "solute",
        "multiphasic",
        "heat",
        "fluid",
        "fluid-FSI",
    ]

    def to_dict(self):
        return {
            "@type": self.type,
        }
