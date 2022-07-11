import numpy as np
from dacite.core import from_dict
from dacite.exceptions import DaciteError

from fepyio.exceptions import UnknownMaterialError

from .material_types import BaseMaterial, material_dict


def convert_to_materials(
    element_materials: np.ndarray, materials_dict: dict[str, dict]
) -> list[BaseMaterial]:
    """Convert dictionary of materials into list of BaseMaterial.

    Material dictionary in format of::

        {
            'material_name': {
                'mat_type': 'neo-Hookean',
                'id': 1,
                'prop1': 0.1,
                'prop2': 0.01,
                ...
            },
            ...
        }

    Parameters
    ----------
    materials : dict
        Dictionary of materials

    Returns
    -------
    List of BaseMaterial
    """

    # create empty list of BaseMaterials
    material_list: list[BaseMaterial] = []

    for name in materials_dict:
        # Make a copy of the material so we can mutate
        _data = materials_dict[name].copy()

        if "mat_type" not in _data:
            raise UnknownMaterialError(
                f"No material type specified for material '{name}'."
            )

        # Remove 'mat_type' and add 'name' keys
        mat_type = _data.pop("mat_type")
        _data["name"] = name

        # Make sure material type is supported
        if mat_type not in material_dict:
            raise UnknownMaterialError(
                f"Material type '{mat_type}' in material '{name}' is not supported."
            )

        # Create a new material dataclass based on the data
        try:
            material_list.append(
                from_dict(data_class=material_dict[mat_type], data=_data)
            )
        except DaciteError:
            raise

    # get unique list of materials in the tetmesh
    unique_mats = np.unique(element_materials)

    return [material for material in material_list if material.id in unique_mats]
