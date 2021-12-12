"""Rmtxop parameters"""
from .optionbase import OptionCollection, BoolOption, StringOptionJoined


class RmtxopOptions(OptionCollection):
    """
    [-v] [-f[afdc]]

    Also see: https://www.radiance-online.org/learning/documentation/manual-pages/pdfs/rmtxop.pdf
    """

    __slots__ = ('_v', '_f',)

    def __init__(self):
        """rmtxop command options."""
        OptionCollection.__init__(self)
        self._on_setattr_check = False
        self._v = BoolOption('v', 'Turn on verbose reporting. Defaults to False')
        self._f = StringOptionJoined('f', 'output data format. Set "a" for ASCII, "d" for'
                                          ' binary doubles, "f" floats and "c" for RGBE'
                                          'colors', valid_values=('a', 'f', 'd', 'c'))

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        self._f = value
