"""rpict command."""

from .options.rpict import RpictOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Rpict(Command):
    """rpict command."""

    __slots__ = ('_octree', '_view')

    def __init__(self, options=None, output=None, octree=None, view=None):
        """Command.

        Args:
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
            octree: File path to the octree file (Default: None).
            view: File path to the octree file (Default: None).
        """
        Command.__init__(self, output=output)
        self.options = options
        self.octree = octree
        self.view = view

    @property
    def options(self):
        """Rpict options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = RpictOptions()

        if not isinstance(value, RpictOptions):
            raise ValueError('Expected RpictOptions not {}'.format(type(value)))

        self._options = value

    @property
    def octree(self):
        """Octree file."""
        return self._octree

    @octree.setter
    def octree(self, value):
        if not value:
            self._octree = value
        else:
            self._octree = typing.normpath(value)

    @property
    def view(self):
        """view."""
        return self._view

    @view.setter
    def view(self, value):
        if not value:
            self._view = None
        else:
            self._view = typing.normpath(value)

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command, self.options.to_radiance(), self.octree]
        cmd = ' '.join(command_parts)
        if not stdin_input and self.view:
            cmd = ' < '.join((cmd, self.view))
        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if self.octree is None:
            raise exceptions.MissingArgumentError(self.command, 'octree')
        if not stdin_input and not self.view:
            raise exceptions.MissingArgumentError(self.command, 'view')
