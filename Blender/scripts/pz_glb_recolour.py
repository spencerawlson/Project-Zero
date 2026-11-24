"""Recolour the accent colour of a prepared GLB: move one hue band to a new hue, leaving neutral (grey/black/
white) pixels alone. Used to turn the owner's Crimson Nightwing wings' red glow cyan (owner request 2026-11-24).

python pz_glb_recolour.py <in.glb> <out.glb> <from_hue_deg> <to_hue_deg> [band_deg=40] [min_sat=0.30]

Only base-colour images are changed (the material's baseColorTexture). A pixel is recoloured when its saturation
is at least min_sat and its hue is within band_deg of from_hue; its saturation and value are kept, so glow
brightness and shading are unchanged. Neutral panels never move. Prints the share of pixels changed per image."""
import io, json, struct, sys
import numpy as np
from PIL import Image

def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    h = h * 60.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx

def hsv_to_rgb(h, s, v):
    c = v * s
    hp = (h % 360) / 60.0
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(h)
    conds = [(hp < 1), (hp < 2), (hp < 3), (hp < 4), (hp < 5), (hp >= 5)]
    vals = [(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]
    r = np.select(conds, [v_[0] for v_ in vals]); g = np.select(conds, [v_[1] for v_ in vals]); b = np.select(conds, [v_[2] for v_ in vals])
    m = v - c
    return np.stack([r + m, g + m, b + m], -1)

def main(src, dst, from_h, to_h, band=40.0, min_sat=0.30):
    data = open(src, "rb").read()
    jl = struct.unpack_from("<I", data, 12)[0]
    js = json.loads(data[20:20 + jl])
    bin0 = 20 + jl + 8
    blen = struct.unpack_from("<I", data, 20 + jl)[0]
    binary = data[bin0:bin0 + blen]
    views = [bytes(binary[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]) for v in js["bufferViews"]]
    colour_images = set()
    for mat in js.get("materials", []):
        t = mat.get("pbrMetallicRoughness", {}).get("baseColorTexture")
        if t is not None:
            colour_images.add(js["textures"][t["index"]]["source"])
    for i in sorted(colour_images):
        im = js["images"][i]
        a = np.asarray(Image.open(io.BytesIO(views[im["bufferView"]])).convert("RGB"), dtype=np.float32) / 255.0
        h, s, v = rgb_to_hsv(a)
        dist = np.abs(((h - from_h + 180) % 360) - 180)
        sel = (s >= min_sat) & (dist <= band) & (v > 0.05)
        h2 = np.where(sel, (h - from_h + to_h) % 360, h)
        out = np.where(sel[..., None], hsv_to_rgb(h2, s, v), a)
        buf = io.BytesIO()
        img = Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8))
        if im.get("mimeType") == "image/jpeg":
            img.save(buf, "JPEG", quality=95)
        else:
            img.save(buf, "PNG")
        views[im["bufferView"]] = buf.getvalue()
        print(f"RECOLOURED {im.get('name', i)}: {sel.mean() * 100:.1f}% of pixels moved {from_h:.0f} -> {to_h:.0f} deg")
    blob = bytearray()
    for v_, d_ in zip(js["bufferViews"], views):
        while len(blob) % 4:
            blob += b"\0"
        v_["byteOffset"] = len(blob); v_["byteLength"] = len(d_); v_["buffer"] = 0
        blob += d_
    while len(blob) % 4:
        blob += b"\0"
    js["buffers"] = [{"byteLength": len(blob)}]
    jb = json.dumps(js, separators=(",", ":")).encode()
    jb += b" " * ((4 - len(jb) % 4) % 4)
    with open(dst, "wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, 28 + len(jb) + len(blob)))
        fh.write(struct.pack("<II", len(jb), 0x4E4F534A)); fh.write(jb)
        fh.write(struct.pack("<II", len(blob), 0x004E4942)); fh.write(blob)
    print("WROTE", dst)

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], float(a[2]), float(a[3]), float(a[4]) if len(a) > 4 else 40.0, float(a[5]) if len(a) > 5 else 0.30)
