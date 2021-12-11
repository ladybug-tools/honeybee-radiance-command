"""Test rcollate options."""
from honeybee_radiance_command.options.rcollate import RcollateOptions
import pytest


def test_default():
    options = RcollateOptions()
    assert options.to_radiance() == ''


def test_assignment():
    options = RcollateOptions()
    options.h = ''
    assert options.to_radiance() == '-h'


def test_multiple_assignment():
    options = RcollateOptions()
    options.h = 'i'
    assert options.to_radiance() == '-hi'
    options.h = 'o'
    assert options.to_radiance() == '-ho'


def test_string_joined():
    options = RcollateOptions()
    options.fa = 6
    assert options.to_radiance() == '-fa6'
    options.fa = ''
    assert options.to_radiance() == '-fa'


def test_exclusives_m():
    options = RcollateOptions()
    options.fa = 6
    with pytest.raises(ValueError):
        options.fd = 6


def test_from_string():
    opt = RcollateOptions()
    opt_str = '-h -oc 8760 -fa3'

    opt.update_from_string(opt_str)
    assert opt.h == ''
    assert opt.oc == 8760
    assert opt.fa == '3'
