import cmd

from .real import InteractiveTurtle


# Usual cmd interface, OO-style
class TurtleRepl(cmd.Cmd):

    # Should probably be in python core implementation
    def do_EOF(self, _):
        "Stop recording, close the turtle window, and exit:  BYE"
        print("Thank you for using Turtle")
        self.tootle.bye()
        return True

    def __init__(self, simulation, completekey='tab', stdin=None, stdout=None):
        self.tootle = InteractiveTurtle(simulation)
        super().__init__(completekey, stdin, stdout)

    tootle = None
    intro = "Welcome to the tootle shell.   Type help or ? to list commands.\n"
    prompt = "(tootle) "

    # ----- basic turtle commands -----
    def do_move(self, distance):
        "Move the turtle forward by the specified distance:  MOVE 10"
        self.tootle.move(distance)

    def do_left(self, angle):
        "Turn turtle right by given number of degrees:  LEFT 20"
        self.tootle.left(angle)

    def do_right(self, angle):
        "Turn turtle right by given number of degrees:  RIGHT 20"
        self.tootle.right(angle)

    def do_home(self, _):
        "Return turtle to the home postion:  HOME"
        self.tootle.home()

    # This is "read-only"
    def do_position(self, _):
        "Print the current turle position:  POSITION"
        print("Current position is {}".format(self.tootle.position()))

    # This is "read-only"
    def do_heading(self, _):
        "Print the current turle heading in degrees:  HEADING"
        print("Current heading is {}".format(self.tootle.heading()))

    # This is only cosmetic :-)
    def do_color(self, arg = None):
        "Set the color:  COLOR BLUE"
        if arg is None or arg is '':
            arg = 'black'
        self.tootle.color(arg.lower())

    def do_reset(self, _):
        "Clear the screen and return turtle to center:  RESET"
        self.do_color()
        self.tootle.reset()

    def do_bye(self, _):
        return self.do_EOF(_)
