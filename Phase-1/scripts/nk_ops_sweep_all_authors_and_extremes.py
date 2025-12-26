
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NK-Ops — Sweep all authors and compute extremes (Phase-1 helper)

This script is a *driver* that:
1) Reads a multi-author CSV (e.g., meals_all.csv).
2) Discovers unique authors.
3) For each author, calls `nk_ops_author_sweep.py` (the per-author analyzer you already use).
4) Collects per-author summary JSONs into:
   - all_authors_index.csv
   - all_authors_tau_shares.csv
   - all_authors_operator_avg.csv
5) Optionally computes "extremes" (top/bottom K) for operator averages AND tau shares,
   producing:
   - extreme_meals.json
   - extremes_table.md

Why this exists:
- Your previous `nk_ops_pick_extremes.py` failed because the input index CSV
  didn't include tau shares. This driver makes the missing table on purpose.

Works on Windows (CMD/PowerShell) and Linux/macOS.

Author: Uğur / NK-Ops
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


# ----------------------------
# Utilities
# ----------------------------

def _read_csv_safely(path: str) -> pd.DataFrame:
    # pandas sep sniff + robust utf-8
    for enc in ("utf-8", "utf-8-sig", "cp1254", "latin1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    # last resort
    return pd.read_csv(path, encoding_errors="ignore")


def _detect_author_col(df: pd.DataFrame) -> str:
    candidates = ["author", "meal_slug", "translator", "meal", "source_author"]
    for c in candidates:
        if c in df.columns:
            return c
    # heuristic: first col that looks categorical (few uniques) and is str
    obj_cols = [c for c in df.columns if df[c].dtype == "object"]
    if not obj_cols:
        raise RuntimeError("No string columns found to infer author column. Provide --author_col.")
    # pick column with smallest unique count but >1
    best = None
    best_u = None
    for c in obj_cols:
        u = df[c].nunique(dropna=True)
        if u > 1 and (best_u is None or u < best_u):
            best = c
            best_u = u
    if best is None:
        raise RuntimeError("Could not infer author column. Provide --author_col.")
    return best


def _slug(s: str) -> str:
    # keep it filesystem-friendly but stable
    s = str(s).strip()
    s = s.replace("\\", "_").replace("/", "_").replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch in ("_", "-", "."))
    return s[:120] if len(s) > 120 else s


def _find_latest_summary(outdir: Path, author_slug: str) -> Path:
    """
    Try hard to find the per-author summary json written by nk_ops_author_sweep.py.
    We search a few patterns and pick the newest by mtime.
    """
    patterns = [
        f"*{author_slug}*_summary.json",
        f"*{author_slug}*summary.json",
        f"author_sweep_{author_slug}_summary.json",
        f"author_sweep_*{author_slug}*_summary.json",
    ]
    hits: List[Path] = []
    for pat in patterns:
        hits.extend(outdir.glob(pat))
    if not hits:
        raise RuntimeError(f"Summary JSON not found for author='{author_slug}'. Looked for: {patterns}")
    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return hits[0]


def _run_author_sweep(
    python_exe: str,
    author_sweep_script: Path,
    csv_path: Path,
    author_value: str,
    outdir: Path,
    msv_version: str,
    extra_args: List[str],
) -> Path:
    """
    Calls `nk_ops_author_sweep.py` for one author.
    Returns the path to the produced summary JSON.
    """
    author_slug = _slug(author_value)

    cmd = [
        python_exe,
        str(author_sweep_script),
        "--csv",
        str(csv_path),
        "--author",
        str(author_value),
        "--outdir",
        str(outdir),
        "--msv_version",
        str(msv_version),
    ] + extra_args

    # run
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        # include stdout+stderr for debugging but keep it compact
        msg = (
            f"[FAIL] author='{author_value}' (slug='{author_slug}')\n"
            f"CMD: {' '.join(cmd)}\n"
            f"STDOUT:\n{proc.stdout[-2000:]}\n"
            f"STDERR:\n{proc.stderr[-2000:]}\n"
        )
        raise RuntimeError(msg)

    # locate summary json
    return _find_latest_summary(outdir, author_slug)


