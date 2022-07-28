from dataclasses import dataclass

import xmltodict

from fepyio.boundary import Boundary
from fepyio.control import Control
from fepyio.globals import Globals
from fepyio.load_data import LoadData
from fepyio.loads import Loads
from fepyio.material import Material
from fepyio.mesh import Mesh
from fepyio.mesh_domains import MeshDomains
from fepyio.module import Module
from fepyio.output import Output

from .feb_base import FebBase


@dataclass
class Feb(FebBase):
    """File interface for FEBio.

    Parameters
    ----------
    module : Module
        Analysis type.
    control : Control
        FEBio Control element.
    globals : Globals
    material : Material
    mesh : Mesh
    mesh_domains : MeshDomains
    boundary : Boundary
    loads : Loads
    load_data : LoadData
    output : Output
    _version : str, default="3.0"
    _key : str, default = "febio_spec"

    Attributes
    ----------
    module : Module
        Analysis type.
    control : Control
        FEBio Control element.
    globals : Globals
    material : Material
    mesh : Mesh
    mesh_domains : MeshDomains
    boundary : Boundary
    loads : Loads
    load_data : LoadData
    output : Output
    _version : str, default="3.0"
    _key : str, default = "febio_spec"

    Notes
    -----
    See: [FEBio Manual section 3.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.1.html).
    """

    module: Module
    control: Control
    globals: Globals
    material: Material
    mesh: Mesh
    mesh_domains: MeshDomains
    boundary: Boundary
    loads: Loads
    load_data: LoadData
    output: Output
    _version: str = "3.0"
    _key: str = "febio_spec"

    def to_dict(self) -> dict:
        # Add top-level feb_spec
        return {self._key: super(Feb, self).to_dict()}

    def save_feb(self, filepath: str) -> None:
        """Save Feb object as .feb file.

        Parameters
        ----------
        filepath : str
            Path to .feb file. Should end in ".feb"

        Returns
        -------
        None
        """
        with open(filepath, "wb") as out_file:
            xmltodict.unparse(self.to_dict(), out_file, pretty=True)
