from Cmd import TurtleRepl


# Testing before run
import pytest
import test_State
pytest.main(['-s', test_State.__file__])

# Manual interaction
TurtleRepl().cmdloop()
