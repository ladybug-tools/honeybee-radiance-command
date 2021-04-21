from honeybee_radiance_command.pcond import Pcond
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pcond = Pcond()
    assert pcond.command == 'pcond'
    assert pcond.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    pcond = Pcond()

    pcond.input = 'image.hdr'
    assert pcond.input == 'image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr'
    pcond.output = 'conditioned_image.hdr'
    assert pcond.output == 'conditioned_image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr > conditioned_image.hdr'


def test_options():
    """Test options."""
    pcond = Pcond()

    pcond.input = 'image.hdr'
    pcond.options.e = '+1.2'
    assert pcond.to_radiance() == 'pcond -e +1.2 image.hdr'
    pcond.options.p = (0.580, 0.340, 0.281, 0.570, 0.153, 0.079, 0.333, 0.333)
    assert pcond.to_radiance() == (
        'pcond -e +1.2 -p 0.58 0.34 0.281 0.57 0.153 0.079 0.333 0.333 image.hdr')
    with pytest.raises(ValueError):
        pcond.options.f = 'film.cal'


def test_stdin():
    """Test stdin."""
    pcond = Pcond()

    pcond.input = 'image.hdr'
    pcond.output = 'conditioned.hdr'
    assert pcond.to_radiance(stdin_input=True) == ('pcond > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    pcond = Pcond()
    with pytest.raises(exceptions.MissingArgumentError):
        pcond.to_radiance()
    pcond.input = 'image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr'
