"""Test Radiance commands options base classes."""
from honeybee_radiance_command.cutil import parse_radiance_options


def test_empty_string():
    options = parse_radiance_options(' ')
    assert options == {}


def test_quotes():
    options = parse_radiance_options('" "')
    assert options == {}


def test_single_quotes():
    options = parse_radiance_options("' ' ")
    assert options == {}