# ----------------------------
# Extremes logic
# ----------------------------

@dataclass
class ExtremeItem:
    metric: str
    top: List[Tuple[str, float]]
    bottom: List[Tuple[str, float]]


def _top_bottom(df: pd.DataFrame, metric: str, topk: int) -> ExtremeItem:
    s = df[["author", metric]].dropna()
    s = s.sort_values(metric, ascending=False)
    top = list(zip(s["author"].head(topk).tolist(), s[metric].head(topk).astype(float).tolist()))
    bottom = list(zip(s["author"].tail(topk).tolist(), s[metric].tail(topk).astype(float).tolist()))
    return ExtremeItem(metric=metric, top=top, bottom=bottom)


def _write_extremes_md(extremes: List[ExtremeItem], out_md: Path, title: str) -> None:
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    for ex in extremes:
        lines.append(f"## {ex.metric}")
        lines.append("")
        lines.append("| Rank | Top (author) | Value | Bottom (author) | Value |")
        lines.append("|---:|---|---:|---|---:|")
        for i in range(max(len(ex.top), len(ex.bottom))):
            top_a, top_v = ex.top[i] if i < len(ex.top) else ("", float("nan"))
            bot_a, bot_v = ex.bottom[i] if i < len(ex.bottom) else ("", float("nan"))
            lines.append(f"| {i+1} | {top_a} | {top_v:.6f} | {bot_a} | {bot_v:.6f} |")
        lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")


