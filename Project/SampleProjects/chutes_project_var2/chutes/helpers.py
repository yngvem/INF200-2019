# -*- coding: utf-8 -*-

"""
This module provides auxiliary functions for use in Chutes & Ladders projects.
"""

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


def type_to_name(data):
    """
    Returns data with all type objects in data replaced by __name__ strings.

    Recursively inspect all elements in data and replace those that are
    instances of type with their __name__ string.

    :Note: Inspects list, tuple and dict only.
    """

    if isinstance(data, list):
        return [type_to_name(elem) for elem in data]
    elif isinstance(data, tuple):
        return tuple(type_to_name(elem) for elem in data)
    elif isinstance(data, dict):
        return {type_to_name(key): type_to_name(val)
                for key, val in data.items()}
    elif isinstance(data, type):
        return data.__name__
    else:
        return data
