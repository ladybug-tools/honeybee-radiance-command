# coding: utf-8
from .optionbase import (
    OptionCollection,
    BoolOption,
    NumericOption,
    StringOption,
    StringOptionJoined,
    IntegerOption,
    TupleOption,
    FileOption
)
import warnings


class GendaylitOptions(OptionCollection):
    """Gendaylit command options.

    Also see: https://floyd.lbl.gov/radiance/gendaylit.1.html
    """

    __slots__ = (
        '_P',
        '_W',
        '_L',
        '_O',
        '_s',
        '_g',
        '_a',
        '_o',
        '_m',
        '_ang'
        )
