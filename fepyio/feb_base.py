"""
Contains base classes for FEB module
"""
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any

from fepyio.utils.dict_utils import prune_dict, unlist_dict
from fepyio.utils.xmltodict_key_converter import prop_to_xml


@dataclass
class FebBase:
    """Base class for FEBio spec objects.

    Attributes
    ----------
    _key : str
        Name to use for class

    Methods
    -------
    to_dict()
        Get the class as a dict from fields.
    _convert_key(key: str)
        Convert an internal field name to key for dictionary. Can be overwritten to
        change key names while maintaining default to_dict().
    """

    @property
    def _key(self) -> str:
        """Return key used for class name. Defaults to class name."""
        return self.__class__.__name__

    def _convert_key(self, key: str) -> str:
        return prop_to_xml(key)

    def to_dict(self) -> dict:
        """Get class as dictionary."""
        _dict: dict = {}

        def _to_dict(value) -> tuple[str, Any]:
            # If the field value is another FebBase object, recursively get dictionary.
            # Additionally, we want to use the FebBase's key instead of whatever the
            # parent has called it
            if isinstance(value, FebBase):
                return (self._convert_key(value._key), value.to_dict())

            else:
                # Convert field name to xmltodict-compatible name
                return (self._convert_key(field.name), value)

        for field in fields(self):
            # Skip '_key' field
            if field.name == "_key":
                continue

            field_val = getattr(self, field.name)

            # Skip empty fields
            if field_val is None:
                continue

            if isinstance(field_val, list):
                # Add each element of list to the dictionary
                _dict[self._convert_key(field.name)] = [
                    _to_dict(value)[1] for value in field_val
                ]
            elif isinstance(field_val, FebEnum):
                # Extract enum value
                _dict[self._convert_key(field.name)] = field_val.get_value()
            else:
                key, value = _to_dict(field_val)
                _dict[key] = value

        return prune_dict(unlist_dict(_dict), prune_empty_iterables=True)


class FebEnum(Enum):
    """Feb Enumeration

    Methods
    -------
    get_value() : Generic get value. Can be overwritten.
    """

    def get_value(self):
        """Generic get value. Can be overrwritten."""
        return self.value
