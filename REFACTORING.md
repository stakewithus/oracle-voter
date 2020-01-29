# Guidelines

## Anti-Patterns

1. Functions that should be objects
   - Similar arguments across functions
   - Mix of mutable and immutable functions
   - Functions spread across multiple python files

2. Objects that should be functions
   - Classes with 1 method (other than __init__())
   - Classes that contain only static methods

3. Converting "Triangular" Code to Flat Code
   - Too much nesting (Mountainous Code)
   - Flat is better than nested, Tim Peters, Zen Of Python
   - Use "returning early" remove level of nesting
   - Use List Comprehensions
   - Use itertools package for non-single dimension lists

4. Handling Complex Dictionaries with Query Tools

   - Used to deal with nested dictionaries
   - Use `jmespath`, provides query language for Python Dictionaries

5. Use `attrs` and `dataclasses` to reduce code
   - Provide `__repr__` and `__str__` methods for boilerplate code.
   - Use `@property` decorator.
   - Python typing with `import typing`
   - Python Data Classes provide fields to class attributes with type annotations.`@dataclass`, `from dataclasses import dataclass`
