"""
Agentpy Tools Module
Content: Errors, generators, and base classes
"""

from numpy import ndarray


class AgentpyError(Exception):
    pass


def make_none():
    return None


def make_matrix(shape, loc_type=make_none, list_type=list):
    """ Returns a nested list with given shape and class instance. """

    if len(shape) == 1:
        return list_type([loc_type()
                          for _ in range(shape[0])])
    return list_type([make_matrix(shape[1:], loc_type, list_type)
                      for _ in range(shape[0])])


def make_list(element, keep_none=False):
    """ Turns element into a list of itself
    if it is not of type list or tuple. """

    if element is None and not keep_none:
        element = []  # Convert none to empty list
    if not isinstance(element, (list, tuple, ndarray)):
        element = [element]
    elif isinstance(element, tuple):
        element = list(element)

    return element


def param_tuples_to_salib(param_ranges_tuples):
    """ Convert param_ranges to SALib Format """

    param_ranges_salib = {
        'num_vars': len(param_ranges_tuples),
        'names': list(param_ranges_tuples.keys()),
        'bounds': []
    }

    for var_key, var_range in param_ranges_tuples.items():
        param_ranges_salib['bounds'].append([var_range[0], var_range[1]])

    return param_ranges_salib


class AttrDict(dict):
    """ Dictionary where attribute calls are handled like item calls.

    Examples:

        >>> ad = ap.AttrDict()
        >>> ad['a'] = 1
        >>> ad.a
        1

        >>> ad.b = 2
        >>> ad['b']
        2
    """

    def __init__(self, *args, **kwargs):
        if args == (None, ):
            args = ()  # Empty tuple
        super().__init__(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            # Important for pickle to work
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __delattr__(self, item):
        del self[item]

    def __repr__(self):
        return f"AttrDict {super().__repr__()}"

    def _short_repr(self):
        len_ = len(self.keys())
        return f"AttrDict {{{len_} entr{'y' if len_ == 1 else 'ies'}}}"
