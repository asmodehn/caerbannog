State Monad
===========

State threading behind the scene.


Problem upgrade
---------------

Lets say the turtle cant go after a certain distance.
We need to return the distance actually moved.
-> Passing the state around is complex, and we can't compose easily as before.

Currying
--------

We transform the functions.
Instead of having one two params function, we get two, one-param, function.
We now say that the state is a wrapper around the function returned from a function.





Pythonic
--------





Pure
----




Monadic
-------



Pros:
- looks imperatve but preserve immutability
- functions are still composable

Cons:
- harder to implement and use
