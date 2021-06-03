from honeybee_radiance_command.falsecolor import Falsecolor
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    falsecolor = Falsecolor()
    assert falsecolor.command == 'falsecolor'
    assert falsecolor.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    falsecolor = Falsecolor()

    falsecolor.input = 'image.hdr'
    assert falsecolor.input == 'image.hdr'
    assert falsecolor.to_radiance() == 'falsecolor -i image.hdr'
    falsecolor.output = 'conditioned_image.hdr'
    assert falsecolor.output == 'conditioned_image.hdr'
    assert falsecolor.to_radiance() == 'falsecolor -i image.hdr > conditioned_image.hdr'


def test_options():
    """Test options."""
    falsecolor = Falsecolor()

    falsecolor.input = 'image.hdr'
    falsecolor.options.pal = 'spec'
    falsecolor.options.s = 'auto'
    falsecolor.options.l = 'lux'
    falsecolor.options.cl = True
    assert falsecolor.to_radiance() == 'falsecolor -cl -l lux -pal spec -s auto -i image.hdr'


def test_stdin():
    """Test stdin."""
    falsecolor = Falsecolor()

    falsecolor.input = 'image.hdr'
    falsecolor.output = 'conditioned.hdr'
    assert falsecolor.to_radiance(stdin_input=True) == ('falsecolor > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    falsecolor = Falsecolor()
    with pytest.raises(exceptions.MissingArgumentError):
        falsecolor.to_radiance()
    falsecolor.input = 'image.hdr'
    assert falsecolor.to_radiance() == 'falsecolor -i image.hdr'
