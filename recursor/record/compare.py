"""
Used to make recursive comparisons, such as for nested Mappings.

Note: This is what made for distribution independently from the general
'record' package. Hence, it will be redundant, and needs to be cleaned up.

@todo: Integrate with record package.
@todo: Remove redundant parts
@todo: Import Record/DiscreteRecord classes from elsewhere.

"""
import collections
import abc



def record_equal(recA, recB):
    pathsA = list(rec_paths(recA))
    pathsB = list(rec_paths(recB))
    for path in set(pathsA+pathsB):
        try:
            elmA = get(recA, path)
        except LookupError:
            return False
        try:
            elmB = get(recB, path)
        except LookupError:
            return False

        isA = isinstance(elmA, DiscreteRecord)
        isB = isinstance(elmB, DiscreteRecord)
        if isA and isB:
            if not record_equal(elmA, elmB):  #recurse...
                return False
            else:
                continue
        elif isA and not isB:
            return False
        elif not isA and isB:
            return False
        else:
            if elmA != elmB:
                return False
            else:
                continue


def rec_compare(record_a, record_b):
    """
    One-way recursive comparison of two Records.
    @type: record_a: Record
    @type: record_b: Record
    @rtype: bool
    """
    for path in rec_paths(record_a):  # terminal paths in record_a
        elm_a = get(record_a, path)
        try:
            elm_b = get(record_b, path)
        except LookupError:
            return False

        if elm_a != elm_b:
            return False
    return True


def rec_eq(record_a, record_b):
    """
    Binary recursive comparison of two Records.
    @type: record_a: Record
    @type: record_b: Record
    @rtype: bool
    """
    if rec_compare(record_a, record_b):
        if rec_compare(record_b, record_a):
            return True
    # Fallthrough
    return False







def rec_iter(record):
    """
    @type: record: Record[Any, Any]
    @rtype: Iterator[Tuple[Sequence[Any], Any]]
    """
    path = tuple()
    history = set()

    return _rec_iter(record, path, history)

def _rec_iter(obj, path, history):
    """
    @type: obj: Record[Any, Any]
    @type: path: Tuple[Any]
    @type: history: Set[Any]
    @rtype: Iterator[Tuple[Sequence[Any], Any]]

    @todo: Fix problem: rec_iter is returning incorrect obj, but correct paths
    """
    if isinstance(obj, DiscreteRecord):
        iterator = pairs(obj)
        identity = id(obj)

        if identity not in history:
            history.add(identity)
            for index, elm in iterator:
                for result in _rec_iter(elm, path+(index, ), history):
                    yield result
            history.remove(identity)
        # else... terminate branch and return nothing
    else:
        yield path, obj

def rec_paths(record):
    """
    Retreive terminal paths only (not elements).
    Terminal paths lead to non-DiscreteRecords
    """
    for path, _ in rec_iter(record):
        yield path





#==============================================================================
#    Local Utility Functions
#==============================================================================
class NotPassed(object):
    """
    Local alternative to None; used when 'None' might be
    passed in on a parameter.
    """
    pass

def iterget(record, indexes, default=NotPassed):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @type: default: Optional[Any]
    @rtype: Iterator[Any]
    """
    indexes = _ensure_tuple(indexes)
    yielded = False
    for index in indexes:
        try:
            yield record[index]
            yielded = True
        except (LookupError, TypeError):
            pass
    if not yielded:
        if default is NotPassed:
            raise LookupError(str.format(
                "Indexes not found: {0}",
                ", ".join(repr(index) for index in indexes)
            ))
        else:
            yield default

def get(record, indexes, default=NotPassed):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @type: default: Optional[Any]
    @rtype: Any
    """
    return _first(iterget(record, indexes, default))

def pairs(record):
    """
    Generalization of Mapping.items().
    @type: record: Record[Any, Any]
    @rtype: Iterator[Tuple[Any, Any]]
    @raises: TypeError
    """
    if isinstance(record, collections.Mapping):
        if hasattr(record, 'items'):
            return iter(record.items())
        else:
            return iter(collections.Mapping.items(record))
    elif isinstance(record, collections.Sequence) and not isinstance(record, basestring):
        return enumerate(record)
    else:
        raise TypeError(str.format(
            "'record' should be a Mapping or Sequence, not {0}.",
            type(record).__name__
        ))

class Record(object):
    """
    Root ABC for all record-types. Record types generalizes Sequence and Mapping,
    representing item-containing objects.

    @todo Add Mixins
    """
    __metaclass__ = abc.ABCMeta
    __getitem__ = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Record:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented


