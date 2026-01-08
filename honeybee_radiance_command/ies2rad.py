"""ies2rad command."""
from .options.ies2rad import Ies2radOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Ies2rad(Command):
    """Ies2rad command.

    Ies2rad converts one or more IES LM-63 photometric files into equivalent
    Radiance scene descriptions. The generated luminaires are centered at
    the origin and oriented along the negative Z-axis.

    Args:
        options: Ies2rad options. Defaults to Radiance defaults if unspecified.
        output: Path to output file (used only when piping or redirecting).
        ies: Path or list of paths to input IES files.

    Properties:
        * options
        * output
        * ies
    """

    __slots__ = ('_ies',)

    def __init__(self, options=None, output=None, ies=None):
        """Initialize Ies2rad command."""
        Command.__init__(self, output=output)
        self.ies = ies
        self.options = options

    @property
    def options(self):
        """Ies2rad options."""
        return self._options

    @options.setter
    def options(self, value):
        if value is None:
            value = Ies2radOptions()

        if not isinstance(value, Ies2radOptions):
            raise ValueError('Expected Ies2radOptions not {}'.format(type(value)))

        self._options = value

    @property
    def ies(self):
        """Input IES file(s)."""
        return self._ies

    @ies.setter
    def ies(self, value):
        if value is None:
            self._ies = None
        elif isinstance(value, (list, tuple)):
            self._ies = [typing.normpath(v) for v in value]
        else:
            self._ies = [typing.normpath(value)]

    def to_radiance(self):
        """Command in Radiance format."""
        self.validate()

        ies_files = ' '.join(self.ies)
        command_parts = [
            self.command,
            self.options.to_radiance(),
            ies_files
        ]

        cmd = ' '.join(command_parts)

        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self):
        """Validate command arguments."""
        Command.validate(self)

        if not self.ies:
            raise exceptions.MissingArgumentError(self.command, 'ies')

    def before_run(self):
        import os

        if self.options.l.is_set:
            libdir = os.path.abspath(self.options.l.value)
        else:
            libdir = os.getcwd()

        if self.options.p.is_set:
            output_dir = os.path.join(libdir, self.options.p.value)
        else:
            output_dir = libdir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
