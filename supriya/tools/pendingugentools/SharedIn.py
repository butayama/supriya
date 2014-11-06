# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.AbstractIn import AbstractIn


class SharedIn(AbstractIn):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen