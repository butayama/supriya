# -*- encoding: utf-8 -*-
import inspect
import pytest
from supriya.tools import documentationtools


pytest.skip()


ignored_names = (
    '__dict__',
    '__init__',
    '__new__',
    '__weakref__',
    )

ignored_classes = (
    )

classes = documentationtools.list_all_supriya_classes()

functions = documentationtools.list_all_supriya_functions()


@pytest.mark.parametrize('obj', classes)
def test_supriya___doc___01(obj):
    r'''All classes have a docstring. All class methods have a docstring.
    '''
    if obj.__doc__ is None:
        message = 'No documentation for: {}'.format(obj.__name__)
        raise Exception(message)
    if obj.__name__ in ignored_classes:
        return
    for attr in inspect.classify_class_attrs(obj):
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not obj:
            continue
        elif attr.kind == 'data':
            continue
        if attr.name[0].isalpha() or attr.name.startswith('__'):
            if getattr(obj, attr.name).__doc__ is None:
                message = 'No documentation for: {}.{}'
                message = message.format(obj.__name__, attr.name)
                raise Exception(message)


@pytest.mark.parametrize('obj', functions)
def test_supriya___doc___02(obj):
    r'''All functions have a docstring.
    '''
    if obj.__doc__ is None:
        message = 'No documentation for: {}'.format(obj.__name__)
        raise Exception(message)