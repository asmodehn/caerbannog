import inspect

import math
import turtle
import cmd
import enum
import logging
import types


# Directly, naively, modeled in python 3.6
# from the code shown in : https://www.youtube.com/watch?v=AG3KuqDbmhM

# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# Code isolated from the side-effects (commands and display)
# Made to look as close as possible from code presented in Scott Wlaschin's NDC talk
# Additionally is serves us as a simulation without relying on any side effects.
#
# note that doing so we already, in a way, separated the "model" from the actual "implementation code".
# We reuse here turtle.Vec2D to get exactly the same code representing the model, and what is actually happening.

class TurtleState:

    # Immutable state
    state = (turtle.Vec2D(0, 0), turtle.Vec2D(1, 0), PenState.DOWN)

    @property
    def position(self):
        return self.state[0]

    @property
    def attitude(self):
        return self.state[1]

    @property
    def penState(self):
        return self.state[2]

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        endPosition = self.position + distance * self.attitude

        # mutating the state(=instance)
        self.state = (endPosition, self.attitude, self.penState)
        return self

    def turn(self, angle: int):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude.rotate(angle), self.penState)
        return self

    def penup(self):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude, PenState.UP)
        return self

    def pendown(self):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude, PenState.DOWN)
        return self

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        # mutating the state(=instance)
        self.state = (turtle.Vec2D(0, 0), turtle.Vec2D(1, 0), self.penState)
        return self


