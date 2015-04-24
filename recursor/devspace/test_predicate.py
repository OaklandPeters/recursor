from predicate_idea import Predicate, PredicateInterface
import pdb
from abc import abstractmethod

#max_depth = Predicate(lambda current, path: len(path) < 10)

class Gaurdian(PredicateInterface):
    @abstractmethod
    def checker(self, current, path):
        # ... defined correct signature for child classes
        return NotImplemented


class MaxDepth(Gaurdian):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def checker(self, current, path):
        return len(path) < self.max_depth
        

class HasAttr(Gaurdian):
    def __init__(self, name):
        self.name = name

    def checker(self, current, path):
        return hasattr(current, self.name)



def test_it():

    current = dict
    path = ('one', 'two', 'three', 'four', 'five')
    _apply = lambda func: func(current, path)


    md3 = MaxDepth(3)
    md6 = MaxDepth(6)

    hadict = HasAttr('__dict__')
    habing = HasAttr('bing')

    result1 = _apply(md3)  # _apply(MaxDepth(3))
    result2 = _apply(md6) # _apply(MaxDepth(6))
    resultd = _apply(hadict)
    resultb = _apply(habing)

    both_true = _apply(HasAttr('__dict__') & MaxDepth(6))
    both_false = _apply(HasAttr('__dict__') & MaxDepth(3))

    not_hadict = _apply(~hadict)

    print()
    print("result1:", type(result1), result1)
    print("result2:", type(result2), result2)
    print("resultd:", type(resultd), resultd)
    print("resultb:", type(resultb), resultb)
    print("both_true:", type(both_true), both_true)
    print("both_false:", type(both_false), both_false)
    print("not_hadict:", type(not_hadict), not_hadict)
    print()
    pdb.set_trace()
    print()



if __name__ == "__main__":
    test_it()

