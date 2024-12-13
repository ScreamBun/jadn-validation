import copy
from typing import Any, MutableMapping


# TODO: **** Replace.....  dict should be good enough.....
# *** Warning.... old src code copy

def immutable(*args, **kwargs) -> None:
    """
    Raise an error for an attempt to alter the FrozenDict
    :param args: positional args
    :param kwargs: key/value args
    :raise TypeError
    """
    raise TypeError('cannot change object - object is immutable')

class ObjectDict(dict):
    """
    Dictionary that acts like an object
    ```python
    d = ObjectDict()

    d['key'] = 'value'
        SAME AS
    d.key = 'value'
    ```
    """
    def __init__(self, seq: MutableMapping = None, **kwargs):
        """
        Initialize an ObjectDict
        :param args: positional parameters
        :param kwargs: key/value parameters
        """
        cls = self.__class__
        data = dict(seq or {}, **kwargs)
        for k, v in data.items():
            if isinstance(v, dict) and not isinstance(v, cls):
                data[k] = cls(v)
            elif isinstance(v, (list, tuple)):
                data[k] = tuple(cls(i) if isinstance(i, dict) else i for i in v)
        super().__init__(data)

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict):
            value = self.__class__(value)  # if len(value.keys()) > 0 else self.__class__()
        super().__setitem__(key, value)

    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__
    __delattr__ = dict.__delitem__

    def __copy__(self):
        cls = self.__class__
        return cls(copy.copy(dict(self)))

    def __deepcopy__(self, memo):
        cls = self.__class__
        return cls(copy.deepcopy(dict(self)))

    def update(self, seq: MutableMapping = None, **kwargs) -> None:
        """Updates the dictionary with the specified key-value pairs"""
        data = dict(seq or {}, **kwargs)
        for k, v in data.items():
            if isinstance(v, dict) and not isinstance(v, self.__class__):
                data[k] = self.__class__(v)
            elif isinstance(v, (list, tuple)):
                data[k] = tuple(self.__class__(i) if isinstance(i, dict) else i for i in v)
        super().update(data)

class FrozenDict(ObjectDict):
    """
    Immutable/Frozen dictionary
    The API is the same as `dict`, without methods that can change the
    immutability. In addition, it supports __hash__().
    """
    __slots__ = ("_hash", )
    _hash: hash

    def __hash__(self) -> hash:
        """
        Calculates the hash if all values are hashable
        :raise TypeError: if a value is not hashable
        :return: object hash
        """
        if self._hash is None:
            self._hash = hash(frozenset(self.items()))
        return self._hash

    __setattr__ = immutable
    __setitem__ = immutable
    __delattr__ = immutable
    __delitem__ = immutable
    clear = immutable
    pop = immutable
    popitem = immutable
    update = immutable
    setdefault = immutable

    # Custom functions
    def unfreeze(self) -> dict:
        """
        Convert the 'FrozenDict' to a standard dict with editable values
        :return: standard dict
        """
        rtn = {}
        for k, v in self.items():
            rtn[k] = self._unfreeze(v)

        return rtn

    # Helper functions
    def _unfreeze(self, obj: Any) -> Any:
        if isinstance(obj, self.__class__):
            return obj.unfreeze()
        if isinstance(obj, tuple):
            return [self._unfreeze(i) for i in obj]
        return obj