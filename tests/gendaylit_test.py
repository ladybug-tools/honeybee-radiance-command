from honeybee_radiance_command.gendaylit import Gendaylit
import pytest


def test_defaults():
    gendaylit = Gendaylit(month=1, day=21, time=23.5)
    assert gendaylit.command == 'gendaylit'
    assert gendaylit.options.to_radiance() == ''


def test_assignment():
    gendaylit = Gendaylit(month=1, day=21, time=23.5)

    gendaylit.options.g = 0.1
    gendaylit.options.O = 2
    gendaylit.options.s = True
    assert gendaylit.month == 1
    assert gendaylit.day == 21
    assert gendaylit.time == '23:30'
    gendaylit.time_zone = 'EST'
    gendaylit.solar_time = True
    assert gendaylit.input == '+1 21 23:30EST'
    assert gendaylit.to_radiance() == 'gendaylit -O 2 -g 0.1 -s +1 21 23:30EST'
    gendaylit.output = 'test.sky'
    assert gendaylit.output == 'test.sky'
    assert gendaylit.to_radiance() == ('gendaylit -O 2 -g 0.1 -s +1 21 23:30EST'
                                       ' > test.sky')


def test_assignment_ang():
    gendaylit = Gendaylit.from_ang((23.33, 45.56))

    gendaylit.options.P = (6.3, 0.12)
    assert gendaylit.to_radiance() == ('gendaylit -P 6.3 0.12 -ang 23.33 45.56')
    gendaylit.output = 'ang.sky'
    assert gendaylit.output == 'ang.sky'
    assert gendaylit.to_radiance() == ('gendaylit -P 6.3 0.12 -ang 23.33 45.56'
                                       ' > ang.sky')


def test_assignment_not_allowed():
    # Test assignments of arguments that are not allowed to be assigned concurrently
    gendaylit = Gendaylit.from_ang((23.33, 45.56))

    try:
        gendaylit.options.W = (840, 135)
        gendaylit.options.L = (165, 200)
        gendaylit.to_radiance()
    except ValueError:
        pass


def test_stdin():
    gendaylit = Gendaylit(month=1, day=21, time='23:33')

    gendaylit.time_zone = 'EST'
    gendaylit.solar_time = True
    gendaylit.output = 'test.sky'
    assert gendaylit.to_radiance(stdin_input=True) == 'gendaylit > test.sky'


def test_missing_arguments():
    gendaylit = Gendaylit()
    assert gendaylit.month is None
