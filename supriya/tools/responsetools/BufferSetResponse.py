# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class BufferSetResponse(SupriyaValueObject, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        items=None,
        ):
        self._buffer_id = buffer_id
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = collections.OrderedDict()
        for item in self:
            result[item.sample_index] = item.sample_value
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items
