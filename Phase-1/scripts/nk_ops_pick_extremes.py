#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NK-Ops Phase-1 helper: pick "extreme" authors/meals from aggregated sweep tables.

Inputs (produced by your Phase-1 sweeps):
  - all_authors_index.csv
  - all_authors_operator_avg.csv

Outputs (recommended to commit):
  - results/extreme_meals.json
  - results/extremes_table.md

Typical usage:
  py scripts/nk_ops_pick_extremes.py ^
    --index_csv "results/all_authors_index.csv" ^
    --avg_csv "results/all_authors_operator_avg.csv" ^
    --out_json "results/extreme_meals.json" ^
    --out_md  "results/extremes_table.md" ^
    --topk 5

Notes:
- This script does NOT re-run MSV. It only ranks authors based on the already aggregated sweep tables.
- Ranking is done both on operator averages and on tau-shares (A/AC/C/LOW_OPS/NOISE).
"""

from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


TAU_COLS = ["share_NOISE", "share_LOW_OPS", "share_A", "share_AC", "share_C"]

# Common operator columns you reported
OP_COLS = [
    "avg_neg", "avg_dat", "avg_acc", "avg_invoke", "avg_anchor",
    "avg_past", "avg_evid", "avg_fut", "avg_prog", "avg_abst",
    "avg_imp", "avg_barrier"
]


def _read_csv(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {p}")
    return pd.read_csv(p)


def _detect_cols(df: pd.DataFrame, wanted: List[str]) -> List[str]:
    cols = []
    for c in wanted:
        if c in df.columns:
            cols.append(c)
    return cols


def _top_bottom(df: pd.DataFrame, col: str, k: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Ignore NaNs
    d = df.dropna(subset=[col]).copy()
    top = d.sort_values(col, ascending=False).head(k)
    bot = d.sort_values(col, ascending=True).head(k)
    return top, bot


def _compact_author_row(row: pd.Series, cols: List[str]) -> Dict:
    out = {"author": row.get("author", None)}
    for c in cols:
        out[c] = float(row[c]) if pd.notna(row[c]) else None
    # convenience
    if "rows" in row.index:
        out["rows"] = int(row["rows"])
    if "msv_version" in row.index:
        out["msv_version"] = row["msv_version"]
    return out


def build_extremes(index_df: pd.DataFrame, avg_df: pd.DataFrame, topk: int) -> Dict:
    # Normalize author key
    if "author" not in index_df.columns or "author" not in avg_df.columns:
        raise RuntimeError("Both CSVs must contain an 'author' column.")

    # Merge: keep shares + rows + operator avgs
    merged = index_df.merge(avg_df, on="author", how="inner", suffixes=("", "_avg"))
    merged = merged.copy()

    # Column detection (be tolerant with naming)
    tau_cols = _detect_cols(merged, TAU_COLS)
    op_cols = _detect_cols(merged, OP_COLS)

    if not tau_cols and not op_cols:
        raise RuntimeError("No expected tau/op columns found. Check your CSV headers.")

    out = {
        "generated_at": pd.Timestamp.utcnow().isoformat() + "Z",
        "topk": topk,
        "tau_extremes": {},
        "operator_extremes": {},
        "notes": [
            "Extremes are computed from aggregated sweep outputs, not from raw MSV per-verse runs.",
            "Use these authors/meals as Phase-1 'stress tests' before you split LOW_OPS further."
        ]
    }

    # Tau extremes
    for col in tau_cols:
        top, bot = _top_bottom(merged, col, topk)
        out["tau_extremes"][col] = {
            "highest": [_compact_author_row(r, ["author", col, "rows"]) for _, r in top.iterrows()],
            "lowest":  [_compact_author_row(r, ["author", col, "rows"]) for _, r in bot.iterrows()],
        }

    # Operator extremes
    for col in op_cols:
        top, bot = _top_bottom(merged, col, topk)
        out["operator_extremes"][col] = {
            "highest": [_compact_author_row(r, ["author", col, "rows"]) for _, r in top.iterrows()],
            "lowest":  [_compact_author_row(r, ["author", col, "rows"]) for _, r in bot.iterrows()],
        }

    return out


def write_md(extremes: Dict, out_md: str) -> None:
    p = Path(out_md)
    p.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append("# NK-Ops Phase-1: Extreme Meals / Authors\n")
    lines.append(f"- generated_at: `{extremes.get('generated_at')}`\n")
    lines.append(f"- topk: `{extremes.get('topk')}`\n")
    lines.append("\nThis page lists \"extreme\" authors under Phase-1 metrics to use as stress tests.\n")

    # Tau
    lines.append("\n## Tau extremes\n")
    for col, bucket in extremes.get("tau_extremes", {}).items():
        lines.append(f"\n### {col}\n")
        lines.append("\n**Highest**\n\n| rank | author | value | rows |\n|---:|---|---:|---:|\n")
        for i, r in enumerate(bucket.get("highest", []), 1):
            lines.append(f"| {i} | {r.get('author')} | {r.get(col):.6f} | {r.get('rows','')} |\n")
        lines.append("\n**Lowest**\n\n| rank | author | value | rows |\n|---:|---|---:|---:|\n")
        for i, r in enumerate(bucket.get("lowest", []), 1):
            lines.append(f"| {i} | {r.get('author')} | {r.get(col):.6f} | {r.get('rows','')} |\n")

    # Operators
    lines.append("\n## Operator extremes\n")
    for col, bucket in extremes.get("operator_extremes", {}).items():
        lines.append(f"\n### {col}\n")
        lines.append("\n**Highest**\n\n| rank | author | value | rows |\n|---:|---|---:|---:|\n")
        for i, r in enumerate(bucket.get("highest", []), 1):
            lines.append(f"| {i} | {r.get('author')} | {r.get(col):.6f} | {r.get('rows','')} |\n")
        lines.append("\n**Lowest**\n\n| rank | author | value | rows |\n|---:|---|---:|---:|\n")
        for i, r in enumerate(bucket.get("lowest", []), 1):
            lines.append(f"| {i} | {r.get('author')} | {r.get(col):.6f} | {r.get('rows','')} |\n")

    p.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index_csv", required=True, help="all_authors_index.csv")
    ap.add_argument("--avg_csv", required=True, help="all_authors_operator_avg.csv")
    ap.add_argument("--out_json", required=True, help="Output JSON path (recommended: results/extreme_meals.json)")
    ap.add_argument("--out_md", required=True, help="Output markdown path (recommended: results/extremes_table.md)")
    ap.add_argument("--topk", type=int, default=5, help="How many highest/lowest to keep per metric")
    args = ap.parse_args()

    index_df = _read_csv(args.index_csv)
    avg_df = _read_csv(args.avg_csv)

    extremes = build_extremes(index_df, avg_df, topk=args.topk)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(extremes, ensure_ascii=False, indent=2), encoding="utf-8")

    write_md(extremes, args.out_md)

    print("[OK] wrote:")
    print(f" - {out_json}")
    print(f" - {args.out_md}")


if __name__ == "__main__":
    main()
