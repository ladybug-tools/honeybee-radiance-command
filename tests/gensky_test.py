from honeybee_radiance_command.gensky import Gensky
import pytest


def test_defaults():
    gensky = Gensky(month=1, day=21, time=23.5)
    assert gensky.command == 'gensky'
    assert gensky.options.to_radiance() == ''


def test_assignment():
    gensky = Gensky(month=1, day=21, time=23.5)

    gensky.options.g = 0.1
    assert gensky.month == 1
    assert gensky.day == 21
    assert gensky.time == '23:30'
    gensky.time_zone = 'EST'
    gensky.solar_time = True
    assert gensky.input == '+1 21 23:30EST'
    assert gensky.to_radiance() == 'gensky -g 0.1 +1 21 23:30EST'
    gensky.output = 'test.sky'
    assert gensky.output == 'test.sky'
    assert gensky.to_radiance() == 'gensky -g 0.1 +1 21 23:30EST > test.sky'


def test_assignment_ang():
    gensky = Gensky.from_ang((23.33, 45.56))
    gensky.options.s = '+'
    gensky.options.g = 0.1
    assert gensky.to_radiance() == 'gensky -ang 23.33 45.56 -g 0.1 +s'
    gensky.output = 'ang.sky'
    assert gensky.output == 'ang.sky'
    assert gensky.to_radiance() == 'gensky -ang 23.33 45.56 -g 0.1 +s > ang.sky'


def test_stdin():
    gensky = Gensky(month=1, day=21, time='23:33')

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    gensky.output = 'test.sky'
    assert gensky.to_radiance(stdin_input=True) == 'gensky > test.sky'


def test_missing_arguments():
    gensky = Gensky()
    assert gensky.month == None
    