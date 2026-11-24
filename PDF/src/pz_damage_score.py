"""Score how far a prepared (Roblox) model drifts from its original, from pz_damage_views.py renders.

python pz_damage_score.py <orig_prefix> <prep_prefix>   ->  prints one JSON line

Per view: mean absolute RGB difference (0-255 scale) over pixels covered by either silhouette, plus the silhouette
mismatch (share of covered pixels where only one image has the model). Score = colour difference averaged over the
three views; 0 = identical. Rough guide from the train before the fix: > 25 = visibly torn or smeared."""
import sys, json
import numpy as np
from PIL import Image

def load(p):
    return np.asarray(Image.open(p).convert("RGBA"), dtype=np.float32)

def score(orig_prefix, prep_prefix):
    views = {}
    for v in ("side", "front34", "top"):
        a, b = load(f"{orig_prefix}_{v}.png"), load(f"{prep_prefix}_{v}.png")
        ma, mb = a[..., 3] > 8, b[..., 3] > 8
        cover = ma | mb
        both = ma & mb
        colour = float(np.abs(a[..., :3][both] - b[..., :3][both]).mean()) if both.any() else 255.0
        sil = float((ma ^ mb).sum() / max(1, cover.sum()))
        views[v] = dict(colour=round(colour, 1), silhouette_mismatch=round(sil, 3))
    total = round(sum(x["colour"] for x in views.values()) / len(views), 1)
    return dict(score=total, views=views)

if __name__ == "__main__":
    print(json.dumps(score(sys.argv[1], sys.argv[2])))
