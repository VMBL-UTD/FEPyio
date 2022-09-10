from dataclasses import dataclass, fields
from typing import ClassVar

from fepyio.feb_base import AtNames, FebBase
from fepyio.material_types import BaseMaterial
from fepyio.utils.dict_utils import unlist_dict


@dataclass
class Material(FebBase):
    """FEBio materials.

    Parameters
    ----------
    materials : list of BaseMaterial
        List of materials

    Attributes
    ----------
    materials : list of BaseMaterial
        List of materials
    _key = "Material"

    Notes
    -----
    See: [FEBio Manual section 3.5](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.5.html).
    """

    materials: list[BaseMaterial]
    _at_names: ClassVar[AtNames] = {"id", "name", "type"}

    def to_dict(self):
        def _getattr(material: BaseMaterial, name: str):
            # BaseMaterial.type is an Enum. We want to get the string key out of it.
            if name == "type":
                return getattr(material, name).value
            else:
                return getattr(material, name)

        _dict = {
            "material": [
                {
                    self._convert_key(field.name): _getattr(material, field.name)
                    for field in fields(material)
                }
                for material in self.materials
            ]
        }

        return unlist_dict(_dict)