# Note we use a class here like "module" was used in the presentation, to encapsulate code.
# There are other ways to achieve the same goal, for example having separate module for each class used here.
# note that we return self here (the state), which gives us a "fluent API" design.
class SimTurtle:

    state = TurtleState()

    #: the list of lines drawn, as the expected side effect.
    drawing = []

    # no init, just like in the code model

    # delegate attributes
    @property
    def position(self):
        return self.state.position

    @property
    def attitude(self):
        return self.state.attitude

    @property
    def penState(self):
        return self.state.penState
    # Note : using self is how we pass the state(=instance) around in python !

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        oldPosition = self.state.position

        self.state.move(distance)

        if self.state.penState == PenState.DOWN:
            self.drawing.append((oldPosition, self.state.position))

        return self

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.state.turn(angle)

        return self

    def heading(self, state: TurtleState):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(state.attitude[1], state.attitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

    def penup(self):
        logging.info("simulating pen UP")
        self.state.penup()
        return self

    def pendown(self):
        logging.info("simulating pen DOWN")
        self.state.pendown()
        return self

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self.state.home()
        return self

    # No bye, no deletion, python garbage collect...


# The "functional" architecture ( from the talk )
# taking turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
class InteractiveTurtle:

    model = SimTurtle()
    real = turtle.Turtle()

    # a basic comparison function to make sure our model stays on track...
    # Also called permanent live testing / Zero Assumptions Programming
    def _compare_model(self):
        assert (
            self.model.position == self.position()
        ), f"Model position {self.model.position} inconsistent with reality : {self.position()}"
        assert (
            self.model.heading(self.model.state) == self.heading()
        ), f"Model angle {self.model.heading(self.model.state)} inconsistent with reality : {self.heading()}"

    def position(self):
        # Apparently we should use here the "real" one
        return self.real.position()

    def heading(self):
        # Apparently we should use here the "real" one
        return self.real.heading()

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        logging.info("move {0}".format(distance))
        self._compare_model()

        self.model.move(distance)
        self.real.forward(distance=distance)

        self._compare_model()
        return self

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree right".format(angle))
        self._compare_model()

        self.model.turn(angle * -1)
        # Note here that with just a minor difference in interface, errors can creep in.
        # This actually means a different model would have been a better fit for our actual implementation.
        self.real.right(angle)

        self._compare_model()
        return self

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree left".format(angle))
        self._compare_model()

        self.model.turn(angle)
        self.real.left(angle)

        self._compare_model()
        return self

    def penup(self):
        logging.info("pen UP")
        # Not asserting : for later visual comparison only
        self.model.penup()
        self.real.penup()
        return self

    def pendown(self):
        logging.info("pen DOWN")
        # Not asserting : for later visual comparison only
        self.model.pendown()
        self.real.pendown()
        return self

    def home(self):
        logging.info("going home")
        self._compare_model()

        self.model.home()
        self.real.home()

        self._compare_model()
        return self

    def reset(self):
        logging.info("RESET!")
        self._compare_model()

        self.model = SimTurtle()
        self.real.reset()

        self._compare_model()
        return self

    def bye(self):
        logging.info("BYE!")
        self.real.getscreen().bye()
        # no return, nothing after.


# Usual cmd interface, "functional" style
class TurtleRepl:

    cmd = cmd.Cmd()

    intro = "Welcome to the tootle shell.   Type help or ? to list commands.\n"
    tootle = InteractiveTurtle()

    def __init__(self):

        # ----- Setting up cmd via delegation-----
        self.cmd.prompt = "(tootle) "

        # Should probably be in python core implementation
        def do_EOF(self, _):
            "Stop recording, close the turtle window, and exit:  BYE"
            print("Thank you for using Turtle")
            repl.tootle.bye()
            return True

        self.cmd.do_EOF = types.MethodType(do_EOF, self.cmd)

        def onecmd(self, line):
            """Interpret the argument as though it had been typed in response
            to the prompt.

            This may be overridden, but should not normally need to be;
            see the precmd() and postcmd() methods for useful execution hooks.
            The return value is a flag indicating whether interpretation of
            commands by the interpreter should stop.

            """
            cmd, arg, line = self.parseline(line)
            if not line:
                return self.emptyline()
            if cmd is None:
                return self.default(line)
            self.lastcmd = line
            if line == 'EOF':
                self.lastcmd = ''
            if cmd == '':
                return self.default(line)
            else:
                try:
                    func = getattr(self, 'do_' + cmd)
                except AttributeError:
                    return self.default(line)

                # inspect the function to discover how many arguments are necessary
                sig = inspect.signature(func)
                # attempt to parse these arguments
                leftover = arg
                # TODO : function compact expression ?
                args = []
                for n in range(0, len(sig.parameters)):
                    arg, leftover, line = self.parseline(leftover)
                    args.append(arg)
                # recover unused arguments
                stop = func(*args)

                # chain the interpreter only if the command has fluent API and return the repl
                if stop is repl:
                    if leftover:
                        # recurse for the rest of the line
                        stop = self.onecmd(leftover)
                else:
                    return self.default(line)  # If the previous command does return the repl, we cannot chain...

                return stop == True  # returns True only if stop is True (stop the repl)

        self.cmd.onecmd = types.MethodType(onecmd, self.cmd)

        # TODO
        # def complete(self, text, state):
        #     """Return the next possible completion for 'text'.
        #
        #     If a command has not been entered, then complete against command list.
        #     Otherwise try to call complete_<command> to get list of completions.
        #     """
        #     if state == 0:
        #         import readline
        #         origline = readline.get_line_buffer()
        #         line = origline.lstrip()
        #         stripped = len(origline) - len(line)
        #         begidx = readline.get_begidx() - stripped
        #         endidx = readline.get_endidx() - stripped
        #         if begidx > 0:
        #             cmd, args, foo = self.parseline(line)
        #             if cmd == '':
        #                 compfunc = self.completedefault
        #             else:
        #                 try:
        #                     compfunc = getattr(self, 'complete_' + cmd)
        #                 except AttributeError:
        #                     compfunc = self.completedefault
        #         else:
        #             compfunc = self.completenames
        #         self.completion_matches = compfunc(text, line, begidx, endidx)
        #     try:
        #         return self.completion_matches[state]
        #     except IndexError:
        #         return None

        # self.cmd.complete = types.MethodType(complete, self.cmd)

        repl = self

        # Note here the repl comes from the closure contect, not from the self (owning instance)
        def do_move(self, distance):
            "Move the turtle forward by the specified distance:  MOVE 10"
            repl.tootle.move(distance)
            return repl

        def do_left(self, angle):
            "Turn turtle right by given number of degrees:  LEFT 20"
            repl.tootle.left(angle)
            return repl

        def do_right(self, angle):
            "Turn turtle right by given number of degrees:  RIGHT 20"
            repl.tootle.right(angle)
            return repl

        def do_home(self, arg):
            "Return turtle to the home postion:  HOME"
            repl.tootle.home()
            return repl

        # This is "read-only"
        def do_position(self, arg):
            "Print the current turle position:  POSITION"
            print("Current position is {}".format(repl.tootle.position()))

        # This is "read-only"
        def do_heading(self, arg):
            "Print the current turle heading in degrees:  HEADING"
            print("Current heading is {}".format(repl.tootle.heading()))

        # This is only cosmetic :-)
        def do_color(self, arg = None):
            "Set the color:  COLOR BLUE"
            if arg is None or arg is '':
                arg = 'black'
            repl.tootle.color(arg.lower())
            return repl

        def do_reset(self, arg):
            "Clear the screen and return turtle to center:  RESET"
            self.do_color()
            repl.tootle.reset()
            return repl

        def do_bye(self, arg):
            "Stop recording, close the turtle window, and exit:  BYE"
            print("Thank you for using Turtle")
            repl.tootle.bye()
            return True

        self.cmd.do_move = types.MethodType(do_move, self.cmd)
        self.cmd.do_left = types.MethodType(do_left, self.cmd)
        self.cmd.do_right = types.MethodType(do_right, self.cmd)
        self.cmd.do_home = types.MethodType(do_home, self.cmd)
        self.cmd.do_position = types.MethodType(do_position, self.cmd)
        self.cmd.do_heading = types.MethodType(do_heading, self.cmd)
        self.cmd.do_color = types.MethodType(do_color, self.cmd)
        self.cmd.do_reset = types.MethodType(do_reset, self.cmd)
        self.cmd.do_bye = types.MethodType(do_bye, self.cmd)

    # delegating

    def cmdloop(self):
        self.cmd.cmdloop(intro=self.intro)


if __name__ == "__main__":
    TurtleRepl().cmdloop()
