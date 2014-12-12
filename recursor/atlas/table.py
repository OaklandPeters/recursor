"""
Subvariety of atlas ~ slotted atlas: ~tuple of named tuples, ~Table.
Also with index support (in SQL sense).
(… would structs be more efficient than tuples?)
"""
from atlas import Atlas


class Table(Atlas):
    pass
