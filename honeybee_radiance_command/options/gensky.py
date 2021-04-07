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


class GenskyOptions(OptionCollection):
    """gensky command options.

    Also see: https://floyd.lbl.gov/radiance/man_html/gensky.1.html
    """

    __slots__ = (
        "_s",
        "_c",
        "_i",
        "_u",
        "_g",
        "_b",
        "_B",
        "_r",
        "_R",
        "_t",
        "_a",
        "_o",
        "_m",
        "_ang")

    def __init__(self):
        """Gensky command options."""

        OptionCollection.__init__(self)

        self._s = BoolOption("s", "Sunny sky without sun - default: False")
        self._c = BoolOption("c", "Cloudy sky - default: False")
        self._i = BoolOption("i", "Intermediate sky without sun - default: False")
        self._u = BoolOption("u", "Uniform cloudy sky - default : False")
        self._g = NumericOption("g", "Average ground reflectance")
        self._b = NumericOption("b", "Zenith brightness from sun angle and sky"
                                " turbidity")
        self._B = NumericOption("B", "Zenith brightness from horizontal"
                                " diffuse irradiance")
        self._r = NumericOption("r", "Solar radiance")
        self._R = NumericOption("R", "Solar radiance computed with horizontal direct"
                                " irradiance")
        self._t = NumericOption("t", "Turbuity factor")
        self._a = NumericOption("a", "Site latitude")
        self._o = NumericOption("o", "Site longitude")
        self._m = NumericOption("m", "Standard meridian")
        self._ang = TupleOption("ang", "Altitude & azimuth", value=None, length=2,
                                numtype=float)
        self._on_setattr_check = True

    def _on_setattr(self):
        """This method executes after setting each new attribute.

        Use this method to add checks that are necessary for OptionCollection. 
        """

        if self._t.is_set:
            assert (self._t.is_set >= 1.0), \
                'Value less than 1.0 are physically impossible. Got %.' % (self._t.value)

