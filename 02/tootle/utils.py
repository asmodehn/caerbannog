
import enum


# Directly, naively, modeled in python 3.6
# from the code shown in : https://www.youtube.com/watch?v=AG3KuqDbmhM

# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1
