"""A collection of common Numpy array types.

Includes
--------
NDArrayBool
NDArrayFloat
NDArrayInt
NDArrayIntOrFloat
"""
from typing import Union

import numpy as np
import numpy.typing as npt

# Single reference to numpy int/float types
_np_int = np.int32
_np_float = np.float64

NDArrayBool = npt.NDArray[np.bool_]
"""numpy.ndarray of dtype=np.bool_
"""

NDArrayFloat = npt.NDArray[_np_float]
"""numpy.ndarray of dtype=np.float64
"""

NDArrayInt = npt.NDArray[_np_int]
"""numpy.ndarray of dtype=np.int32
"""

NDArrayIntOrFloat = npt.NDArray[Union[_np_int, _np_float]]
"""numpy.ndarray of dtype=np.int32 or np.float64
"""
