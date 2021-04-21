from honeybee_radiance_command.gensky import Gensky
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    gensky = Gensky(1, 21, 23.5)

    gensky.to_radiance()
    assert gensky.command == 'gensky'
    assert gensky.options.to_radiance() == ''


def test_assignment():
    """Test assigning options."""
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
    """Test form_ang method."""
    gensky = Gensky.from_ang((23.33, 45.56))

    gensky.options.s = '+'
    gensky.options.g = 0.1
    assert gensky.to_radiance() == 'gensky -ang 23.33 45.56 -g 0.1 +s'
    gensky.output = 'ang.sky'
    assert gensky.output == 'ang.sky'
    assert gensky.to_radiance() == 'gensky -ang 23.33 45.56 -g 0.1 +s > ang.sky'


def test_assignment_both_methods():
    """Gensky command can be used either with method one: month, day and time inputs or 
    using method two: -ang option with altitude and azimuth values. Both methods can
    not be used together."""
    gensky = Gensky(1, 21, 23.5)

    gensky.options.ang = (23.33, 45.56)
    with pytest.raises(ValueError):
        gensky.to_radiance()

    gensky.options.ang = None
    assert gensky.to_radiance() == 'gensky 1 21 23:30'


def test_stdin():
    """Test stdin."""
    gensky = Gensky(month=1, day=21, time='23:33')

    gensky.time_zone = 'EST'
    gensky.solar_time = True
    gensky.output = 'test.sky'
    assert gensky.to_radiance(stdin_input=True) == 'gensky > test.sky'


def test_assignment_not_allowed():
    """Test assignments of arguments that are not allowed to be assigned concurrently."""
    gensky = Gensky.from_ang((23.33, 45.56))

    with pytest.raises(ValueError):
        gensky.options.s = '+'
        gensky.options.i = '+'


def test_assignment_warning():
    """Test warning when one of the argument will be ignored."""
    gensky = Gensky.from_ang((23.33, 45.56))

    with pytest.warns(Warning):
        gensky.options.m = -18.00


def test_missing_arguments():
    """Test validate command."""
    gensky = Gensky()

    with pytest.raises(exceptions.MissingArgumentError):
        # missing month
        gensky.to_radiance()

    gensky.month = 1
    with pytest.raises(exceptions.MissingArgumentError):
        # missing day
        gensky.to_radiance()

    gensky.day = 21
    with pytest.raises(exceptions.MissingArgumentError):
        # missing time
        gensky.to_radiance()

    gensky.time = 21.5

    assert gensky.to_radiance() == 'gensky 1 21 21:30'
    