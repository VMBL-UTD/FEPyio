import numpy as np
import pytest
from dacite.exceptions import MissingValueError, WrongTypeError

from fepyio import material_types
from fepyio.convert_materials import UnknownMaterialError, convert_to_materials


@pytest.fixture(scope="class")
def opts_materials() -> dict:
    return {
        "arterial": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.3,
            "v": 0.48,
            "id": 1,
            "color": "black",
        },
        "calcium": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 10,
            "v": 0.48,
            "id": 2,
            "color": "blue",
        },
        "sleeve": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.4,
            "v": 0.48,
            "id": 3,
            "color": "purple",
        },
        "fibrotic": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.6,
            "v": 0.48,
            "id": 4,
            "color": "green",
        },
        "fibrofatty": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.5,
            "v": 0.48,
            "id": 5,
            "color": "yellow",
        },
        "necrotic": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.02,
            "v": 0.48,
            "id": 6,
            "color": "red",
        },
        "adventitia": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.3,
            "v": 0.48,
            "id": 7,
            "color": "hotpink",
        },
        "media": {
            "mat_type": "neo-Hookean",
            "density": 1.0,
            "E": 0.3,
            "v": 0.48,
            "id": 8,
            "color": "gray",
        },
    }


@pytest.fixture(scope="class")
def element_materials():
    return np.array([3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8])


class TestConvertToMaterials:
    def test_populate_materials(self, element_materials, opts_materials):
        # Add coupled mooney-rivlin sample
        old_fibrotic = opts_materials["fibrotic"]
        opts_materials["fibrotic"] = {
            "mat_type": "coupled Mooney-Rivlin",
            "density": 1.0,
            "id": 4,
            "c1": 0.46,
            "c2": 0.48,
            "k": 0.5,
        }

        materials = convert_to_materials(element_materials, opts_materials)

        assert materials[0] == material_types.NeoHookean(
            name="sleeve",
            id=3,
            density=1.0,
            E=0.4,
            v=0.48,
        )

        assert materials[1] == material_types.CoupledMooneyRivlin(
            name="fibrotic",
            id=4,
            density=1.0,
            c1=0.46,
            c2=0.48,
            k=0.5,
        )

        # Restore opts_dictionary to not interfere with other tests
        opts_materials["fibrotic"] = old_fibrotic

    def test_unsupported_material(self):
        unsupported_material_type = {
            "material": {
                "mat_type": "foo",
                "density": 1.0,
                "id": 1,
                "E": 0.1,
                "v": 0.1,
            }
        }

        unlisted_material_type = {
            "material": {
                "density": 1.0,
                "id": 1,
                "E": 0.1,
                "v": 0.1,
            }
        }

        with pytest.raises(UnknownMaterialError):
            convert_to_materials(np.zeros(3), unsupported_material_type)

        with pytest.raises(UnknownMaterialError):
            convert_to_materials(np.zeros(3), unlisted_material_type)

    def test_missing_properties(self):
        missing_id = {
            "material": {
                "mat_type": "neo-Hookean",
                "density": 1.0,
                "E": 0.1,
                "v": 0.1,
            }
        }

        with pytest.raises(MissingValueError):
            convert_to_materials(np.zeros(3), missing_id)

    def test_wrong_property_type(self):
        wrong_property_type = {
            "material": {
                "mat_type": "neo-Hookean",
                "density": 1.0,
                "id": "a",
                "E": 0.1,
                "v": 0.1,
            }
        }

        with pytest.raises(WrongTypeError):
            convert_to_materials(np.zeros(3), wrong_property_type)
