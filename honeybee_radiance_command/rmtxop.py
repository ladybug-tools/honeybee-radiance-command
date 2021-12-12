"""rmtxop command."""
from .options.rmtxop import RmtxopOptions
from ._command import Command
import honeybee_radiance_command._exception as exceptions
import honeybee_radiance_command._typing as typing


class Rmtxop(Command):
    """Rmtxop command.

    Concatenate, add, multiply, divide, transpose, scale, and convert matrices. The
    implementation here allows for matrix operations on upto three matrices at the same
    time. While the Radiance binary allows for even more, this restriction has been
    imposed here to keep the code somewhat clean.
    """

    __slots__ = ('_mtx1', '_mtx1_trnsps', '_mtx1_trnsfrm', '_mtx1_scl',
                 '_mtx2', '_mtx2_trnsps', '_mtx2_trnsfrm', '_mtx2_scl',
                 '_mtx3', '_mtx3_trnsps', '_mtx3_trnsfrm', '_mtx3_scl',
                 '_mtx12_oprtr', '_mtx23_oprtr', '_is_one_mtx_calc', '_is_two_mtx_calc',
                 '_is_three_mtx_calc',)

    def __init__(self, options=None, output=None, mtx1=None, mtx1_trnsfrm=None,
                 mtx1_scl=None, mtx1_trnsps=None, mtx2=None, mtx2_trnsfrm=None,
                 mtx2_scl=None, mtx2_trnsps=None, mtx3=None, mtx3_trnsfrm=None,
                 mtx3_scl=None, mtx3_trnsps=None, mtx12_oprtr=None, mtx23_oprtr=None,
                 is_one_mtx_calc=False, is_two_mtx_calc=False, is_three_mtx_calc=False):
        """Initialize Command."""
        Command.__init__(self, output=output)
        self.options = options
        self.output = output
        self.mtx1 = mtx1
        self.mtx1_trnsfrm = mtx1_trnsfrm
        self.mtx1_scl = mtx1_scl
        self.mtx1_trnsps = mtx1_trnsps
        self.mtx2 = mtx2
        self.mtx2_trnsfrm = mtx2_trnsfrm
        self.mtx2_scl = mtx2_scl
        self.mtx2_trnsps = mtx2_trnsps
        self.mtx3 = mtx3
        self.mtx3_trnsfrm = mtx3_trnsfrm
        self.mtx3_scl = mtx3_scl
        self.mtx3_trnsps = mtx3_trnsps
        self.mtx12_oprtr = mtx12_oprtr
        self.mtx23_oprtr = mtx23_oprtr
        self.is_one_mtx_calc = is_one_mtx_calc
        self.is_two_mtx_calc = is_two_mtx_calc
        self.is_three_mtx_calc = is_three_mtx_calc

    @property
    def options(self):
        """Rmtxop options."""
        return self._options

    @options.setter
    def options(self, value):
        if value is None:
            value = RmtxopOptions()

        if not isinstance(value, RmtxopOptions):
            raise ValueError('Expected RmtxopOptions not {}'.format(type(value)))

        self._options = value

    @property
    def mtx1(self):
        return self._mtx1

    @mtx1.setter
    def mtx1(self, value):
        self._mtx1 = typing.path_checker(value)

    @property
    def mtx2(self):
        return self._mtx2

    @mtx2.setter
    def mtx2(self, value):
        self._mtx2 = typing.path_checker(value)

    @property
    def mtx3(self):
        return self._mtx3

    @mtx3.setter
    def mtx3(self, value):
        self._mtx3 = typing.path_checker(value)

    @property
    def is_one_mtx_calc(self):
        return self._is_one_mtx_calc

    @is_one_mtx_calc.setter
    def is_one_mtx_calc(self, value):
        self._is_one_mtx_calc = value

    @property
    def is_two_mtx_calc(self):
        return self._is_two_mtx_calc

    @is_two_mtx_calc.setter
    def is_two_mtx_calc(self, value):
        self._is_two_mtx_calc = value

    @property
    def is_three_mtx_calc(self):
        return self._is_three_mtx_calc

    @is_three_mtx_calc.setter
    def is_three_mtx_calc(self, value):
        self._is_three_mtx_calc = value

    @staticmethod
    def __scl_trnsfrm_setter(value):
        """Check the input provided for the scalar or transform and return a list
        of floating point numbers"""
        # If the input is a single number then convert into a single element list.
        # Do a check for floating point number in both cases.
        if value is not None:
            if type(value) in (list, tuple):
                return [float(num) for num in value]
            else:
                return [float(value)]
        else:
            return None

    @property
    def mtx1_trnsfrm(self):
        """Transformation coefficients for mtx1 that are specified as a single floating
        point number or a tuple or list of floating point numbers. If specified as tuple
        or list, then its length should be an even multiple of the original matrix
        components.
        """
        return self._mtx1_trnsfrm

    @mtx1_trnsfrm.setter
    def mtx1_trnsfrm(self, value):
        self._mtx1_trnsfrm = self.__scl_trnsfrm_setter(value)

    @property
    def mtx1_scl(self):
        """Scalar factor to scale the elements of the matrix that are specified as a
        single floating point number or a tuple or list of floating point numbers. If
        specified as a tuple or list, then its length should be equal to the original
        matrix components"""
        return self._mtx1_scl

    @mtx1_scl.setter
    def mtx1_scl(self, value):
        self._mtx1_scl = self.__scl_trnsfrm_setter(value)

    @property
    def mtx2_trnsfrm(self):
        """Transformation coefficients for mtx2 that are specified as a single floating
        point number or a tuple or list of floating point numbers. If specified as tuple
        or list, then its length should be an even multiple of the original matrix
        components.
        """
        return self._mtx2_trnsfrm

    @mtx2_trnsfrm.setter
    def mtx2_trnsfrm(self, value):
        self._mtx2_trnsfrm = self.__scl_trnsfrm_setter(value)

    @property
    def mtx2_scl(self):
        """Scalar factor to scale the elements of the matrix that are specified as a
        single floating point number or a tuple or list of floating point numbers. If
        specified as a tuple or list, then its length should be equal to the original
        matrix components"""
        return self._mtx2_scl

    @mtx2_scl.setter
    def mtx2_scl(self, value):
        self._mtx2_scl = self.__scl_trnsfrm_setter(value)

    @property
    def mtx3_trnsfrm(self):
        """Transformation coefficients for mtx3 that are specified as a single floating
        point number or a tuple or list of floating point numbers. If specified as tuple
        or list, then its length should be an even multiple of the original matrix
        components.
        """
        return self._mtx3_trnsfrm

    @mtx3_trnsfrm.setter
    def mtx3_trnsfrm(self, value):
        self._mtx3_trnsfrm = self.__scl_trnsfrm_setter(value)

    @property
    def mtx3_scl(self):
        """Scalar factor to scale the elements of the matrix that are specified as a
        single floating point number or a tuple or list of floating point numbers. If
        specified as a tuple or list, then its length should be equal to the original
        matrix components"""
        return self._mtx3_scl

    @mtx3_scl.setter
    def mtx3_scl(self, value):
        self._mtx3_scl = self.__scl_trnsfrm_setter(value)

    @property
    def mtx1_trnsps(self):
        """Set to True if mtx1 is to be transposed."""
        return self._mtx1_trnsps

    @mtx1_trnsps.setter
    def mtx1_trnsps(self, value):
        self._mtx1_trnsps = value

    @property
    def mtx2_trnsps(self):
        """Set to True if mtx2 is to be transposed."""
        return self._mtx2_trnsps

    @mtx2_trnsps.setter
    def mtx2_trnsps(self, value):
        self._mtx2_trnsps = value

    @property
    def mtx3_trnsps(self):
        """Set to True if mtx3 is to be transposed."""
        return self._mtx3_trnsps

    @mtx3_trnsps.setter
    def mtx3_trnsps(self, value):
        self._mtx3_trnsps = value

    @staticmethod
    def _oprtr_setter(oprtr_value, oprtr):
        """Check the input provided for the operator from the list of possible of
        options"""
        if oprtr_value:
            valid_values = ('+', '*', '/', '.')

            if oprtr_value not in valid_values:
                raise exceptions.InvalidValueError('rmtxop', oprtr,
                                                   valid_values=valid_values)
            return oprtr_value
        else:
            return None

    @property
    def mtx12_oprtr(self):
        """The operator for specifying addition('+'), subtraction('-'),
        multiplication('*'), division(/) or concatentation(.) between the first and
         second matrix if two matrices are provided. The default operation is
         concatenation. 
         In the case of addition, the two matrices involved must have the same number of 
         components. If subtraction is desired, use addition (’+’) with a scaling 
         parameter of -1 for the second matrix (the −s option). For element-wise 
         multiplication and division, the second matrix is permitted to have a single 
         component per element, which will be applied equally to all components of the 
         first matrix. If element-wise division is specified, any zero elements in the 
         second matrix will result in a warning and the corresponding component(s) in the
          first matrix will be set to zero."""
        return self._mtx12_oprtr

    @mtx12_oprtr.setter
    def mtx12_oprtr(self, value):
        self._mtx12_oprtr = self._oprtr_setter(value, 'mtx12_oprtr')

    @property
    def mtx23_oprtr(self):
        """The operator for specifying addition('+'), subtraction('-'),
        multiplication('*'), division(/) or concatentation(.) between the second and
         third matrix if two matrices are provided. The default operation is
         concatenation. 
         In the case of addition, the two matrices involved must have the same number of 
         components. If subtraction is desired, use addition (’+’) with a scaling 
         parameter of -1 for the second matrix (the −s option). For element-wise 
         multiplication and division, the second matrix is permitted to have a single 
         component per element, which will be applied equally to all components of the 
         first matrix. If element-wise division is specified, any zero elements in the 
         second matrix will result in a warning and the corresponding component(s) in the
          first matrix will be set to zero."""
        return self._mtx23_oprtr

    @mtx23_oprtr.setter
    def mtx23_oprtr(self, value):
        self._mtx12_oprtr = self._oprtr_setter(value, 'mtx23_oprtr')

    def to_radiance(self, stdin_input=False):
        """Command in Radiance format.

        Args:
            stdin_input: A boolean that indicates if the input for this command
                comes from stdin. This is for instance the case when you pipe the input
                from another command (default: False).
        """
        self.validate(stdin_input)

        command_parts = [self.command, self.options.to_radiance()]

        # The first matrix has to be present for all the calcs
        if self.is_one_mtx_calc or self.is_two_mtx_calc or self.is_three_mtx_calc:
            if self.mtx1_trnsps:
                command_parts.append('-t')
            if self.mtx1_trnsfrm:
                command_parts.extend(['-c'] + ['%s' % val for val in self.mtx1_trnsfrm])
            if self.mtx1_scl:
                command_parts.extend(['-s'] + ['%s' % val for val in self.mtx1_scl])
            command_parts.append(self.mtx1)

        # The second matrix has to be present for two and three matrix calcs.
        if self.is_two_mtx_calc or self.is_three_mtx_calc:
            if self.mtx12_oprtr:
                command_parts.append(self.mtx12_oprtr)
            if self.mtx2_trnsps:
                command_parts.append('-t')
            if self.mtx2_trnsfrm:
                command_parts.extend(['-c'] + ['%s' % val for val in self.mtx2_trnsfrm])
            if self.mtx2_scl:
                command_parts.extend(['-s'] + ['%s' % val for val in self.mtx2_scl])
            command_parts.append(self.mtx2)

        if self.is_three_mtx_calc:
            if self.mtx23_oprtr:
                command_parts.append(self.mtx23_oprtr)
            if self.mtx3_trnsps:
                command_parts.append('-t')
            if self.mtx3_trnsfrm:
                command_parts.extend(['-c'] + ['%s' % val for val in self.mtx3_trnsfrm])
            if self.mtx3_scl:
                command_parts.extend(['-s'] + ['%s' % val for val in self.mtx3_scl])
            command_parts.append(self.mtx3)

        cmd = ' '.join(command_parts)

        if self.pipe_to:
            cmd = ' | '.join((cmd, self.pipe_to.to_radiance(stdin_input=True)))
        elif self.output:
            cmd = ' > '.join((cmd, self.output))

        return ' '.join(cmd.split())

    def validate(self, stdin_input=False):
        Command.validate(self)

        calc_inputs_dict = {'is_one_mtx_calc': ('mtx1',),
                            'is_two_mtx_calc': ('mtx1', 'mtx2'),
                            'is_three_mtx_calc': ('mtx1', 'mtx2', 'mtx3')}

        # Perform three checks, to ensure that:
        #   Check1: Exactly one of the calc types are set to be run.
        #   Check2: All the inputs are available for the selected calc type.
        #   Check3: For a particular matrix scalar and transformation coefficients are
        #   not specified together.
        # What can still go wrong:
        #   If inputs that are not required for a particular calc type are set,
        #   they will be ignored.

        # Check 1
        calc_list = [(key, getattr(self, key)) for key in calc_inputs_dict.keys()]
        calc_set_true = [key for key, val in calc_list if val]

        assert len(calc_set_true) == 1, \
            'Exactly one of the calc types must be set to True. Currently the following ' \
            'calcs have been set to True: %s' % (', '.join(calc_set_true)
                                                 if calc_set_true else 'None')

        # Check 2
        calc_type_set = calc_set_true.pop()
        inputs_for_calc = calc_inputs_dict[calc_type_set]
        inputs_not_set = [val for val in inputs_for_calc if not getattr(self, val)]

        assert not inputs_not_set, \
            'The follwing inputs for the calc ' \
            'type "%s" have not been set: %s' % (
                calc_type_set, ', '.join(inputs_not_set))

        # Check 3
        if self.mtx1_trnsfrm and self.mtx1_scl:
            raise Exception('Transformation coefficients mtx1_trnsrm(%s) and scalar '
                            'coefficients mtx1_sclr(%s) have been specified at the same'
                            'time. These options are mutually exclusive' %
                            (self.mtx1_trnsfrm, self.mtx1_scl))
        if self.mtx2_trnsfrm and self.mtx2_scl:
            raise Exception('Transformation coefficients mtx2_trnsrm(%s) and scalar '
                            'coefficients mtx2_sclr(%s) have been specified at the same'
                            'time. These options are mutually exclusive' %
                            (self.mtx2_trnsfrm, self.mtx2_scl))
        if self.mtx3_trnsfrm and self.mtx3_scl:
            raise Exception('Transformation coefficients mtx3_trnsrm(%s) and scalar '
                            'coefficients mtx3_sclr(%s) have been specified at the same'
                            'time. These options are mutually exclusive' %
                            (self.mtx3_trnsfrm, self.mtx3_scl))

    @classmethod
    def for_one_matrix_calc(cls, options=None, output=None, mtx1=None, mtx1_trnsfrm=None,
                            mtx1_scl=None, mtx1_trnsps=None):
        """Return a class instance explicitly for a single matrix calculation"""
        mtx1_cls = cls(options=options, output=output, mtx1=mtx1,
                       mtx1_trnsfrm=mtx1_trnsfrm,
                       mtx1_scl=mtx1_scl, mtx1_trnsps=mtx1_trnsps)
        mtx1_cls.is_one_mtx_calc = True
        return mtx1_cls

    @classmethod
    def for_two_matrix_calc(cls, options=None, output=None, mtx1=None, mtx1_trnsfrm=None,
                            mtx1_scl=None, mtx1_trnsps=None, mtx2=None,
                            mtx2_trnsfrm=None,
                            mtx2_scl=None, mtx2_trnsps=None, mtx12_oprtr=None):

        mtx2_cls = cls(options=options, output=output, mtx1=mtx1,
                       mtx1_trnsfrm=mtx1_trnsfrm,
                       mtx1_scl=mtx1_scl, mtx1_trnsps=mtx1_trnsps, mtx2=mtx2,
                       mtx2_trnsfrm=mtx2_trnsfrm, mtx2_scl=mtx2_scl,
                       mtx2_trnsps=mtx2_trnsps, mtx12_oprtr=mtx12_oprtr)
        mtx2_cls.is_two_mtx_calc = True
        return mtx2_cls

    @classmethod
    def for_three_matrix_calc(cls, options=None, output=None, mtx1=None,
                              mtx1_trnsfrm=None,
                              mtx1_scl=None, mtx1_trnsps=None, mtx2=None,
                              mtx2_trnsfrm=None,
                              mtx2_scl=None, mtx2_trnsps=None, mtx12_oprtr=None,
                              mtx3=None, mtx3_trnsfrm=None,
                              mtx3_scl=None, mtx3_trnsps=None, mtx23_oprtr=None):

        mtx3_cls = cls(options=options, output=output, mtx1=mtx1,
                       mtx1_trnsfrm=mtx1_trnsfrm, mtx1_scl=mtx1_scl,
                       mtx1_trnsps=mtx1_trnsps, mtx2=mtx2, mtx2_trnsfrm=mtx2_trnsfrm,
                       mtx2_scl=mtx2_scl, mtx2_trnsps=mtx2_trnsps,
                       mtx12_oprtr=mtx12_oprtr, mtx3=mtx3, mtx3_trnsfrm=mtx3_trnsfrm,
                       mtx3_scl=mtx3_scl, mtx3_trnsps=mtx3_trnsps,
                       mtx23_oprtr=mtx23_oprtr)

        mtx3_cls.is_three_mtx_calc = True
        return mtx3_cls
