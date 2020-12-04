# Supriya

[![](https://img.shields.io/pypi/pyversions/supriya)]()
[![](https://img.shields.io/pypi/l/supriya)]()
[![](https://img.shields.io/github/workflow/status/josiah-wolf-oberholtzer/supriya/Testing/master)]()

[Supriya](https://github.com/josiah-wolf-oberholtzer/supriya) is a
[Python](https://www.python.org/) API for
[SuperCollider](http://supercollider.github.io/).

Supriya lets you:

- Control SuperCollider's ``scsynth`` synthesis server in
  [realtime](http://josiahwolfoberholtzer.com/supriya/api/supriya/realtime/index.html)
- Compile
  [SynthDef](http://josiahwolfoberholtzer.com/supriya/api/supriya/synthdefs/index.html)s
natively in Python
- Explore non-realtime composition with object-oriented
  [Session](http://josiahwolfoberholtzer.com/supriya/api/supriya/nonrealtime/index.html)s
- Build realtime/non-realtime-agnostic,
  [asyncio](https://docs.python.org/3/library/asyncio.html)-aware applications
with
[Provider](http://josiahwolfoberholtzer.com/supriya/api/supriya/provider.html)s
- Schedule callbacks with tempo- and meter-aware
  [Clock](http://josiahwolfoberholtzer.com/supriya/api/supriya/clock/index.html)s
- Integrate with [IPython](http://ipython.org/),
  [Sphinx](https://www.sphinx-doc.org/en/master/) and
[Graphviz](http://graphviz.org/)

Complete documentation available at http://josiahwolfoberholtzer.com/supriya/.

## Installation

Get [SuperCollider]() from [http://supercollider.github.io/](http://supercollider.github.io/).

Get Supriya from [PyPI]():

```bash
pip install supriya
```

... or from source:

```bash
git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
cd supriya/
pip install -e .
```

## Example: Hello World!

Let's make some noise. One synthesis context, one synth, one parameter change.

```
>>> import supriya
```

### Realtime

```python
>>> server = supriya.Server.default().boot()
>>> synth = supriya.Synth().allocate()
>>> synth["frequency"] = 123.45
>>> synth.free()
>>> server.quit()
```

### Non-realtime

```python
>>> session = supriya.Session()
>>> with session.at(0):
...     synth = session.add_synth(duration=2)
...
>>> with session.at(1):
...     synth["frequency"] = 123.45
...
>>> session.render(duration=3)
(0, PosixPath('/Users/josiah/Library/Caches/supriya/session-981245bde945c7550fa5548c04fb47f7.aiff'))
```

## Example: Defining SynthDefs

Let's build a simple SynthDef for playing an audio buffer as a one-shot, with
panning and speed controls.

First, some imports, just to save horizontal space:

```python
>>> from supriya.ugens import Out, Pan2, PlayBuf
```

Second, define a builder with the control parameters we want for our SynthDef:

```python
>>> builder = supriya.SynthDefBuilder(amplitude=1, buffer_id=0, out=0, panning=0.0, rate=1.0)
```

Third, use the builder as a context manager. Unit generators defined inside the
context will be added automatically to the builder:

```python
>>> with builder:
...     player = PlayBuf.ar(
...         buffer_id=builder["buffer_id"],
...         done_action=supriya.DoneAction.FREE_SYNTH,
...         rate=builder["rate"],
...     )
...     panner = Pan2.ar(
...         source=player,
...         position=builder["panning"],
...         level=builder["amplitude"],
...     )
...     _ = Out.ar(bus=builder["out"], source=panner)
...
```

Finally, build the SynthDef, and print its structure. Supriya has given the
SynthDef a name automatically by hashing its structure:

```python
>>> synthdef = builder.build()
>>> print(synthdef)
synthdef:
    name: a056603c05d80c575333c2544abf0a05
    ugens:
    -   Control.kr: null
    -   PlayBuf.ar:
            buffer_id: Control.kr[1:buffer_id]
            done_action: 2.0
            loop: 0.0
            rate: Control.kr[4:rate]
            start_position: 0.0
            trigger: 1.0
    -   Pan2.ar:
            level: Control.kr[0:amplitude]
            position: Control.kr[3:panning]
            source: PlayBuf.ar[0]
    -   Out.ar:
            bus: Control.kr[2:out]
            source[0]: Pan2.ar[0]
            source[1]: Pan2.ar[1]
```

## Example: Playing Samples

```python
>>> server = supriya.Server.default().boot()
>>> buffer_ = supriya.Buffer().allocate_from_file(
...     file_path="supriya/assets/audio/birds/birds-01.wav",
... )
>>> 
```

## Example: Performing Patterns
