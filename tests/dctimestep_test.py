from honeybee_radiance_command.dctimestep import Dctimestep
import pytest


def test_defaults():
    dctimestep = Dctimestep()
    assert dctimestep.command == 'dctimestep'
    assert dctimestep.options.to_radiance() == ''
    with pytest.raises(AssertionError):
        # None of the calculation types have been set.
        dctimestep.to_radiance()


def test_assignment():
    dctimestep = Dctimestep()
    dctimestep._study_type = 'daylight_coef'
    dctimestep.day_coef_matrix = 'dc.mtx'
    assert dctimestep.day_coef_matrix == 'dc.mtx'
    with pytest.raises(AssertionError):
        # Sky vector is missing.
        dctimestep.validate()
    dctimestep.sky_vector = 'sky.vec'

    assert dctimestep.to_radiance() == 'dctimestep dc.mtx sky.vec'
    dctimestep.output = 'illum.mtx'
    assert dctimestep.output == 'illum.mtx'
    assert dctimestep.to_radiance() == 'dctimestep dc.mtx sky.vec > illum.mtx'


def test_classmethod():
    dctimestep = Dctimestep.four_phase_calc(options=None, output='res.mtx',
                                            view_matrix='view.mtx',
                                            daylight_matrix='daylight.mtx',
                                            t_matrix='tmtx.xml',
                                            sky_vector='sky.vec')
    assert dctimestep._study_type == 'four_phase'
    assert dctimestep._study_type != 'three_phase'
    with pytest.raises(AssertionError):
        dctimestep.validate()
    dctimestep.facade_matrix = 'facade.mtx'
    dctimestep.validate()


def test_file_type_assignment():
    dctimestep = Dctimestep()
    with pytest.raises(ValueError):
        dctimestep.t_matrix = 'some.vec'
    dctimestep.t_matrix = 'some.xml'
    dctimestep.t_matrix = 'some.XML'


def test_exclusive_options():
    dctimestep = Dctimestep()
    dctimestep._study_type = 'daylight_coef'
    dctimestep.day_coef_matrix = 'dc.mtx'
    dctimestep.sky_vector = 'sky.vec'
    dctimestep.options.o = 'output%02d.mtx'
    dctimestep.validate()
    assert dctimestep.to_radiance() == 'dctimestep -o output%02d.mtx dc.mtx sky.vec'
    dctimestep.options.o = None
    dctimestep.output = 'output.mtx'
    assert dctimestep.to_radiance() == 'dctimestep dc.mtx sky.vec > output.mtx'
    dctimestep.options.o = 'output%02d.mtx'
    with pytest.raises(Exception):
        dctimestep.to_radiance()
