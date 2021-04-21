from honeybee_radiance_command.gendaylit import Gendaylit
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    gendaylit = Gendaylit(month=1, day=21, time=23.5)
    assert gendaylit.command == 'gendaylit'
    assert gendaylit.options.to_radiance() == ''


def test_assignment():
    """Test assigning options."""
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
    """Test form_ang method."""
    gendaylit = Gendaylit.from_ang((23.33, 45.56))

    gendaylit.options.P = (6.3, 0.12)
    assert gendaylit.to_radiance() == ('gendaylit -P 6.3 0.12 -ang 23.33 45.56')
    gendaylit.output = 'ang.sky'
    assert gendaylit.output == 'ang.sky'
    assert gendaylit.to_radiance() == ('gendaylit -P 6.3 0.12 -ang 23.33 45.56'
                                       ' > ang.sky')


def test_assignment_not_allowed():
    """Test assignments of arguments that are not allowed to be assigned concurrently."""
    gendaylit = Gendaylit.from_ang((23.33, 45.56))

    gendaylit.options.W = (840, 135)
    with pytest.raises(ValueError):
        gendaylit.options.L = (165, 200)


def test_assignment_error():
    """Test warning when one of the argument will be ignored."""
    gendaylit = Gendaylit.from_ang((23.33, 45.56))

    with pytest.raises(ValueError):
        gendaylit.options.m = -18.00


def test_stdin():
    """Test stdin."""
    gendaylit = Gendaylit(month=1, day=21, time='23:33')

    gendaylit.time_zone = 'EST'
    gendaylit.solar_time = True
    gendaylit.output = 'test.sky'
    assert gendaylit.to_radiance(stdin_input=True) == 'gendaylit > test.sky'


def test_missing_arguments():
    """Test validate command."""
    gendaylit = Gendaylit()

    with pytest.raises(exceptions.MissingArgumentError):
        # missing month
        gendaylit.to_radiance()

    gendaylit.month = 1
    with pytest.raises(exceptions.MissingArgumentError):
        # missing day
        gendaylit.to_radiance()

    gendaylit.day = 21
    with pytest.raises(exceptions.MissingArgumentError):
        # missing time
        gendaylit.to_radiance()

    gendaylit.time = 21.5

    assert gendaylit.to_radiance() == 'gendaylit 1 21 21:30'
