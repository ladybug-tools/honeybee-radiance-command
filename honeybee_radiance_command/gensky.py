"""gensky command."""

from .options.gensky import GenskyOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions


class Gensky(Command):
    """gensky command."""

    __slots__ = ('_ang', '_month', '_day', '_time', '_time_zone', '_solar_time',
                 '_input')

    def __init__(self, ang=None, month=None, day=None, time=None, time_zone=None,
                 solar_time=False, options=None, output=None):
        """Command.

        Args:
            ang: A tuple of altitude and azimuth values.
            month: An integer representing the number of the month. Count starts from 01.
            day: An integer representing the number of the day in a month. Count starts
                from 01.
            time: A float representing hour and minute.
            time_zone: A three letter text representing the time zone.
                Following are acceptable time zones with their corresponding hour
                differences from Greenwhich mean time;
                YST +9, PST +8, MST +7, CST +6, EST +5, GMT 0, CET -1, EET -2, AST -3,
                GST -4, IST -5.5, JST -9, NZST -12, YDT +8, PDT +7, MDT +6, CDT +5,
                EDT +4, BST -1, CEST -2, EEST -3, ADT -4, GDT -5, IDT -6.5, JDT -10,
                NZDT -13
            solar_time: A boolean to use local solar time. If set to True then the time
                is preceded by '+' sign and local solar time is used instead of local
                standard time.
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
        """
        Command.__init__(self, output=output)
        self.options = options
        if ang:
            self.options = ang
            self._ang = ang
            self._month = None
            self._day = None
            self._time = None
            self._time_zone = None
            self._solar_time = None
        else:
            self._ang = None
            self._month = month
            self._day = day
            self._time = time
            self._time_zone = time_zone
            self._solar_time = solar_time

    @property
    def options(self):
        """Rpict options."""
        return self._options

    @options.setter
    def options(self, value):
        if not value:
            value = GenskyOptions()

        if not isinstance(value, GenskyOptions):
            raise ValueError('Expected GenskyOptions not {}'.format(type(value)))

        self._options = value

    @property
    def ang(self):
        """Angles for altitude and azimuth."""
        return self._ang

    @ang.setter
    def ang(self, value):
        self._ang.value = value

    @property
    def month(self):
        """Month."""
        return self._month

    @month.setter
    def month(self, value):
        if value and isinstance(value, int) and value in range(1, 13):
            self._month = value
        else:
            raise ValueError('The value of month needs to be an integer between'
                             ' 1 and 12 inclusive. Instead got %.' % (value))

    @property
    def day(self):
        """Day."""
        return self._day

    @day.setter
    def day(self, value):
        if value and isinstance(value, int) and value in range(1, 32):
            self._day = value
        else:
            raise ValueError('The value of day needs to be an integer between'
                             ' 1 and 31 inclusive. Instead got %.' % (value))

    @property
    def time(self):
        """time."""
        return self._time

    @time.setter
    def time(self, value):
        if value and isinstance(value, float, int):
            hour, minute = str(float(value)).split('.')
            if 1 <= int(hour) <= 24 and 0 <= int(minute) <= 59:
                self._time = value
            else:
                raise ValueError(
                    'The value of time is not valid.'
                )
        else:
            raise ValueError(
                'The value of time must be a number. Instead got %s' % (value)
            )

    @property
    def time_zone(self):
        """time zone."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value):
        time_zones = [
            'YST', 'PST', 'MST', 'CST', 'EST', 'GMT', 'CET', 'EET', 'AST', 'GST', 'IST',
            'JST', 'NZST', 'YDT', 'PDT', 'MDT', 'CDT', 'EDT', 'BST', 'CEST', 'EEST',
            'ADT', 'GDT', 'IDT', 'JDT', 'NZDT']
        if not value:
            return None
        if value and value.upper() in time_zones:
            self._time_zone = value
        else:
            raise ValueError(
                'Time zone must a three letter string from the following'
                ' options %.' % (time_zones)
            )

    @property
    def solar_time(self):
        """Whether solar time is requested."""
        return self._solar_time

    @solar_time.setter
    def solar_time(self, value):
        if isinstance(value, bool):
            self._solar_time = value
        else:
            raise ValueError('Solar time only accepts True or False as a value.')

    @property
    def input(self):
        """Input string for gensky."""

        # Only month, day and time provided as arguments
        if not (self.time_zone and self.solar_time):
            self._input  = '%s %s %s' % (str(self.month), str(self.day), str(self.time))
            return self._input

        # Time zone is provided
        elif self.time_zone and not self.solar_time:
            self._input = '%s %s %s%s' % (str(self.month), str(self.day),
                                           str(self.time), self.time_zone)
            return self._input

        # Local solar time requested
        elif self.solar_time and not self.time_zone:
            self._input = '+%s %s %s' % (str(self.month), str(self.day),
                                          str(self.time))
            return self._input

        # Time zone and solar time both requested
        elif self.time_zone and self.solar_time:
            self._input = '+%s %s %s%s' % (str(self.month), str(self.day),
                                           str(self.time), self.time_zone)
            return self._input

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command]

        if self.options:
            command_parts.append(self.options.to_radiance())

        cmd = ' '.join(command_parts)

        if not stdin_input and self.input:
            cmd = ' '.join((cmd, self.input))

        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))

        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)
        if not stdin_input and not self.month:
            raise exceptions.MissingArgumentError(self.command, 'month')
        if not stdin_input and not self.day:
            raise exceptions.MissingArgumentError(self.command, 'day')
        if not stdin_input and not self.time:
            raise exceptions.MissingArgumentError(self.command, 'time')