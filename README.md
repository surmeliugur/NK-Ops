# NK-Ops — Meaning Under Stress

**NK-Ops** is an experimental research repository that studies how *meaning-bearing operators* behave under controlled stress conditions.
Instead of embeddings or token similarity, NK-Ops measures **operator-level divergence** at the ayah (verse) level and aggregates it into **author-level behavioral signatures**.

This repository documents a reproducible phenomenon:
> **When semantic stress increases, translators do not drift randomly — they separate into stable behavioral classes.**

---

## What is measured?

For each author (Qur'an translation):

- Ayah-level operator response (`SOFT`, `SILENCE`)
- Binary divergence signal (`divergent ∈ {0,1}`)
- Stress parameter \( s ∈ {0.2, 0.5, 0.8} \)
- Aggregated **divergence rate** per stress level

These measurements are *deterministic* and *fully reproducible*.

---

## Pipeline Overview

1. **Ayah-level stress experiments**
   - Run independently for each author and stress level
   - Output: `by_author/<author>/ayet_results.tsv`

2. **Author profile construction**
   - Aggregates divergence rates across stress levels
   - Output: `author-profile.tsv`

3. **Stress-response clustering**
   - Authors clustered by response curve shape (not embeddings)
   - Output: `author-profile-clustered.tsv`
   - Visualization:
     - `author_stress_response_mean.png`
     - `author_stress_response_clusters.png`

---

## Key Findings

- **Low stress (s = 0.2):**
  - System is globally stable
  - Divergence rates are minimal

- **Mid stress (s = 0.5):**
  - Early differentiation appears
  - Author behaviors begin to separate

- **High stress (s = 0.8):**
  - Clear phase transition
  - Authors form **three distinct behavioral clusters**
  - Separation is structural, not lexical

This indicates that *meaning response under pressure* is a measurable and classifiable property.

---

## Why this matters

- Demonstrates a viable alternative to token/embedding-centric NLP
- Shows that **meaning can be treated as an operational field**
- Opens the door to:
  - Meaning-based alignment metrics
  - Stress-testing semantic systems
  - Operator-level AI interpretability

NK-Ops is a subsystem of the broader **NeuroCosmology (NK)** research program.

---

## Reproducibility

All results in this repository can be reproduced using the provided scripts and datasets.
No stochastic components are used in the analysis pipeline.

---

## Status

This repository documents **Phase-2: Author Stress Response Analysis**.
Further phases will extend operator taxonomy and cross-text generalization.
