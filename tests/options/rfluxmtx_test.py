"""Test rfluxmtx options."""
from honeybee_radiance_command.options.rfluxmtx import RfluxmtxOptions, \
    RfluxmtxControlParameters
import pytest
import honeybee_radiance_command._exception as exceptions


def test_default():
    options = RfluxmtxOptions()
    assert options.to_radiance() == ''


def test_assignment():
    options = RfluxmtxOptions()
    options.v = True
    assert options.v == True
    assert options.to_radiance() == '-v'


def test_reassignment():
    options = RfluxmtxOptions()
    options.v = True
    assert options.v == True
    assert options.to_radiance() == '-v'
    # remove assigned values
    options.v = None
    assert options.v == None
    assert options.to_radiance() == ''


def test_protected_assignment():
    options = RfluxmtxOptions()
    with pytest.raises(exceptions.ProtectedOptionError):
        options.f = 'bins.cal'
    with pytest.raises(exceptions.ProtectedOptionError):
        options.e = '2*$1=$2'
    with pytest.raises(exceptions.ProtectedOptionError):
        options.m = 'modifier'
    with pytest.raises(exceptions.ProtectedOptionError):
        options.m = None
        options.M = './suns.mod'


def test_rfluxmtx_control_params():
    options = RfluxmtxControlParameters()
    assert options.to_radiance() == '#@rfluxmtx h=u u=Y'

def test_rfluxmtx_control_params_parsing():
    input_string = '#@rfluxmtx u=0,1,0 h=kf o=skylight..class_room.vmx'
    options = RfluxmtxControlParameters.from_string(input_string)
    assert options.to_radiance() == '#@rfluxmtx h=kf u=0,1,0 o=skylight..class_room.vmx'
    assert options.up_direction == '0,1,0'
    assert options.sampling_type == 'kf'
    assert options.output_spec == 'skylight..class_room.vmx'


def test_rfluxmtx_control_params_from_file():
    fp = './tests/assets/receiver.rad'
    options = RfluxmtxControlParameters.from_file(fp)
    assert options.to_radiance() == '#@rfluxmtx h=kf u=0,1,0 o=skylight..class_room.vmx'
    assert options.up_direction == '0,1,0'
    assert options.sampling_type == 'kf'
    assert options.output_spec == 'skylight..class_room.vmx'
