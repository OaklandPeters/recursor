"""


Desired syntax:

    gaurdian = MaxDepth(10) & HasAttr('__dict__')

    if gaurdian(current, path):
        # ....

    walker(obj, gaurd=MaxDepth(10) & HasAttr('__dict__'))



@note: I put example wrapper decorators at the bottom.
@todo: Come up with simple-ish logical structure alternative to the wrapper decorators
    ... the point is that they be iterable/viewable AND callable
    @todo: ~a partial application class that lets you iterate over the arguments
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Callable





class PredicateInterface(Callable):
    __metaclass__ = ABCMeta
    # def __init__(self, checker):
    #     assert isinstance(checker, Callable)
    #     self.checker = checker

    @abstractmethod
    def checker(self):
        return NotImplemented

    def __call__(self, *args, **kwargs):
        return self.checker(*args, **kwargs)

    def __or__(self, other):
        assert isinstance(other, Callable)
        # replace this inner function with a wrapper
        call_or = lambda *args, **kwargs: self(*args, **kwargs) | other(*args, **kwargs)
        # def call_or(*args, **kwargs):
        #     return self(*args, **kwargs) | other(*args, **kwargs)
        
        return Predicate(call_or)

    def __and__(self, other):
        assert isinstance(other, Callable)

        call_and = lambda *args, **kwargs: self(*args, **kwargs) & other(*args, **kwargs)
        #  ... I don't think the lambda binds the closure properly, so have to use a function....
        # def call_and(*args, **kwargs):
        #     return self(*args, **kwargs) & other(*args, **kwargs)

        return Predicate(call_and)

    def __invert__(self):
        call_not = lambda *args, **kwargs: not self(*args, **kwargs)
        return Predicate(call_not)

class Predicate(PredicateInterface):
    def __init__(self, checker):
        assert isinstance(checker, Callable)
        self._checker = checker

    def checker(self, *args, **kwargs):
        return self._checker(*args, **kwargs)






# wrapping these is slightly inferior to a logic tree structure
# ... since I can't view the structure without calling it
def wrap_or(left, right):
    def call_or(*args, **kwargs):
        return left(*args, **kwargs) | right(*args, **kwargs)
    call_or.__iter__ = iter([left, right])
    return call_or

def wrap_and(left, right):
    def call_and(*args, **kwargs):
        return left(*args, **kwargs) & right(*args, **kwargs)
    call_and.__iter__ = iter([left, right])
    return call_and
