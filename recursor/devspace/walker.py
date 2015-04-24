"""
Notes on the rigorous, complex, class-ish version of a recursive iterator,
which generalizes across iter, item, and attr -getter versions.

@todo: To allow gaurd functions to work, they will have to be able to get
    paths (~keys) AND histories (~values). This can done either by storing
    the history (simple but space inefficient), or providing a getter
    (getter(path) == history; complex but space efficient).


Typedefs:

    CurrentType = Any
    PathType = Tuple[Any]
    GaurdianType = Callable[[CurrentType, PathType], bool]
"""
from abc import abstractproperty, abstractmethod, ABCMeta
from collections import Callable, Iterator


class GaurdianType(Callable):
    """
    Functions that 
    GaurdianType = Callable[[CurrentType, PathType], bool]
    """


class WalkerInterface(object):


class Walker(object):
    """
    @todo: Make inherit from Iterator
    """
    def __init__(self, root,
        path=None,
        history=None,
        iterator=iter,
        gaurd=):
        pass

class WalkerInterface(object):
    pass

class ItemWalker(Walker):
    pass

class AttributeWalker(Walker):
    pass

class IterWalker(Walker):
    pass

 Walker(root, path=None, history=None)




def attr_walker(obj, path=None):
    if path is None:
        path = tuple()
    elif isinstance(path, tuple):
        yield path
    else:
        path = tuple([path])
        yield path
    if len(path) >= 10:
        return
    if not hasattr(obj, '__dict__'):
        return
    for key, value in vars(obj).items():
        for _path in walker(value, path=path+(key,)):
            yield _path
