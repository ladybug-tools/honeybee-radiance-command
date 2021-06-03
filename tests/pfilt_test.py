from honeybee_radiance_command.pfilt import Pfilt
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pfilt = Pfilt()
    assert pfilt.command == 'pfilt'
    assert pfilt.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    pfilt = Pfilt()

    pfilt.input = 'image.hdr'
    assert pfilt.input == 'image.hdr'
    assert pfilt.to_radiance() == 'pfilt image.hdr'
    pfilt.output = 'conditioned_image.hdr'
    assert pfilt.output == 'conditioned_image.hdr'
    assert pfilt.to_radiance() == 'pfilt image.hdr > conditioned_image.hdr'


def test_options():
    """Test options."""
    pfilt = Pfilt()

    pfilt.input = 'image.hdr'
    pfilt.options._1 = True
    assert pfilt.to_radiance() == 'pfilt -1 image.hdr'


def test_stdin():
    """Test stdin."""
    pfilt = Pfilt()

    pfilt.input = 'image.hdr'
    pfilt.output = 'conditioned.hdr'
    assert pfilt.to_radiance(stdin_input=True) == ('pfilt > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    pfilt = Pfilt()
    with pytest.raises(exceptions.MissingArgumentError):
        pfilt.to_radiance()
    pfilt.input = 'image.hdr'
    assert pfilt.to_radiance() == 'pfilt image.hdr'
