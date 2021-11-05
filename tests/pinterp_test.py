from honeybee_radiance_command.pinterp import Pinterp
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    """Test command."""
    pinterp = Pinterp()
    
    assert pinterp.command == 'pinterp'
    assert pinterp.options.to_radiance() == ''


def test_assignment():
    """Test assignments."""
    pinterp = Pinterp()

    pinterp.view = 'view.vf'
    assert pinterp.view == 'view.vf'
    pinterp.image = 'image.hdr'
    assert pinterp.image == ['image.hdr']
    pinterp.output = 'output.hdr'
    assert pinterp.output == 'output.hdr'
    pinterp.zspec = 1
    assert pinterp.zspec == [1]
    assert pinterp.to_radiance() == 'pinterp -vf view.vf image.hdr 1 > output.hdr'


def test_options():
    """Test assignment of some of the options."""
    pinterp = Pinterp()

    pinterp.view = 'view.vf'
    pinterp.image = 'image.hdr'
    pinterp.zspec = 1
    pinterp.options.ff = True
    pinterp.options.x = 800
    pinterp.options.y = 800
    assert pinterp.to_radiance() == 'pinterp -ff -vf view.vf -x 800 -y 800 image.hdr 1'


def test_stdin():
    """Test stdin."""
    pinterp = Pinterp()

    pinterp.image = 'image.hdr'
    pinterp.output = 'output.hdr'
    pinterp.zspec = 1
    assert pinterp.to_radiance(stdin_input=True) == 'pinterp -vf - image.hdr 1 > output.hdr'


def test_validation():
    """Test if errors are raised on missing arguments."""
    pinterp = Pinterp()

    with pytest.raises(exceptions.MissingArgumentError):
        # missing view
        pinterp.to_radiance()
    
    pinterp.view = 'view.vf'
    with pytest.raises(exceptions.MissingArgumentError):
        # missing image
        pinterp.to_radiance()
    
    pinterp.image = 'image.hdr'
    with pytest.raises(exceptions.MissingArgumentError):
        # missing zpec
        pinterp.to_radiance()
    
    pinterp.zspec = 1
    assert pinterp.to_radiance() == 'pinterp -vf view.vf image.hdr 1'
