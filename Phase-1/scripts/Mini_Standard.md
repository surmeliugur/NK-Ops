NK-Ops Phase-1 — Scripts Mini Standard (v0.1)

Goal: fresh clone → single command → deterministic outputs.

1) CLI & args (argparse)
- Every script must support:
  --csv PATH            input CSV
  --outdir PATH         output directory (created if missing)
  --msv_version VER     e.g. 0.1.3 (required)
  --text_col NAME       default 'text' (when applicable)
  --sep SEP             optional; if omitted: auto-detect
  --config PATH         optional; if omitted: use configs/msv_{msv_version}.json if present
  --quiet               reduce logs
  --debug               verbose logs + exception trace
- Print a short [SUMMARY] JSON to stdout on success.

2) Logging format
- Single-line status logs, stable prefixes:
  [OK]    for input acceptance + detected columns/sep
  [WROTE] for every file written
  [INFO]  for non-essential notes
  [WARN]  for recoverable issues
  [ERR]   for failures (then exit code 1)

3) Output naming (deterministic)
- nk_msv_single_ayat.py:
  msv_results_{sure:03d}_{ayet:03d}.csv
  msv_results_{sure:03d}_{ayet:03d}.jsonl
  shai_summary_{sure:03d}_{ayet:03d}.json
- nk_ops_author_sweep.py:
  author_sweep_{author_slug}_msv.csv
  author_sweep_{author_slug}_summary.json
- nk_ops_text_sweep.py:
  nk_ops_sweep_{input_basename}.csv
  nk_ops_sweep_{input_basename}_summary.json

4) Data contract (minimum)
- Quran meal CSV: must contain columns:
  sure (int), ayet (int), text (str)
  optional: author, lang
- Generic text sweep CSV: must contain:
  text (str) plus optional id columns (e.g., id, chapter)

5) Determinism rules
- No randomness.
- Stable ordering: sort by (sure, ayet) or by id columns if given.
- Stable float formatting in outputs: 6 decimals for display; raw floats in JSON ok.

6) Error handling & exit codes
- Missing required columns: raise RuntimeError, print [ERR], exit 1
- Empty selection (e.g., author not found): exit 1 with hints (top 50 authors)

7) Repro metadata in every *_summary.json
- generated_at (ISO timestamp)
- msv_version
- source_file
- row_count
- sep_detected
- text_col
- tau_counts, tau_shares
- operator_totals, operator_avg_per_row (or per_verse)

8) Repo hygiene
- scripts must not assume Windows paths.
- Accept both \ and /; store source_file exactly as received.
