from honeybee_radiance_command.ra_gif import Ra_GIF
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    ra_gif = Ra_GIF()
    
    assert ra_gif.command == 'ra_gif'
    assert ra_gif.options.to_radiance() == ''


def test_assignment():
    """Test assignments."""
    ra_gif = Ra_GIF()

    ra_gif.input = 'image.hdr'
    assert ra_gif.input == 'image.hdr'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr'
    ra_gif.output = 'image.gif'
    assert ra_gif.output == 'image.gif'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr > image.gif'


def test_options():
    """Test assignment of some of the options."""
    ra_gif = Ra_GIF()

    ra_gif.input = 'image.hdr'
    ra_gif.options.d = True
    assert ra_gif.to_radiance() == 'ra_gif -d image.hdr'
    with pytest.raises(AssertionError):
        ra_gif.options.c = 257.2


def test_stdin():
    """Test stdin."""
    ra_gif = Ra_GIF()

    ra_gif.input = 'image.hdr'
    ra_gif.output = 'image.gif'
    assert ra_gif.to_radiance(stdin_input=True) == ('ra_gif > image.gif')


def test_validation():
    """Test if errors are raised on missing arguments."""
    ra_gif = Ra_GIF()

    with pytest.raises(exceptions.MissingArgumentError):
        ra_gif.to_radiance()
    ra_gif.input = 'image.hdr'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr'
    
