# NK Phase-3 — Causal Decision Law (ABL → B → C)

This repository section documents **Phase-3** of the **NeuroCosmology (NK)** project.
Phase-3 establishes a *measured, testable law* that connects **causality** to **decision**,
explicitly separating **reason (ABL)** from **purpose (DAT)**.

> **Core Result**
> Decision does **not** emerge from teleological intent.
> Decision emerges only when **causal traces** accumulate beyond a threshold.

---

## What Phase-3 Solves

Modern AI systems often justify actions using *goals* rather than *reasons*.
Phase-3 addresses this failure mode by introducing a **causal decision gate**:

- **ABL (Cause)** → produces measurable causal traces  
- **DAT (Purpose)** → produces directional bias but **no decision**  
- **COND (Condition)** → constrains context, never generalizes  
- **C (Decision)** → emerges only after thresholded causal accumulation  

---

## Phase-3 Structure

### Phase-3A — Causality Surface
- Formal definition of `CASE.ABL`
- Identification of *false causality*:
  - rhetorical
  - conditional
  - teleological

### Phase-3B — Cause vs Purpose
- Explicit separation of `CASE.ABL` and `CASE.DAT`
- Measurement of causal vs teleological dominance
- Zero false-positive causal attribution

### Phase-3C — Decision Threshold Law
- Dynamic accumulation of causal traces
- Hysteresis-based decision stability
- Teleology and condition veto mechanisms
- **Tested with real corpus data**

---

## Key Result (Verified)

```
ABL_dominant           → 138 decisions
teleological_surface  →   0 decisions
conditional_only      →   0 decisions
unknown               →   0 decisions
```

There are **no false positives**.
Only causal dominance produces decisions.

---

## Files in This Phase

```
Phase-3/
├── README.md
├── results/
│   ├── phase3c_decision.csv
│   └── phase3c_trace_sample.csv
└── scripts/
    ├── nk_phase3c_decision_gate_public.py
    └── nk_phase3c_make_public_samples.py
```

---

## Reproduce (Public)

This Phase-3 public release shares:
- the **measurement scripts** (decision gate + sampler)
- **public-sized result artifacts** (decision table + trace sample)

### 1) Generate Phase-3C outputs (local / private corpus)

```bat
py scripts\nk_phase3c_decision_gate_public.py ^
  --in-csv  "C:\NK\NK-CORPUS\scores\phase3\4B\phase3_4b_abl_vs_dat_v2.csv" ^
  --out-csv "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_decision.csv" ^
  --trace-csv "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_trace.csv" ^
  --trace-filter "8:53,7:96,2:10" ^
  --steps 12
```

### 2) Create GitHub-friendly public artifacts

```bat
py scripts\nk_phase3c_make_public_samples.py ^
  --trace-in  "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_trace.csv" ^
  --trace-out "Phase-3\results\phase3c_trace_sample.csv" ^
  --pairs "8:53,7:96,2:10" ^
  --max-per-meal 6
```

```bat
py scripts\nk_phase3c_make_public_samples.py ^
  --decision-in  "C:\NK\NK-CORPUS\scores\phase3\4C\phase3c_decision.csv" ^
  --decision-out "Phase-3\results\phase3c_decision.csv" ^
  --decision-public
```

### Notes
- This release provides **results and measurement logic**, not the full NK-Ops extraction pipeline.
- `phase3c_trace_sample.csv` is intentionally small; it is a *proof slice*.
- With an equivalent operator-scoring setup, the same decision distribution can be reproduced.

---

## Scientific Status

- ✔ Measured  
- ✔ Tested  
- ✔ Zero false-positive decisions  
- ✔ Reproducible with provided public artifacts  

Phase-3 is **closed**.
Further phases will extend the system, not revise this law.
