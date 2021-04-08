"""gensky command."""

from .options.gensky import GenskyOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions


class Gensky(Command):
    """gensky command."""

    __slots__ = ('_month', '_day', '_time', '_time_zone', '_solar_time', '_input')

    def __init__(self, month, day, time, time_zone=None, solar_time=False,
                 options=None, output=None):
        """Command.

        Args:
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
            solar_time: A boolean to use local solar time
            options: Command options. It will be set to Radiance default values if not
                provided by user.
            output: File path to the output file (Default: None).
        """
        Command.__init__(self, output=output)
        if options:
            self._options = options
        else:
            self._options = GenskyOptions()

        self._month = self.check_month(month)
        self._day = self.check_day(day)
        self._time = self.check_time(time)
        self._time_zone = self.check_time_zone(time_zone)
        self._solar_time = self.check_solar_time(solar_time)

    @staticmethod
    def check_month(month):
        """Validate the value of month."""
        if month and isinstance(month, int) and month in range(1, 13):
            return month
        else:
            raise ValueError('The value of month needs to be an integer between'
                             ' 1 and 12 inclusive. Instead got %.' % (month))

    @staticmethod
    def check_day(day):
        """Validate the value of day."""
        if day and isinstance(day, int) and day in range(1, 32):
            return day
        else:
            raise ValueError('The value of day needs to be an integer between'
                             ' 1 and 31 inclusive. Instead got %.' % (day))

    @staticmethod
    def check_time(time):
        """Validate the value of time."""
        if time and isinstance(time, float):
            hour, minute = str(time).split('.')
            if int(hour) in range(1, 25) and int(minute) in range(0, 60):
                return time
            else:
                raise ValueError(
                    'The value of time is not in the 24 hours format.'
                )
        else:
            raise ValueError(
                'The value of time must be a decimal representing hours and minutes.'
            )

    @staticmethod
    def check_time_zone(time_zone):
        """Validate the value of time-zone."""
        time_zones = [
            'YST', 'PST', 'MST', 'CST', 'EST', 'GMT', 'CET', 'EET', 'AST', 'GST', 'IST',
            'JST', 'NZST', 'YDT', 'PDT', 'MDT', 'CDT', 'EDT', 'BST', 'CEST', 'EEST',
            'ADT', 'GDT', 'IDT', 'JDT', 'NZDT']
        if not time_zone:
            return None
        if time_zone and time_zone.upper() in time_zones:
            return time_zone
        else:
            raise ValueError(
                'Time zone must a three letter string from the following'
                ' options %.' % (time_zones)
            )

    @staticmethod
    def check_solar_time(solar_time):
        """Validate value for solar time."""
        if isinstance(solar_time, bool):
            return solar_time
        else:
            raise ValueError('Solar time only accepts True or False as a value.')

    def _gensky_time(self):
        """Get time string to be used in gensky command."""
        # Only month, day and time provided as arguments
        if not (self.time_zone and self.solar_time):
            gensky_input = ' '.join((str(self.month), str(self.day), str(self.time)))
            return gensky_input
        # Time zone is provided
        elif self.time_zone and not self.solar_time:
            gensky_time = ''.join((str(self.time), self.time_zone))
            gensky_input = ' '.join((str(self.month), str(self.day), gensky_time))
            return gensky_input
        # Local solar time requested
        elif self.solar_time and not self.time_zone:
            gensky_time = ' '.join((str(self.month), str(self.day), str(self.time)))
            gensky_input = ''.join(('+', gensky_time))
            return gensky_input
        # Time zone and solar time both requested
        elif self.time_zone and self.solar_time:
            gensky_time = ''.join((str(self.time), self.time_zone))
            gensky_time = ' '.join((str(self.month), str(self.day), gensky_time))
            gensky_input = ''.join(('+', gensky_time))
            return gensky_input

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
    def month(self):
        """Month."""
        return self._month

    @month.setter
    def month(self, value):
        self._month = self.check_month(value)

    @property
    def day(self):
        """Day."""
        return self._day

    @day.setter
    def day(self, value):
        self._day = self.check_day(value)

    @property
    def time(self):
        """time."""
        return self._time

    @time.setter
    def time(self, value):
        self._time = self.check_time(value)

    @property
    def time_zone(self):
        """time zone."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value):
        self._time_zone = self.check_time_zone(value)

    @property
    def solar_time(self):
        """Whether solar time is requested."""
        return self._solar_time

    @solar_time.setter
    def solar_time(self, value):
        self._solar_time = self.check_solar_time(value)

    @property
    def input(self):
        """Input string for gensky."""
        self._input = self._gensky_time()
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