class Discrete(collections.Sized, collections.Iterable):
    """
    ABC for collections of finite size, which are iterable. Intended to be used
    with

    IE has abstract methods: __len__, __iter__
    """
    __metaclass__ = abc.ABCMeta
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Discrete:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented


class DiscreteRecord(Record, Discrete):
    """
    Finite and iterable Record. Importantly, strings are Records but not DiscrteRecords.

    Quandry: Should DiscreteRecord inherit from Container?
        Context: Sequence, Set, and Mapping inherit from Sized, Iterable, and Container.
    """
    __metaclass__ = abc.ABCMeta
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is DiscreteRecord:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented


def _ensure_tuple(obj):
    """Ensure that object is a tuple, or is wrapped in one.
    Also handles some special cases.
    Tuples are unchanged; NonStringSequences and Iterators are converted into
    a tuple containing the same elements; all others are wrapped by a tuple.
    """
    #Tuples - unchanged
    if isinstance(obj, tuple):
        return obj
    #Sequences - convert to tuple containing same elements.
    elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
        return tuple(obj)
    #Iterators & Generators - consume into a tuple
    elif isinstance(obj, collections.Iterator):
        return tuple(obj)
    #Other Iterables, Strings, and non-Iterables - wrap in iterable first
    else:
        return tuple([obj])


def _first(iterable):
    """
    @type: iterable: Iterable[Any]
    @rtype: Any
    """
    return iter(iterable).next()

def _hasattr(subklass, attr):
    """Determine if subklass, or any ancestor class, has an attribute.
    Copied shamelessly from the abc portion of collections.py.
    """
    try:
        return any(attr in B.__dict__ for B in subklass.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(subklass, attr)

def _meets(obj, abstract):
    """Determines if an object meets an abstract interface (from abc module)."""
    return all(
        _hasattr(obj, attr) for attr in abstract.__abstractmethods__
    )


if __name__ == "__main__":
    #  Unit tests of the compare.py file - not specifically related to 'cdsparser'
    import unittest

    dicta = {'a':1, 'b':2}
    dictb = {'a':1, 'b':2}
    dictc = {'a':1, 'b':'2'}
    lista = [1, 2]
    listb = ['a','b']
    listc = [('a',1), ('b',2)]
    listd = [2, 1]
    liste = (1, 2)

    nesta = {'a':(1, 2), 'b':3}
    nestb = {'b':3, 'a':(1, 2)}
    nestc = {0:(1, 2), 1:3}
    nestd = [(1, 2), 3]

    rec_eq(nesta, nestb)

    class RecursionTests(unittest.TestCase):
        def test_rec_eq(self):
            self.assertTrue(rec_eq(dicta, dictb))
            self.assertFalse(rec_eq(dicta, dictc))
            self.assertFalse(rec_eq(dicta, lista))
            self.assertFalse(rec_eq(dicta, listb))
            self.assertFalse(rec_eq(dicta, listc))
            self.assertFalse(rec_eq(dicta, listd))
            self.assertFalse(rec_eq(dicta, liste))

            self.assertFalse(rec_eq(dictb, dictc))
            self.assertFalse(rec_eq(dictb, lista))
            self.assertFalse(rec_eq(dictb, listb))
            self.assertFalse(rec_eq(dictb, listc))
            self.assertFalse(rec_eq(dictb, listd))
            self.assertFalse(rec_eq(dictb, liste))

            self.assertFalse(rec_eq(dictc, lista))
            self.assertFalse(rec_eq(dictc, listb))
            self.assertFalse(rec_eq(dictc, listc))
            self.assertFalse(rec_eq(dictc, listd))
            self.assertFalse(rec_eq(dictc, liste))

            self.assertFalse(rec_eq(lista, listb))
            self.assertFalse(rec_eq(lista, listc))
            self.assertFalse(rec_eq(lista, listd))
            self.assertTrue(rec_eq(lista, liste))

            self.assertFalse(rec_eq(listb, listc))
            self.assertFalse(rec_eq(listb, listd))
            self.assertFalse(rec_eq(listb, liste))

            self.assertFalse(rec_eq(listc, listd))
            self.assertFalse(rec_eq(listc, liste))

            self.assertFalse(rec_eq(listd, liste))

        def test_rec_eq_nested(self):
            self.assertTrue(rec_eq(nesta, nestb))
            self.assertFalse(rec_eq(nesta, nestc))
            self.assertFalse(rec_eq(nesta, nestd))
            
            self.assertFalse(rec_eq(nestb, nestc))
            self.assertFalse(rec_eq(nestb, nestd))

            self.assertTrue(rec_eq(nestc, nestd))


    unittest.main()
