"""Make a GLB's metalness explicit for Roblox: multiply each metallicRoughness texture's blue (metal) channel by the
material's metallicFactor, then set the factor to 1. Blender's glTF exporter writes B = 1 with a small factor when
Metallic is a constant; Roblox ignores the factor and renders the whole model as chrome (it looks flat grey).

python pz_glb_fix_metal.py <in.glb> [out.glb]      (out defaults to in; prints one line per fixed image)"""
import io, json, struct, sys
import numpy as np
from PIL import Image

def fix(src, dst):
    b = open(src, "rb").read()
    jl = struct.unpack_from("<I", b, 12)[0]
    js = json.loads(b[20:20 + jl])
    bin0 = 20 + jl + 8
    blen = struct.unpack_from("<I", b, 20 + jl)[0]
    binary = b[bin0:bin0 + blen]
    views = [bytes(binary[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]) for v in js["bufferViews"]]
    done, report = {}, []
    for mat in js.get("materials", []):
        pbr = mat.get("pbrMetallicRoughness", {})
        t = pbr.get("metallicRoughnessTexture")
        f = pbr.get("metallicFactor", 1.0)
        if not t or f >= 0.999:
            continue
        img_i = js["textures"][t["index"]]["source"]
        if img_i in done and done[img_i] != f:
            raise SystemExit(f"image {img_i} shared by materials with different metallicFactor")
        if img_i not in done:
            im = js["images"][img_i]
            a = np.asarray(Image.open(io.BytesIO(views[im["bufferView"]])).convert("RGB"), dtype=np.float32)
            before = a[..., 2].mean()
            a[..., 2] = np.clip(np.round(a[..., 2] * f), 0, 255)
            out = io.BytesIO()
            if im.get("mimeType") == "image/jpeg":
                Image.fromarray(a.astype(np.uint8)).save(out, "JPEG", quality=95)
            else:
                Image.fromarray(a.astype(np.uint8)).save(out, "PNG")
            views[im["bufferView"]] = out.getvalue()
            done[img_i] = f
            report.append(f"{im.get('name', img_i)}: metal B {before:.0f} -> {a[..., 2].mean():.1f} (factor {f:.3f})")
        pbr["metallicFactor"] = 1.0
    if not report:
        print("NO_CHANGE", src); return
    blob = bytearray()
    for v, data in zip(js["bufferViews"], views):
        while len(blob) % 4:
            blob += b"\0"
        v["byteOffset"] = len(blob); v["byteLength"] = len(data); v["buffer"] = 0
        blob += data
    while len(blob) % 4:
        blob += b"\0"
    js["buffers"] = [{"byteLength": len(blob)}]
    jb = json.dumps(js, separators=(",", ":")).encode()
    jb += b" " * ((4 - len(jb) % 4) % 4)
    total = 12 + 8 + len(jb) + 8 + len(blob)
    with open(dst, "wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, total))
        fh.write(struct.pack("<II", len(jb), 0x4E4F534A)); fh.write(jb)
        fh.write(struct.pack("<II", len(blob), 0x004E4942)); fh.write(blob)
    for r in report:
        print("FIXED", r)
    print("WROTE", dst, f"{total / 1e6:.2f} MB")

if __name__ == "__main__":
    fix(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
