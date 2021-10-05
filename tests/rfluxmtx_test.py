from honeybee_radiance_command.rfluxmtx import Rfluxmtx
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    rfluxmtx = Rfluxmtx()
    assert rfluxmtx.command == 'rfluxmtx'
    assert rfluxmtx.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        rfluxmtx.to_radiance()


def test_assignment():
    rfluxmtx = Rfluxmtx()
    rfluxmtx.receivers = "receivers.rad"
    assert rfluxmtx.receivers == "receivers.rad"
    rfluxmtx.octree = 'input.oct'
    assert rfluxmtx.octree == 'input.oct'
    rfluxmtx.sensors = 'sensors.pts'
    assert rfluxmtx.sensors == 'sensors.pts'
    assert rfluxmtx.to_radiance() == \
           'rfluxmtx - receivers.rad -i """input.oct""" < sensors.pts'
    rfluxmtx.output = 'results.dat'
    assert rfluxmtx.output == 'results.dat'
    assert rfluxmtx.to_radiance() == \
           'rfluxmtx - receivers.rad -i """input.oct""" < sensors.pts > results.dat'
    rfluxmtx.options.c = 1000
    assert rfluxmtx.to_radiance() == \
           'rfluxmtx -c 1000 - receivers.rad -i """input.oct""" < sensors.pts > results.dat'

    # This is to check the option of assigning sending surfaces instead of sensors.
    rfluxmtx = Rfluxmtx()
    rfluxmtx.receivers = 'receivers.rad'
    assert rfluxmtx.receivers == 'receivers.rad'
    rfluxmtx.sender = 'sender.rad'
    assert rfluxmtx.sender == 'sender.rad'
    rfluxmtx.output = 'results.dat'
    assert rfluxmtx.output == 'results.dat'
    assert rfluxmtx.to_radiance() == 'rfluxmtx sender.rad receivers.rad > results.dat'


def test_stdin():
    rfluxmtx = Rfluxmtx()
    rfluxmtx.sensors = 'sensors.pts'
    rfluxmtx.receivers = "receivers.rad"
    rfluxmtx.output = 'results.dat'
    assert rfluxmtx.to_radiance(
        stdin_input=True) == 'rfluxmtx - receivers.rad > results.dat'


def test_validation():
    rfluxmtx = Rfluxmtx()
    with pytest.raises(exceptions.MissingArgumentError):
        # missing receivers
        rfluxmtx.to_radiance()

    rfluxmtx.receivers = 'receivers.rad'
    with pytest.raises(exceptions.MissingArgumentError):
        # missing sensors
        rfluxmtx.to_radiance()

    rfluxmtx.sensors = 'sensors.pts'
    assert rfluxmtx.to_radiance() == 'rfluxmtx - receivers.rad < sensors.pts'
