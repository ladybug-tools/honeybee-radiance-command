from honeybee_radiance_command.pcompos import Pcompos
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pcompos = Pcompos()

    assert pcompos.command == 'pcompos'
    assert pcompos.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    pcompos = Pcompos()

    pcompos.input = ['image1.hdr', 'image2.hdr']
    assert pcompos.input == 'image1.hdr image2.hdr'
    assert pcompos.to_radiance() == 'pcompos image1.hdr image2.hdr'
    pcompos.output = 'combined.hdr'
    assert pcompos.output == 'combined.hdr'
    assert pcompos.to_radiance() == 'pcompos image1.hdr image2.hdr > combined.hdr'


def test_assignment_options():
    """Test assigning options."""
    pcompos = Pcompos()

    pcompos.input = ['image1.hdr', 'image2.hdr']
    pcompos.options.h = True
    pcompos.options.a = 1
    assert pcompos.to_radiance() == 'pcompos -a 1 -h image1.hdr image2.hdr'


def test_stdin():
    """Test stdin."""
    pcompos = Pcompos()

    pcompos.input = ['image1.hdr', 'image2.hdr']
    pcompos.output = 'combined.hdr'
    assert pcompos.to_radiance(stdin_input=True) == ('pcompos > combined.hdr')


def test_validation():
    """Validate error for missing argument."""
    pcompos = Pcompos()

    with pytest.raises(exceptions.MissingArgumentError):
        pcompos.to_radiance()

    pcompos.input = ['image1.hdr', 'image2.hdr']
    assert pcompos.to_radiance() == 'pcompos image1.hdr image2.hdr'
