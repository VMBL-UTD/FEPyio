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

    @classmethod
    def _convert_material_key(cls, key):
        return f"@{key}" if key in {"id", "name", "type"} else key

    @classmethod
    def material_to_dict(cls, material: BaseMaterial):
        def _getattr(material: BaseMaterial, name: str):
            # BaseMaterial.type is an Enum. We want to get the string key out of it.
            return (
                getattr(material, name).value
                if name == "type"
                else getattr(material, name)
            )

        return {
            cls._convert_material_key(field.name): _getattr(material, field.name)
            for field in fields(material)
        }

    def to_dict(self):
        _dict = {
            "material": [self.material_to_dict(material) for material in self.materials]
        }

        return unlist_dict(_dict)
