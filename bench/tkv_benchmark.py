"""Benchmark NephroRx's Total Kidney Volume (TKV) step against voxel-count ground truth.

What it measures
----------------
For every labelled kidney mask (KiTS-style NIfTI: 0 = background, >0 = kidney/tumor/cyst):

* reference TKV = (# voxels with label > 0) x voxel volume  -- the standard way TKV is
  read off a ground-truth segmentation
* NephroRx TKV  = ``calculations.process_seg_file(...)["volume_cm3"]`` -- the exact function
  the ``/analyze`` endpoint calls (marching cubes, step_size=2, signed-tetrahedron volume)
* latency       = wall-clock time of that call (NIfTI load + meshing + volume), best of N

This isolates the geometry pipeline. It does NOT measure segmentation quality: the input is
already a ground-truth mask, so the AI segmentation step (TotalSegmentator) is skipped, exactly as
the app does when it receives a mask.

Usage
-----
    python bench/tkv_benchmark.py backend/samples/segmentation.nii.gz
    python bench/tkv_benchmark.py path/to/kits23/dataset --repeats 1 --out bench/results_kits23

A directory argument is searched recursively for ``segmentation.nii.gz`` files.
"""

from __future__ import annotations

import argparse
import csv
import os
import platform
import statistics
import sys
import time
from pathlib import Path

import nibabel as nib
import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "backend"))
import calculations  # noqa: E402  (the app's own module)


def find_masks(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            out.extend(sorted(p.rglob("segmentation.nii.gz")))
        else:
            out.append(p)
    return out


def reference_tkv_ml(path: Path) -> tuple[float, tuple[int, ...], tuple[float, ...]]:
    img = nib.load(str(path))
    data = np.asanyarray(img.dataobj)
    zooms = tuple(float(z) for z in img.header.get_zooms()[:3])
    voxel_ml = float(np.prod(zooms)) / 1000.0
    return float(np.count_nonzero(data)) * voxel_ml, data.shape, zooms


def bench_one(path: Path, repeats: int) -> dict:
    ref_ml, shape, zooms = reference_tkv_ml(path)
    times = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = calculations.process_seg_file(str(path), 1.0)
        times.append(time.perf_counter() - t0)
    app_ml = float(result["volume_cm3"])
    return {
        "case": path.parent.name if path.name == "segmentation.nii.gz" else path.name,
        "shape": "x".join(map(str, shape)),
        "spacing_mm": "x".join(f"{z:.3g}" for z in zooms),
        "ref_ml": round(ref_ml, 2),
        "app_ml": round(app_ml, 2),
        "err_pct": round(100.0 * (app_ml - ref_ml) / ref_ml, 3) if ref_ml else float("nan"),
        "seconds": round(min(times), 3),
        "mesh_vertices": len(result["mesh"]["vertices"]) // 3,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="mask files or directories")
    ap.add_argument("--repeats", type=int, default=3, help="timed runs per mask (best is kept)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N masks (0 = all)")
    ap.add_argument("--out", default=str(REPO / "bench" / "results"), help="output prefix for .csv/.md")
    args = ap.parse_args()

    masks = find_masks(args.paths)
    if args.limit:
        masks = masks[: args.limit]
    if not masks:
        sys.exit("no masks found")

    rows = []
    for i, m in enumerate(masks, 1):
        try:
            r = bench_one(m, args.repeats)
        except Exception as e:  # keep going; report failures in the summary
            print(f"[{i}/{len(masks)}] {m}: FAILED {e}", flush=True)
            continue
        if r["ref_ml"] == 0:
            print(f"[{i}/{len(masks)}] {r['case']}: empty mask, skipped", flush=True)
            continue
        rows.append(r)
        print(f"[{i}/{len(masks)}] {r['case']}: ref {r['ref_ml']} mL  app {r['app_ml']} mL  "
              f"err {r['err_pct']:+.3f}%  {r['seconds']} s", flush=True)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out.with_suffix(".csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    abs_err = [abs(r["err_pct"]) for r in rows]
    secs = sorted(r["seconds"] for r in rows)
    p95 = secs[min(len(secs) - 1, int(round(0.95 * (len(secs) - 1))))]
    summary = {
        "masks": len(rows),
        "failed_or_empty": len(masks) - len(rows),
        "mean_abs_err_pct": round(statistics.mean(abs_err), 3),
        "median_abs_err_pct": round(statistics.median(abs_err), 3),
        "max_abs_err_pct": round(max(abs_err), 3),
        "mean_signed_err_pct": round(statistics.mean(r["err_pct"] for r in rows), 3),
        "median_seconds": round(statistics.median(secs), 3),
        "p95_seconds": round(p95, 3),
        "median_mesh_vertices": int(statistics.median(r["mesh_vertices"] for r in rows)),
    }
    import numpy as _np, skimage as _sk
    env = (f"{platform.processor() or platform.machine()} | {platform.system()} {platform.release()} | "
           f"Python {platform.python_version()} | numpy {_np.__version__} | scikit-image {_sk.__version__} | "
           f"CPU only, single process, best of {args.repeats}")

    md = ["# TKV benchmark", "",
          f"Command: `python bench/tkv_benchmark.py {' '.join(args.paths)} --repeats {args.repeats}"
          + (f" --limit {args.limit}" if args.limit else "") + "`", "",
          f"Environment: {env}", "",
          "| metric | value |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in summary.items()]
    md += ["", f"Per-mask results: `{out.with_suffix('.csv').name}`", ""]
    out.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    main()
