"""rfluxmtx command"""

from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing
from .options.rfluxmtx import RfluxmtxOptions, RfluxmtxControlParameters


# octree to octree and so on
class Rfluxmtx(Command):
    """
    Rfluxmtx command.

    Rfluxmtx computes the flux transfer matrices for a RADIANCE scene.

    """

    __slots__ = ('_input', "_sensors", "_sender", "_octree", "_receivers", "_system")

    def __init__(self, options=None, output=None, sensors=None, sender=None, receivers=None, system=None,
                 octree=None):
        """Initialize Command."""
        Command.__init__(self, output=output)
        self.options = options
        self.sensors = sensors
        self.octree = octree
        self.sender = sender
        self.receivers = receivers
        self.system = system

    @property
    def options(self):
        """Rfluxmtx options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = RfluxmtxOptions()

        if not isinstance(value, RfluxmtxOptions):
            raise ValueError('Expected Rfluxmtx options not {}'.format(value))

        self._options = value

    @property
    def sensors(self):
        """Sensor file."""
        return self._sensors

    @sensors.setter
    def sensors(self, value):
        if value is None:
            self._sensors = None
        else:
            self._sensors = typing.normpath(value)

    @property
    def sender(self):
        """Sender file."""
        return self._sender

    @sender.setter
    def sender(self, value):
        if value is None:
            self._sender = None
        else:
            self._sender = typing.normpath(value)

    @property
    def receivers(self):
        """Receivers file."""
        return self._receivers

    @receivers.setter
    def receivers(self, value):
        if value is None:
            self._receivers = None
        else:
            self._receivers = typing.normpath(value)

    @property
    def system(self):
        """System file. Note that rfluxmtx can accept any number of system files, however, to keep
        the implementation clean, only one system file is being allowed. (SS: 23.Sep.2021)"""
        return self._system

    @system.setter
    def system(self, value):
        if value is None:
            self._system = None
        else:
            self._system = typing.normpath(value)

    @property
    def octree(self):
        """Octree file."""
        return self._octree

    @octree.setter
    def octree(self, value):
        if value is None:
            self._octree = None
        else:
            self._octree = typing.normpath(value)

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command, self.options.to_radiance()]
        command_parts += [self.sender or "-"]
        command_parts += [self.receivers]
        command_parts += ["-i", '"""%s"""' % self.octree] if self.octree else []
        command_parts += [self.system] if self.system else []

        cmd = ' '.join(command_parts)

        if not stdin_input and self.sensors:
            cmd = ' < '.join((cmd, self.sensors))
        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if self.receivers is None:
            raise exceptions.MissingArgumentError(self.command, 'receivers')
        if not stdin_input and not self.sensors and not self.sender:
            raise exceptions.MissingArgumentError(self.command, 'sensors')
