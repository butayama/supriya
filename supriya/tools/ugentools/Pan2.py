# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pan2(MultiOutUGen):
    r'''A two channel equal power panner.

    ::

        >>> source = ugentools.WhiteNoise.ar()
        >>> pan_2 = ugentools.Pan2.ar(
        ...     source=source,
        ...     )
        >>> pan_2
        UGenArray({2})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'position',
        'level',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        level=1.,
        position=0.,
        rate=None,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            channel_count=2,
            level=level,
            position=position,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1.,
        position=0.,
        source=None,
        ):
        r'''Constructs an audio-rate two channel equal power panner.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> pan_2 = ugentools.Pan2.ar(
            ...     source=source,
            ...     )
            >>> pan_2
            UGenArray({4})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            position=position,
            level=level,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def level(self):
        r'''Gets `level` input of Pan2.

        ::

            >>> level = 0.9
            >>> source = ugentools.WhiteNoise.ar()
            >>> pan_2_outputs = ugentools.Pan2.ar(
            ...     level=level,
            ...     source=source,
            ...     )
            >>> pan_2 = pan_2_outputs[0].source
            >>> pan_2.level
            0.9

        Returns input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def position(self):
        r'''Gets `position` input of Pan2.

        ::

            >>> position = 0.5
            >>> source = ugentools.WhiteNoise.ar()
            >>> pan_2_outputs = ugentools.Pan2.ar(
            ...     position=position,
            ...     source=source,
            ...     )
            >>> pan_2 = pan_2_outputs[0].source
            >>> pan_2.position
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Pan2.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> pan_2_outputs = ugentools.Pan2.ar(
            ...     source=source,
            ...     )
            >>> pan_2 = pan_2_outputs[0].source
            >>> pan_2.source
            OutputProxy(
                source=WhiteNoise(
                    rate=<CalculationRate.AUDIO: 2>
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]