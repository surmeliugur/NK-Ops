#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Phase-3C (Public Release) — ABL → C Decision Gate (Measurement Script)

Purpose
-------
This script reproduces Phase-3C "decision gate" measurements from a Phase-3B/4B v2 CSV.
It computes:
- dynamic causal-trace accumulation (B_abl)
- dynamic teleology accumulation (T_teleo)
- decision potential Pi
- hysteresis-based decision state D_c

Inputs (expected columns; auto-mapped if names vary)
----------------------------------------------------
segment_id, meal_slug, sure, ayet
ABL_score, DAT_score
sart_flag
class  (ABL_dominant / mixed / teleological_surface / conditional_only / unknown)

Outputs
-------
--out-csv   : per-segment final metrics + decision
--trace-csv : optional per-step trace for selected ayet(s) or segment_id(s)

Example (Windows CMD / PowerShell)
---------------------------------
py nk_phase3c_decision_gate_public.py ^
  --in-csv  "C:\NK\NK-CORPUS\scores\phase3\4B\phase3_4b_abl_vs_dat_v2.csv" ^
  --out-csv "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_decision.csv" ^
  --steps 12

Trace sample for 8:53, 7:96, 2:10:
py nk_phase3c_decision_gate_public.py ^
  --in-csv "..." ^
  --out-csv "..." ^
  --trace-csv "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_trace.csv" ^
  --trace-filter "8:53,7:96,2:10" ^
  --steps 12
