"""pcond command."""

from .options.pcond import PcondOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Pcond(Command):
    """pcond command."""

    __slots__ = ('_input',)

    def __init__(self, options=None, output=None, input=None):
        """Command.

        Args:
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
            input: File path to the radiance generated hdr file (Default: None).
        """
        Command.__init__(self, output=output)
        self.options = options
        self._input = input

    @property
    def options(self):
        """pcond options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = PcondOptions()

        if not isinstance(value, PcondOptions):
            raise ValueError('Expected Pcond options not {}'.format(value))

        self._options = value

    @property
    def input(self):
        """Radiance HDR image file."""
        return self._input

    @input.setter
    def input(self, value):
        if value[-4:].lower() != '.hdr':
            raise ValueError(
                'Radiance generated HDR required. Instead got %.' % (value))
        else:
            self._input = typing.normpath(value)

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command, self.options.to_radiance()]
        cmd = ' '.join(command_parts)

        if not stdin_input and self.input:
            cmd = '%s %s' % (cmd, self.input)

        if self.pipe_to:
            cmd = '%s | %s' % (cmd, self.pipe_to.to_radiance(stdin_input=True))

        elif self.output:
            cmd = '%s > %s' % (cmd, self.output)

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if not stdin_input and not self.input:
            raise exceptions.MissingArgumentError(self.command, 'input')
    