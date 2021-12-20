"""Test rmtxop options."""
from honeybee_radiance_command.options.rmtxop import RmtxopOptions
import pytest
import honeybee_radiance_command._exception as exceptions


def test_default():
    options = RmtxopOptions()
    assert options.to_radiance() == ''


def test_assignment():
    options = RmtxopOptions()
    options.v = True
    assert options.v == True
    assert options.to_radiance() == '-v'


def test_reassignment():
    options = RmtxopOptions()
    options.v = True
    assert options.v == True
    assert options.to_radiance() == '-v'
    # remove assigned values
    options.v = None
    assert options.v == None
    assert options.to_radiance() == ''


def test_incorrect_assignment():
    options = RmtxopOptions()
    options.f = 'a'
    assert options.to_radiance() == '-fa'
    with pytest.raises(exceptions.InvalidValueError):
        options.f = 'k'


def test_from_string():
    options = RmtxopOptions()
    options.update_from_string('-v')
    assert options.v == True
