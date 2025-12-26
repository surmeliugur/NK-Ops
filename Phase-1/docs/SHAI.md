# SHAİ — Ayat-Aligned Semantic Invariance

**SHAİ (Semantic Harmony Across Interpretations)** is a metric that measures
whether a semantic unit remains invariant across multiple translations or interpretations.

In NK-Ops, SHAİ answers a single, precise question:

> *Do different renderings of the same source preserve the same meaning state?*

---

## Motivation

Traditional translation analysis relies on:
- lexical overlap
- stylistic similarity
- subjective commentary

These methods fail to detect:
- operator drift
- loss of intent
- semantic deformation

SHAİ replaces interpretation with **measurement**.

---

## Definition

For a fixed semantic source (e.g., a Qur’anic ayah):

1. Each translation is converted into an MSV
2. Pairwise MSV similarities are computed
3. The distribution of similarities defines invariance

Formally:


Where:
- MSVᵢ is the Marble State Vector of translation *i*
- cosine similarity is used for scale-invariant comparison

---

## Interpretation Scale

| SHAİ Value | Interpretation |
|-----------|----------------|
| **≥ 0.95** | Strong semantic invariance |
| **0.85 – 0.95** | Acceptable interpretive variance |
| **0.75 – 0.85** | Noticeable semantic drift |
| **< 0.75** | Structural meaning divergence |

SHAİ does **not** judge correctness.
It measures **consistency**.

---

## What SHAİ Detects

SHAİ is sensitive to:
- loss or gain of imperative force
- removal of directionality (DAT / ACC)
- dilution of negation
- anchoring distortion
- over-interpretation artifacts

It ignores:
- stylistic differences
- word choice preferences
- sentence length variation

---

## SHAİ vs Classical Metrics

| Metric | Measures | Limitation |
|------|---------|------------|
| BLEU | Lexical overlap | Blind to meaning |
| ROUGE | Token recall | Surface-level |
| BERTScore | Latent similarity | Opaque |
| **SHAİ** | Operator invariance | Explicit |

SHAİ operates on **meaning physics**, not language statistics.

---

## Empirical Observation

In controlled experiments:

- High SHAİ values are observed in:
  - directive ayahs with clear operator structure
  - ontologically anchored statements
- Lower SHAİ values appear in:
  - narrative passages
  - interpretively expanded translations

This behavior is **expected**, not a flaw.

---

## SHAİ Is Language-Agnostic

Because MSV construction is operator-based:

- SHAİ does not depend on language family
- Translations across different linguistic systems are comparable
- Semantic alignment survives surface transformation

This makes SHAİ suitable for:
- cross-language analysis
- historical translation comparison
- ideological drift detection

---

## Relation to Tau Classes

SHAİ should be evaluated **within the same τ-class**.

Comparing:
- A vs C
- NOISE vs AC

is invalid and will produce misleading results.

Tau consistency is a prerequisite for SHAİ validity.

---

## Limits of SHAİ (Phase-1)

SHAİ Phase-1 does not capture:
- discourse-level coherence
- inter-ayah dependencies
- long-range narrative flow

It measures **local semantic invariance only**.

---

## Summary

- SHAİ measures meaning stability, not truth
- It replaces interpretation with geometry
- It exposes semantic drift objectively
- It is reproducible and deterministic
- It grounds translation analysis in NK-Ops physics
