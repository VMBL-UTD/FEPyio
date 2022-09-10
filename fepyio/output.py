from dataclasses import dataclass, field
from typing import ClassVar, Optional

from .feb_base import AtNames, FebBase


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

    _at_names: ClassVar[AtNames] = {"data", "file", "name", "delim", "format"}


@dataclass
class LogFile(FebBase):
    """FEBio > Output > LogFile


    Parameters
    ----------
    file : str
        Full path to log file.
    node_data : list of LogData, optional
        Request nodal data.
    face_data : list of LogData, optional
        Request surface data.
    element_data : list of LogData, optional
        Request element data.
    rigid_body_data : list of LogData, optional
        Request rigid body data.

    Attributes
    ----------
    file : str
        Full path to log file.
    node_data : list of LogData, optional
        Request nodal data.
    face_data : list of LogData, optional
        Request surface data.
    element_data : list of LogData, optional
        Request element data.
    rigid_body_data : list of LogData, optional
        Request rigid body data.
    _key = "logfile"

    Notes
    -----
    See: [FEBio Manual section 3.18.1](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.18.1.html).
    """

    file: str
    node_data: list[LogData] = field(default_factory=lambda: [])
    face_data: list[LogData] = field(default_factory=lambda: [])
    element_data: list[LogData] = field(default_factory=lambda: [])
    rigid_body_data: list[LogData] = field(default_factory=lambda: [])
    _key: str = "logfile"
    _at_names: ClassVar[AtNames] = {"file"}


@dataclass
class Output(FebBase):
    """FEBio > Output

    Defines how FEBio outputs data.

    Parameters
    ----------
    logfiles : list of LogFile
        List of LogFile objects.

    Attributes
    ----------
    logfiles : list of LogFile
        List of LogFile objects.
    _key = "Output"

    Notes
    -----
    See: [FEBio Manual section 3.18](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.18.html)
    """

    logfiles: list[LogFile]

    def _convert_key(self, key: str) -> str:
        return key[:-1] if key.endswith("s") else super()._convert_key(key)
