Object Oriented Turtle
======================

Data and behavior are combined into one object.
Client calls a turtle class instance. Turtle class needs to keep track of the Turtle 'State'.

The state is defined here for simplicity as (position, angle, pen's state - up or down).

In this design, the turtle class holds the turtle state and mutates it.
This makes it quite simple to wrap the python turtle API and even "extend" it.

Our tootle class has a few methods :
- move(distance)
- left(angle)
- right(angle)
- penup()
- pendown()

Side note : we use pint for unit of measure (radians / degrees)

Client code
-----------

The client code is quite simple.
We create a Tootle instance named 'tt'

.. literalinclude:: ../01/client.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  6-8
   :emphasize-lines: 7

And we call Tootle's methods to draw a triangle

.. literalinclude:: ../01/client.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  6-14
   :emphasize-lines: 10-14


Tootle code
-----------

The tootle code is usual object oriented code

We use an enum for the two possible penstate values, as well as having penstate as a type.


.. literalinclude:: ../01/tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  9-12
   :emphasize-lines: 10


We also have a Tootle class, wrapping the existing python Turtle class.
It exposes the state as members of this class.


.. literalinclude:: ../01/tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  15-52
   :emphasize-lines: 26-37

It also provides methods matching our API, that are used to mutate the state (via the python Turtle instance).


.. literalinclude:: ../01/tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  15-52
   :emphasize-lines: 38-52

Notice also how the code uses docstrings and doctests to certify the documentation stays uptodate.

If you know python, this code should have no mystery for you.


Tootle test
-----------

Since we want our code to work, we need to test it.

First we do not want to display a graphical "TurtleScreen" everytime we run a test.
This is quite tricky to do, and for now we will rely on a monkey patch.
TODO

Then we define our test class, using the unittest core library


.. literalinclude:: ../01/test_tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  15-52
   :emphasize-lines: 38-52


You can notice how we have a few 'check_' functions that verify the behavior of a Turtle method for a specific parameter.


.. literalinclude:: ../01/test_tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  15-52
   :emphasize-lines: 38-52

Then we have a few 'test_method' that actually run these checks for a larger number of parameters.
It helps us have a better coverage of the data space.


.. literalinclude:: ../01/test_tootle.py
   :encoding: utf-8
   :language: python
   :caption:
   :linenos:
   :lines:  15-52
   :emphasize-lines: 38-52

Despite these efforts to test our turtle, there are many cases that we did not consider.
For example :
- We test only from the initial turtle state, but what if the method behavior depends on the turtle state ?
- We test only a very small set of possible values, what is the method behavior is different for some untested value ?
- How will be the behavior for "unexpected" inputs ? Will it crash ? throw and exception ? which one ? We do not test the unexpected (obviously)

These are the current limitation of basic python tests. We will attempt to improve our test coverage in the following chapters.

Conclusion
----------


Pros:

- Familiar for most python programmers.

Cons :

- Stateful. Hard to test methods independently from the state.
- Inheritance effectively provides a blackbox, that can be hard to setup for tests.
- Cannot compose between method calls, we have to actually do one behavior at a time.
- Hard coded dependencies in module, the client needs to bring in everything.

API
---

:doc:`API/object_oriented_turtle`