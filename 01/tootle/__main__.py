
from .uif.repl import TurtleRepl


# Testing before run
import pytest
from .tests import test_state
pytest.main(['-s', test_state.__file__])

# Manual interaction
TurtleRepl().cmdloop()
