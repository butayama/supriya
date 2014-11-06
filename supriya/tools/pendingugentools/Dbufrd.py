# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.DUGen import DUGen


class Dbufrd(DUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bufnum=0,
        loop=1,
        phase=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            loop=loop,
            phase=phase,
            )
        return ugen