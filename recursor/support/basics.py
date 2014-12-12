"""
Core functions for the 'recursor' package.
All are assumed to apply to 'Record' interface objects (same interface as defined in itemize)

Guiding Principles:
(1) Strictness: These should depend ONLY on the 4 core functions of iter, set, get, del


Recursive support functions. ~rec_iter (as from rich_recursion)
Built-in support for History tracking (~paths), support for avoiding loops
Handle recursive getter/setter/deleter as per itemize style
Two functions:
iter_find (return elements matching pattern/predicate
iter_pairs




@todo: ADVANCED: combine these (path compatible) with itemize (chainable/fallback compatible)
"""

import recursor.interfaces as interfaces
import recursor.extern.unroll as unroll
import recursor.shared as shared

class Recursor(interfaces.DiscreteMutableRecord):
	__iter__ = iter_walk
	__getitem__ = getter
	__setitem__ = setter
	__delitem__ = deleter



def iter_walk(record):
	"""Recursive iterator, yielding paths.
	@type: record: interfaces.Record
	@returns: interfaces.Path
	"""
	# This is fairly complicated.
	# I've implemented it before in rich_recursion.py
	# ... but I'm not writing it here at the moment
	yield NotImplemented

def walk(record):
	"""
	@type: record: interfaces.Record
	@returns: list
	"""
	return list(iter_walk(record))



def getter(record, path, default=shared.NotPassed):
	pass

def setter(record, path, value):
	pass

def deleter(record, path):
	pass



# More advanced functions
def find():
	pass
def pairs():
	pass
