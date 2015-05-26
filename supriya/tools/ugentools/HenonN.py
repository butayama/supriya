# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class HenonN(UGen):
    r'''A non-interpolating henon map chaotic generator.

    ::

        >>> henon_n = ugentools.HenonN.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ...     )
        >>> henon_n
        HenonN.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'a',
        'b',
        'x_0',
        'x_1',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1.4,
        b=0.3,
        frequency=22050,
        x_0=0,
        x_1=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            x_0=x_0,
            x_1=x_1,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.4,
        b=0.3,
        frequency=22050,
        x_0=0,
        x_1=0,
        ):
        r'''Constructs an audio-rate HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n
            HenonN.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            x_0=x_0,
            x_1=x_1,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        r'''Gets `a` input of HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n.a
            1.4

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        r'''Gets `b` input of HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n.b
            0.3

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n.frequency
            22050.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def x_0(self):
        r'''Gets `x_0` input of HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n.x_0
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('x_0')
        return self._inputs[index]

    @property
    def x_1(self):
        r'''Gets `x_1` input of HenonN.

        ::

            >>> henon_n = ugentools.HenonN.ar(
            ...     a=1.4,
            ...     b=0.3,
            ...     frequency=22050,
            ...     x_0=0,
            ...     x_1=0,
            ...     )
            >>> henon_n.x_1
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('x_1')
        return self._inputs[index]