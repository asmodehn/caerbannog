# functional-python
From Python to Functional Code, follow the white snake.

In modern/latest Python (3.6), with a touch of interactivity and a focus on correctness.

Inspired by the step by step introduction to functional programming by [Scott Wlaschin' NDC 2017 talk](https://www.youtube.com/watch?v=AG3KuqDbmhM)

Along the way we are gathering and reusing useful code in a package on the side...

Overview : 
- A simulated turtle storing the drawing in a list, for easy comparison later (maybe automated ?)
- A turtle state (as per the talk), with live testing (comparison of state and observed reality)
- An interface to the "real" visible turtle ( our link to the python turtle module )
- An interface to an interpreter (python cmd module), used to manipulate the turtle.

Dataflow : 
- Forward : Interpreter ==> Simulation & state ==> Graphics 
- Backward : Always explicit (query turtle's position or attitude)

Along the way we will isolate functional patterns that enable us to : 
- Improve our turtle simulation and our turtle state representation
- Improve how we can do live automated testing
- Improve our interface with the "real" turtle (the python module)
- Improve our interface with the user (our interpreter)

The journey :

- 00_Tootle : the Object Oriented (Interactive) Turtle. Using the inheritance-style interface from python classes.
- 01_ComposedTootle : A Tootle, with composition/delegation, but no inheritance. Repl now support sequence of arguments.
- 02_FunctionalTurtle : A Functional Turtle.
- more to come...



#TODO :
- [ ] somehow make a nice (interactive & visual) webpage of literal programming.
