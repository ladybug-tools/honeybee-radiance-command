# coding: utf-8
import os

from .optionbase import (
    OptionCollection, BoolOption, StringOption, StringOptionJoined,
    TupleOption, NumericOption, FileOption
)
import honeybee_radiance_command._exception as exceptions


class Ies2radOptions(OptionCollection):
    """ies2rad options.

    Also see:
    https://radsite.lbl.gov/radiance/man_html/ies2rad.1.html
    """

    __slots__ = (
        '_l', '_p', '_o', '_s', '_d', '_i', '_g',
        '_f', '_t', '_c', '_u', '_m'
    )

    def __init__(self):
        """ies2rad command options."""
        OptionCollection.__init__(self)
        self._on_setattr_check = False

        self._l = StringOption('l', 'Library directory path - default: current working directory')
        self._p = StringOption('p', 'Library subdirectory path - default: empty')
        self._o = StringOption('o', 'Output file name root')
        self._s = BoolOption('s', 'Send scene information to stdout')
        self._d = StringOptionJoined('d', 'Output units (e.g. m, m/1000)')
        self._i = NumericOption(
            'i',
            'Ignore IES geometry and use illum sphere of given radius',
            min_value=0
        )
        self._g = BoolOption('g', 'Compile MGF geometry into a separate octree')
        self._f = FileOption('f', 'Lamp lookup table file')
        self._t = StringOption('t', 'Force lamp type for all input files')
        self._c = TupleOption(
            'c',
            'Default lamp RGB color',
            length=3,
            numtype=float
        )
        self._u = StringOption('u', 'Default lamp color from lookup table')
        self._m = NumericOption('m', 'Multiply output quantities by factor')

        self._on_setattr_check = True

    def _on_setattr(self):
        """Validate mutually exclusive options."""
        if self.c.is_set and self.u.is_set:
            raise exceptions.ExclusiveOptionsError(self.command, 'c', 'u')
        if self.i.is_set and self.g.is_set:
            raise exceptions.ExclusiveOptionsError(self.command, 'i', 'g')
        if self.p.is_set and os.path.isabs(self.p.value):
            raise exceptions.InvalidValueError(
                self.command,
                '-p must be a relative path (subdirectory of -l)'
            )

    @property
    def l(self):
        """Library directory path."""
        return self._l

    @l.setter
    def l(self, value):
        self._l.value = value

    @property
    def p(self):
        """Library subdirectory path."""
        return self._p

    @p.setter
    def p(self, value):
        self._p.value = value

    @property
    def o(self):
        """Output file name root."""
        return self._o

    @o.setter
    def o(self, value):
        self._o.value = value

    @property
    def s(self):
        """Send scene information to standard output."""
        return self._s

    @s.setter
    def s(self, value):
        self._s.value = value

    @property
    def d(self):
        """Output units."""
        return self._d

    @d.setter
    def d(self, value):
        self._d.value = value

    @property
    def i(self):
        """Ignore IES geometry and use an illum sphere."""
        return self._i

    @i.setter
    def i(self, value):
        self._i.value = value

    @property
    def g(self):
        """Compile MGF geometry into a separate octree."""
        return self._g

    @g.setter
    def g(self, value):
        self._g.value = value

    @property
    def f(self):
        """Lamp lookup table file."""
        return self._f

    @f.setter
    def f(self, value):
        self._f.value = value

    @property
    def t(self):
        """Force lamp type."""
        return self._t

    @t.setter
    def t(self, value):
        self._t.value = value

    @property
    def c(self):
        """Default lamp RGB color."""
        return self._c

    @c.setter
    def c(self, value):
        self._c.value = value

    @property
    def u(self):
        """Default lamp color from lookup table."""
        return self._u

    @u.setter
    def u(self, value):
        self._u.value = value

    @property
    def m(self):
        """Multiply output quantities by factor."""
        return self._m

    @m.setter
    def m(self, value):
        self._m.value = value
