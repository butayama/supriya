# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGen import UGen


class OffsetOut(UGen):
    r'''A bus output unit generator with sample-accurate timing.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        OffsetOut.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            bus=bus,
            rate=rate,
            )
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            self._configure_input('source', single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        source=None,
        ):
        r'''Constructs a sample-accurately-timed audio-rate bus output.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> offset_out = ugentools.OffsetOut.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> offset_out
            OffsetOut.ar()
        
        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        return cls._new_expanded(
            bus=bus,
            rate=rate,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of OffsetOut.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> offset_out = ugentools.OffsetOut.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> offset_out.bus
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]