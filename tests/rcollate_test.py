from honeybee_radiance_command.rcollate import Rcollate
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    rcollate = Rcollate()
    assert rcollate.command == 'rcollate'
    assert rcollate.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    rcollate = Rcollate()

    rcollate.input = 'matrix.mtx'
    assert rcollate.input == 'matrix.mtx'
    assert rcollate.to_radiance() == 'rcollate matrix.mtx'
    rcollate.output = 'transposed_matrix.mtx'
    assert rcollate.output == 'transposed_matrix.mtx'
    assert rcollate.to_radiance() == 'rcollate matrix.mtx > transposed_matrix.mtx'


def test_options():
    """Test options."""
    rcollate = Rcollate()
    rcollate.input = 'matrix.mtx'
    rcollate.options.t = True
    assert rcollate.to_radiance() == 'rcollate -t matrix.mtx'



def test_validation():
    """Test if exception is raised for missing arguments."""
    rcollate = Rcollate()
    with pytest.raises(exceptions.MissingArgumentError):
        rcollate.to_radiance()
    rcollate.input = 'matrix.mtx'
    assert rcollate.to_radiance() == 'rcollate matrix.mtx'
