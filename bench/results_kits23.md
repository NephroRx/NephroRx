# TKV benchmark — AFTER (binarized + padded mask, full-resolution volume mesh)

Command: `python bench/tkv_benchmark.py <kits23-checkout>/dataset --repeats 3`

Environment: AMD64 Family 26 Model 68 Stepping 0, AuthenticAMD | Windows 11 | Python 3.14.5 | numpy 2.5.5 | scikit-image 0.26.0 | CPU only, single process, best of 3

| metric | value |
|---|---|
| masks | 50 |
| failed_or_empty | 0 |
| mean_abs_err_pct | 0.027 |
| median_abs_err_pct | 0.018 |
| max_abs_err_pct | 0.092 |
| mean_signed_err_pct | -0.019 |
| median_seconds | 0.578 |
| p95_seconds | 3.648 |
| median_mesh_vertices | 14028 |

Per-mask results: `results_kits23.csv`
