import pkgutil
from enum import Enum
from pprint import pformat
from typing import Any

import numpy as np
import pytest
import xmltodict
from deepdiff import DeepDiff

from fepyio import Feb, material_types
from fepyio.boundary import Boundary, FixedBoundary
from fepyio.control import Control, Solver, TimeStepper
from fepyio.exceptions import ArrayShapeError
from fepyio.globals import Globals
from fepyio.load_data import LoadCurve, LoadData
from fepyio.loads import Loads, PressureLoad
from fepyio.material import Material
from fepyio.mesh import (
    Elements,
    ElementType,
    Face,
    FaceType,
    Mesh,
    Nodes,
    NodeSet,
    Surface,
)
from fepyio.mesh_domains import MeshDomains, SolidDomain
from fepyio.module import Module
from fepyio.output import LogData, LogFile, Output
from fepyio.utils import dict_utils


def assert_equal_dict(dict1: dict, dict2: dict, **kwargs):
    diff = DeepDiff(
        dict1,
        dict2,
        ignore_order=True,
        **kwargs,
    )
    assert diff == {}, f"Diff is not None: {pformat(diff)}"


def post_processor(path, key, value):
    # Skip keys
    if key in {"@version", "#text"}:
        return (key, value)

    # Try to convert values to float or int
    try:
        _value = float(value)
        if _value.is_integer():
            _value = int(_value)

        return (key, _value)
    except (ValueError, TypeError):
        return (key, value)


def get_feb(relative_path: str) -> dict[str, Any]:
    file = pkgutil.get_data(__name__, relative_path)
    assert file is not None
    xml = xmltodict.parse(file, postprocessor=post_processor)
    # Convert to standard dict so the deepdiffs are more readable.
    return dict_utils.to_dict(xml)  # type: ignore


# FEB Files


@pytest.fixture(scope="class")
def feb_file1(request):
    request.cls.feb_file1 = get_feb("data/Model1.feb")
    # with open(file_path, "rb") as file:


@pytest.fixture(scope="class")
def feb_file2(request):
    request.cls.feb_file2 = get_feb("data/Model2.feb")


# FEB Object Components


@pytest.fixture(scope="class")
def load_curves():
    return {
        "tuple-list": LoadCurve(
            id=1,
            interpolate="smooth",
            points=[(0, 0), (1, 1)],
        ),
        "ndarray": LoadCurve(
            id=1,
            interpolate="smooth",
            points=np.array([[0, 0], [1, 1]]),
        ),
        "linear": LoadCurve(
            id=2,
            interpolate="linear",
            points=[(0, 0), (1, 1)],
        ),
        "step": LoadCurve(
            id=3,
            interpolate="step",
            points=[(0, 0), (0.5, 0.5), (1, 1)],
        ),
    }


@pytest.fixture(scope="class")
def control():
    return Control(
        analysis="STATIC",
        time_steps=25,
        step_size=0.1,
        solver=Solver(
            max_refs=15,
            max_ups=10,
            diverge_reform=1,
            reform_each_time_step=1,
            dtol=0.001,
            etol=0.01,
            rtol=0,
            lstol=0.9,
            min_residual=1.0e-20,
            qnmethod="BFGS",
            rhoi=0,
        ),
        time_stepper=TimeStepper(
            dtmin=0.01,
            dtmax=0.1,
            max_retries=5,
            opt_iter=10,
        ),
    )


@pytest.fixture(scope="class")
def feb_globals():
    return Globals(
        R=0,
        T=0,
        Fc=0,
    )


@pytest.fixture(scope="class")
def feb_materials():
    return {
        "neo-Hookean": material_types.NeoHookean(
            name="material_1",
            density=1,
            id=1,
            E=3e-01,
            v=4.8e-01,
        ),
        "Mooney-Rivlin": material_types.CoupledMooneyRivlin(
            name="material_2",
            density=1,
            id=2,
            c1=0.1,
            c2=0.1,
            k=0.1,
        ),
    }


