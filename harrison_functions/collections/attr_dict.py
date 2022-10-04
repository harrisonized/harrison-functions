from collections import Mapping, MutableSequence

# Objects
# # ConvenienceDict
# # AttrDict


class ConvenienceDict(dict):
    """
    | Provides extra functionality over normal dictionaries:

    #. Enable nested key creation
    #. Access first-layer keys as attributes (and avoid overwriting class methods, like .items())

    .. warning::

       | Accessing keys as attributes currently only works for the first layer
       | If you want to access nested dictionaries using attribute notation, use :py:class:`AttrDict <tython.utils.collections.AttrDict>`.
    """

    def __init__(self, *args, **kwargs):
        """See: https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute"""
        super(ConvenienceDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getitem__(self, item):
        """See: https://stackoverflow.com/questions/2600790/multiple-levels-of-collection-defaultdict-in-python"""
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class AttrDict:
    """
    | A read-only façade for navigating a JSON-like object
    | using attribute notation

    | See: https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

    """

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            return AttrDict.build(self._data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, Mapping):
            return cls(obj)
        elif isinstance(obj, MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
        
    def __repr__(self):
        return self._data.__repr__()
