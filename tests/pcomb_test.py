from honeybee_radiance_command.pcomb import Pcomb
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    pcomb = Pcomb()
    assert pcomb.command == 'pcomb'
    assert pcomb.options.to_radiance() == ''
    with pytest.raises(exceptions.MissingArgumentError):
        pcomb.to_radiance()


def test_assignment():
    pcomb = Pcomb()

    pcomb.input = ['image1.hdr', 'image2.hdr']
    assert pcomb.input == 'image1.hdr image2.hdr'
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr'
    pcomb.output = 'combined.hdr'
    assert pcomb.output == 'combined.hdr'
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr > combined.hdr'


def test_stdin():
    pcomb = Pcomb()
    pcomb.input = ['image1.hdr', 'image2.hdr']
    pcomb.output = 'combined.hdr'
    assert pcomb.to_radiance(stdin_input=True) == ('pcomb < image1.hdr image2.hdr'
                                                   ' > combined.hdr')


def test_validation():
    pcomb = Pcomb()
    with pytest.raises(exceptions.MissingArgumentError):
        pcomb.to_radiance()
    pcomb.input = ['image1.hdr', 'image2.hdr']
    assert pcomb.to_radiance() == 'pcomb image1.hdr image2.hdr'
    
