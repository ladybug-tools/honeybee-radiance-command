"""rpict command."""

from honeybee_radiance.view import View
from .options.rpict import RpictOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Rpict(Command):
    """rpict command."""

    __slots__ = ('output_name', 'octree', 'view', 'sky_file', 'simulation_type')

    def __init__(self, options=RpictOptions(), output=None, octree=None,
                 output_name='unnamed.hdr', view=None, sky_file=None, simulation_type=0):
        """Command.

        Args:
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
            octree: File path to the octree file (Default: None).
            output_name: A text string to be used as a name for the output file. Defaults
                to unnamed.hdr.
            view: A honeybee-radiance view object.
            sky_file: File path to the sky-file.
            simulation_type: An integer representing the study type;
                0 -> Illuminance(lux), 
                1 -> Radiation (kWh), 
                2 -> Luminance (Candela) 
                Defaults to 0.
        """
        Command.__init__(self, options, output)
        self.options = options
        self.output = output
        self.octree = octree

        self.output_name = output_name if output_name.lower().endswith(".hdr") \
            else output_name
        self.view = view
        self.sky_file = sky_file
        self.simulation_type = simulation_type

    @property
    def options(self):
        """Rpict options."""
        return self.options

    @options.setter
    def options(self, prop, value):
        if value:
            assert hasattr(self.options, prop), 'Expected RpictOptions'
            ' not {}'.format(prop)
            self.options.prop = value
        else:
            self.options = RpictOptions()

    @property
    def octree(self):
        """Octree file."""
        return self.octree

    @octree.setter
    def octree(self, value):
        if value:
            self.octree = typing.normpath(value)
        else:
            self.octree = None

    @property
    def view(self):
        """view."""
        return self.view
    
    @view.setter
    def view(self, value):
        if value:
            assert isinstance(value, View), 'Radiance view required.'
            ' You provided {}'.format(value)
            self.view = value
        else:
            self.view = None

    @property
    def sky_file(self):
        """sky file."""
        return self.sky_file
    
    @sky_file.setter
    def sky_file(self, value):
        if value:
            self.sky_file = typing.normpath(value)

    @property
    def simulation_type(self):
        """Get simulation type."""
        return self.simulation_type
    
    @simulation_type.setter
    def simulation_type(self, value):
        """Set simulation type.

        0: Illuminance(lux), 1: Radiation (kWh), 2: Luminance (Candela) (Default: 0)
        """
        assert value in [0, 1, 2], 'Simulation type must be between 0-2. The value'
        ' you provided is.format{}'.format(value)
        self.simulation_type = value
        if self.simulation_type in [0, 1]:
            self.options._i = True

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
        if not stdin_input and self.output_name and self.view and \
                self.sky_file and self.simulation_type:
            cmd = ' < '.join((cmd, self.output_name, self.view,
                              self.sky_file, self.simulation_type))
        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if self.octree is None:
            raise exceptions.MissingArgumentError(self.command, 'octree')
        if not stdin_input and not self.sky_file:
            raise exceptions.MissingArgumentError(self.command, 'sky_file')
        if not stdin_input and not self.view:
            raise exceptions.MissingArgumentError(self.command, 'view')
        if not stdin_input and not self.output_name:
            raise exceptions.MissingArgumentError(self.command, 'output_name')
        if not stdin_input and not self.simulation_type:
            raise exceptions.MissingArgumentError(self.command, 'simulation_type')
