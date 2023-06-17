# X.
from color_hsluv_to_rgb import (
    hsluv_to_rgb,
    hsluv_from_rgb,

    hsluv_to_hexcode,
    hsluv_from_hexcode,
)

def hexcode_to_rgb(h):
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def hsluv_from_hexcode(h):
    rgb = hexcode_to_rgb(h)
    return hsluv_from_rgb(*rgb)

with open("/src/emacs/inkpot-theme/inkpot-theme.el", 'r', encoding='utf-8') as fh:
    data = fh.read()
ls = data.splitlines(keepends=True)

NAMED_VALUES = {}

for i in range(len(ls)):
    line = ls[i]
    if not line.endswith(" NAMED_VALUES_BEGIN\n"):
        continue
    i += 1

    while not (line := ls[i]).endswith(" NAMED_VALUES_END\n"):
        line = line.lstrip(";").strip()
        x = line.find(";")
        if x != -1:
            line = line[:x]
        k, v = line.split()
        NAMED_VALUES[k] = v
        print(k, v)
        i += 1

    break

for i in range(len(ls)):
    line = ls[i]
    nhex = line.find(' "#')
    if nhex == -1:
        continue
    nhex += 3
    hex_color = line[nhex: nhex + 6]

    ntmp = line.find(' ; (', nhex + 6)
    if ntmp == -1:
        continue

    beg = ntmp + 4
    end = line.find(')', beg)
    if end == -1:
        print("No matching bracket for template, line:", i + 1)

    hsluv_color = line[beg:end].strip()

    if not hsluv_color:
        hsluv_color = "{:.3f}, {:.3f}, {:.3f}".format(*hsluv_from_hexcode(hex_color))
        ls[i] = line[:beg] + hsluv_color + line[end:]
    else:
        value_str = [(c.strip()) for c in hsluv_color.split(",")]
        for j in range(3):
            t =  NAMED_VALUES.get(value_str[j])
            if t is not None:
                value_str[j] = t
            value_str[j] = float(value_str[j])

        hx = hsluv_to_hexcode(*value_str)
        ls[i] = line[:nhex] + hx.lower() + line[nhex+6:]



data = "".join(ls)


with open("/src/emacs/inkpot-theme/inkpot-theme.el", 'w', encoding='utf-8') as fh:
    fh.write(data)