@pytest.fixture(scope="class")
def feb_obj1(request, load_curves, control, feb_globals, feb_materials):
    request.cls.feb_obj1 = Feb(
        module=Module("solid"),
        control=control,
        globals=feb_globals,
        material=Material(materials=[feb_materials["neo-Hookean"]]),
        mesh=Mesh(
            nodes=[
                Nodes(
                    name="AllNodes",
                    coords=np.array([[0, 0, 0]]),
                    ids=np.arange(1) + 1,
                )
            ],
            elements=[
                Elements(
                    type=ElementType.TET4,
                    name="element_group_1",
                    elements=np.array([[1, 2, 3, 4]]),
                    ids=np.array([1]),
                )
            ],
            surfaces=[
                Surface(
                    name="surface_1",
                    faces=[
                        Face(
                            type=FaceType.TRI3,
                            id=1,
                            nodes=np.array([1, 2, 3]),
                        )
                    ],
                )
            ],
        ),
        mesh_domains=MeshDomains(
            solid_domains=[SolidDomain(name="element_group_1", mat="material_1")]
        ),
        boundary=Boundary(
            boundary_conditions=[
                FixedBoundary(
                    name="fixed_surface",
                    node_set="@surface:surface_1",
                    dofs=("x", "y", "z"),
                )
            ]
        ),
        loads=Loads(
            surface_loads=[
                PressureLoad(
                    name="pressure_1",
                    surface="surface_1",
                    pressure=0.016,
                    load_curve=1,
                    linear=False,
                    symmetric_stiffness=True,
                )
            ]
        ),
        load_data=LoadData(load_controllers=load_curves["tuple-list"]),
        output=Output(
            logfiles=[
                LogFile(
                    file="C:\\Users\\Public\\Desktop\\Model1.log",
                    element_data=[
                        LogData(
                            data="Ex;Ey;Ez",
                            delim=",",
                            file="Model1_strain.csv",
                        )
                    ],
                )
            ]
        ),
    )

    request.cls.feb_dict1 = request.cls.feb_obj1.to_dict()


@pytest.fixture(scope="class")
def feb_obj2(request, load_curves, control, feb_globals, feb_materials):
    request.cls.feb_obj2 = Feb(
        module=Module("solid"),
        control=control,
        globals=feb_globals,
        material=Material(
            materials=[
                feb_materials["neo-Hookean"],
                feb_materials["Mooney-Rivlin"],
            ]
        ),
        mesh=Mesh(
            nodes=[
                Nodes(
                    name="Object03",
                    coords=np.array(
                        [
                            [3, 0, 0],
                            [3.25, 0, 0],
                            [3.5, 0, 0],
                        ]
                    ),
                    ids=np.arange(3) + 1,
                ),
                Nodes(
                    name="Object04",
                    coords=np.array(
                        [
                            [-1.06066017, -1.06066017, 0],
                            [0, -1.06066017, 0],
                            [1.06066017, -1.06066017, 0],
                        ]
                    ),
                    ids=np.arange(3) + 1441,
                ),
            ],
            elements=[
                Elements(
                    type=ElementType.HEX8,
                    name="Part8",
                    elements=np.arange(24).reshape(3, 8) + 1,
                    ids=np.arange(3) + 1,
                ),
                Elements(
                    type=ElementType.TET4,
                    name="Part7",
                    elements=np.arange(12).reshape(3, 4) + 1,
                    ids=np.arange(3) + 1,
                ),
                Elements(
                    type=ElementType.TET4,
                    name="Part6",
                    elements=np.arange(12).reshape(3, 4) + 11,
                    ids=np.arange(3) + 4,
                ),
            ],
            surfaces=[
                Surface(
                    name="fixed",
                    faces=[
                        Face(type=FaceType.QUAD4, nodes=_nodes, id=_id)
                        for (_nodes, _id) in zip(
                            np.arange(12).reshape(3, 4) + 13,
                            np.arange(3) + 1,
                        )
                    ],
                ),
                Surface(
                    name="BP",
                    faces=[
                        Face(type=FaceType.TRI3, nodes=_nodes, id=_id)
                        for (_nodes, _id) in zip(
                            np.arange(9).reshape(3, 3) + 1,
                            np.arange(3) + 4,
                        )
                    ],
                ),
                Surface(
                    name="Surf3",
                    faces=[
                        Face(type=_type, nodes=_nodes, id=_id)  # type: ignore
                        for (_type, _nodes, _id) in zip(
                            [FaceType.TRI3, FaceType.TRI3, FaceType.QUAD4],
                            [np.arange(3) + 1, np.arange(3) + 4, np.arange(4) + 7],
                            np.arange(3) + 7,
                        )
                    ],
                ),
            ],
        ),
        mesh_domains=MeshDomains(
            solid_domains=[
                SolidDomain(name="Part8", mat="material_2"),
                SolidDomain(name="Part7", mat="material_1"),
            ]
        ),
        boundary=Boundary(
            boundary_conditions=[
                FixedBoundary(
                    name="fixed",
                    node_set="@surface:fixed",
                    dofs=("x", "y", "z"),
                )
            ]
        ),
        loads=Loads(
            surface_loads=[
                PressureLoad(
                    name="BP",
                    surface="BP",
                    pressure=0.016,
                    load_curve=1,
                    linear=False,
                    symmetric_stiffness=True,
                ),
                PressureLoad(
                    name="Load3",
                    surface="Surf3",
                    pressure=0.34,
                    load_curve=2,
                    linear=True,
                    symmetric_stiffness=False,
                ),
            ]
        ),
        load_data=LoadData(
            load_controllers=[
                load_curves["linear"],
                load_curves["step"],
            ]
        ),
        output=Output(
            logfiles=[
                LogFile(
                    file="C:\\Users\\Public\\Desktop\\Model2a.log",
                    element_data=[
                        LogData(
                            data="Ex;Ey;Ez",
                            delim=",",
                            file="Model1_strain.csv",
                        ),
                        LogData(
                            data="sx;sy;sz",
                            delim=",",
                            file="Model1_stress.csv",
                        ),
                    ],
                ),
                LogFile(
                    file="C:\\Users\\Public\\Desktop\\Model2b.log",
                    element_data=[
                        LogData(
                            data="Ex;Ey;Ez",
                            delim=",",
                            file="Model2_strain.csv",
                        ),
                        LogData(
                            data="sx;sy;sz",
                            delim=",",
                            file="Model2_stress.csv",
                        ),
                    ],
                ),
            ]
        ),
    )

    request.cls.feb_dict2 = request.cls.feb_obj2.to_dict()


