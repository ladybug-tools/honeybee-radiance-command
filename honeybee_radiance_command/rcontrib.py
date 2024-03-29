"""rcontrib command."""
from .options.rcontrib import RcontribOptions
from .rtrace import Rtrace


class Rcontrib(Rtrace):
    """rcontrib command.

    Rcontrib computes ray coefficients for objects whose modifiers are named in one or
    more -m settings. These modifiers are usually materials associated with light sources
    or sky domes, and must directly modify some geometric primitives to be considered in
    the output. A modifier list may also be read from a file using the -M option. The
    RAYPATH environment variable determines directories to search for this file. (No
    search takes place if a file name begins with a '.', '/' or '~' character.).

    Args:
        options: Command options. It will be set to Radiance default values
            if unspecified.
        output: Output file (Default: None).
        octree: Octree file (Default: None).
        sensors: Sensors file (Default: None).

    Properties:
        * options
        * output
        * octree
        * sensors

    Note:
    https://www.radiance-online.org/learning/documentation/manual-pages/pdfs/rcontrib.pdf
    """

    __slots__ = ()

    @property
    def options(self):
        """Rcontrib options."""
        return self._options

    @options.setter
    def options(self, value):
        if value is None:
            value = RcontribOptions()

        if not isinstance(value, RcontribOptions):
            raise ValueError('Expected RcontribOptions not {}'.format(type(value)))

        self._options = value
