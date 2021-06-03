# coding: utf-8

from .optionbase import OptionCollection, BoolOption


class GetinfoOptions(OptionCollection):
    """getinfo options.

    Also see: https://floyd.lbl.gov/radiance/man_html/getinfo.1.html
    """

    __slots__ = ('_d',)

    def __init__(self):
        """getinfo command options."""

        OptionCollection.__init__(self)
        self._d = BoolOption("d", "Print the dimensions instead - default: False")
        self._on_setattr_check = False

    @property
    def d(self):
        """Print the dimensions instead - default: False

        The −d option can be used to print the dimensions of an octree or picture
        file instead of getting the header. For an octree, getinfo −d prints the
        bounding cube (xmin ymin zmin size). For a picture, getinfo −d prints the
        y and x resolution (−Y yres +X xres).
        """
        return self._d

    @d.setter
    def d(self, value):
        self._d.value = value
