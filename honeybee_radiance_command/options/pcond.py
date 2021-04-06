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


class PcondOptions(OptionCollection):
    """pcond options.

    Also see: https://floyd.lbl.gov/radiance/man_html/pcond.1.html
    """

    __slots__ = (
        "_h",
        "_a",
        "_v",
        "_s",
        "_c",
        "_w",
        "_i",
        "_I",
        "_l",
        "_e",
        "_u",
        "_d",
        "_p",
        "_f",
        "_x"
    )

    def __init__(self):
        """pcond command options."""

        super.__init__(self)
        self._h = BoolOption("h", "Human visual response - default: True")
        self._a = BoolOption("a", "Human visual acuity loss - default: False")
        self._v = BoolOption("v", "Veiling glare- default: False")
