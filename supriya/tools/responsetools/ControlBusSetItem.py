# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class ControlBusSetItem(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_index',
        '_bus_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_index=None,
        bus_value=None,
        ):
        self._bus_index = bus_index
        self._bus_value = bus_value

    ### PUBLIC PROPERTIES ###

    @property
    def bus_index(self):
        return self._bus_index

    @property
    def bus_value(self):
        return self._bus_value
