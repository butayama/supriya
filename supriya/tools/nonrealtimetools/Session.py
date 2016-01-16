# -*- encoding: utf-8 -*-
import collections
import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
from abjad.tools import mathtools
from abjad.tools import timespantools
from supriya.tools import osctools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import timetools
from supriya.tools.osctools.OscMixin import OscMixin


class Session(OscMixin):
    r'''A non-realtime session.

    ::

        >>> from supriya.tools import nonrealtimetools
        >>> session = nonrealtimetools.Session()

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder(frequency=440)
        >>> with builder:
        ...     out = ugentools.Out.ar(
        ...         source=ugentools.SinOsc.ar(
        ...             frequency=builder['frequency'],
        ...             )
        ...         )
        ...
        >>> synthdef = builder.build()

    ::

        >>> synth_a = session.add_synth(0, 10, synthdef=synthdef)
        >>> synth_b = session.add_synth(5, 15, synthdef=synthdef, frequency=443)
        >>> synth_c = session.add_synth(0, 15, synthdef=synthdef, frequency=666)

    ::

        >>> with session.at(7.5):
        ...     synth_a['frequency'] = 880
        ...     synth_b['frequency'] = 990
        ...

    ::

        >>> for osc_bundle in session.to_osc_bundles():
        ...     osc_bundle
        ...
        OscBundle(
            timestamp=0.0,
            contents=(
                OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 9c4eb4778dc0faf39459fa8a5cd45c19\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01C\xdc\x00\x00\x00\x00\x00\x01\tfrequency\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1000, 0, 0),
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1001, 0, 0, 'frequency', 666),
                )
            )
        OscBundle(
            timestamp=5.0,
            contents=(
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1002, 0, 0, 'frequency', 443),
                )
            )
        OscBundle(
            timestamp=7.5,
            contents=(
                OscMessage('/n_set', 1000, 'frequency', 880),
                OscMessage('/n_set', 1002, 'frequency', 990),
                )
            )
        OscBundle(
            timestamp=10.0,
            contents=(
                OscMessage('/n_free', 1000),
                )
            )
        OscBundle(
            timestamp=15.0,
            contents=(
                OscMessage('/n_free', 1001, 1002),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_input_bus_group',
        '_audio_output_bus_group',
        '_buses',
        '_input_count',
        '_output_count',
        '_session_moments',
        '_synths',
        )

    _prioritized_request_types = [
        requesttools.SynthDefReceiveRequest,
        requesttools.ControlBusSetRequest,
        requesttools.GroupNewRequest,
        requesttools.SynthNewRequest,
        requesttools.NodeMapToAudioBusRequest,
        requesttools.NodeMapToControlBusRequest,
        requesttools.NodeSetRequest,
        ]

    ### INITIALIZER ###

    def __init__(self, input_count=0, output_count=2):
        from supriya.tools import nonrealtimetools

        input_count = int(input_count or 0)
        assert 0 <= input_count
        self._input_count = input_count

        output_count = int(output_count or 0)
        assert 0 <= output_count
        self._output_count = output_count

        audio_input_bus_group = None
        if self._input_count:
            audio_input_bus_group = nonrealtimetools.AudioInputBusGroup(self)
        self._audio_input_bus_group = audio_input_bus_group

        audio_output_bus_group = None
        if self._output_count:
            audio_output_bus_group = nonrealtimetools.AudioOutputBusGroup(self)
        self._audio_output_bus_group = audio_output_bus_group

        self._buses = collections.OrderedDict()
        self._session_moments = []
        self._synths = timetools.TimespanCollection()

    ### PRIVATE METHODS ###

    def _build_bus_id_mapping(self):
        input_count = self._input_count or 0
        output_count = self._output_count or 0
        first_private_bus_id = input_count + output_count
        audio_bus_allocator = servertools.BlockAllocator(
            heap_minimum=first_private_bus_id,
            )
        control_bus_allocator = servertools.BlockAllocator()
        mapping = {}
        if output_count:
            bus_group = self.audio_output_bus_group
            for bus_id, bus in enumerate(bus_group):
                mapping[bus] = bus_id
        if input_count:
            bus_group = self.audio_input_bus_group
            for bus_id, bus in enumerate(bus_group, output_count):
                mapping[bus] = bus_id
        for bus in self._buses:
            if bus in mapping:
                continue
            if bus.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                allocator = audio_bus_allocator
            else:
                allocator = control_bus_allocator
            if bus.bus_group is None:
                mapping[bus] = allocator.allocate(1)
            else:
                block_id = allocator.allocate(len(bus.bus_group))
                mapping[bus.bus_group] = block_id
                for bus_id in range(block_id, block_id + len(bus.bus_group)):
                    mapping[bus] = bus_id
        return mapping

    def _build_synth_id_mapping(self):
        from supriya.tools import nonrealtimetools
        prototype = (nonrealtimetools.Synth,)
        allocator = servertools.NodeIdAllocator()
        mapping = {}
        for timespan in sorted(self._synths):
            if not isinstance(timespan, prototype):
                continue
            elif timespan in mapping:
                continue
            mapping[timespan] = allocator.allocate_node_id()
        return mapping

    def _build_command(
        self,
        output_filename,
        input_filename=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        **kwargs
        ):
        r'''Builds non-realtime rendering command.

        ::

            >>> session._build_command('output.aiff')
            'scsynth -N {} _ output.aiff 44100 aiff int24'

        '''
        parts = ['scsynth', '-N', '{}']
        if input_filename:
            parts.append(os.path.expanduser(input_filename))
        else:
            parts.append('_')
        parts.append(os.path.expanduser(output_filename))
        parts.append(str(int(sample_rate)))
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        parts.append(header_format.name.lower())  # Must be lowercase.
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        parts.append(sample_format.name.lower())  # Must be lowercase.
        server_options = servertools.ServerOptions(**kwargs)
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = ' '.join(parts)
        return command

    def _collect_bus_requests(self, request_mapping, id_mapping):
        events_by_offset = {}
        for bus in self._buses:
            if bus.calculation_rate != synthdeftools.CalculationRate.CONTROL:
                continue
            bus_id = id_mapping[bus]
            for offset, value in bus._events:
                events_by_offset.setdefault(offset, {})[bus_id] = value
        for offset, events in events_by_offset.items():
            requests = request_mapping.setdefault(offset, [])
            index_value_pairs = sorted(events.items())
            request = requesttools.ControlBusSetRequest(
                index_value_pairs=index_value_pairs,
                )
            requests.append(request)
        return request_mapping

    def _collect_synth_requests(self, request_mapping, id_mapping):
        comparator = lambda x: (x._get_timespan(x), id_mapping[x])
        synths = sorted(self._synths[:], key=comparator)
        for synth in synths:
            items = synth._collect_requests(id_mapping).items()
            for offset, synth_requests in items:
                requests = request_mapping.setdefault(offset, [])
                requests.extend(synth_requests)
        return request_mapping

    def _collect_synthdef_requests(self, request_mapping):
        from supriya.tools import nonrealtimetools
        prototype = (nonrealtimetools.Synth,)
        synthdefs_to_offsets = {}
        for simultaneity in self._synths.iterate_simultaneities():
            start_events = set(simultaneity.start_timespans)
            for start_event in start_events:
                if not isinstance(start_event, prototype):
                    continue
                synthdef = start_event.synthdef
                if synthdef in synthdefs_to_offsets:
                    continue
                synthdefs_to_offsets[synthdef] = start_event.start_offset
        offsets_to_synthdefs = {}
        for synthdef, offset in synthdefs_to_offsets.items():
            if offset not in offsets_to_synthdefs:
                offsets_to_synthdefs[offset] = []
            offsets_to_synthdefs[offset].append(synthdef)
        for offset, synthdefs in offsets_to_synthdefs.items():
            synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
            request = requesttools.SynthDefReceiveRequest(
                synthdefs=synthdefs,
                )
            requests = request_mapping.setdefault(offset, [])
            requests.append(request)
        return request_mapping

    def _process_requests(self, offset, requests):
        timestamp = float(offset)
        requests_by_type = {}
        for request in requests:
            requests_by_type.setdefault(type(request), []).append(request)
        osc_messages = []
        for request_type in self._prioritized_request_types:
            for request in requests_by_type.get(request_type, []):
                osc_message = request.to_osc_message(
                    with_textual_osc_command=True,
                    )
                osc_messages.append(osc_message)
        if requesttools.NodeFreeRequest in requests_by_type:
            node_ids = []
            for request in requests_by_type[requesttools.NodeFreeRequest]:
                node_ids.extend(request.node_ids)
            request = requesttools.NodeFreeRequest(node_ids=node_ids)
            osc_message = request.to_osc_message(with_textual_osc_command=True)
            osc_messages.append(osc_message)
        osc_bundle = osctools.OscBundle(timestamp, osc_messages)
        return osc_bundle

    def _process_terminal_event(self, final_offset, timespan):
        osc_bundles = []
        if timespan is not None:
            prototype = (mathtools.Infinity(), mathtools.NegativeInfinity)
            if timespan.stop_offset not in prototype and \
                final_offset < timespan.stop_offset:
                osc_bundle = osctools.OscBundle(
                    timestamp=float(timespan.stop_offset),
                    contents=[osctools.OscMessage(0)],
                    )
                osc_bundles.append(osc_bundle)
        return osc_bundles

    def _process_timespan_mask(self, timespan):
        if timespan is not None and self._synths:
            assert isinstance(timespan, timespantools.Timespan)
            synths = timespantools.TimespanInventory(self._synths)
            original_timespan = synths.timespan
            synths = synths & timespan
            if timespan.start_offset not in (
                mathtools.Infinity(), mathtools.NegativeInfinity):
                translation = timespan.start_offset - \
                    original_timespan.start_offset
                synths = synths.translate(translation)
            session = type(self)()
            session._synths.insert(synths[:])
        else:
            session = self
        return session

    ### PUBLIC METHODS ###

    def at(self, offset):
        from supriya.tools import nonrealtimetools
        session_moment = nonrealtimetools.SessionMoment(
            session=self,
            offset=offset,
            )
        return session_moment

    def add_bus(self, calculation_rate='control'):
        from supriya.tools import nonrealtimetools
        bus = nonrealtimetools.Bus(self, calculation_rate=calculation_rate)
        self._buses[bus] = None
        return bus

    def add_bus_group(self, bus_count=1, calculation_rate='control'):
        from supriya.tools import nonrealtimetools
        bus_group = nonrealtimetools.BusGroup(
            self,
            bus_count=bus_count,
            calculation_rate=calculation_rate,
            )
        for bus in bus_group:
            self._buses[bus] = None
        return bus_group

    def add_synth(
        self,
        start_offset=None,
        stop_offset=None,
        synthdef=None,
        add_action=None,
        **synth_kwargs
        ):
        from supriya.tools import nonrealtimetools
        synth = nonrealtimetools.Synth(
            self,
            start_offset=start_offset,
            stop_offset=stop_offset,
            synthdef=synthdef,
            add_action=add_action,
            **synth_kwargs
            )
        self._synths.insert(synth)
        return synth

    def render(
        self,
        output_filename,
        input_filename=None,
        timespan=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **kwargs
        ):
        datagram = self.to_datagram(timespan=timespan)
        md5 = hashlib.md5()
        md5.update(datagram)
        md5 = md5.hexdigest()
        temp_directory_path = tempfile.mkdtemp()
        file_path = os.path.join(temp_directory_path, '{}.osc'.format(md5))
        with open(file_path, 'wb') as file_pointer:
            file_pointer.write(datagram)
        command = self._build_command(
            output_filename,
            input_filename=None,
            sample_rate=sample_rate,
            header_format=header_format,
            sample_format=sample_format,
            **kwargs
            )
        command = command.format(file_path)
        exit_code = subprocess.call(command, shell=True)
        if debug:
            return exit_code, file_path
        else:
            shutil.rmtree(temp_directory_path)
            return exit_code, None

    def to_datagram(self, timespan=None):
        osc_bundles = self.to_osc_bundles(timespan=timespan)
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def to_osc_bundles(self, timespan=None):
        osc_bundles = []
        session = self._process_timespan_mask(timespan)
        id_mapping = {}
        id_mapping.update(session._build_synth_id_mapping())
        id_mapping.update(session._build_bus_id_mapping())
        request_mapping = {}
        request_mapping = session._collect_bus_requests(request_mapping, id_mapping)
        request_mapping = session._collect_synthdef_requests(request_mapping)
        request_mapping = session._collect_synth_requests(request_mapping, id_mapping)
        if not request_mapping:
            raise ValueError
        for offset, requests in sorted(request_mapping.items()):
            osc_bundle = session._process_requests(offset, requests)
            osc_bundles.append(osc_bundle)
        osc_bundles += session._process_terminal_event(offset, timespan)
        return osc_bundles

    ### PUBLIC PROPERTIES ###

    @property
    def audio_input_bus_group(self):
        return self._audio_input_bus_group

    @property
    def audio_output_bus_group(self):
        return self._audio_output_bus_group

    @property
    def input_count(self):
        return self._input_count

    @property
    def output_count(self):
        return self._output_count