import cmd
import inspect

from real import InteractiveTurtle

# Usual cmd interface, "functional" style
import types


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
                elif line:
                    return self.default(line)  # If the previous command does return the repl, we cannot chain...

                return stop is True  # returns True only if stop is True (stop the repl)

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

