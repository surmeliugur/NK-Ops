# Methodology

This document describes the methodological foundations of NK-Ops Phase-1.

The goal is not persuasion, but transparency and reproducibility.

---

## 1. Core Principle

NK-Ops is based on a single methodological commitment:

> Meaning is not inferred.  
> Meaning is measured through explicit structural operators.

No learning, fitting, or optimization is performed.

---

## 2. Unit of Analysis

The fundamental unit of analysis is a **text segment**.

Examples:
- a single verse
- a paragraph
- a narrative fragment

Each segment is treated independently.

There is no cross-segment memory or contextual carryover.

---

## 3. Operator-Based Representation

Each segment is scanned for a predefined set of **semantic operators**.

Operators are explicit, rule-based, and inspectable.

Examples:
- negation
- imperative
- direction (dative / accusative)
- ontological anchoring
- temporal markers
- abstraction
- evidentiality

Operators are not inferred statistically.
They are detected deterministically.

---

## 4. Signal Extraction

For each segment:

1. Operators are detected
2. Operator counts and weights are accumulated
3. Weak-only or ambiguous signals are flagged
4. Noise conditions are evaluated

No operator implies intent.
Operators only indicate structural force.

---

## 5. Vector Construction (MSV)

Each segment produces a **Meaning State Vector (MSV)**.

The MSV is a fixed-length vector composed of:
- operator intensities
- directional forces
- barrier and invocation signals
- structural balance indicators

MSV vectors are comparable across:
- authors
- translations
- languages (with adapters)

---

## 6. Similarity Metrics

Two similarity measures are used:

- **x_cos**: structural similarity between segments
- **v_cos**: operator-force similarity

Cosine similarity is used because:
- magnitude is meaningful
- directionality is preserved
- results are scale-independent

No clustering or dimensionality reduction is applied in Phase-1.

---

## 7. τ (Tau) Classification

Each segment is assigned a τ-class based on dominant structure.

Primary classes:
- A
- C
- AC
- LOW_OPS
- NOISE

Classification is rule-based and threshold-driven.
There is no probabilistic assignment.

---

## 8. NOISE and LOW_OPS Handling

Segments are classified as NOISE or LOW_OPS when:
- operator signal is insufficient
- structure is ambiguous
- signal strength is below threshold

These are valid outcomes, not failures.

They preserve methodological honesty.

---

## 9. Multi-Author and Multi-Text Sweeps

NK-Ops supports:
- single-author full-corpus sweeps
- multi-author comparative sweeps
- non-scriptural text sweeps

Each sweep uses the same operator rules and thresholds.

Comparability is guaranteed by design.

---

## 10. Language Adaptation

Language-specific behavior is handled via:
- explicit operator mappings
- transparent morphological rules

No language-specific tuning is hidden.

Adapters can be replaced without affecting the core system.

---

## 11. Error Model

NK-Ops explicitly allows for error.

Primary error sources:
- segmentation artifacts
- incomplete operator definitions
- language-specific ambiguity
- threshold miscalibration

Errors are observable and debuggable.

---

## 12. Reproducibility

Given:
- the same input text
- the same operator definitions
- the same MSV version

Results are deterministic.

No randomness is involved.

---

## 13. Scope Limitation

NK-Ops does not:
- interpret meaning
- judge correctness
- infer intention
- evaluate truth or value

It measures structural properties only.

---

## 14. Phase-1 Constraint

Phase-1 is intentionally limited.

There is no:
- learning
- adaptation
- feedback loop
- meta-optimization

Future phases are optional and non-assumed.

---

## Closing Note

This methodology favors constraint over coverage.

Its strength lies in what it refuses to do.
