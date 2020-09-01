from .optionbase import BoolOption
from .rcontrib import RcontribOptions
import honeybee_radiance_command._exception as exceptions


class RfluxmtxOptions(RcontribOptions):
    """rcontrib command options."""

    __slots__ = ('_v',)

    def __init__(self):
        """rcontrib command options."""
        RcontribOptions.__init__(self)
        self._on_setattr_check = False
        self._v = BoolOption('v', 'verbose report - default: off')
        self._protected = ('f', 'e', 'p', 'b', 'bn', 'm', 'M')
        self._on_setattr_check = True

    def _on_setattr(self):
        """This method executes after setting each new attribute.

        Use this method to add checks that are necessary for OptionCollection. For
        instance in rtrace option collection -ti and -te are exclusive. You can include a
        check to ensure this is always correct.
        """
        RcontribOptions._on_setattr(self)
        for opt in self._protected:
            if getattr(self, opt).is_set:
                raise exceptions.ProtectedOptionError('rfluxmtx', opt)

    @property
    def v(self):
        """Verbose report - default: off"""
        return self._v

    @v.setter
    def v(self, value):
        self._v.value = value
