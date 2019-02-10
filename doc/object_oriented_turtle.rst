Object Oriented Turtle
======================

Data and behavior are combined into one object.

Client calls a turtle class instance. Turtle class needs to keep track of the Turtle 'State'.
The turtle state is defined here for simplicity as (position, angle, pen's state - up or down).
The turtle class holds the turtle state and mutates it.

The turtle class has a few methods :
- move(distance)
- left(angle)
- right(angle)
- penup()
- pendown()

Note : we use pint for unit of measure (radians / degrees)




.. literalinclude:: ../01/tootle.py
   :encoding: utf-8
   :language: python
   :emphasize-lines: 12,15-18





Pros:

- Familiar

Cons :

- Stateful/Blackbox/hard to test
- CAnt compose
- Hard coded dependencies

API
---

:doc:`API/object_oriented_turtle`