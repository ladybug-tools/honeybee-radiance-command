"""pinterp command."""

from .options.pinterp import PinterpOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions


class Pinterp(Command):
    """Pinterp command.

    Pinterp interpolates or extrapolates a new view from one or more RADIANCE pictures 
    and sends the result to the standard output.

    Args:
        options: Command options. It will be set to Radiance default values
            if unspecified.
        output: File path to the output file (Default: None).
        view: View to interpolate or extrapolate (Default: None).
        image: Radiance pictures to interpolate or extrapolate from (Default: None).
        zspec: The distance to each pixel in the image(s) (Default: None).

    Properties:
        * options
        * output
        * view
        * image
        * zspec
    """

    __slots__ = ('_view', '_image', '_zspec')

    def __init__(
        self, options=None, output=None, view=None, image=None, zspec=None):
        """Initialize Command."""
        Command.__init__(self, output=output)
        self.options = options
        self.view = view
        self.image = image
        self.zspec = zspec

    @property
    def options(self):
        """pinterp options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = PinterpOptions()

        if not isinstance(value, PinterpOptions):
            raise ValueError('Expected Pinterp options not {}'.format(value))

        self._options = value

    @property
    def view(self):
        """View to interpolate or extrapolate."""
        return self._view

    @view.setter
    def view(self, value):
        # Add some checks for the view
        self._view = value

    @property
    def image(self):
        """Radiance HDR image file(s)."""
        return self._image

    @image.setter
    def image(self, value):
        if not isinstance(value, (list, tuple)):
            self._image = [value]
        else:
            self._image = value

    @property
    def zspec(self):
        """z specification for input image(s)"""
        return self._zspec

    @zspec.setter
    def zspec(self, value):
        if not isinstance(value, (list, tuple)):
            self._zspec = [value]
        else:
            self._zspec = value

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command. (Default: False).
        """
        self.validate(stdin_input)

        if stdin_input: self.options.vf = '-'
        else: self.options.vf = self.view

        command_parts = [self.command, self.options.to_radiance()]
        cmd = ' '.join(command_parts)

        for (img, z) in zip(self.image, self.zspec):
            cmd = '%s %s %s' % (cmd, img, z)

        if self.pipe_to:
            cmd = '%s | %s' % (cmd, self.pipe_to.to_radiance(stdin_input=True))

        elif self.output:
            cmd = '%s > %s' % (cmd, self.output)

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if not stdin_input and not self.view:
            raise exceptions.MissingArgumentError(self.command, 'view')
        if not self.image:
            raise exceptions.MissingArgumentError(self.command, 'image')
        if not self.zspec:
            raise exceptions.MissingArgumentError(self.command, 'zspec')
