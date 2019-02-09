# 01 Tootle

Inspired by the step by step introduction to functional programming by [Scott Wlaschin' NDC 2017 talk](https://www.youtube.com/watch?v=AG3KuqDbmhM)

The traditional Object Oriented / Inheritance-based code Architecture
In modern/latest Python (3.6), with a touch of interactivity and a focus on correctness.

This is a python package as code example, meant to be run by starting : 
`python -m tootle`

Note the virtual environment should be setup previously, from this directory, by running :
`pipenv shell`.
This folder also supports direnv to setup the environment, as soon as you `cd` into it.

This is not intended to be distributed, since python requires more boilerplate for this, and we do not want to over-complicate or hide the point.

## Contents

- `tootle.uif.repl` : A basic interpreter for turtle commands. Interprets one command at a time. EOF (Ctrl-D) to exit.
- `tootle.uif.real` : A "real" turtle (for us it is the graphical display, that we treat as side-effects)
- `tootle.sim` : A simulated turtle (to compare with reality, before and after we launch a turtle command).
        It is also the client/user of the State module, used to illustrate the various points regarding code architecture made in the talk.
- `tootle.state` : A data structure representing the turtle state, that we will manipulate in code.
- `tootle.utils` : misc. small useful stuff.
- `tootle.__init__` : module used to mark these modules as a package. Effectively the "programming API" of the package.
- `tootle.__main__` : modules used to make this package as runnable. Effectively the "user API" of the package, and usually where the command line code lives.

## TODO : 
- docs and doctests
- sphinx doc generation
- allow interactive tests from webpage (??)