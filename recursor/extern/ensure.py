import collections


# ==============================================================================
#    Utility Functions
# ==============================================================================
def _ensure_tuple(obj):
    """Ensure that object is a tuple, or is wrapped in one.
    Also handles some special cases.
    Tuples are unchanged; NonStringSequences and Iterators are converted into
    a tuple containing the same elements; all others are wrapped by a tuple.
    """
    # Tuples - unchanged
    if isinstance(obj, tuple):
        return obj
    # Sequences - convert to tuple containing same elements.
    elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
        return tuple(obj)
    # Iterators & Generators - consume into a tuple
    elif isinstance(obj, collections.Iterator):
        return tuple(obj)
    # Other Iterables, Strings, and non-Iterables - wrap in iterable first
    else:
        return tuple([obj])
