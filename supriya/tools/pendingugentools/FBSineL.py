# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.FBSineN import FBSineN


class FBSineL(FBSineN):
    r'''

    ::

        >>> fbsine_l = ugentools.FBSineL.(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ...     )
        >>> fbsine_l

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'im',
        'fb',
        'a',
        'c',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1.1,
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        FBSineN.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.1,
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        r'''Constructs an audio-rate FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        r'''Gets `a` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def c(self):
        r'''Gets `c` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.c

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def fb(self):
        r'''Gets `fb` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.fb

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('fb')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def im(self):
        r'''Gets `im` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.im

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('im')
        return self._inputs[index]

    @property
    def xi(self):
        r'''Gets `xi` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.xi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        r'''Gets `yi` input of FBSineL.

        ::

            >>> fbsine_l = ugentools.FBSineL.ar(
            ...     a=1.1,
            ...     c=0.5,
            ...     fb=0.1,
            ...     frequency=22050,
            ...     im=1,
            ...     xi=0.1,
            ...     yi=0.1,
            ...     )
            >>> fbsine_l.yi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]