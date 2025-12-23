# scripts/

This folder contains Phase-1 analysis scripts.

## Conventions

- Input: a CSV with a `text` column (default) and optional id columns (e.g., `sure,ayet`).
- Output: CSV + JSON summary written under `results/` (recommended) or any `--outdir`.
- Always pass `--msv_version` so results remain comparable across runs.

## Typical scripts

- `nk_ops_author_sweep.py`: sweep a single author/translation across a full corpus.
- `nk_ops_text_sweep.py`: sweep any segmented text (books, essays, articles).

## Output hygiene

Generated outputs can grow fast. Keep them out of Git history:
- commit only small demo outputs under `examples/`
- keep real runs under `results/` and add that to `.gitignore`
