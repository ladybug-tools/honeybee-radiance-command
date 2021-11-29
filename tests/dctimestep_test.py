from honeybee_radiance_command.dctimestep import Dctimestep
import pytest


def test_defaults():
    dctimestep = Dctimestep()
    assert dctimestep.command == 'dctimestep'
    assert dctimestep.options.to_radiance() == ''
    with pytest.raises(ValueError):
        # At least one of the option groups for dc/sun/view matrices and sky vector
        # must be provided.
        dctimestep.to_radiance()


def test_assignment():
    dctimestep = Dctimestep()
    dctimestep.day_coef_matrix = 'dc.mtx'
    assert dctimestep.day_coef_matrix == 'dc.mtx'
    with pytest.raises(AssertionError):
        dctimestep.validate()
    dctimestep.sky_vector = 'sky.vec'

    assert dctimestep.to_radiance() == 'dctimestep dc.mtx sky.vec'
    dctimestep.output = 'illum.mtx'
    assert dctimestep.output == 'illum.mtx'
    assert dctimestep.to_radiance() == 'dctimestep dc.mtx sky.vec > illum.mtx'


def test_exclusive_inputs():
    dctimestep = Dctimestep()
    dctimestep.day_coef_matrix = 'dc.mtx'
    dctimestep.view_matrix = 'view.mtx'
    with pytest.raises(ValueError):
        dctimestep.validate()

def test_unused_inputs2():
    dctimestep = Dctimestep()
    dctimestep.day_coef_matrix = 'dc.mtx'
    dctimestep.sky_vector = 'sky.vec'
    dctimestep.validate()

    dctimestep.sun_coef_matrix='sun.mtx'
    with pytest.raises(ValueError):
        dctimestep.validate()
