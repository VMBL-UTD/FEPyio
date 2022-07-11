"""
Convert key prefixes between underscores (valid python attributes) and key prefixes used
by the xmltodict library for properties.

Example:
    For xml:
        <node id="1", type="fixed">0.7, 3.0</node>

    +-----------+----------+------------+
    | xmltodict |  python  |    value   |
    +===========+==========+============+
    |     "@id" |    "_id" |          1 |
    +-----------+----------+------------+
    |   "@type" |  "_type" |    "fixed" |
    +-----------+----------+------------+
    |   "#text" | "__text" | "0.7, 3.0" |
    +-----------+----------+------------+
"""


def prop_to_xml(key: str) -> str:
    """Convert prefix of a key in python property syntax to xmltodict syntax.

    Convert names according to:

    - _id    -> @id
    - __text -> #text
    - value  -> value

    Args
    ----
    key : str
        Key to be converted

    Returns
    -------
    str
        Key with new predix

    Example
    -------
    >>> prop_to_xml('_id')
    '@id'
    >>> prop_to_xml('__text')
    '#text'
    >>> prop_to_xml('value')
    'value'
    """
    if key.startswith("__"):
        return key.replace("__", "#", 1)
    elif key.startswith("_"):
        return key.replace("_", "@", 1)
    else:
        return key


def xml_to_prop(key: str) -> str:
    """Convert prefix of a key in xmltodict syntax to python property.

    Converts names according to:
    - @id   -> _id
    - #text -> __text
    - value -> value

    Parameters
    ----------
    key : str
        Key to be converted

    Returns
    -------
    str
        Key with new predix

    Example
    -------
    >>> prop_to_xml('_id')
    '@id'
    >>> prop_to_xml('__text')
    '#text'
    >>> prop_to_xml('value')
    'value'
    """
    if key.startswith("#"):
        return key.replace("#", "__", 1)
    elif key.startswith("@"):
        return key.replace("@", "_", 1)
    else:
        return key


if __name__ == "__main__":
    import doctest

    doctest.testmod()
