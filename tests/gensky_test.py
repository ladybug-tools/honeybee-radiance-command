from honeybee_radiance_command.gensky import Gensky
import pytest


def test_defaults():
    gensky = Gensky(1, 21, 23.33)
    assert gensky.command == 'gensky'
    assert gensky.options.to_radiance() == ''


def test_assignment():
    gensky = Gensky(1, 21, 23.23)

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    assert gensky.input == '+1 21 23.23EST'
    assert gensky.to_radiance() == 'gensky +1 21 23.23EST'
    gensky.output = 'test.sky'
    assert gensky.output == 'test.sky'
    assert gensky.to_radiance() == 'gensky +1 21 23.23EST > test.sky'


def test_stdin():
    gensky = Gensky(1, 21, 23.23)

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    gensky.output = 'test.sky'
    assert gensky.to_radiance(stdin_input=True) == 'gensky > test.sky'

