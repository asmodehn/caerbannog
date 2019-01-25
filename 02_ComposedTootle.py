import collections

import math
import turtle
import cmd
import enum
import logging
import types
import inspect


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
    _position = turtle.Vec2D(0, 0)
    _attitude = turtle.Vec2D(1, 0)
    _penState = PenState.DOWN

    # Read-only state
    @property
    def position(self):
        return self._position

    @property
    def attitude(self):
        return self._attitude

    @property
    def penState(self):
        return self._penState

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        endPosition = self.position + distance * self.attitude

        # mutating the state(=instance)
        self._position = endPosition

    def turn(self, angle: int):

        # mutating the state(=instance)
        self._attitude = self.attitude.rotate(angle)

    def penup(self):
        logging.info("simulating pen UP")
        self._penState=PenState.UP

    def pendown(self):
        logging.info("simulating pen DOWN")
        self._penState=PenState.DOWN

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self._position=turtle.Vec2D(0, 0)
        self._attitude=turtle.Vec2D(1, 0)


# Note we use a class here like "module" was used in the presentation, to encapsulate code.
# There are other ways to achieve the same goal, for example having separate module for each class used here.
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

    # Note the state here is also passed around in self.
    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        oldpos = self.position
        self.state.move(distance)
        newpos = self.position

        # just because we manage the drawing here and not in the TurtleState
        if self.penState == PenState.DOWN:
            self.drawing.append((oldpos, newpos))

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.state.turn(angle)

    def heading(self):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(self.attitude[1], self.attitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

    def penup(self):
        logging.info("simulating pen UP")
        self.state.penup()

    def pendown(self):
        logging.info("simulating pen DOWN")
        self.state.pendown()

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self.state.home()

    # No bye, no deletion, python garbage collect...


# The composed (delegation) OO architecture
# Taking SimTurtle turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
class InteractiveTurtle:

    model = SimTurtle()
    view = turtle.Turtle()

    # abasic comparison function to make sure our model stays on track...
    def _compare_model(self):
        assert (
            self.model.position == self.position()
        ), f"Model position {self.model.position} inconsistent with reality : {self.position()}"
        assert (
            self.model.heading() == self.heading()
        ), f"Model angle {self.model.heading()} inconsistent with reality : {self.heading()}"

    def position(self):
        # Apparently we should use here the "real" one (from the view)
        return self.view.position()

    def heading(self):
        # Apparently we should use here the "real" one (from the view)
        return self.view.heading()

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        logging.info("move {0}".format(distance))
        self._compare_model()

        self.model.move(distance)
        self.view.forward(distance=distance)

        self._compare_model()

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree right".format(angle))
        self._compare_model()

        self.model.turn(angle * -1)
        # Note here that with just a minor difference in interface, errors can creep in.
        # This actually means a different model would have been a better fit for our actual implementation.
        self.view.right(angle)

        self._compare_model()

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree left".format(angle))
        self._compare_model()

        self.model.turn(angle)
        self.view.left(angle)

        self._compare_model()

    def penup(self):
        logging.info("pen UP")
        # Not asserting : for later visual comparison only
        self.model.penup()
        self.view.penup()

    def pendown(self):
        logging.info("pen DOWN")
        # Not asserting : for later visual comparison only
        self.model.pendown()
        self.view.pendown()

    def home(self):
        logging.info("going home")
        self._compare_model()

        self.model.home()
        self.view.home()

        self._compare_model()

    def reset(self):
        logging.info("RESET!")
        self._compare_model()

        self.model = SimTurtle()
        self.view.reset()

        self._compare_model()

    def bye(self):
        logging.info("BYE!")
        self.view.getscreen().bye()


# Usual cmd interface, composed OO-style
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
                    arg, leftover, _ = self.parseline(leftover)
                    args.append(arg)
                # recover unused arguments
                stop = func(*args)

                if not stop:
                    if leftover:
                        # recurse for the rest of the line
                        stop = self.onecmd(leftover)

                return stop

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

        def do_move(self, distance):
            "Move the turtle forward by the specified distance:  MOVE 10"
            repl.tootle.move(distance)

        def do_left(self, angle):
            "Turn turtle right by given number of degrees:  LEFT 20"
            repl.tootle.left(angle)

        def do_right(self, angle):
            "Turn turtle right by given number of degrees:  RIGHT 20"
            repl.tootle.right(angle)

        def do_home(self, arg):
            "Return turtle to the home postion:  HOME"
            repl.tootle.home()

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

        def do_reset(self, arg):
            "Clear the screen and return turtle to center:  RESET"
            self.do_color()
            repl.tootle.reset()

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
