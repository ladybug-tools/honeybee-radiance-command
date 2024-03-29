"""Test Radiance commands options base classes."""
from honeybee_radiance_command.options import StringOptionJoined, NumericOption, \
    IntegerOption, BoolOption,  OptionCollection, StringOption
import pytest
import honeybee_radiance_command._exception as exceptions


def test_string_option():
    view_type = StringOptionJoined(
        'vt', 'view type', valid_values=['v', 'h', 'l', 'a'])
    # test default
    assert view_type.to_radiance() == ''
    # test assignment
    view_type.value = 'v'
    assert view_type.to_radiance() == '-vtv'
    # test invalid value
    with pytest.raises(exceptions.InvalidValueError):
        view_type.value = 'm'
    # check the value is still there
    assert view_type.to_radiance() == '-vtv'


def test_numeric_option():
    aa = NumericOption('aa', 'ambient accuracy', min_value=0)
    assert aa.to_radiance() == ''

    aa.value = 0
    assert aa.to_radiance() == '-aa 0.0'

    with pytest.raises(TypeError):
        aa.value = 'm'

    with pytest.raises(AssertionError):
        aa.value = -10


def test_integer_option():
    ab = IntegerOption('ab', 'ambient bounces', min_value=0)
    assert ab.to_radiance() == ''

    ab.value = 0
    assert ab.to_radiance() == '-ab 0'

    ab.value = 6.21
    assert ab.to_radiance() == '-ab 6'

    with pytest.raises(TypeError):
        ab.value = 'm'

    with pytest.raises(AssertionError):
        ab.value = -10


def test_bool_option():
    ld = BoolOption('ld', 'limit distance')
    assert ld.to_radiance() == ''

    ld.value = True
    assert ld.to_radiance() == '-ld'

    ld.value = False
    assert ld.to_radiance() == '-ld-'


class OptionsTestClass(OptionCollection):

    __slots__ = ('_ab', '_aa', '_ld', '_fa', '_as', '_o')

    def __init__(self):
        OptionCollection.__init__(self)
        self._ab = IntegerOption('ab', 'ambient bounces', min_value=0)
        self._aa = NumericOption('aa', 'ambient accuracy', min_value=0)
        self._ld = BoolOption('ld', 'limit distance')
        self._fa = StringOptionJoined('fa', 'output format', valid_values=['a', 'd'])
        self._as = IntegerOption('as', 'ambient somthing!', min_value=0)
        self._o = StringOption('o', 'output file format.')

    @property
    def ab(self):
        return self._ab.value

    @ab.setter
    def ab(self, value):
        self._ab.value = value

    @property
    def aa(self):
        return self._aa.value

    @aa.setter
    def aa(self, value):
        self._aa.value = value

    @property
    def fa(self):
        return self._fa.value

    @fa.setter
    def fa(self, value):
        self._fa.value = value

    @property
    def ld(self):
        return self._ld.value

    @ld.setter
    def ld(self, value):
        self._ld.value = value

    @property
    def as_(self):
        return self._as.value

    @as_.setter
    def as_(self, value):
        self._as.value = value

    @property
    def o(self):
        """Format output."""
        return self._o

    @o.setter
    def o(self, value):
        self._o.value = value


def test_collection():
    options_test = OptionsTestClass()
    options_test.ab = 2
    options_test.update_from_string('-ab 5 -ld- -ad 2500 -as 128')
    assert options_test.ab == 5
    assert options_test.ld == False
    assert options_test.to_radiance() == '-ab 5 -as 128 -ld- -ad 2500'

    options_test.ab = None
    options_test.ld = True
    assert options_test.to_radiance() == '-as 128 -ld -ad 2500'

    options_test.o = '%%s.vmtx'
    assert '-o %s.vmtx' in options_test.to_radiance()
    with pytest.raises(AttributeError):
        options_test.ad = 2400
