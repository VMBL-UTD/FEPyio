from typing import Optional, Union, overload


class ArrayShapeError(Exception):
    """Exception raised for unexpected array shapes.

    Default Message::

    "Expected shape {expected_shape} for '{array_name}', but got {array_shape}{extra}."

    Attributes
    ----------
    array_name : str
        Name of array.
    array_shape : str, int, or tuple of (int, ...)
        Actual (incorrect) array shape.
    expected_shape : str, int, or tuple of (int, ...)
        Expected shape.
    """

    @overload
    def __init__(
        self,
        array_name: str,
        array_shape: Union[str, int, tuple[int, ...]],
        expected_shape: Union[str, int, tuple[int, ...]],
        *,
        message: Optional[str] = None,
        extra: Optional[str] = None,
        **kwargs,
    ):
        """Exception raised for unexpected array shapes.

        Default Message:
            "Expected shape {expected_shape} for '{array_name}', but got {array_shape}."

        Parameters
        ----------
        array_name : str
            Name of the array.
        array_shape : str, int, or tuple of (int, ...)
            Actual (incorrect) array shape.
        expected_shape : str, int, or tuple of (int, ...)
            Expected array shape.
        message : str
            Message to be displayed. Formatted with class properties. See above for
            default message. Keyword-only parameter.
        extra : str, optional
            Extra string to include between '{array_shape}' and '.' in `message`.
            Keyword-only parameter.
        **kwargs : dict, optional
            Arbitrary keyword arguments.

        Examples
        --------
        >>> raise ArrayShapeError('my_array', (2,3), (3,))
        ArrayShapeError: Expected shape (2, 3) for 'my_array', but got (3,).
        >>> raise ArrayShapeError('my_array', '(2,3)', '(3,)')
        ArrayShapeError: Expected shape (2, 3) for 'my_array', but got (3,).
        """

    @overload
    def __init__(
        self,
        array_name: None = None,
        array_shape: None = None,
        expected_shape: None = None,
        *,
        message: str = "",
        extra: Optional[str] = None,
        **kwargs,
    ):
        """Exception raised for unexpected array shapes.

        Parameters
        ----------
        message : str
            Message to be displayed. Formatted with class properties. Keyword-only
            parameter.
        **kwargs : dict, optional
            Arbitrary keyword arguments.
        """

    def __init__(
        self,
        array_name=None,
        array_shape=None,
        expected_shape=None,
        *,
        message=None,
        extra=None,
        **kwargs,
    ):
        self.array_name = array_name
        self.array_shape = array_shape
        self.expected_shape = expected_shape
        self.message = (
            message
            if message is not None
            else "Expected shape {expected_shape} for '{array_name}', but got {array_shape}{extra}."
        )
        self.extra = extra or ""

        if kwargs:
            self.__dict__.update(kwargs)

    def __str__(self):
        return self.message.format(**self.__dict__)


class UnknownMaterialError(Exception):
    ...
