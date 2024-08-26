# Typeoverride

Small Python typechess toy project.

Imagine this situation: you want to write an integration library that allows optional schema specification but that would still work and typecheck even if schema is not specified. You want this in a nutshell:

```python
value1 = function(arg)  # value1 is of type dict[str, Any]
value2 = function[Schema](arg)  # value2 is of type Schema
```

Or even this:

```python
value1 = client.call(arg)  # value1 is of type dict[str, Any]
value2 = client.call[Schema](arg)  # value2 is of type Schema
```

Fear not, it is now totally possible thanks to Python's `typing` module (and a bit of descriptors). 
