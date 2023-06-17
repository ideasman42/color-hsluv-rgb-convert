# Originally from https://github.com/hsluv/hsluv-python/blob/master/hsluv.py (v5.0.3)

__all__ = (
    "hsluv_to_rgb",
    "hsluv_from_rgb",
)

from math import (
    cos as _cos,
    radians as _radians,
    sin as _sin,
    atan2 as _atan2,
    hypot as _hypot,
    degrees as _degrees,
    pow as _pow,
)

from typing import (
    List,
    Sequence,
    Tuple,
)

_M = (
    (3.240969941904521, -1.537383177570093, -0.498610760293),
    (-0.96924363628087, 1.87596750150772, 0.041555057407175),
    (0.055630079696993, -0.20397695888897, 1.056971514242878),
)
_MIN_V = (
    (0.41239079926595, 0.35758433938387, 0.18048078840183),
    (0.21263900587151, 0.71516867876775, 0.072192315360733),
    (0.019330818715591, 0.11919477979462, 0.95053215224966),
)

_REF_Y = 1.0
_REF_U = 0.19783000664283
_REF_V = 0.46831999493879
_KAPPA = 903.2962962
_EPSILON = 0.0088564516


def _length_of_ray_until_intersect(theta: float, line: Tuple[float, float]) -> float:
    return line[1] / (_sin(theta) - line[0] * _cos(theta))


def _get_bounds(l: float) -> List[Tuple[float, float]]:
    sub1 = _pow(l + 16.0, 3.0) / 1560896.0
    sub2 = sub1 if sub1 > _EPSILON else l / _KAPPA
    # Values are never used.
    result: List[Tuple[float, float]] = [(0.0, 0.0)] * 6
    i = 0
    for m1, m2, m3 in _M:
        for t in range(2):
            top1 = (284517 * m1 - 94839 * m3) * sub2
            top2 = (838422 * m3 + 769860 * m2 + 731718 * m1) * l * sub2 - (769860 * t) * l
            bottom = (632260 * m3 - 126452 * m2) * sub2 + 126452 * t
            # Line is slope intercept pairs.
            result[i] = (top1 / bottom, top2 / bottom)
            i += 1

    return result


def _max_chroma_for_lh(l: float, h: float) -> float:
    hrad = _radians(h)
    lengths = [_length_of_ray_until_intersect(hrad, bound) for bound in _get_bounds(l)]
    return min(length for length in lengths if length >= 0)


