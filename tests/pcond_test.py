from honeybee_radiance_command.pcond import Pcond
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    pcond = Pcond()
    assert pcond.command == 'pcond'
    assert pcond.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        pcond.to_radiance()


def test_assignment():
    pcond = Pcond()

    pcond.input = 'image.hdr'
    assert pcond.input == 'image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr'
    pcond.output = 'conditioned_image.hdr'
    assert pcond.output == 'conditioned_image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr conditioned_image.hdr'


def test_stdin():
    pcond = Pcond()
    pcond.input = 'image.hdr'
    pcond.output = 'conditioned_image.hdr'
    assert pcond.to_radiance(stdin_input=True) == 'pcond conditioned_image.hdr'


def test_validation():
    pcond = Pcond()
    with pytest.raises(exceptions.MissingArgumentError):
        pcond.to_radiance()
    pcond.input = 'image.hdr'
    assert pcond.to_radiance() == 'pcond image.hdr'
