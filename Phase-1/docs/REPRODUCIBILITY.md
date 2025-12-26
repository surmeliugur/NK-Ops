# Reproducibility

NK-Ops Phase-1 is designed to be fully deterministic and reproducible.

This document explains how results can be independently verified,
re-run, and compared across environments.

---

## 1. Determinism by Design

NK-Ops Phase-1 has **no stochastic components**.

- No random initialization
- No training
- No learned parameters
- No sampling

Given the same:
- input text
- operator set
- thresholds
- MSV version

the output is **bitwise identical**.

---

## 2. Fixed Inputs

Reproducibility requires fixing the following inputs:

### Required
- CSV file (UTF-8)
- Text column name
- MSV version (e.g. `0.1.3`)

### Optional but Recommended
- Explicit separator (`,` or `;`)
- Explicit ID columns

Example input schema:

---

## 3. Fixed Operator Set

Phase-1 uses a **closed operator set**:

- NEG
- CASE (DAT / ACC)
- INVOKE
- ANCHOR
- IMP
- TENSE (PAST / FUT / PROG)
- EVID
- ABST
- BARRIER

No dynamic operator discovery occurs in Phase-1.

Operator definitions are documented in:
- `docs/OPERATORS.md`

---

## 4. Fixed τ-Classification Rules

τ-classes are assigned using explicit rules:

- NOISE
- LOW_OPS
- A
- AC
- C

Rules are:
- threshold-based
- order-independent
- documented

See:
- `docs/TAU_CLASSES.md`

No probabilistic scoring or soft classification is used.

---

## 5. Command-Line Reproduction

### Single Verse (Multi-Meal)

py nk_msv_single_ayat.py \
  --csv meals_all.csv \
  --sure 2 \
  --ayet 6 \
  --outdir scores/msv \
  --msv_version 0.1.3

### Single Author Sweep

py nk_ops_author_sweep.py \
  --csv meals_all.csv \
  --author_contains ynuri \
  --outdir scores/msv \
  --msv_version 0.1.3

 ### Arbitrary Text Corpus

py nk_ops_text_sweep.py \
  --csv DOC_orwell_1984.csv \
  --text_col text \
  --id_cols id,chapter \
  --outdir scores/msv \
  --msv_version 0.1.3

Running the same command twice produces identical outputs.
6. Output Stability

Each run produces:

Per-segment CSV

Aggregate JSON summary

Example files:

nk_ops_sweep_*.csv

*_summary.json

No timestamps or run-specific noise affect computed values.

7. Cross-System Reproducibility

NK-Ops Phase-1 has been tested on:

Windows

Linux

Different Python versions (≥ 3.9)

Results remain identical as long as:

text encoding is preserved

MSV version is unchanged

8. Versioning Policy

Reproducibility is guaranteed within the same MSV version.

If:

operator thresholds change

new operators are added

τ-rules are modified

the MSV version must be incremented.

See:

docs/MSV.md

9. What Is Not Guaranteed

Phase-1 does not guarantee:

semantic equivalence

interpretive agreement

philosophical conclusions

It guarantees only:

identical structure produces identical measurements.

10. Why This Matters

Reproducibility is the minimum requirement for science.

NK-Ops Phase-1 meets that requirement
without training,
without data fitting,
without hidden state.

The system can be audited line by line.

Closing Statement

If a system cannot be reproduced,
it cannot be trusted.

NK-Ops Phase-1 is reproducible by construction.
