
import sys
import os
import unittest

from typing import (
    Tuple,
    Sequence,
)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASEDIR, ".."))

from color_hsluv_to_rgb import (
    hsluv_to_rgb,
    hsluv_from_rgb,

    hsluv_to_hexcode,
    hsluv_from_hexcode,
)


def seq_round(seq: Sequence[float], prec: float) -> Tuple[float, ...]:
    return tuple(round(val, prec) for val in seq)


class Testing(unittest.TestCase):

    def test_hsluv_from_hexcode(self):
        self.assertEqual(seq_round(hsluv_from_hexcode("CD8B00"), 4), (48.837, 100.0, 62.8823))
        self.assertEqual(seq_round(hsluv_from_hexcode("000000"), 4), (0.0, 0.0, 0.0))
        self.assertEqual(seq_round(hsluv_from_hexcode("FFFFFF"), 4), (0.0, 0.0, 100.0))
        self.assertEqual(seq_round(hsluv_from_hexcode("FF0000"), 4), (12.1771, 100.0, 53.2371))
        self.assertEqual(seq_round(hsluv_from_hexcode("00FF00"), 4), (127.715, 100.0, 87.7355))
        self.assertEqual(seq_round(hsluv_from_hexcode("0000FF"), 4), (265.8743, 100.0, 32.3009))

    def test_hsluv_to_hexcode(self):
        self.assertEqual(hsluv_to_hexcode(48.84, 100.0, 62.88), "CD8B00")
        self.assertEqual(hsluv_to_hexcode(0.0, 0.0, 0.0), "000000")
        self.assertEqual(hsluv_to_hexcode(0.0, 0.0, 100.0), "FFFFFF")
        self.assertEqual(hsluv_to_hexcode(12.1771, 100.0, 53.2371), "FF0000")
        self.assertEqual(hsluv_to_hexcode(127.715, 100.0, 87.7355), "00FF00")
        self.assertEqual(hsluv_to_hexcode(265.8743, 100.0, 32.3009), "0000FF")


if __name__ == '__main__':
    unittest.main()
