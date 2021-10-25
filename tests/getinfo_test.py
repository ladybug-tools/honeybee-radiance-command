from honeybee_radiance_command.getinfo import Getinfo
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    getinfo = Getinfo()

    assert getinfo.command == 'getinfo'
    assert getinfo.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    getinfo = Getinfo()

    getinfo.input = ['image1.hdr', 'image2.hdr']
    assert getinfo.input == 'image1.hdr image2.hdr'
    assert getinfo.to_radiance() == 'getinfo image1.hdr image2.hdr'
    getinfo.output = 'combined.hdr'
    assert getinfo.output == 'combined.hdr'
    assert getinfo.to_radiance() == 'getinfo image1.hdr image2.hdr > combined.hdr'


def test_assignment_options():
    """Test assigning options."""
    getinfo = Getinfo()

    getinfo.input = ['image1.hdr', 'image2.hdr']
    getinfo.options.d = True
    assert getinfo.to_radiance() == 'getinfo -d image1.hdr image2.hdr'


def test_assignment_options_append():
    """Test assigning options."""
    getinfo = Getinfo()

    getinfo.input = ['image1.hdr']
    getinfo.options.a = 'This is some Text to append to the header'
    assert getinfo.to_radiance() == \
        'getinfo -a "This is some Text to append to the header" < image1.hdr' \
        or getinfo.to_radiance() == \
        "getinfo -a 'This is some Text to append to the header' < image1.hdr"


def test_stdin():
    """Test stdin."""
    getinfo = Getinfo()

    getinfo.input = ['image1.hdr', 'image2.hdr']
    getinfo.output = 'combined.hdr'
    assert getinfo.to_radiance(stdin_input=True) == ('getinfo > combined.hdr')


def test_validation():
    """Validate error for missing argument."""
    getinfo = Getinfo()

    with pytest.raises(exceptions.MissingArgumentError):
        getinfo.to_radiance()

    getinfo.input = ['image1.hdr', 'image2.hdr']
    assert getinfo.to_radiance() == 'getinfo image1.hdr image2.hdr'
