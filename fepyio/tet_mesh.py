"""
Convert a TetMesh object into a Feb object
"""


import numpy as np

from fepyio.boundary import Boundary, FixedBoundary
from fepyio.control import Control, Solver, TimeStepper
from fepyio.globals import Globals
from fepyio.load_data import LoadCurve, LoadData
from fepyio.loads import Loads, PressureLoad
from fepyio.material import Material
from fepyio.material_types import BaseMaterial
from fepyio.mesh import Elements, ElementType, Face, FaceType, Mesh, Nodes, Surface
from fepyio.mesh_domains import MeshDomains, SolidDomain
from fepyio.module import Module
from fepyio.output import LogData, LogFile, Output
from fepyio.typing.mesh import TetMesh

from .feb import Feb


def tetmesh_to_feb(
    tetmesh: TetMesh,
    materials: list[BaseMaterial],
    logfile: str,
    pressure: float,
    time_steps: int = 25,
    step_size: float = 0.1,
    **kwargs,
) -> Feb:
    """Create FEBio input file from Tetmesh.

    Parameters
    ----------
    tetmesh : TetMesh
        Tetmesh to convert to Feb.
    materials : list of BaseMaterial
        List of materials used by the TetMesh.
    logfile : str
        Absolute path to logfile.
    pressure : float
        Specified pressure load.
    time_steps : int
        Total number of time steps.
    step_size : float
        The initial time step size.
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    Feb
    """
    # Get sorted materials
    sorted_materials = sorted(materials, key=lambda m: m.id)

    # Group elements by material
    elements = group_elements_by_material(tetmesh=tetmesh, materials=sorted_materials)

    # Link element groups to materials
    # Element names in the format of: f"Elements_{materials[mat_id].name}"
    solid_domains = [
        SolidDomain(name=element.name, mat=element.name[9:]) for element in elements
    ]

    # Create mesh
    _mesh = Mesh(
        nodes=Nodes(
            name="AllNodes",
            coords=tetmesh.vertices,
            # Offset ids +1 for FEBio (base 1 instead of 0)
            ids=np.arange(tetmesh.vertices.shape[0]) + 1,
        ),
        elements=elements,
        surfaces=get_surfaces(tetmesh),
    )

    # Control parameters
    _control = Control(
        analysis="STATIC",
        time_steps=time_steps,
        step_size=step_size,
        output_level="OUTPUT_FINAL",
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

    # Create boundary conditions
    _boundary = Boundary(
        boundary_conditions=FixedBoundary(
            name="FixedEndcaps",
            node_set="@surface:ArterySurface_EndCaps",
            dofs=("x", "y", "z"),
        )
    )

    # Create loading conditions
    _loads = Loads(
        surface_loads=PressureLoad(
            name="Load",
            surface="ArterySurface_Lumen",
            pressure=pressure,
            load_curve=1,
            linear=True,
            symmetric_stiffness=True,
        )
    )

    # Create output section
    _output = Output(
        logfiles=LogFile(
            file=logfile,
            element_data=[
                LogData(data="sx;sy;sz", file="stress.csv", delim=","),
                LogData(data="Ex;Ey;Ez", file="strain.csv", delim=","),
            ],
        )
    )

    # Re-index the id for each material
    for i, material in enumerate(sorted_materials):
        material.id = i + 1

    # Return Feb object
    return Feb(
        module=Module(type="solid"),
        control=_control,
        globals=Globals(R=0, T=0, Fc=0),
        mesh=_mesh,
        material=Material(materials=sorted_materials),
        mesh_domains=MeshDomains(solid_domains=solid_domains),
        boundary=_boundary,
        loads=_loads,
        load_data=LoadData(load_controllers=LoadCurve.linear_curve(id=1)),
        output=_output,
    )


# Helper functions


def group_elements_by_material(
    tetmesh: TetMesh, materials: list[BaseMaterial]
) -> list[Elements]:
    """Group tetmesh elements by material and return list of feb.Elements.

    Material lookup is performed by material id, i.e., `tetmesh.element_materials` and
    `materials[x].id`, where `x` is a valid index.

    Parameters
    ----------
    tetmesh : TetMesh
        Tetmesh containing elements to be grouped.
    materials : list of BaseMaterial
        List of materials used to group elements by.

    Returns
    -------
    List of Elements
        For each material specified in `materials`.

    Raises
    ------
    AssertionError
        When `tetmesh.element_materials` contains duplicate material ids or a material
        id not specified by `materials`.
    """
    # Get a unique list of materials in the tetmesh (np.unique returns sorted array)
    unique_materials = np.unique(tetmesh.element_materials)

    # Create dictionary of materials using the material id as the key. Even though we
    # are given a list of materials, we cannot just use the index because the material
    # ids may not be continuous.
    material_dict = {material.id: material for material in materials}

    # If the length of the dictionary doesn't match the length of the materials list,
    # there is a duplicate key.
    assert len(material_dict) == len(materials), "Duplicate material ids in 'materials'"

    # Check if we unique materials contains any ids not in material dict
    missing_materials = set(unique_materials) - set(material_dict.keys())
    assert (
        len(missing_materials) == 0
    ), f"'tetmesh' contains materials with ids ({', '.join(missing_materials)}) "
    "that do not have a corresponding id in 'materials'"

    # create empty list for element groups
    elements_list = []
    elem_count = 0

    # group elements by their material id
    for i, mat_id in enumerate(unique_materials):
        element_group = [
            (_id, element)
            for _id, (element, material) in enumerate(
                zip(tetmesh.elements, tetmesh.element_materials)
            )
            if material == mat_id
        ]

        elements_list.append(
            Elements(
                name=f"Elements_{materials[i].name}",
                type=ElementType.TET4,
                elements=np.array([element[1] for element in element_group]) + 1,
                ids=np.arange(elem_count, elem_count + len(element_group)) + 1,
            )
        )
        elem_count += len(element_group)

    return elements_list


def get_surfaces(tetmesh: TetMesh) -> list[Surface]:
    """Get a list of feb.Surface objects from an ArterySurface object.

    Parameters
    ----------
    surfaces : ArterySurface
        Artery surfaces to be converted.

    Returns
    -------
    List of Surface
        Objects corresponding to the lumen and each endcap.
    """
    surfaces = tetmesh.surfaces

    surface_list = [
        Surface(
            name="ArterySurface_Lumen",
            faces=[
                Face(type=FaceType.TRI3, nodes=node, id=_id + 1)
                for (_id, node) in enumerate(surfaces.lumen.faces + 1)
            ],
        )
    ]

    # ArterySurface.endcaps (fixed)
    surface_list.append(
        Surface(
            name="ArterySurface_EndCaps",
            faces=[
                Face(type=FaceType.TRI3, nodes=node, id=_id + 1)
                for (_id, node) in enumerate(surfaces.endcaps.faces + 1)
            ],
        )
    )

    return surface_list