def _dot_product(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(i * j for i, j in zip(a, b))


def _from_linear(c: float) -> float:
    if c <= 0.0031308:
        return 12.92 * c
    return (1.055 * _pow(c, (5.0 / 12.0))) - 0.055


def _to_linear(c: float) -> float:
    if c > 0.04045:
        return _pow((c + 0.055) / 1.055, 2.4)
    return c / 12.92


def _l_to_y(l: float) -> float:
    if l <= 8.0:
        return _REF_Y * l / _KAPPA
    return (_REF_Y * _pow((l + 16.0) / 116.0, 3.0))


def _y_to_l(y: float) -> float:
    if y <= _EPSILON:
        return y / _REF_Y * _KAPPA

    return (116.0 * _pow(y / _REF_Y, 1.0 / 3.0) - 16.0)


def _xyz_to_rgb(x: float, y: float, z: float) -> Tuple[float, float, float]:
    xyz = x, y, z
    return (
        _from_linear(_dot_product(_M[0], xyz)),
        _from_linear(_dot_product(_M[1], xyz)),
        _from_linear(_dot_product(_M[2], xyz)),
    )


def _luv_to_xyz(l: float, u: float, v: float) -> Tuple[float, float, float]:
    if l <= 0.0:
        return (0.0, 0.0, 0.0)
    var_u = u / (13 * l) + _REF_U
    var_v = v / (13 * l) + _REF_V
    y = _l_to_y(l)
    x = y * 9 * var_u / (4 * var_v)
    z = y * (12 - 3 * var_u - 20 * var_v) / (4 * var_v)
    return (x, y, z)


def _lch_to_luv(l: float, c: float, h: float) -> Tuple[float, float, float]:
    hrad = _radians(h)
    u = _cos(hrad) * c
    v = _sin(hrad) * c
    return (l, u, v)


def _hsluv_to_lch(h: float, s: float, l: float) -> Tuple[float, float, float]:
    if l > 100.0 - 1e-7:
        return (100.0, 0.0, h)
    if l < 1e-08:
        return (0.0, 0.0, h)
    _hx_max = _max_chroma_for_lh(l, h)
    c = _hx_max / 100.0 * s
    return (l, c, h)


def _lch_to_rgb(l: float, c: float, h: float) -> Tuple[float, float, float]:
    return _xyz_to_rgb(*_luv_to_xyz(*_lch_to_luv(l, c, h)))


def _luv_to_lch(l: float, u: float, v: float) -> Tuple[float, float, float]:
    c = _hypot(u, v)
    if c < 1e-08:
        h = 0.0
    else:
        hrad = _atan2(v, u)
        h = _degrees(hrad)
        if h < 0:
            h += 360.0
    return (l, c, h)


def _rgb_to_xyz(r: float, g: float, b: float) -> Tuple[float, float, float]:
    rgbl = (
        _to_linear(r),
        _to_linear(g),
        _to_linear(b),
    )
    return (
        _dot_product(_MIN_V[0], rgbl),
        _dot_product(_MIN_V[1], rgbl),
        _dot_product(_MIN_V[2], rgbl),
    )


def _xyz_to_luv(x: float, y: float, z: float) -> Tuple[float, float, float]:
    l = _y_to_l(y)
    if l == 0:
        return (0.0, 0.0, 0.0)
    divider = x + 15 * y + 3 * z
    if divider == 0.0:
        u = v = float("nan")
        return (l, u, v)
    var_u = 4 * x / divider
    var_v = 9 * y / divider
    u = 13 * l * (var_u - _REF_U)
    v = 13 * l * (var_v - _REF_V)
    return (l, u, v)


def _rgb_to_lch(r: float, g: float, b: float) -> Tuple[float, float, float]:
    return _luv_to_lch(*_xyz_to_luv(*_rgb_to_xyz(r, g, b)))


def _lch_to_hsluv(l: float, c: float, h: float) -> Tuple[float, float, float]:
    if l > 100 - 1e-7:
        return (h, 0.0, 100)
    if l < 1e-08:
        return (h, 0.0, 0.0)
    _hx_max = _max_chroma_for_lh(l, h)
    # Imprecision can exceed 100.0.
    s = min(c / _hx_max, 1.0)
    return (h, s * 100, l)


# Hex-code functions (for convenience).

def _hexcode_to_rgb(hexcode: str) -> Tuple[float, float, float]:
    return tuple(int(hexcode[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _hexcode_from_rgb(r: float, g: float, b: float) -> str:
    return '{:02X}{:02X}{:02X}'.format(
        max(min(int(round(r * 255)), 255), 0),
        max(min(int(round(g * 255)), 255), 0),
        max(min(int(round(b * 255)), 255), 0),
    )


# Public RGB Functions.

def hsluv_to_rgb(h: float, s: float, l: float) -> Tuple[float, float, float]:
    """ HSL-UV to RGB, where: H [0..360], S [0..100], L [0..100]. """
    return _lch_to_rgb(*_hsluv_to_lch(float(h), float(s), float(l)))


def hsluv_from_rgb(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """ RGB to USL-UV where: R,G,B are between 0 and 1.0. """
    return _lch_to_hsluv(*_rgb_to_lch(r, g, b))


# Public HEX-CODE Functions.

def hsluv_to_hexcode(h: float, s: float, l: float) -> str:
    return _hexcode_from_rgb(*hsluv_to_rgb(h, s, l))


def hsluv_from_hexcode(hexcode: str) -> Tuple[float, float, float]:
    return hsluv_from_rgb(*_hexcode_to_rgb(hexcode))
