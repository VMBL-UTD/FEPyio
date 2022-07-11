from enum import Enum


class FebEnum(Enum):
    """Feb Enumeration

    Methods
    -------
    get_value() : Generic get value. Can be overwritten.
    """

    def get_value(self):
        """Generic get value. Can be overrwritten."""
        return self.value
