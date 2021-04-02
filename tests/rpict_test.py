from honeybee_radiance_command.rpict import Rpict
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    rpict = Rpict()
    assert rpict.command == 'rpict'
    assert rpict.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        # missing octree
        rpict.to_radiance()


def test_assignment():
    rpict = Rpict()  
    rpict.octree = 'input.oct'
    assert rpict.octree == 'input.oct'
    rpict.view = 'view.vf'
    assert rpict.view == 'view.vf'
    assert rpict.to_radiance() == 'rpict input.oct < view.vf'
    rpict.output = 'results.dat'
    assert rpict.output == 'results.dat'
    assert rpict.to_radiance() == 'rpict input.oct < view.vf > results.dat'


def test_stdin():
    rpict = Rpict()  
    rpict.octree = 'input.oct'
    rpict.view = 'view.vf'
    rpict.output = 'results.dat'
    assert rpict.to_radiance(stdin_input=True) == 'rpict input.oct > results.dat'


def test_validation():
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
