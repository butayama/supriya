# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Index import Index


class IndexInBetween(Index):
    r'''

    ::

        >>> index_in_between = ugentools.IndexInBetween.(
        ...     buffer_id=None,
        ...     source=None,
        ...     )
        >>> index_in_between

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        ):
        Index.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        r'''Constructs an audio-rate IndexInBetween.

        ::

            >>> index_in_between = ugentools.IndexInBetween.ar(
            ...     buffer_id=None,
            ...     source=None,
            ...     )
            >>> index_in_between

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        ):
        r'''Constructs a control-rate IndexInBetween.

        ::

            >>> index_in_between = ugentools.IndexInBetween.kr(
            ...     buffer_id=None,
            ...     source=None,
            ...     )
            >>> index_in_between

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of IndexInBetween.

        ::

            >>> index_in_between = ugentools.IndexInBetween.ar(
            ...     buffer_id=None,
            ...     source=None,
            ...     )
            >>> index_in_between.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of IndexInBetween.

        ::

            >>> index_in_between = ugentools.IndexInBetween.ar(
            ...     buffer_id=None,
            ...     source=None,
            ...     )
            >>> index_in_between.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]