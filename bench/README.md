# TKV accuracy benchmark

Checks how close NephroRx's Total Kidney Volume (TKV) is to ground truth, and how long the step
takes per scan.

## Method

* **Data:** the first 50 cases (`case_00000`–`case_00049`) of the public
  [KiTS23](https://github.com/neheller/kits23) kidney-tumor CT dataset (commit `c108835`). Only
  the expert ground-truth masks (`segmentation.nii.gz`) are used, not the CT images. Slice
  thickness ranges from 0.5 mm to 5 mm.
* **Reference TKV:** the number of voxels with label > 0 (kidney, tumor or cyst) × voxel volume.
  This is the standard way to read TKV off a segmentation.
* **NephroRx TKV:** the output of `backend/calculations.py::process_seg_file`. This is the same
  function `/analyze` calls, imported directly, not a re-implementation.
* **Latency:** wall-clock time of that call (NIfTI load + meshing + volume), best of 3, on one CPU
  core.

What this does **not** measure: segmentation quality. The input is already a ground-truth mask, so
the result shows how faithful the geometry pipeline is, not how well an AI model finds the kidney.

## Results (50 KiTS23 scans)

| | mean \|error\| | median \|error\| | max \|error\| | median latency | p95 latency |
|---|---|---|---|---|---|
| Before (hackathon code) | 1.018% | 0.496% | 4.532% | 0.50 s | 2.09 s |
| **After** | **0.027%** | **0.018%** | **0.092%** | **0.58 s** | **3.65 s** |

The full output, with per-scan CSVs, is in [`results_kits23_before.md`](results_kits23_before.md)
and [`results_kits23.md`](results_kits23.md). Machine: AMD desktop CPU, Windows 11, Python 3.14,
numpy 2.5, scikit-image 0.26.

### What changed

The hackathon version ran marching cubes on the raw label volume with `step_size=2`. That caused
three errors:

1. **Skipped slices.** `step_size=2` drops every other slice. On 3–5 mm CT that loses up to
   ~4.5% of the volume. Five of the six worst cases had slices 3–5 mm thick.
2. **Label values bias the surface.** At tumor (2) and cyst (3) boundaries, the 0.5 iso-surface
   sits closer to the background. Even at full resolution this inflated volume by +0.41% on
   average (+0.78% combined with skipped slices).
3. **Open meshes.** Kidneys that touch the edge of the scan produce an open surface, which has no
   well-defined volume.

The fix binarizes the mask, pads it by one voxel, and computes volume from a full-resolution
mesh. The browser still gets the `step_size=2` mesh, so the 3D viewer's payload stays about the
same size.

## Reproduce

```bash
# masks only (~15 MB for 50 cases)
git clone --filter=blob:none --no-checkout --depth 1 https://github.com/neheller/kits23
cd kits23 && git sparse-checkout init --no-cone
for i in $(seq -f "%05g" 0 49); do echo "/dataset/case_$i/segmentation.nii.gz"; done > .git/info/sparse-checkout
git checkout && cd ..

python bench/tkv_benchmark.py kits23/dataset --repeats 3 --out bench/results_kits23
```

CI runs the same script on the bundled sample scan and fails if the error exceeds 1%.

KiTS23 data: Heller et al., *The KiTS21 Challenge* (and KiTS23). See the KiTS23 repository for
the data license and citation.
