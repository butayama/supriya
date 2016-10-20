# -*- encoding: utf-8 -*-
import abc
from supriya.tools.ugentools.UGen import UGen


class MultiOutUGen(UGen):
    """
    Abstract base class for ugens with multiple outputs.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = (
        '_channel_count',
        )

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        channel_count=1,
        **kwargs
        ):
        self._channel_count = int(channel_count)
        if 'channel_count' in self._ordered_input_names:
            kwargs['channel_count'] = channel_count
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            **kwargs
            )

    ### SPECIAL METHODS ###

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return self.channel_count

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        special_index=0,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        ugen = super(MultiOutUGen, cls)._new_expanded(
            special_index=special_index,
            **kwargs
            )
        output_proxies = []
        if isinstance(ugen, ugentools.UGen):
            output_proxies.extend(ugen[:])
        else:
            for x in ugen:
                output_proxies.extend(x[:])
        if len(output_proxies) == 1:
            return output_proxies[0]
        result = synthdeftools.UGenArray(output_proxies)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        """
        Gets channel count of multi-output ugen.

        Returns integer.
        """
        return self._channel_count
