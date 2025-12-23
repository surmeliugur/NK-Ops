"""nk_ops_<NAME>.py — NK-Ops Phase-1 script

Purpose:
    <ONE LINE>

Inputs:
    CSV with at least: <COLUMNS>

Outputs:
    <FILES>

Run:
    python scripts/nk_ops_<NAME>.py --csv <PATH> --outdir <DIR> --msv_version 0.1.3

Notes:
    - Deterministic outputs (no randomness)
    - Logs: [OK]/[WROTE]/[INFO]/[WARN]/[ERR]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def eprint(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def log(prefix: str, msg: str, quiet: bool = False) -> None:
    if not quiet:
        print(f"[{prefix}] {msg}")


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def detect_sep(sample: str) -> str:
    # Simple heuristic; you can replace with your existing detector.
    # Prefer comma, then tab, then semicolon.
    candidates = [",", "\t", ";"]
    scores = {c: sample.count(c) for c in candidates}
    return max(scores, key=scores.get) if max(scores.values()) > 0 else ","


def read_csv_rows(path: Path, sep: Optional[str], encoding: str = "utf-8") -> Tuple[List[Dict[str, str]], str]:
    raw = path.read_text(encoding=encoding, errors="replace")
    detected = sep or detect_sep(raw[:5000])
    reader = csv.DictReader(raw.splitlines(), delimiter=detected)
    rows = [r for r in reader if any((v or "").strip() for v in r.values())]
    return rows, detected


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Input CSV")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--msv_version", required=True, help="MSV version, e.g. 0.1.3")
    ap.add_argument("--config", default=None, help="Optional config JSON")
    ap.add_argument("--text_col", default="text", help="Text column name")
    ap.add_argument("--sep", default=None, help="CSV separator override")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--debug", action="store_true")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    ensure_dir(outdir)

    try:
        rows, sep_detected = read_csv_rows(csv_path, args.sep)
        if not rows:
            raise RuntimeError("input has 0 rows after parsing")

        if args.text_col not in rows[0]:
            raise RuntimeError(f"missing text_col='{args.text_col}'")

        log("OK", f"rows={len(rows)} sep={sep_detected} text_col='{args.text_col}' msv_version={args.msv_version}", args.quiet)

        # TODO: call NK-Ops/MSV core here and produce per-row outputs

        # Example: summary stub
        summary = {
            "rows": len(rows),
            "msv_version": args.msv_version,
            "source_file": str(csv_path),
            "sep_detected": sep_detected,
            "text_col": args.text_col,
            "generated_at": iso_now(),
        }

        summary_path = outdir / f"<OUTPUT_NAME>_summary.json"
        write_json(summary_path, summary)
        log("WROTE", str(summary_path), args.quiet)

        print("[SUMMARY]")
        print(json.dumps(summary, ensure_ascii=False, indent=2))

        return 0

    except Exception as ex:
        log("ERR", str(ex), quiet=False)
        if args.debug:
            raise
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