# FEB File tests


@pytest.mark.usefixtures(
    "feb_file1",
    "feb_obj1",
    "load_curves",
    "feb_file2",
    "feb_obj2",
)
class TestFebCreation:
    # Need to assign something to the types for the linter to pick up on, but
    # they're actually assigned as fixtures
    feb_obj1: Feb
    feb_file1: dict
    feb_dict1: dict

    feb_obj2: Feb
    feb_file2: dict
    feb_dict2: dict

    def test_version(self):
        assert (
            self.feb_dict1["febio_spec"]["@version"]
            == self.feb_file1["febio_spec"]["@version"]
        )
        assert (
            self.feb_dict2["febio_spec"]["@version"]
            == self.feb_file2["febio_spec"]["@version"]
        )

    def test_top_level_spec(self):
        # Make sure top level keys are equal
        assert self.feb_dict1.keys() == self.feb_file1.keys()

        # Compare second-level keys are equivalent
        assert (
            self.feb_dict1["febio_spec"].keys() == self.feb_file1["febio_spec"].keys()
        )

        # Check model2
        assert self.feb_dict2.keys() == self.feb_file2.keys()
        assert (
            self.feb_dict2["febio_spec"].keys() == self.feb_file2["febio_spec"].keys()
        )

    def test_module(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Module"],
            self.feb_dict1["febio_spec"]["Module"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Module"],
            self.feb_dict2["febio_spec"]["Module"],
        )

    def test_control(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Control"],
            self.feb_dict1["febio_spec"]["Control"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Control"],
            self.feb_dict2["febio_spec"]["Control"],
        )

    def test_globals(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Globals"],
            self.feb_dict1["febio_spec"]["Globals"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Globals"],
            self.feb_dict2["febio_spec"]["Globals"],
        )

    def test_material(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Material"],
            self.feb_dict1["febio_spec"]["Material"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Material"],
            self.feb_dict2["febio_spec"]["Material"],
        )

    def test_mesh(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Mesh"],
            self.feb_dict1["febio_spec"]["Mesh"],
            ignore_numeric_type_changes=True,
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Mesh"],
            self.feb_dict2["febio_spec"]["Mesh"],
            ignore_numeric_type_changes=True,
        )

    def test_mesh_domains(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["MeshDomains"],
            self.feb_dict1["febio_spec"]["MeshDomains"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["MeshDomains"],
            self.feb_dict2["febio_spec"]["MeshDomains"],
        )

    def test_boundary(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Boundary"],
            self.feb_dict1["febio_spec"]["Boundary"],
            ignore_type_in_groups=(str, Enum),
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Boundary"],
            self.feb_dict2["febio_spec"]["Boundary"],
        )

        # Check key
        assert FixedBoundary("Name", "Set", dofs=("x", "y", "z"))._key == "bc"

    def test_loads(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Loads"],
            self.feb_dict1["febio_spec"]["Loads"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Loads"],
            self.feb_dict2["febio_spec"]["Loads"],
        )

    def test_load_data(self, load_curves):
        # Try from full Feb object
        assert_equal_dict(
            self.feb_file1["febio_spec"]["LoadData"],
            self.feb_dict1["febio_spec"]["LoadData"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["LoadData"],
            self.feb_dict2["febio_spec"]["LoadData"],
        )

        # Try ndarray loadcurve
        assert_equal_dict(
            self.feb_file1["febio_spec"]["LoadData"]["load_controller"],
            load_curves["ndarray"].to_dict(),
        )

    @pytest.mark.parametrize(
        "points", [np.zeros((1, 2)), np.zeros((3, 1)), np.zeros((2, 2, 2)), [(0, 0)]]
    )
    def test_load_data_exceptions(self, points):
        with pytest.raises(ArrayShapeError):
            LoadCurve(id=0, points=points, interpolate="linear")

    def test_output(self):
        assert_equal_dict(
            self.feb_file1["febio_spec"]["Output"],
            self.feb_dict1["febio_spec"]["Output"],
        )
        assert_equal_dict(
            self.feb_file2["febio_spec"]["Output"],
            self.feb_dict2["febio_spec"]["Output"],
        )


class TestFebMesh:
    def test_nodes_errors(self):
        # Wrong coords shape
        with pytest.raises(ArrayShapeError):
            Nodes(name="nodes", coords=np.zeros(5), ids=np.zeros(3))

        with pytest.raises(ArrayShapeError):
            Nodes(name="nodes", coords=np.zeros((5, 3, 2)), ids=np.zeros(3))

        # Wrong ids shape
        with pytest.raises(ArrayShapeError):
            Nodes(name="nodes", coords=np.zeros((5, 3, 2)), ids=np.zeros((5, 3)))

        # Coords/ids shape mismatch
        with pytest.raises(ArrayShapeError):
            Nodes(name="nodes", coords=np.zeros((5, 3)), ids=np.zeros(3))

    def test_elements_errors(self):
        # Wrong array dimensions
        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros(5),
                ids=np.zeros(5),
            )

        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros((5, 4, 1)),
                ids=np.zeros(5),
            )

        # Wrong elements per type
        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros((5, 8)),
                ids=np.zeros(5),
            )

        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET10,
                elements=np.zeros((5, 4)),
                ids=np.zeros(5),
            )

        # Wrong ids shape
        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros((5, 4)),
                ids=np.zeros(4),
            )

        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros((5, 4)),
                ids=np.zeros((5, 2)),
            )

        # elements / ids shape mismatch
        with pytest.raises(ArrayShapeError):
            Elements(
                name="elms",
                type=ElementType.TET4,
                elements=np.zeros((5, 4)),
                ids=np.zeros((3)),
            )

    def test_node_set_errors(self):
        with pytest.raises(ArrayShapeError):
            NodeSet(name="nodeset", node_ids=np.zeros((5, 2)))

    def test_face_errors(self):
        # Wrong node shape
        with pytest.raises(ArrayShapeError):
            Face(type=FaceType.QUAD4, nodes=np.zeros((4, 2)), id=0)

        # Wrong node count
        with pytest.raises(ArrayShapeError):
            Face(type=FaceType.QUAD4, nodes=np.zeros(3), id=0)

        with pytest.raises(ArrayShapeError):
            Face(type=FaceType.TRI3, nodes=np.zeros(4), id=0)
