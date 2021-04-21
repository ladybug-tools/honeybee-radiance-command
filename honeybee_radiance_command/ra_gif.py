# coding: utf-8

"""ra_gif command."""

from .options.ra_gif import Ra_GIFOptions
from ._command import Command
import honeybee_radiance_command._typing as typing
import honeybee_radiance_command._exception as exceptions


class Ra_GIF(Command):
    """ra_gif command."""

    __slots__ = ('_input')

    def __init__(self, options=None, output=None, input=None):
        Command.__init__(self, output=output)
        self._input = input
        self.options = options

    @property
    def options(self):
        """Ra_GIF options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = Ra_GIFOptions()

        if not isinstance(value, Ra_GIFOptions):
            raise ValueError('Expected RaGIF options not {}'.format(value))

        self._options = value

    @property
    def input(self):
        """Radiance HDR image."""
        return self._input

    @input.setter
    def input(self, value):
        if value[-4:].lower() != '.hdr':
            raise ValueError(
                'An HDR file is required. Instead got %.' % (value))
        else:
            self._input = typing.normpath(value)

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command comes
                from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command, self.options.to_radiance()]
        cmd = ' '.join(command_parts)

        if not stdin_input and self.input:
            cmd = ' '.join((cmd, self.input))

        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))

        elif self.output:
            cmd = '%s > %s' % (cmd, self.output)

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if not stdin_input and not self.input:
            raise exceptions.MissingArgumentError(self.command, 'input')
            
    
