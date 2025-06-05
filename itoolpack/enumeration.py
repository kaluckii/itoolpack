from enum import Enum
from typing import List, Dict, Any


class Enumeration:
    _ATTR_FILTER_PREFIX = "_"

    def __class_getitem__(cls, item):
        """
        Enables dictionary-style access to the class attributes
        excluding those starting with the filter prefix.

        Example:
            MyEnum['SOME_KEY'] → returns corresponding value
        """

        return cls._get_child_dict()[item]

    @classmethod
    def _get_child_dict(cls):
        """
        Retrieves all class attributes that do not start with the filter prefix.

        :return: Dictionary of class attribute name-value pairs.
        """

        return {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith(cls._ATTR_FILTER_PREFIX)
        }

    @classmethod
    def get_all_values(cls) -> List:
        """
        Returns a list of all values of the class attributes,
        excluding those that start with the filter prefix.

        :return: List of attribute values.
        """

        return list(cls._get_child_dict().values())

    @classmethod
    def values_to_dict(cls) -> Dict[Any, Any]:
        """
        Returns a dictionary of class attributes excluding private ones.

        :return: Dictionary of attribute names and their corresponding values.
        """

        return cls._get_child_dict()

    @classmethod
    def to_enum(cls) -> type[Enum]:
        """
        Converts the class into a Python Enum using the filtered attributes.

        :return: Enum type constructed from the class attributes.
        """

        members_dict = cls._get_child_dict()
        return Enum(cls.__name__, members_dict)
