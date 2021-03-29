from .optionbase import (
    OptionCollection,
    BoolOption,
    NumericOption,
    StringOption,
    StringOptionJoined,
    IntegerOption,
    TupleOption,
)


class RpictOptions(OptionCollection):
    """rpict command options."""

    __slots__ = (
        "_vt",
        "_vp",
        "_vd",
        "_vu",
        "_vh",
        "_vv",
        "_vo",
        "_va",
        "_vs",
        "_vl",
        "_x",
        "_y",
        "_pa",
        "_pj",
        "_pm",
        "_pd",
        "_ps",
        "_pt",
        "_t",
        "_w",
        "_i",
        "_u",
        "_bv",
        "_dt",
        "_dc",
        "_dj",
        "_ds",
        "_dr",
        "_dp",
        "_dv",
        "_ss",
        "_st",
        "_av",
        "_aw",
        "_ab",
        "_aa",
        "_ar",
        "_ad",
        "_as_",
        "_me",
        "_ma",
        "_mg",
        "_ms",
        "_lr",
        "_lw",
        "_am",
    )

    def __init__(self):
        """rpict command options."""
        self._vt = StringOptionJoined("vt", "view type perspective - default: vtv")
        self._vp = TupleOption(
            "vp", "view point - default: 0.000000 0.000000 0.000000", 3, float
        )
        self._vd = TupleOption(
            "vd", "view direction - default: 0.000000 1.000000 0.000000", 3, float
        )
        self._vu = TupleOption(
            "vu", "view up - default: 0.000000 0.000000 1.000000", 3, float
        )
        self._vh = NumericOption("vh", "view horizontal size - default: 45.000000")
        self._vv = NumericOption("vv", "view vertical size - default: 45.000000")
        self._vo = NumericOption("vo", "view fore clipping plane - default: 0.000000")
        self._va = NumericOption("va", "view aft clipping plane - default: 0.000000")
        self._vs = NumericOption("vs", "view shift - default: 0.000000")
        self._vl = NumericOption("vl", "view lift - default: 0.000000")
        self._x = IntegerOption("x", "x resolution - default: 512")
        self._y = IntegerOption("y", "y resolution - default: 512")
        self._pa = NumericOption("pa", "pixel aspect ratio - default: 1.000000")
        self._pj = NumericOption("pj", "pixel jitter - default: 0.670000")
        self._pm = NumericOption("pm", "pixel motion - default: 0.000000")
        self._pd = NumericOption("pd", "pixel depth-of-field - default: 0.000000")
        self._ps = IntegerOption("ps", "pixel sample - default: 4")
        self._pt = NumericOption("pt", "pixel threshold - default: 0.050000")
        self._t = IntegerOption("t", "time between reports - default: 0")
        self._w = BoolOption("w", "warning messages - default: on")
        self._i = BoolOption("i", "irradiance calculation - default: off")
        self._u = BoolOption(
            "u", "correlated quasi-Monte Carlo sampling - default: off"
        )
        self._bv = BoolOption("bv", "back face visibility - default: on")
        self._dt = NumericOption("dt", "direct threshold - default: 0.050000")
        self._dc = NumericOption("dc", "direct certainty - default: 0.500000")
        self._dj = NumericOption("dj", "direct jitter - default: 0.000000")
        self._ds = NumericOption("ds", "direct sampling - default: 0.250000")
        self._dr = IntegerOption("dr", "direct relays - default: 1")
        self._dp = IntegerOption("dp", "direct pretest density - default: 512")
        self._dv = BoolOption("dv", "direct visibility - default: on")
        self._ss = NumericOption("ss", "specular sampling - default: 1.000000")
        self._st = NumericOption("st", "specular threshold - default: 0.150000")
        self._av = TupleOption(
            "av", "ambient value - default: 0.000000 0.000000 0.000000", 3, float
        )
        self._aw = IntegerOption("aw", "ambient value weight - default: 0")
        self._ab = IntegerOption("ab", "ambient bounces - default: 0")
        self._aa = NumericOption("aa", "ambient accuracy - default: 0.200000")
        self._ar = IntegerOption("ar", "ambient resolution - default: 64")
        self._ad = IntegerOption("ad", "ambient divisions - default: 512")
        self._as_ = IntegerOption("as_", "ambient super-samples - default: 128")
        self._me = TupleOption(
            "me",
            "mist extinction coefficient - default: 0.00e+00 0.00e+00 0.00e+00",
            3,
            float,
        )
        self._ma = TupleOption(
            "ma",
            "mist scattering albedo - default: 0.000000 0.000000 0.000000",
            3,
            float,
        )
        self._mg = NumericOption(
            "mg", "mist scattering eccentricity - default: 0.000000"
        )
        self._ms = NumericOption("ms", "mist sampling distance - default: 0.000000")
        self._lr = IntegerOption("lr", "limit reflection - default: 7")
        self._lw = NumericOption("lw", "limit weight - default: 1.00e-03")
        self._am = NumericOption("am", "max photon search radius - default: 0.0")
        self._on_setattr_check = True

    @property
    def vt(self):
        """view type perspective - default: vtv"""
        return self._vt

    @vt.setter
    def vt(self, value):
        self._vt.value = value

    @property
    def vp(self):
        """view point - default: 0.000000 0.000000 0.000000"""
        return self._vp

    @vp.setter
    def vp(self, value):
        self._vp.value = value

    @property
    def vd(self):
        """view direction - default: 0.000000 1.000000 0.000000"""
        return self._vd

    @vd.setter
    def vd(self, value):
        self._vd.value = value

    @property
    def vu(self):
        """view up - default: 0.000000 0.000000 1.000000"""
        return self._vu

    @vu.setter
    def vu(self, value):
        self._vu.value = value

    @property
    def vh(self):
        """view horizontal size - default: 45.000000"""
        return self._vh

    @vh.setter
    def vh(self, value):
        self._vh.value = value

    @property
    def vv(self):
        """view vertical size - default: 45.000000"""
        return self._vv

    @vv.setter
    def vv(self, value):
        self._vv.value = value

    @property
    def vo(self):
        """view fore clipping plane - default: 0.000000"""
        return self._vo

    @vo.setter
    def vo(self, value):
        self._vo.value = value

    @property
    def va(self):
        """view aft clipping plane - default: 0.000000"""
        return self._va

    @va.setter
    def va(self, value):
        self._va.value = value

    @property
    def vs(self):
        """view shift - default: 0.000000"""
        return self._vs

    @vs.setter
    def vs(self, value):
        self._vs.value = value

    @property
    def vl(self):
        """view lift - default: 0.000000"""
        return self._vl

    @vl.setter
    def vl(self, value):
        self._vl.value = value

    @property
    def x(self):
        """x resolution - default: 512"""
        return self._x

    @x.setter
    def x(self, value):
        self._x.value = value

    @property
    def y(self):
        """y resolution - default: 512"""
        return self._y

    @y.setter
    def y(self, value):
        self._y.value = value

    @property
    def pa(self):
        """pixel aspect ratio - default: 1.000000"""
        return self._pa

    @pa.setter
    def pa(self, value):
        self._pa.value = value

    @property
    def pj(self):
        """pixel jitter - default: 0.670000"""
        return self._pj

    @pj.setter
    def pj(self, value):
        self._pj.value = value

    @property
    def pm(self):
        """pixel motion - default: 0.000000"""
        return self._pm

    @pm.setter
    def pm(self, value):
        self._pm.value = value

    @property
    def pd(self):
        """pixel depth-of-field - default: 0.000000"""
        return self._pd

    @pd.setter
    def pd(self, value):
        self._pd.value = value

    @property
    def ps(self):
        """pixel sample - default: 4"""
        return self._ps

    @ps.setter
    def ps(self, value):
        self._ps.value = value

    @property
    def pt(self):
        """pixel threshold - default: 0.050000"""
        return self._pt

    @pt.setter
    def pt(self, value):
        self._pt.value = value

    @property
    def t(self):
        """time between reports - default: 0"""
        return self._t

    @t.setter
    def t(self, value):
        self._t.value = value

    @property
    def w(self):
        """warning messages - default: on"""
        return self._w

    @w.setter
    def w(self, value):
        self._w.value = value

    @property
    def i(self):
        """irradiance calculation - default: off"""
        return self._i

    @i.setter
    def i(self, value):
        self._i.value = value

    @property
    def u(self):
        """correlated quasi-Monte Carlo sampling - default: off"""
        return self._u

    @u.setter
    def u(self, value):
        self._u.value = value

    @property
    def bv(self):
        """back face visibility - default: on"""
        return self._bv

    @bv.setter
    def bv(self, value):
        self._bv.value = value

    @property
    def dt(self):
        """direct threshold - default: 0.050000"""
        return self._dt

    @dt.setter
    def dt(self, value):
        self._dt.value = value

    @property
    def dc(self):
        """direct certainty - default: 0.500000"""
        return self._dc

    @dc.setter
    def dc(self, value):
        self._dc.value = value

    @property
    def dj(self):
        """direct jitter - default: 0.000000"""
        return self._dj

    @dj.setter
    def dj(self, value):
        self._dj.value = value

    @property
    def ds(self):
        """direct sampling - default: 0.250000"""
        return self._ds

    @ds.setter
    def ds(self, value):
        self._ds.value = value

    @property
    def dr(self):
        """direct relays - default: 1"""
        return self._dr

    @dr.setter
    def dr(self, value):
        self._dr.value = value

    @property
    def dp(self):
        """direct pretest density - default: 512"""
        return self._dp

    @dp.setter
    def dp(self, value):
        self._dp.value = value

    @property
    def dv(self):
        """direct visibility - default: on"""
        return self._dv

    @dv.setter
    def dv(self, value):
        self._dv.value = value

    @property
    def ss(self):
        """specular sampling - default: 1.000000"""
        return self._ss

    @ss.setter
    def ss(self, value):
        self._ss.value = value

    @property
    def st(self):
        """specular threshold - default: 0.150000"""
        return self._st

    @st.setter
    def st(self, value):
        self._st.value = value

    @property
    def av(self):
        """ambient value - default: 0.000000 0.000000 0.000000"""
        return self._av

    @av.setter
    def av(self, value):
        self._av.value = value

    @property
    def aw(self):
        """ambient value weight - default: 0"""
        return self._aw

    @aw.setter
    def aw(self, value):
        self._aw.value = value

    @property
    def ab(self):
        """ambient bounces - default: 0"""
        return self._ab

    @ab.setter
    def ab(self, value):
        self._ab.value = value

    @property
    def aa(self):
        """ambient accuracy - default: 0.200000"""
        return self._aa

    @aa.setter
    def aa(self, value):
        self._aa.value = value

    @property
    def ar(self):
        """ambient resolution - default: 64"""
        return self._ar

    @ar.setter
    def ar(self, value):
        self._ar.value = value

    @property
    def ad(self):
        """ambient divisions - default: 512"""
        return self._ad

    @ad.setter
    def ad(self, value):
        self._ad.value = value

    @property
    def as_(self):
        """ambient super-samples - default: 128"""
        return self._as_

    @as_.setter
    def as_(self, value):
        self._as_.value = value

    @property
    def me(self):
        """mist extinction coefficient - default: 0.00e+00 0.00e+00 0.00e+00"""
        return self._me

    @me.setter
    def me(self, value):
        self._me.value = value

    @property
    def ma(self):
        """mist scattering albedo - default: 0.000000 0.000000 0.000000"""
        return self._ma

    @ma.setter
    def ma(self, value):
        self._ma.value = value

    @property
    def mg(self):
        """mist scattering eccentricity - default: 0.000000"""
        return self._mg

    @mg.setter
    def mg(self, value):
        self._mg.value = value

    @property
    def ms(self):
        """mist sampling distance - default: 0.000000"""
        return self._ms

    @ms.setter
    def ms(self, value):
        self._ms.value = value

    @property
    def lr(self):
        """limit reflection - default: 7"""
        return self._lr

    @lr.setter
    def lr(self, value):
        self._lr.value = value

    @property
    def lw(self):
        """limit weight - default: 1.00e-03"""
        return self._lw

    @lw.setter
    def lw(self, value):
        self._lw.value = value

    @property
    def am(self):
        """max photon search radius - default: 0.0"""
        return self._am

    @am.setter
    def am(self, value):
        self._am.value = value
