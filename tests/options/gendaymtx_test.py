"""Test gendaymtx options."""
from honeybee_radiance_command.options.gendaymtx import GendaymtxOptions
import pytest
import honeybee_radiance_command._exception as exceptions


def test_default():
    options = GendaymtxOptions()
    assert options.to_radiance() == ''


def test_assignment():
    options = GendaymtxOptions()
    options.v = True
    assert options.v == True
    assert options.to_radiance() == '-v'


def test_exclusives_m():
    opt = GendaymtxOptions()
    opt.d = True
    with pytest.raises(exceptions.ExclusiveOptionsError):
        opt.s = True


def test_multiple_assignment():
    options = GendaymtxOptions()
    options.o = 'f'
    options.O = '1'
    assert '-O1' in options.to_radiance()
    assert '-of' in options.to_radiance()


def test_from_string():
    opt = GendaymtxOptions()
    opt_str = '-n -D sunpath.mtx -M suns.mod -O1 -r 0.0 -v -m 4'

    opt.update_from_string(opt_str)
    assert opt.n == True
    assert opt.D == 'sunpath.mtx'
    assert opt.M == 'suns.mod'
    assert opt.O == '1'
    assert opt.r == 0
    assert opt.v == True
    assert opt.m == 4
