"""pcomb command."""

from .options.pcomb import PcombOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Pcomb(Command):
    """pcomb command."""

    __slots__ = ('_input')

    def __init__(self, options=None, output=None, input=[]):
        """Command.

        Args:
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
            input: A list of paths to radiance generated hdr images. (Default: []).
        """
        Command.__init__(self, output=output)
        if options:
            self._options = options
        else:
            self._options = PcombOptions()
        self._input = input

    @property
    def options(self):
        """pcomb options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = PcombOptions()

        if not isinstance(value, PcombOptions):
            raise ValueError('Expected PcombOptions not {}'.format(type(value)))

        self._options = value

    @property
    def input(self):
        """A list of paths to radiance generated hdr images."""
        return self._input

    @input.setter
    def input(self, value):
        if isinstance(value, list):
            hdr_check = [image[-4:].lower() == '.hdr' for image in value]
            hdrs = hdr_check.count(True)
            if hdrs == len(value):
                image_paths = [typing.normpath(path) for path in value]
                joined_paths = ' '.join(image_paths)
                self._input = joined_paths
        elif not value:
            self._input = []
        else:
            raise ValueError(
                'A list of .hdr files required. Instead got %.' % (value)
            )

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
            cmd = ' < '.join((cmd, self.input))
        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if not stdin_input and not self.input:
            raise exceptions.MissingArgumentError(self.command, 'input')
    
