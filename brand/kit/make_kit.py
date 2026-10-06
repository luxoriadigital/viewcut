# -*- coding: utf-8 -*-
"""Build the Viewcut logo kit from concept A (Cadre tranche)."""
import math, os, io, re
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

KIT = r"C:\Users\moham\Downloads\viewcut\brand\kit"
FONT = os.path.join(os.environ["TEMP"], r"opencode\fonts\Inter-var.ttf")
os.makedirs(KIT, exist_ok=True)

def r2(s):
    return re.sub(r"-?\d+\.\d{3,}", lambda m: "%.2f" % float(m.group()), s)

# ---------- symbol geometry (concept A) ----------
W = H = 256.0
RX, RY, S, RAD = 36.0, 36.0, 184.0, 44.0
CX = CY = 128.0
ANG = math.radians(-30.0)
DX, DY = math.cos(ANG), math.sin(ANG)
NX, NY = -DY, DX            # normal (down-right side)
OFFX, OFFY = 14 * DX, 14 * DY   # slide along the cut
REB = (-6.05, 3.5)          # optical rebalance of the whole mark

def cut_polys(gap, pre):
    h = gap / 2.0
    def pts(sgn):
        ax, ay = CX + 500 * DX + sgn * h * NX, CY + 500 * DY + sgn * h * NY
        bx, by = CX - 500 * DX + sgn * h * NX, CY - 500 * DY + sgn * h * NY
        k = sgn * 400
        return (ax, ay, bx, by, bx + k * NX, by + k * NY, ax + k * NX, ay + k * NY)
    lo, up = pts(+1), pts(-1)
    def poly(v, idn):
        return ('    <clipPath id="%s"><polygon points="%.2f,%.2f %.2f,%.2f '
                '%.2f,%.2f %.2f,%.2f"/></clipPath>\n') % (idn, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7])
    body = '  <defs>\n' + poly(lo, pre + 'Lower') + poly(up, pre + 'Upper') + '  </defs>\n'
    body += '  <g transform="translate(%.3f,%.3f)">\n' % REB
    body += ('    <rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" clip-path="url(#%sLower)"/>\n'
             % (RX, RY, S, S, RAD, pre))
    body += '    <g transform="translate(%.3f,%.3f)">\n' % (OFFX, OFFY)
    body += ('      <rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" clip-path="url(#%sUpper)"/>\n'
             % (RX, RY, S, S, RAD, pre))
    body += '    </g>\n  </g>\n'
    return body

def symbol_file(path, gap, pre, title="Viewcut"):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" '
           'aria-label="Viewcut">\n  <title>%s</title>\n' % title) + cut_polys(gap, pre) + '</svg>\n'
    io.open(path, "w", encoding="utf-8").write(svg)

symbol_file(os.path.join(KIT, "viewcut-symbol.svg"), 18, "vcSym")
symbol_file(os.path.join(KIT, "viewcut-symbol-small.svg"), 24, "vcSsm")      # small-size cut
symbol_file(os.path.join(KIT, "viewcut-symbol-reversed.svg"), 21, "vcSrv")  # thinned white

# ink box of the symbol in its 256-space (rect + rebalance + slide)
IX0 = RX + REB[0]
IX1 = RX + S + REB[0] + OFFX
IY0 = RY + REB[1] + OFFY
IY1 = RY + S + REB[1]
IW, IH = IX1 - IX0, IY1 - IY0

# ---------- wordmark: Inter 900 outlined ----------
SIZE = 170.0
TRACK = -0.022
WORD = "Viewcut"
font = TTFont(FONT)
axes = {a.axisTag for a in font["fvar"].axes} if "fvar" in font else set()
pin = {"wght": 900}
if "opsz" in axes:
    pin["opsz"] = 28
font = instancer.instantiateVariableFont(font, pin, inplace=True)
upem = font["head"].unitsPerEm
s = SIZE / upem
cap = font["OS/2"].sCapHeight * s
cmap = font.getBestCmap()
hmtx = font["hmtx"]
gs = font.getGlyphSet()

x = 0.0
parts = []
bminx = bminy = 1e9
bmaxx = bmaxy = -1e9
for ch in WORD:
    gname = cmap[ord(ch)]
    tr = Transform().translate(x, 0.0).scale(s, -s)
    pen = SVGPathPen(gs)
    bpen = BoundsPen(gs)
    glyph = gs[gname]
    glyph.draw(TransformPen(pen, tr))
    glyph.draw(TransformPen(bpen, tr))
    parts.append(pen.getCommands())
    if bpen.bounds:
        gx0, gy0, gx1, gy1 = bpen.bounds
        bminx, bminy = min(bminx, gx0), min(bminy, gy0)
        bmaxx, bmaxy = max(bmaxx, gx1), max(bmaxy, gy1)
    x += hmtx[gname][0] * s + TRACK * SIZE

