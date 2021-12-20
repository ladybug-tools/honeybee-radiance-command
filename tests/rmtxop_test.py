from honeybee_radiance_command.rmtxop import Rmtxop
import pytest
import honeybee_radiance_command._exception as exceptions
import os


def test_defaults():
    """Test command."""
    rmtxop = Rmtxop()

    assert rmtxop.command == 'rmtxop'
    assert rmtxop.options.to_radiance() == ''


def test_assignment():
    """Test assignments."""
    rmtxop = Rmtxop()

    rmtxop.matrices = ['dc.mtx', 'sky.mtx']
    assert rmtxop.to_radiance() == 'rmtxop dc.mtx sky.mtx'
    rmtxop.output = 'output.mtx'
    assert rmtxop.output == 'output.mtx'
    assert rmtxop.to_radiance() == 'rmtxop dc.mtx sky.mtx > output.mtx'


def test_options():
    """Test assignment of some of the options."""
    rmtxop = Rmtxop()
    rmtxop.matrices = ['daylight.mtx']
    rmtxop.options.v = True
    assert rmtxop.to_radiance() == 'rmtxop -v daylight.mtx'
    with pytest.raises(exceptions.InvalidValueError):
        rmtxop.options.f = 'n'


def test_param_lengths():
    """For multiple matrices and parameters check if parameters are correctly assigned"""
    rmtxop = Rmtxop()
    rmtxop.matrices = ['daylight.mtx']
    rmtxop.transposes = True
    rmtxop.scalars = 2
    rmtxop.validate()
    assert rmtxop.to_radiance() == 'rmtxop -t -s 2.0 daylight.mtx'
    rmtxop.transposes = [True]
    rmtxop.scalars = None
    # This should raise an Assertion Error because the assumption is that these are
    # three separate transform.
    rmtxop.transforms = [2, 3, 4]
    with pytest.raises(AssertionError):
        rmtxop.validate()
    # The solution, to assign these factors to the same matrix, is to put them in a
    # nested list.
    rmtxop.transforms = [[2, 3, 4]]
    assert rmtxop.to_radiance() == 'rmtxop -t -c 2.0 3.0 4.0 daylight.mtx'

    # Now trying multiple matrices
    rmtxop.matrices = ['daylight.mtx', 'sky.mtx']
    # Assertion error will be raised because the transpose and transform parameters are
    # still assigned for a single matrix.
    with pytest.raises(AssertionError):
        rmtxop.validate()
    # The solution is to incorporate transpose and transforms for both matrices.
    rmtxop.transforms = [[2, 3, 4], None]
    rmtxop.transposes = [True, None]
    assert rmtxop.to_radiance() == 'rmtxop -t -c 2.0 3.0 4.0 daylight.mtx sky.mtx'


def test_transforms_scalars():
    """Check if scalar and transform is assigned for the same matrix"""
    rmtxop = Rmtxop()
    rmtxop.matrices = ['sky1.mtx', 'sky2.mtx']
    rmtxop.scalars = [11, 12]
    assert rmtxop.to_radiance() == 'rmtxop -s 11.0 sky1.mtx -s 12.0 sky2.mtx'
    rmtxop.scalars = [None, 12]
    assert rmtxop.to_radiance() == 'rmtxop sky1.mtx -s 12.0 sky2.mtx'
    rmtxop.transforms = [(1, 2, 3), (1, 2, 3)]
    # Don't allow scalar and transform to be assigned to the same matrix.
    with pytest.raises(Exception):
        rmtxop.validate()
    rmtxop.transforms = [(1, 2, 3), None]
    rmtxop.validate()
    assert rmtxop.to_radiance() == 'rmtxop -c 1.0 2.0 3.0 sky1.mtx -s 12.0 sky2.mtx'


def test_multiplication_operator():
    """This operator will be different for Windows and Unix."""
    """Test assignments."""
    rmtxop = Rmtxop()
    rmtxop.matrices = ['dc.mtx', 'sky.mtx']
    rmtxop.operators = ['*']
    if os.name == 'posix':
        assert rmtxop.to_radiance() == "rmtxop dc.mtx '*' sky.mtx"
    else:
        assert rmtxop.to_radiance() == 'rmtxop dc.mtx * sky.mtx'


def test_input_matrix_limit():
    """More than for matrices are not allowed as inputs."""
    rmtxop = Rmtxop()
    rmtxop.matrices = ['dc1.mtx', 'dc2.mtx', 'dc3.mtx', 'dc4.mtx', 'dc5.mtx']
    with pytest.raises(AssertionError):
        rmtxop.validate()
