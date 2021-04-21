from honeybee_radiance_command.rpict import Rpict
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    rpict = Rpict()

    assert rpict.command == 'rpict'
    assert rpict.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    assert rpict.octree == 'input.oct'
    rpict.view = 'view.vf'
    assert rpict.view == 'view.vf'
    assert rpict.to_radiance() == 'rpict input.oct < view.vf'
    rpict.output = 'results.dat'
    assert rpict.output == 'results.dat'
    assert rpict.to_radiance() == 'rpict input.oct < view.vf > results.dat'


def test_assignment_options():
    """Test assignment of a few options."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.options.vt = 'v'
    assert rpict.to_radiance() == 'rpict -vtv input.oct < view.vf'
    with pytest.raises(exceptions.InvalidValueError):
        rpict.options.vt = 'k'
    rpict.options.av = (0.0, 0.0, 0.0)
    assert rpict.to_radiance() == 'rpict -av 0.0 0.0 0.0 -vtv input.oct < view.vf'
    rpict.options.x = 512
    assert rpict.to_radiance() == 'rpict -av 0.0 0.0 0.0 -vtv -x 512 input.oct < view.vf'


def test_stdin():
    """Test stdin."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.output = 'results.dat'
    assert rpict.to_radiance(stdin_input=True) == ('rpict input.oct > results.dat')


def test_validation():
    """Test for errors in case of missing arguments."""
    rpict = Rpict()

    with pytest.raises(exceptions.MissingArgumentError):
        # missing octree
        rpict.to_radiance()
    rpict.octree = 'input.oct'

    with pytest.raises(exceptions.MissingArgumentError):
        # missing view file
        rpict.to_radiance()

    rpict.view = 'view.vf'
    assert rpict.to_radiance() == 'rpict input.oct < view.vf'


def test_error_0():
    """Test if errors are being raised when incompatible options are assigned."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.options.ai = 'mod'
    with pytest.raises(ValueError):
        rpict.options.ae = 'mod'


def test_error_1():
    """Test if errors are being raised when incompatible options are assigned."""
    rpict1 = Rpict()

    rpict1.octree = 'input.oct'
    rpict1.view = 'view.vf'
    rpict1.options.aI = 'mod'
    with pytest.raises(ValueError):
        rpict1.options.aE = 'mod'


def test_warning_0():
    """Test if warnings are being raised when incompatible options are assigned."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.options.ps = -1
    assert rpict.to_radiance() == 'rpict -ps -1 input.oct < view.vf'
    with pytest.warns(Warning):
        rpict.options.dj = 0.0


def test_warning_1():
    """Test if warnings are being raised when incompatible options are assigned."""
    rpict = Rpict()

    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.options.i = True
    assert rpict.to_radiance() == 'rpict -i input.oct < view.vf'
    with pytest.warns(Warning):
        rpict.options.dv = True