word_d = " ".join(parts)
word_w = x - TRACK * SIZE
# baseline placed so the ink sits centered later; store raw (baseline y=0, y-up flipped)
PAD = 8.0
# flipped space: cap top at y=PAD, baseline at y=PAD+cap  (ink may overshoot slightly)
BASE = PAD - bminy
vb_w = (bmaxx - bminx) + 2 * PAD
vb_h = (bmaxy - bminy) + 2 * PAD
# shift path: translate so bminx -> PAD, and baseline -> BASE
TX = PAD - bminx

def word_transformed(tx):
    # rebuild parts with final placement (baseline at BASE, left ink at TX)
    xp = tx
    out = []
    x0 = bminx
    for ch in WORD:
        gname = cmap[ord(ch)]
        tr = Transform().translate(xp, BASE).scale(s, -s)
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, tr))
        out.append(pen.getCommands())
        xp += hmtx[gname][0] * s + TRACK * SIZE
    return " ".join(out)

# ---------- wordmark file ----------
d_word = word_transformed(TX)
wm = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" role="img" '
      'aria-label="Viewcut">\n  <title>Viewcut wordmark</title>\n'
      '  <path fill="#000000" d="%s"/>\n</svg>\n') % (vb_w, vb_h, r2(d_word))
io.open(os.path.join(KIT, "viewcut-wordmark.svg"), "w", encoding="utf-8").write(wm)

# ---------- horizontal lockup ----------
LW, LH = 1024.0, 256.0
sym_h = 160.0                 # visible symbol height in the lockup
k = sym_h / IH
word_size = 148.0
s2 = word_size / upem
cap2 = font["OS/2"].sCapHeight * s2
# measure word at lockup size
xw = 0.0
minx = 1e9; maxx = -1e9
for ch in WORD:
    gname = cmap[ord(ch)]
    tr = Transform().translate(xw, 0.0).scale(s2, -s2)
    bpen = BoundsPen(gs)
    gs[gname].draw(TransformPen(bpen, tr))
    if bpen.bounds:
        minx = min(minx, bpen.bounds[0]); maxx = max(maxx, bpen.bounds[2])
    xw += hmtx[gname][0] * s2 + TRACK * word_size
word_w2 = (maxx - minx)
gap_w = 0.55 * cap2
content_w = IW * k + gap_w + word_w2
pad = (LW - content_w) / 2.0
sym_x = pad - IX0 * k
sym_y = (LH - sym_h) / 2.0 - IY0 * k
word_left = pad + IW * k + gap_w - minx
base_y = LH / 2.0 + cap2 / 2.0

d_h = word_transformed  # noqa (keep helper)
def word_at(size, left_ink, baseline):
    sw = size / upem
    x0 = 0.0
    minxx = 1e9
    for ch in WORD:
        gname = cmap[ord(ch)]
        tr = Transform().translate(x0, 0.0).scale(sw, -sw)
        bpen = BoundsPen(gs)
        gs[gname].draw(TransformPen(bpen, tr))
        if bpen.bounds:
            minxx = min(minxx, bpen.bounds[0])
        x0 += hmtx[gname][0] * sw + TRACK * size
    shift = left_ink - minxx
    xp = shift
    out = []
    for ch in WORD:
        gname = cmap[ord(ch)]
        tr = Transform().translate(xp, baseline).scale(sw, -sw)
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, tr))
        out.append(pen.getCommands())
        xp += hmtx[gname][0] * sw + TRACK * size
    return " ".join(out)

d_lock = word_at(word_size, word_left, base_y)
hor = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 256" role="img" '
       'aria-label="Viewcut">\n  <title>Viewcut</title>\n'
       '  <defs>\n%s  </defs>\n'
       '  <g transform="translate(%.2f,%.2f) scale(%.5f)">\n'
       '    <g transform="translate(%.3f,%.3f)">\n'
       '      <rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" clip-path="url(#vcHorLower)"/>\n'
       '      <g transform="translate(%.3f,%.3f)">\n'
       '        <rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" clip-path="url(#vcHorUpper)"/>\n'
       '      </g>\n    </g>\n  </g>\n'
       '  <path fill="#000000" d="%s"/>\n</svg>\n')

