# coding: utf-8

"""ra_gif command."""

from .options.ra_gif import RaGIFOptions
from ._command import Command
import warnings
import honeybee_radiance_command._typing as typing


class RaGIF(Command):
    """ra_gif command."""

    __slots__ = ('_input')

    def __init__(self, options=None, output=None, input=None):
        Command.__init__(self, output=output)
        self._input = input
        self._options = options
    
    @property
    def options(self):
        """RaGIF options."""
        return self._options
    
    @options.setter
    def options(self, value):
        if not value:
            value = RaGIFOptions()
    
