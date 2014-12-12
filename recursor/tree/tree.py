"""
Branching recursive sequence (~list or tuple like),
except for downward & upward methods:
    .parent, .root, .map, and built-in support for recursion.
History tracking (~paths), support for avoiding loops
DirectoryTree: basic Tree, but __getitem__ populates .data via os.listdir


Core class itself should be an ABC/interface.
Then - a differently named 'hard' implementation should also be provided.
"""
import abc


class Tree(object):
    __metaclass__ = abc.ABCMeta