"""

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def read_csv_any_delim(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    first = text.splitlines()[0] if text else ""
    delims = [",", ";", "\t"]
    best = ","
    best_cols = -1
    for d in delims:
        cols = first.count(d)
        if cols > best_cols:
            best_cols = cols
            best = d
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter=best)
        rows: List[Dict[str, str]] = []
        for r in reader:
            rows.append({k: (v if v is not None else "") for k, v in r.items()})
        return list(reader.fieldnames or []), rows


def pick_col(fieldnames: List[str], candidates: List[str]) -> Optional[str]:
    lower = {c.lower(): c for c in fieldnames}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    return None


def pick_col_regex(fieldnames: List[str], pattern: str) -> Optional[str]:
    rx = re.compile(pattern, re.IGNORECASE)
    for c in fieldnames:
        if rx.search(c):
            return c
    return None


def to_float(s: str, default: float = 0.0) -> float:
    s = (s or "").strip()
    if not s:
        return default
    s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return default


def norm_flag(s: str) -> int:
    s = (s or "").strip().lower()
    return 1 if s in ("1", "1.0", "true", "t", "yes", "y") else 0


@dataclass
class Params:
    wB: float = 1.0
    wT: float = 1.0
    wCond: float = 1.5
    wG: float = 1.0
    theta_on: float = 1.2
    theta_off: float = 0.6
    k_gen: float = 0.35
    k_dec: float = 0.15
    kT_gen: float = 0.35
    kT_dec: float = 0.15
    G_const: float = 0.0


def sigma_abl(cls: str) -> float:
    cls = (cls or "").strip().lower()
    return 1.0 if cls in ("abl_dominant", "mixed") else 0.0


def sigma_teleo(cls: str) -> float:
    cls = (cls or "").strip().lower()
    return 1.0 if cls in ("teleological_surface", "dat_dominant") else 0.0


def pi_value(B: float, T: float, cond: int, G: float, p: Params) -> float:
    return (p.wB * B) - (p.wT * T) - (p.wCond * float(cond)) - (p.wG * G)


def hysteresis(prev: int, Pi: float, p: Params) -> int:
    if Pi >= p.theta_on:
        return 1
    if Pi <= p.theta_off:
        return 0
    return prev


def parse_trace_filter(spec: str) -> Tuple[set, set]:
    pairs = set()
    segids = set()
    if not spec:
        return pairs, segids
    items = [x.strip() for x in spec.split(",") if x.strip()]
    for it in items:
        if it.lower().startswith("segment_id="):
            segids.add(it.split("=", 1)[1].strip())
        elif ":" in it:
            s, a = it.split(":", 1)
            pairs.add((s.strip(), a.strip()))
    return pairs, segids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-csv", required=True, help="Phase-3B/4B v2 CSV (with ABL_score/DAT_score/class/sart_flag)")
    ap.add_argument("--out-csv", required=True, help="Output decision CSV")
    ap.add_argument("--trace-csv", default="", help="Optional output trace CSV")
    ap.add_argument("--trace-filter", default="", help='e.g. "8:53,7:96,2:10" or "segment_id=..."')
    ap.add_argument("--steps", type=int, default=12)

    ap.add_argument("--wB", type=float, default=1.0)
    ap.add_argument("--wT", type=float, default=1.0)
    ap.add_argument("--wCond", type=float, default=1.5)
    ap.add_argument("--wG", type=float, default=1.0)
    ap.add_argument("--theta-on", type=float, default=1.2)
    ap.add_argument("--theta-off", type=float, default=0.6)

    ap.add_argument("--k-gen", type=float, default=0.35)
    ap.add_argument("--k-dec", type=float, default=0.15)
    ap.add_argument("--kT-gen", type=float, default=0.35)
    ap.add_argument("--kT-dec", type=float, default=0.15)

    ap.add_argument("--G-const", type=float, default=0.0)

    args = ap.parse_args()

    p = Params(
        wB=args.wB, wT=args.wT, wCond=args.wCond, wG=args.wG,
        theta_on=args.theta_on, theta_off=args.theta_off,
        k_gen=args.k_gen, k_dec=args.k_dec,
        kT_gen=args.kT_gen, kT_dec=args.kT_dec,
        G_const=args.G_const,
    )

    in_path = Path(args.in_csv)
    out_path = Path(args.out_csv)
    trace_path = Path(args.trace_csv) if args.trace_csv else None
    trace_pairs, trace_segids = parse_trace_filter(args.trace_filter)

    if not in_path.exists():
        raise SystemExit(f"[ERR] input not found: {in_path}")

    fields, rows = read_csv_any_delim(in_path)

    col_seg = pick_col(fields, ["segment_id", "id", "seg_id", "segment"]) or "segment_id"
    col_meal = pick_col(fields, ["meal_slug", "author", "score_author"]) or "meal_slug"
    col_sure = pick_col(fields, ["sure", "score_sure"]) or pick_col_regex(fields, r"\bsure\b") or "sure"
    col_ayet = pick_col(fields, ["ayet", "score_ayet"]) or pick_col_regex(fields, r"\bayet\b") or "ayet"

    col_A = pick_col(fields, ["ABL_score", "abl_score"]) or pick_col_regex(fields, r"\babl[_ ]?score\b") or "ABL_score"
    col_T = pick_col(fields, ["DAT_score", "dat_score"]) or pick_col_regex(fields, r"\bdat[_ ]?score\b") or "DAT_score"
    col_cond = pick_col(fields, ["sart_flag", "cond_flag"]) or pick_col_regex(fields, r"sart") or "sart_flag"
    col_cls = pick_col(fields, ["class", "cls", "label"]) or "class"

    out_rows: List[Dict[str, str]] = []
    trace_rows: List[Dict[str, str]] = []

    seen = set()
    for r in rows:
        seg = (r.get(col_seg, "") or "").strip()
        if not seg or seg in seen:
            continue
        seen.add(seg)

        sure = (r.get(col_sure, "") or "").strip()
        ayet = (r.get(col_ayet, "") or "").strip()
        meal = (r.get(col_meal, "") or "").strip()
        cls = (r.get(col_cls, "") or "").strip()

        A0 = to_float(r.get(col_A, "0"), 0.0)
        T0 = to_float(r.get(col_T, "0"), 0.0)
        cond = norm_flag(r.get(col_cond, "0"))
        G = p.G_const

        Pi0 = pi_value(B=A0, T=T0, cond=cond, G=G, p=p)
        D0 = 1 if Pi0 >= p.theta_on else 0  # static

        B = 0.0
        T = 0.0
        D = 0
        sA = sigma_abl(cls)
        sTeleo = sigma_teleo(cls)

        for t in range(args.steps):
            B = (1.0 - p.k_dec) * B + p.k_gen * (A0 * sA)

            teleo_gate = 1.0 if (sTeleo == 1.0 or cls.strip().lower() == "mixed") else 0.0
            T = (1.0 - p.kT_dec) * T + p.kT_gen * (T0 * teleo_gate)

            Pi = pi_value(B=B, T=T, cond=cond, G=G, p=p)
            D = hysteresis(D, Pi, p)

            if trace_path is not None:
                trace_this = (seg in trace_segids) or (trace_pairs and (sure, ayet) in trace_pairs)
                if trace_this:
                    trace_rows.append({
                        "t": str(t),
                        "segment_id": seg,
                        "meal_slug": meal,
                        "sure": sure,
                        "ayet": ayet,
                        "class": cls,
                        "cond": str(cond),
                        "A0_ABL_score": f"{A0:.6f}",
                        "T0_DAT_score": f"{T0:.6f}",
                        "B_abl": f"{B:.6f}",
                        "T_teleo": f"{T:.6f}",
                        "Pi": f"{Pi:.6f}",
                        "D_c": str(D),
                    })

        out_rows.append({
            "segment_id": seg,
            "meal_slug": meal,
            "sure": sure,
            "ayet": ayet,
            "class": cls,
            "cond_sart_flag": str(cond),
            "A0_ABL_score": f"{A0:.6f}",
            "T0_DAT_score": f"{T0:.6f}",
            "Pi0_static": f"{Pi0:.6f}",
            "D0_static": str(D0),
            "steps": str(args.steps),
            "B_final": f"{B:.6f}",
            "T_final": f"{T:.6f}",
            "Pi_final": f"{pi_value(B=B, T=T, cond=cond, G=G, p=p):.6f}",
            "D_final": str(D),
            "params": f"wB={p.wB},wT={p.wT},wCond={p.wCond},wG={p.wG},theta_on={p.theta_on},theta_off={p.theta_off},k_gen={p.k_gen},k_dec={p.k_dec},kT_gen={p.kT_gen},kT_dec={p.kT_dec},G={p.G_const}",
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        cols = [
            "segment_id","meal_slug","sure","ayet","class","cond_sart_flag",
            "A0_ABL_score","T0_DAT_score","Pi0_static","D0_static",
            "steps","B_final","T_final","Pi_final","D_final","params"
        ]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for rr in out_rows:
            w.writerow(rr)

    print(f"[OK] wrote {len(out_rows)} rows -> {out_path}")

    if trace_path is not None:
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        with trace_path.open("w", encoding="utf-8", newline="") as f:
            cols = ["t","segment_id","meal_slug","sure","ayet","class","cond","A0_ABL_score","T0_DAT_score","B_abl","T_teleo","Pi","D_c"]
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for rr in trace_rows:
                w.writerow(rr)
        print(f"[OK] wrote trace rows={len(trace_rows)} -> {trace_path}")


if __name__ == "__main__":
    main()
