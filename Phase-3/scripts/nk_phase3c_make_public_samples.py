#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Phase-3C — Public Release Helpers

Creates small, GitHub-friendly outputs from Phase-3C results.

1) Trace sampler:
   - Input : full phase3c_trace.csv
   - Output: phase3c_trace_sample.csv
   - Filters by sure:ayet list (default: 8:53, 7:96, 2:10)
   - Optionally caps rows per (sure,ayet,meal_slug) group to keep size small.

2) (Optional) Decision minimizer:
   - Input : phase3c_decision.csv
   - Output: phase3c_decision_public.csv
   - Keeps only the public columns (no params if you want).

Examples
--------
py nk_phase3c_make_public_samples.py ^
  --trace-in  "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_trace.csv" ^
  --trace-out "C:\GitHub\NK-Ops\Phase-3\results\phase3c_trace_sample.csv" ^
  --pairs "8:53,7:96,2:10" ^
  --max-per-meal 6

py nk_phase3c_make_public_samples.py ^
  --decision-in  "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_decision.csv" ^
  --decision-out "C:\GitHub\NK-Ops\Phase-3\results\phase3c_decision.csv" ^
  --decision-public
"""

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple


def parse_pairs(spec: str) -> List[Tuple[str, str]]:
    items = [x.strip() for x in (spec or "").split(",") if x.strip()]
    pairs = []
    for it in items:
        if ":" not in it:
            continue
        s, a = it.split(":", 1)
        pairs.append((s.strip(), a.strip()))
    return pairs


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return list(r.fieldnames or []), rows


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for rr in rows:
            w.writerow(rr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace-in", default="", help="Full phase3c_trace.csv")
    ap.add_argument("--trace-out", default="", help="Output phase3c_trace_sample.csv")
    ap.add_argument("--pairs", default="8:53,7:96,2:10", help="sure:ayet list, comma-separated")
    ap.add_argument("--max-per-meal", type=int, default=6, help="Max t-rows per (sure,ayet,meal_slug)")

    ap.add_argument("--decision-in", default="", help="phase3c_decision.csv")
    ap.add_argument("--decision-out", default="", help="Output decision CSV (public or full)")
    ap.add_argument("--decision-public", action="store_true", help="Keep only public columns")

    args = ap.parse_args()

    # Trace sampling
    if args.trace_in and args.trace_out:
        in_path = Path(args.trace_in)
        out_path = Path(args.trace_out)
        if not in_path.exists():
            raise SystemExit(f"[ERR] trace-in not found: {in_path}")

        fields, rows = read_csv(in_path)
        pairs = set(parse_pairs(args.pairs))

        # Group cap
        counts = {}
        out_rows = []
        for rr in rows:
            sure = (rr.get("sure", "") or "").strip()
            ayet = (rr.get("ayet", "") or "").strip()
            if (sure, ayet) not in pairs:
                continue

            meal = (rr.get("meal_slug", "") or "").strip()
            key = (sure, ayet, meal)
            counts[key] = counts.get(key, 0) + 1
            if counts[key] > args.max_per_meal:
                continue

            out_rows.append(rr)

        # Keep only a stable subset of columns (public-friendly)
        public_cols = [
            "t","segment_id","meal_slug","sure","ayet","class","cond",
            "A0_ABL_score","T0_DAT_score","B_abl","T_teleo","Pi","D_c"
        ]
        # Some files may omit certain columns; intersect with existing
        cols = [c for c in public_cols if c in fields] or fields
        write_csv(out_path, cols, out_rows)
        print(f"[OK] wrote trace sample rows={len(out_rows)} -> {out_path}")

    # Decision minimizer / copier
    if args.decision_in and args.decision_out:
        in_path = Path(args.decision_in)
        out_path = Path(args.decision_out)
        if not in_path.exists():
            raise SystemExit(f"[ERR] decision-in not found: {in_path}")

        fields, rows = read_csv(in_path)

        if args.decision_public:
            keep = [
                "segment_id","meal_slug","sure","ayet","class","cond_sart_flag",
                "A0_ABL_score","T0_DAT_score","Pi0_static","D0_static",
                "steps","B_final","T_final","Pi_final","D_final"
            ]
            cols = [c for c in keep if c in fields]
        else:
            cols = fields

        write_csv(out_path, cols, rows)
        print(f"[OK] wrote decision rows={len(rows)} -> {out_path}")


if __name__ == "__main__":
    main()
