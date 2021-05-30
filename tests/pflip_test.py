from honeybee_radiance_command.pflip import Pflip
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pflip = Pflip()
    assert pflip.command == 'pflip'
    assert pflip.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    pflip = Pflip()

    pflip.input = 'image.hdr'
    assert pflip.input == 'image.hdr'
    assert pflip.to_radiance() == 'pflip image.hdr'
    pflip.output = 'conditioned_image.hdr'
    assert pflip.output == 'conditioned_image.hdr'
    assert pflip.to_radiance() == 'pflip image.hdr > conditioned_image.hdr'


def test_options():
    """Test options."""
    pflip = Pflip()

    pflip.input = 'image.hdr'
    pflip.options.h = True
    assert pflip.to_radiance() == 'pflip -h image.hdr'


def test_stdin():
    """Test stdin."""
    pflip = Pflip()

    pflip.input = 'image.hdr'
    pflip.output = 'conditioned.hdr'
    assert pflip.to_radiance(stdin_input=True) == ('pflip > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    pflip = Pflip()
    with pytest.raises(exceptions.MissingArgumentError):
        pflip.to_radiance()
    pflip.input = 'image.hdr'
    assert pflip.to_radiance() == 'pflip image.hdr'
