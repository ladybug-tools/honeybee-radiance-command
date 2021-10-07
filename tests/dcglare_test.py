from honeybee_radiance_command.dcglare import Dcglare
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    dcglare = Dcglare()
    assert dcglare.command == 'dcglare'
    assert dcglare.options.to_radiance() == ''


def test_assignment():
    dcglare = Dcglare()
    dcglare.dc_direct = 'dc_direct.mtx'
    assert dcglare.dc_direct == 'dc_direct.mtx'
    dcglare.dc_total = 'dc_total.mtx'
    assert dcglare.dc_total == 'dc_total.mtx'
    dcglare.sky_matrix = 'sky_matrix.mtx'
    assert dcglare.sky_matrix == 'sky_matrix.mtx'
    assert dcglare.to_radiance() == 'dcglare dc_direct.mtx dc_total.mtx sky_matrix.mtx'


def test_view_file():
    dcglare = Dcglare()
    dcglare.dc_direct = 'dc_direct.mtx'
    dcglare.dc_total = 'dc_total.mtx'
    dcglare.sky_matrix = 'sky_matrix.mtx'
    dcglare.options.vf = 'views.ray'
    assert dcglare.to_radiance() == \
        'dcglare -vf views.ray dc_direct.mtx dc_total.mtx sky_matrix.mtx'


def test_three_phase():
    dcglare = Dcglare()
    dcglare.dc_direct = 'dc_direct.mtx'
    dcglare.tmtx = 'tmtx.mtx'
    dcglare.vmtx = 'vmtx.mtx'
    dcglare.dmtx = 'dmtx.mtx'
    dcglare.sky_matrix = 'sky_matrix.mtx'
    assert dcglare.to_radiance() == \
        'dcglare dc_direct.mtx vmtx.mtx tmtx.mtx dmtx.mtx sky_matrix.mtx'

def test_stdin():
    dcglare = Dcglare()  
    dcglare.dc_direct = 'dc_direct.mtx'
    dcglare.dc_total = 'dc_total.mtx'
    dcglare.sky_matrix = 'sky_matrix.mtx'
    dcglare.output = 'views.dgp'
    assert dcglare.to_radiance(stdin_input=True) == \
        'dcglare dc_direct.mtx dc_total.mtx > views.dgp'


def test_validation():
    dcglare = Dcglare()
    with pytest.raises(exceptions.MissingArgumentError):
        # missing dcdirect
        dcglare.to_radiance()

    dcglare.dc_direct = 'dc_direct.mtx'
    with pytest.raises(exceptions.MissingArgumentError):
        # missing dc_total
        dcglare.to_radiance()

    dcglare.dc_total = 'dc_total.mtx'
    with pytest.raises(exceptions.MissingArgumentError):
        # missing sky_matrix
        dcglare.to_radiance()

    dcglare.sky_matrix = 'sky_matrix.mtx'
    assert dcglare.to_radiance() == 'dcglare dc_direct.mtx dc_total.mtx sky_matrix.mtx'