# ----------------------------
# Main
# ----------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Run nk_ops_author_sweep.py for ALL authors and aggregate results + extremes."
    )
    ap.add_argument("--csv", required=True, help="Multi-author CSV (e.g., meals_all.csv)")
    ap.add_argument("--author_col", default="", help="Author column name. If empty, auto-detect.")
    ap.add_argument("--outdir", required=True, help="Output directory for per-author sweeps + aggregated tables")
    ap.add_argument("--msv_version", default="0.1.3", help="MSV version to pass through")
    ap.add_argument("--python", default=sys.executable, help="Python executable to use")
    ap.add_argument("--author_sweep_script", default="nk_ops_author_sweep.py", help="Path to nk_ops_author_sweep.py")
    ap.add_argument("--topk", type=int, default=5, help="Top/bottom K for extremes tables")
    ap.add_argument("--no_run", action="store_true", help="Do not run per-author sweeps; only aggregate from existing summaries")
    ap.add_argument("--extra", default="", help="Extra args forwarded to nk_ops_author_sweep.py (string)")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    author_sweep_script = Path(args.author_sweep_script)
    if not author_sweep_script.exists():
        # try relative to this file
        here = Path(__file__).resolve().parent
        alt = here / args.author_sweep_script
        if alt.exists():
            author_sweep_script = alt
        else:
            raise RuntimeError(f"author_sweep_script not found: {args.author_sweep_script}")

    df = _read_csv_safely(str(csv_path))
    author_col = args.author_col.strip() or _detect_author_col(df)

    if author_col not in df.columns:
        raise RuntimeError(f"author_col='{author_col}' not found in CSV. Available: {list(df.columns)}")

    # unique authors
    authors = sorted([a for a in df[author_col].dropna().unique().tolist() if str(a).strip() != ""])
    if not authors:
        raise RuntimeError("No authors found in author column.")

    # run sweeps
    extra_args = [x for x in args.extra.strip().split() if x]
    summary_paths: Dict[str, Path] = {}

    if not args.no_run:
        print(f"[INFO] authors={len(authors)} author_col='{author_col}' msv_version={args.msv_version}")
        for i, a in enumerate(authors, 1):
            print(f"[RUN] {i:02d}/{len(authors)} author='{a}'")
            p = _run_author_sweep(
                python_exe=args.python,
                author_sweep_script=author_sweep_script,
                csv_path=csv_path,
                author_value=str(a),
                outdir=outdir,
                msv_version=args.msv_version,
                extra_args=extra_args,
            )
            summary_paths[str(a)] = p
    else:
        print("[INFO] --no_run enabled: collecting from existing summary JSONs in outdir")
        # try to locate summary for each author
        for a in authors:
            author_slug = _slug(a)
            summary_paths[str(a)] = _find_latest_summary(outdir, author_slug)

    # aggregate
    index_rows = []
    tau_rows = []
    op_rows = []

    for a in authors:
        sp = summary_paths[str(a)]
        data = json.loads(sp.read_text(encoding="utf-8"))
        rows = int(data.get("rows") or data.get("n") or 0)

        index_rows.append({"author": _slug(a), "rows": rows})

        # tau shares
        tau_shares = data.get("tau_shares", {})
        # ensure stable columns for Phase-1
        tau_cols = ["NOISE", "LOW_OPS", "A", "C", "AC", "AB", "ABC", "BC"]
        tau_row = {"author": _slug(a), "rows": rows, "msv_version": data.get("msv_version", args.msv_version)}
        for t in tau_cols:
            tau_row[f"tau_{t}"] = float(tau_shares.get(t, 0.0))
        tau_rows.append(tau_row)

        # operator averages
        op_avg = data.get("operator_avg_per_verse") or data.get("operator_avg_per_row") or {}
        op_row = {"author": _slug(a), "rows": rows, "msv_version": data.get("msv_version", args.msv_version)}
        # canonical Phase-1 operator names (match your summary JSON keys)
        op_keys = ["neg", "dat", "acc", "invoke", "anchor", "past", "evid", "fut", "prog", "abst", "imp", "barrier"]
        for k in op_keys:
            op_row[f"avg_{k}"] = float(op_avg.get(k, 0.0))
        op_rows.append(op_row)

    index_df = pd.DataFrame(index_rows).sort_values("author")
    tau_df = pd.DataFrame(tau_rows).sort_values("author")
    op_df = pd.DataFrame(op_rows).sort_values("author")

    out_index = outdir / "all_authors_index.csv"
    out_tau = outdir / "all_authors_tau_shares.csv"
    out_ops = outdir / "all_authors_operator_avg.csv"

    index_df.to_csv(out_index, index=False)
    tau_df.to_csv(out_tau, index=False)
    op_df.to_csv(out_ops, index=False)

    print(f"[WROTE] {out_index}")
    print(f"[WROTE] {out_tau}")
    print(f"[WROTE] {out_ops}")

    # extremes
    topk = args.topk
    extremes: Dict[str, Dict[str, List[Tuple[str, float]]]] = {}

    tau_metrics = [c for c in tau_df.columns if c.startswith("tau_")]
    op_metrics = [c for c in op_df.columns if c.startswith("avg_")]

    tau_ext = [_top_bottom(tau_df, m, topk) for m in tau_metrics]
    op_ext = [_top_bottom(op_df, m, topk) for m in op_metrics]

    # write combined JSON (easy for GitHub)
    out_json = outdir / "extreme_meals.json"
    extremes_payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "msv_version": args.msv_version,
        "topk": topk,
        "tau_extremes": {ex.metric: {"top": ex.top, "bottom": ex.bottom} for ex in tau_ext},
        "operator_extremes": {ex.metric: {"top": ex.top, "bottom": ex.bottom} for ex in op_ext},
    }
    out_json.write_text(json.dumps(extremes_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[WROTE] {out_json}")

    out_md = outdir / "extremes_table.md"
    _write_extremes_md(tau_ext + op_ext, out_md, title="NK-Ops Phase-1 — Extremes (Tau + Operators)")
    print(f"[WROTE] {out_md}")

    print("[DONE] all-authors sweep aggregation + extremes complete.")


if __name__ == "__main__":
    main()
