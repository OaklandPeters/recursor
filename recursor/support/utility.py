"""
This is basically all recursive "paths" related stuff.
It really need a paths set of getters & setters
(and those will be different than itemize's iter_get, get functions)

The recursive versions are best structued in a module like itemize's:
recursor/
    basics.py
        iter_get()
        get()


Core functions are basically just the magic methods on recursive version
of Record
    __iter__
    __getitem__
    __setitem__
    __delitem__

@todo: Turn recursive into its own package, themed on itemize

"""
import recursor.support.basics as basics
from recursor.extern.nulltype import NotPassed


def iter_pairs(record):
    """
    Returns (path, element) for record
    Example use:
    pairs(record, iter_walk)

    @type: record: recursor.record.interfaces.Record
    @returns: tuple
    """
    for path in basics.iter_walk(record):
        yield path, basics.get(record, path)


def iter_find(record, predicate=bool, paths=NotPassed):
    """
    @type: record: interfaces.Record
    @returns:
    """
    for path in basics.iter_walk(record, paths=paths):
        if predicate(basics.get(record, path)):
            yield path
