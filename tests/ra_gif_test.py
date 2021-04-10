from honeybee_radiance_command.ra_gif import Ra_GIF
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    ra_gif = Ra_GIF()
    assert ra_gif.command == 'ra_gif'
    assert ra_gif.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        ra_gif.to_radiance()


def test_assignment():
    ra_gif = Ra_GIF()

    ra_gif.input = 'image.hdr'
    assert ra_gif.input == 'image.hdr'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr'
    ra_gif.output = 'image.gif'
    assert ra_gif.output == 'image.gif'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr image.gif'


def test_stdin():
    ra_gif = Ra_GIF()
    ra_gif.input = 'image.hdr'
    ra_gif.output = 'image.gif'
    assert ra_gif.to_radiance(stdin_input=True) == 'ra_gif image.gif'


def test_validation():
    ra_gif = Ra_GIF()
    with pytest.raises(exceptions.MissingArgumentError):
        ra_gif.to_radiance()
    ra_gif.input = 'image.hdr'
    assert ra_gif.to_radiance() == 'ra_gif image.hdr'
    
