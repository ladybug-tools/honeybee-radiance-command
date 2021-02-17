from honeybee_radiance_command.gendaymtx import Gendaymtx
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    gendaymtx = Gendaymtx()
    assert gendaymtx.command == 'gendaymtx'
    assert gendaymtx.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        # missing wea
        gendaymtx.to_radiance()


def test_assignment():
    gendaymtx = Gendaymtx()
    gendaymtx.wea = 'input.wea'
    assert gendaymtx.wea == 'input.wea'
    assert gendaymtx.to_radiance() == 'gendaymtx input.wea'
    gendaymtx.output = 'sky.mtx'
    assert gendaymtx.output == 'sky.mtx'
    assert gendaymtx.to_radiance() == 'gendaymtx input.wea > sky.mtx'


def test_validation():
    gendaymtx = Gendaymtx()
    with pytest.raises(exceptions.MissingArgumentError):
        # missing wea
        gendaymtx.to_radiance()

    gendaymtx.wea = 'input.wea'
    assert gendaymtx.to_radiance() == 'gendaymtx input.wea'
