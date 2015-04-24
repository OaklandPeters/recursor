Core: walk()
=================
- Most important single function
- an iterator for recursive structures (ex. trees)
- Probably several forms are useful, simple VS rigorous
- Simple forms:
    - walk_items:
    - walk_attrs:
- Rigorous and complex:
    - walker(root, path, history, iterator, gaurd)
    - Maybe good as a class


Predicate
============
- Translate this into a Mixin for FunctionalLogical
- Simple version
    - One mixin to add logical operators:
        - __or__, __and__, __invert__
    - A seperate class (created by those operators)
        - class Logical()  ~ Predicate
            - can somehow map/iter over its components (left/right)
            - should be variadic (not just left/right)
        - Similar to previous attempts at FunctionalLogical
            - But I want it simpler, more functional (use closures for simplicity)
