from honeybee_radiance_command.ra_xyze import Ra_xyze
import pytest
import honeybee_radiance_command._exception as exceptions


def test_defaults():
    ra_xyze = Ra_xyze()
    assert ra_xyze.command == 'ra_xyze'
    assert ra_xyze.options.to_radiance() == ''


def test_assignment():
    ra_xyze = Ra_xyze()
    ra_xyze.input = 'image.hdr'
    assert ra_xyze.input == 'image.hdr'
    ra_xyze.output = 'output.hdr'
    assert ra_xyze.output == 'output.hdr'
    assert ra_xyze.to_radiance() == 'ra_xyze image.hdr > output.hdr'


def test_options():
    ra_xyze = Ra_xyze()
    ra_xyze.input = 'image.hdr'
    ra_xyze.options.e = '+1.2'
    assert ra_xyze.to_radiance() == 'ra_xyze -e 1.2 image.hdr'


def test_options_primaries():
    ra_xyze = Ra_xyze()
    ra_xyze.options.p = (.670, .330, .210, .710, .140, .080, 0.333, 0.333)
    assert ra_xyze.options.p == '-p 0.67 0.33 0.21 0.71 0.14 0.08 0.333 0.333' or \
        '-p 0.670 0.330 0.210 0.710 0.140 0.080 0.333 0.333'


def test_stdin():
    ra_xyze = Ra_xyze()
    ra_xyze.options.c = True
    ra_xyze.output = 'output_xyz.hdr'
    assert ra_xyze.to_radiance(stdin_input=True) == \
        'ra_xyze -c > output_xyz.hdr'


def test_validation():
    ra_xyze = Ra_xyze()
    with pytest.raises(exceptions.MissingArgumentError):
        # missing input
        ra_xyze.to_radiance()
