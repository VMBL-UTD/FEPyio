from typing import TypeVar, Union

T = TypeVar("T")


def unlist(listable: Union[T, list[T], tuple[T]]) -> Union[T, list[T], tuple[T]]:
    """Convert a list or tuple of length 1 to a single item, otherwise pass.

    Examples
    --------
    >>> unlist([1, 2, 3])
    [1, 2, 3]
    >>> unlist([1])
    1
    >>> unlist((1, 2, 3))
    (1, 2, 3)
    >>> unlist((1,))
    1
    >>> unlist(1)
    1
    """
    if isinstance(listable, (list, tuple)) and len(listable) == 1:
        return listable[0]
    else:
        return listable


if __name__ == "__main__":
    import doctest

    doctest.testmod()
