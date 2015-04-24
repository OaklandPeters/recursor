"""

PROBLEM:
This doesn't allow the gaurdian functions to be specified clearly.
"""

# Desired syntax




walker(obj, gaurd=lambda current, path: len(path) < 10 and hasattr(current, '__dict__'))


def walker(obj, path=None):
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
