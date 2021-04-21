from honeybee_radiance_command.pcomb import Pcomb
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pcomb = Pcomb()

    assert pcomb.command == 'pcomb'
    assert pcomb.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    pcomb = Pcomb()

    pcomb.input = ['image1.hdr', 'image2.hdr']
    assert pcomb.input == 'image1.hdr image2.hdr'
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr'
    pcomb.output = 'combined.hdr'
    assert pcomb.output == 'combined.hdr'
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr > combined.hdr'


def test_assignment_options():
    """Test assignning options."""
    pcomb = Pcomb()

    pcomb.input = ['image1.hdr', 'image2.hdr']
    pcomb.options.h = True
    pcomb.options.c = (0.125, 0.133, 0.250)
    assert pcomb.to_radiance() == 'pcomb -c 0.125 0.133 0.25 -h image1.hdr image2.hdr'
    with pytest.raises(AssertionError):
        # Making sure less than zero values are not able to be assigned to resolution
        pcomb.options.x = 0.12


def test_stdin():
    """Test stdin."""
    pcomb = Pcomb()

    pcomb.input = ['image1.hdr', 'image2.hdr']
    pcomb.output = 'combined.hdr'
    assert pcomb.to_radiance(stdin_input=True) == ('pcomb > combined.hdr')


def test_validation():
    """Validate error for missing argument."""
    pcomb = Pcomb()

    with pytest.raises(exceptions.MissingArgumentError):
        pcomb.to_radiance()

    pcomb.input = ['image1.hdr', 'image2.hdr']
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr'
