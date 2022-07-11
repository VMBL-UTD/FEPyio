from dataclasses import dataclass
from typing import Optional

from fepyio.typing.listable import Listable
from fepyio.utils.dict_utils import prune_dict
from fepyio.utils.listable_utils import listable_map

from ._base import FebBase, apply_to_dict


@dataclass
class LogData(FebBase):
    """FEBio > Output > LogFile > LogData

    Parameters
    ----------
    data : str
        An expression defining the data that is to be stored.
    file : str
        File name ONLY of the output file where data is stored.
    name : str, optional
        A descriptive name for the data. Default is data expression.
    delim : str, default=" " (space)
        The delimeter used to separate data in multi-column format.
    format : str, optional
        Optional format string. Default is None.

    Attributes
    ----------
    data : str
        An expression defining the data that is to be stored.
    file : str
        File name ONLY of the output file where data is stored.
    name : str, optional
        A descriptive name for the data. Default is data expression.
    delim : str, default=" " (space)
        The delimeter used to separate data in multi-column format.
    format : str, optional
        Optional format string. Default is None.
    _key = "LogData"

    Notes
    -----
    See: [FEBio Manual section 3.18.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.18.1.html).
    """

    data: str
    file: str
    name: Optional[str] = None
    delim: Optional[str] = None
    format: Optional[str] = None

    def _convert_key(self, key: str) -> str:
        return f"@{key}"


@dataclass
class LogFile(FebBase):
    """FEBio > Output > LogFile


    Parameters
    ----------
    file : str
        Full path to log file.
    node_data : Listable of LogData, optional
        Request nodal data.
    face_data : Listable of LogData, optional
        Request surface data.
    element_data : Listable of LogData, optional
        Request element data.
    rigid_body_data : Listable of LogData, optional
        Request rigid body data.

    Attributes
    ----------
    file : str
        Full path to log file.
    node_data : Listable of LogData, optional
        Request nodal data.
    face_data : Listable of LogData, optional
        Request surface data.
    element_data : Listable of LogData, optional
        Request element data.
    rigid_body_data : Listable of LogData, optional
        Request rigid body data.
    _key = "logfile"

    Notes
    -----
    See: [FEBio Manual section 3.18.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.18.1.html).
    """

    file: str
    node_data: Optional[Listable[LogData]] = None
    face_data: Optional[Listable[LogData]] = None
    element_data: Optional[Listable[LogData]] = None
    rigid_body_data: Optional[Listable[LogData]] = None
    _key: str = "logfile"

    def to_dict(self):
        return prune_dict(
            {
                "@file": self.file,
                "node_data": listable_map(apply_to_dict, self.node_data),
                "face_data": listable_map(apply_to_dict, self.face_data),
                "element_data": listable_map(apply_to_dict, self.element_data),
                "rigid_body_data": listable_map(apply_to_dict, self.rigid_body_data),
            }
        )


@dataclass
class Output(FebBase):
    """FEBio > Output

    Defines how FEBio outputs data.

    Parameters
    ----------
    logfiles : Listable of LogFile
        Single or list of LogFile objects.

    Attributes
    ----------
    logfiles : Listable of LogFile
        Single or list of LogFile objects.
    _key = "Output"

    Notes
    -----
    See: [FEBio Manual section 3.18](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.18.html)
    """

    logfiles: Listable[LogFile]

    def _convert_key(self, key: str) -> str:
        return key[:-1] if key.endswith("s") else super()._convert_key(key)
