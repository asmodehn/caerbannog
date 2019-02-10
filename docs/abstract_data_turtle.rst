Abstract Data Turtle
====================


Data is separate from behaviour.

Data structure is mutable, private, and only the turtle functions can change the data
From hte caller point of view it is an opaque data structure

Each function needs the state to be passed in.


.. literalinclude:: ../02/abstle.py
   :encoding: utf-8
   :language: python
   :emphasize-lines: 12,15-18



Pros:

- simple to implement
- cant do inheritance -> forces composition

Cons:

- Stateful/Blackbox/hard to test



Pythonic
--------



API
---

:doc:`API/abstract_data_turtle`