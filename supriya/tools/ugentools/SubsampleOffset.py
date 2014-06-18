# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class SubsampleOffset(InfoUGenBase):
    r'''Subsample-offset info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.SubsampleOffset.ir()
        SubsampleOffset.ir()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            calculation_rate=calculation_rate,
            )