import enum
from supriya.tools.audio.UGen import UGen
from supriya.tools.audio import ArgumentSpecification


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('left'),
        ArgumentSpecification('right'),
        )

    class BinaryOperator(enum.IntEnum):
        PLUS = 0
        MINUS = 1
        TIMES = 2
        DIVIDE = 3
        MOD = 4
        MIN = 5
        MAX = 6
        LOG = 25
        LOG2 = 26
        LOG10 = 27