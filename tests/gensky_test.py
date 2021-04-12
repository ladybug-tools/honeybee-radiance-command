from honeybee_radiance_command.gensky import Gensky
import pytest


def test_defaults():
    gensky = Gensky(month=1, day=21, time=23.33, ang=None)
    assert gensky.command == 'gensky'
    assert gensky.options.to_radiance() == ''


def test_assignment():
    gensky = Gensky(month=1, day=21, time=23.33, ang=None)

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    print(gensky.solar_time)
    assert gensky.input == '+1 21 23.33EST'
    assert gensky.to_radiance() == 'gensky +1 21 23.33EST'
    gensky.output = 'test.sky'
    assert gensky.output == 'test.sky'
    assert gensky.to_radiance() == 'gensky +1 21 23.33EST > test.sky'


def test_stdin():
    gensky = Gensky(month=1, day=21, time=23.33, ang=None)

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    gensky.output = 'test.sky'
    assert gensky.to_radiance(stdin_input=True) == 'gensky > test.sky'

