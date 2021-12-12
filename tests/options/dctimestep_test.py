"""Test dctimestep options"""
from honeybee_radiance_command.options.dctimestep import DctimestepOptions
import pytest


def test_defaults():
    options = DctimestepOptions()
    assert options.to_radiance() == ''


def test_assignment():
    options = DctimestepOptions()
    options.op_fmt = 'f'
    assert options.op_fmt == 'f'
    assert options.to_radiance() == '-of'


def test_multiple_assignment():
    options = DctimestepOptions()
    options.i = 'f'
    options.n = '1'
    assert '-if' in options.to_radiance()
    assert '-n 1' in options.to_radiance()


def test_invalid_assignment():
    options = DctimestepOptions()
    with pytest.raises(AttributeError):
        options.dc = 30
    with pytest.raises(TypeError):
        options.n = "One"
