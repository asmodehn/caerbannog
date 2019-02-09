# 02 Composed Tootle

Inspired by the step by step introduction to functional programming by [Scott Wlaschin' NDC 2017 talk](https://www.youtube.com/watch?v=AG3KuqDbmhM)

The Object Oriented with delegation code Architecture
In modern/latest Python (3.6), with a touch of interactivity and a focus on correctness.

This is a set of modules as code example, these python modules are made to run here, together, by starting : 
`python __main__.py`

This is not intended to be a package, as to not over-complicate or hide the point.
The tests have also been kept minimal.

## Contents

- `cmd.py` : A basic interpreter for turtle commands. Can interpret multiple commands at once. EOF (Ctrl-D) to exit.
- `real.py` : A "real" turtle (for us it is the graphical display, that we treat as side-effects).
- `sim.py` : A simulated turtle (to compare with reality, before and after we launch a turtle command).
             It is also the client/user of the State module, used to illustrate the various points regarding code architecture made in the talk.
- `state.py` : A data structure representing the turtle state, that we will use in code.
- `utils.py` : misc. small useful stuff.

## TODO : 
- explode the code in multiple modules.
-...
- docs and doctests
- sphinx doc generation
- allow interactive tests from webpage (??)