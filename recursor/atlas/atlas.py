"""
~list of dicts. Common use case.
Sequence with Mapping-like get item support.
__iter__ over sequence though, not keys, and does not have
.keys method (since keys may vary between each element).


Core class itself should be an ABC/interface.
Then - a differently named 'hard' implementation should also be provided.
"""


class Atlas():
    """
    Interface
    """
    pass
