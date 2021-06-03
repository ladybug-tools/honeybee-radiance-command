from honeybee_radiance_command.psign import Psign
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    psign = Psign()
    assert psign.command == 'psign'
    assert psign.options.to_radiance() == ''


def test_assignment():
    """Test assignment."""
    psign = Psign()

    psign.text = '21 Jun 12:00'
    assert psign.text == '21 Jun 12:00'
    assert psign.to_radiance() == 'psign "21 Jun 12:00"'
    psign.output = 'conditioned_image.hdr'
    assert psign.output == 'conditioned_image.hdr'
    assert psign.to_radiance() == 'psign "21 Jun 12:00" > conditioned_image.hdr'


def test_options():
    """Test options."""
    psign = Psign()

    psign.text = '21 Jun 12:00'
    psign.options.cb = (0, 0, 0)
    psign.options.cf = (1, 1, 1)
    assert psign.to_radiance() == 'psign -cb 0.0 0.0 0.0 -cf 1.0 1.0 1.0 "21 Jun 12:00"'


def test_stdin():
    """Test stdin."""
    psign = Psign()

    psign.text = '21 Jun 12:00'
    psign.output = 'conditioned.hdr'
    assert psign.to_radiance(stdin_input=True) == ('psign > conditioned.hdr')


def test_validation():
    """Test if exception is raised for missing arguments."""
    psign = Psign()
    with pytest.raises(exceptions.MissingArgumentError):
        psign.to_radiance()
    psign.text = '21 Jun 12:00'
    assert psign.to_radiance() == 'psign "21 Jun 12:00"'
