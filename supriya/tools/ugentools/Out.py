# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGen import UGen


class Out(UGen):
    r'''A bus output unit generator.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.Out.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        Out.ar()

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
        r'''Constructs an audio-rate bus output.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> out = ugentools.Out.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            Out.ar()
        
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

    @classmethod
    def kr(
        cls,
        bus=0,
        source=None,
        ):
        r'''Constructs a control-rate bus output.
        
        ::

            >>> source = ugentools.SinOsc.kr(frequency=[4, 2])
            >>> out = ugentools.Out.kr(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            Out.kr()
        
        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
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
        r'''Gets `bus` input of Out.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> out = ugentools.Out.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> out.bus
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]