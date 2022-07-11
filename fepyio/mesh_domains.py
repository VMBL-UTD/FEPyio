from dataclasses import dataclass

from fepyio.typing.listable import Listable
from fepyio.utils.listable_utils import listable_map

from ._base import FebBase, apply_to_dict


@dataclass
class SolidDomain(FebBase):
    """FEBio > Mesh Domains > Solid Domain

    Parameters
    ----------
    name : str
        The name of element set (defined in an Elements section). The element set must
        only contain solid elements.
    mat : str
        The name of the material that will be assigned to this domain

    Attributes
    ----------
    name : str
        The name of element set (defined in an Elements section). The element set must
        only contain solid elements.
    mat : str
        The name of the material that will be assigned to this domain
    _key = "SolidDomain"

    Notes
    -----
    See: [FEBio manual section 3.7.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.7.1.html).
    """

    name: str
    mat: str

    def _convert_key(self, key: str) -> str:
        return f"@{key}"


@dataclass
class MeshDomains(FebBase):
    """FEBio > Mesh Domains

    Parameters
    ----------
    solid_domains : Listable of SolidDomain
        Listable of SolidDomains

    Attributes
    ----------
    solid_domains : Listable of SolidDomain
        Listable of SolidDomains
    _key = "MeshDomains"

    Notes
    -----
    See: [FEBio manual section](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.7.html).
    """

    solid_domains: Listable[SolidDomain]

    def to_dict(self):
        return {
            "SolidDomain": listable_map(apply_to_dict, self.solid_domains),
        }
