# X.
from color_hsluv_to_rgb import (
    hsluv_to_rgb,
    hsluv_from_rgb,
)

def hexcode_to_rgb(h):
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def hsluv_from_hexcode(h):
    rgb = hexcode_to_rgb(h)
    return hsluv_from_rgb(*rgb)



# print(*hsluv_to_rgb(355.0, 90.0, 100.0))
# print(hsluv_from_rgb(*hsluv_to_rgb(355.0, 90.0, 100.0)))
# print(hsluv_to_rgb(*hsluv_from_rgb(0, 1, 0)))

# print(hsluv_from_hexcode("cd8b00"))