def clip_defs(pre):
    out = ""
    h = 9.0
    for name, sgn in (("Lower", 1), ("Upper", -1)):
        ax, ay = CX + 500 * DX + sgn * h * NX, CY + 500 * DY + sgn * h * NY
        bx, by = CX - 500 * DX + sgn * h * NX, CY - 500 * DY + sgn * h * NY
        k2 = sgn * 400
        out += ('    <clipPath id="%s%s"><polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f"/></clipPath>\n'
                % (pre, name, ax, ay, bx, by, bx + k2 * NX, by + k2 * NY, ax + k2 * NX, ay + k2 * NY))
    return out

hor = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 256" role="img" aria-label="Viewcut">\n'
       '  <title>Viewcut</title>\n  <defs>\n' + clip_defs("vcHor") + '  </defs>\n'
       '  <g transform="translate(%.2f,%.2f) scale(%.5f)">\n'
       '    <g transform="translate(%.3f,%.3f)">\n'
       '      <rect x="36" y="36" width="184" height="184" rx="44" clip-path="url(#vcHorLower)"/>\n'
       '      <g transform="translate(%.3f,%.3f)">\n'
       '        <rect x="36" y="36" width="184" height="184" rx="44" clip-path="url(#vcHorUpper)"/>\n'
       '      </g>\n    </g>\n  </g>\n'
       '  <path fill="#000000" d="%s"/>\n</svg>\n'
       % (sym_x, sym_y, k, REB[0], REB[1], OFFX, OFFY, r2(d_lock)))
io.open(os.path.join(KIT, "viewcut-horizontal.svg"), "w", encoding="utf-8").write(hor)

# ---------- stacked lockup ----------
SW2, SH2 = 512.0, 512.0
sym2 = 200.0
k2 = sym2 / IH
word_size3 = 112.0
sw3 = word_size3 / upem
cap3 = font["OS/2"].sCapHeight * sw3
# measure
x0 = 0.0; minx3 = 1e9; maxx3 = -1e9
for ch in WORD:
    gname = cmap[ord(ch)]
    tr = Transform().translate(x0, 0.0).scale(sw3, -sw3)
    bpen = BoundsPen(gs)
    gs[gname].draw(TransformPen(bpen, tr))
    if bpen.bounds:
        minx3 = min(minx3, bpen.bounds[0]); maxx3 = max(maxx3, bpen.bounds[1] if False else bpen.bounds[2])
    x0 += hmtx[gname][0] * sw3 + TRACK * word_size3
word_w3 = maxx3 - minx3
gap3 = 52.0
content_h = sym2 + gap3 + cap3
top = (SH2 - content_h) / 2.0
sym_x2 = (SW2 - IW * k2) / 2.0 - IX0 * k2
sym_y = top - IY0 * k2
word_cx = SW2 / 2.0
word_left3 = word_cx - word_w3 / 2.0 - minx3
base3 = top + sym2 + gap3 + cap3
d_stk = word_at(word_size3, word_left3, base3)
stk = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Viewcut">\n'
       '  <title>Viewcut</title>\n  <defs>\n' + clip_defs("vcStk") + '  </defs>\n'
       '  <g transform="translate(%.2f,%.2f) scale(%.5f)">\n'
       '    <g transform="translate(%.3f,%.3f)">\n'
       '      <rect x="36" y="36" width="184" height="184" rx="44" clip-path="url(#vcStkLower)"/>\n'
       '      <g transform="translate(%.3f,%.3f)">\n'
       '        <rect x="36" y="36" width="184" height="184" rx="44" clip-path="url(#vcStkUpper)"/>\n'
       '      </g>\n    </g>\n  </g>\n'
       '  <path fill="#000000" d="%s"/>\n</svg>\n'
       % (sym_x2, sym_y, k2, REB[0], REB[1], OFFX, OFFY, r2(d_stk)))
io.open(os.path.join(KIT, "viewcut-stacked.svg"), "w", encoding="utf-8").write(stk)

print("kit written:", sorted(os.listdir(KIT)))
print("word w@170: %.1f cap@170: %.1f | lockup word w@148: %.1f cap2: %.1f" % (word_w, cap, word_w2, cap2))
print("horizontal pad: %.1f gap: %.1f | stacked word w: %.1f" % (pad, gap_w, word_w3))
