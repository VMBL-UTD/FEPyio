from dataclasses import dataclass, fields

from fepyio.typing import Listable
from fepyio.utils.dict_utils import unlist_dict

from ._base import FebBase
from .material_types import BaseMaterial


@dataclass
class Material(FebBase):
    """FEBio materials.

    Parameters
    ----------
    materials : BaseMaterial or list of BaseMaterial
        Single or list of materials

    Attributes
    ----------
    materials : BaseMaterial or list of BaseMaterial
        Single or list of materials
    _key = "Material"

    Notes
    -----
    See: [FEBio Manual section 3.5](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.5.html).
    """

    materials: Listable[BaseMaterial]

    def _convert_key(self, key: str) -> str:
        if key in {"id", "name", "type"}:
            return f"@{key}"
        else:
            return super()._convert_key(key)

    def to_dict(self):
        def _getattr(material: BaseMaterial, name: str):
            # BaseMaterial.type is an Enum. We want to get the string key out of it.
            if name == "type":
                return getattr(material, name).value
            else:
                return getattr(material, name)

        # Force list
        materials = (
            self.materials if isinstance(self.materials, list) else [self.materials]
        )

        _dict = {
            "material": [
                {
                    self._convert_key(field.name): _getattr(material, field.name)
                    for field in fields(material)
                }
                for material in materials
            ]
        }

        return unlist_dict(_dict)