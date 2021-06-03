from honeybee_radiance_command.evalglare import Evalglare
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    evalglare = Evalglare()
    assert evalglare.command == 'evalglare'
    assert evalglare.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    evalglare = Evalglare()

    evalglare.input = 'image.hdr'
    assert evalglare.input == 'image.hdr'
    assert evalglare.to_radiance() == 'evalglare image.hdr'
    evalglare.output = 'conditioned_image.hdr'
    assert evalglare.output == 'conditioned_image.hdr'
    assert evalglare.to_radiance() == 'evalglare image.hdr > conditioned_image.hdr'


def test_options():
    """Test options."""
    evalglare = Evalglare()

    evalglare.input = 'image.hdr'
    evalglare.options.c = 'checkfile.hdr'
    evalglare.options.d = True
    assert evalglare.to_radiance() == 'evalglare -c checkfile.hdr -d image.hdr'


def test_stdin():
    """Test stdin."""
    evalglare = Evalglare()

    evalglare.input = 'image.hdr'
    evalglare.output = 'conditioned.hdr'
    assert evalglare.to_radiance(stdin_input=True) == ('evalglare > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    evalglare = Evalglare()
    with pytest.raises(exceptions.MissingArgumentError):
        evalglare.to_radiance()
    evalglare.input = 'image.hdr'
    assert evalglare.to_radiance() == 'evalglare image.hdr'
