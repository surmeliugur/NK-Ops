# Marble State Vector (MSV)

The **Marble State Vector (MSV)** is the quantitative representation of meaning in NK-Ops.

It encodes how semantic operators act on a text segment as a measurable state in meaning-space.

MSV is **not an embedding**.
It is a structured vector derived from detected operators and their interactions.

---

## Why MSV Exists

Most NLP systems represent meaning as:
- token embeddings
- latent probability distributions
- opaque neural states

NK-Ops rejects this approach.

Instead, MSV represents meaning as:
- explicit
- interpretable
- reproducible
- operator-driven

MSV answers:
> *What semantic forces are active here, and in what proportions?*

---

## MSV Structure

An MSV consists of three primary components:


Where:

- **A** — Meaning / Semantic Structure
- **B** — Informational Load (reserved for Phase-2)
- **C** — Intentional / Conscious Force

Phase-1 operates primarily on **A** and **C** components.

---

## A-Component (Semantic Mass)

The **A-component** measures:
- conceptual content
- abstraction level
- semantic density

It is influenced by:
- anchoring
- abstraction
- temporal operators
- negation

High A-values indicate:
- descriptive content
- narrative structure
- conceptual exposition

---

## C-Component (Intentional Force)

The **C-component** measures:
- directionality
- address
- command
- invocation

It is influenced by:
- imperative operators
- invocation
- dative direction
- barriers

High C-values indicate:
- exhortation
- command
- appeal
- directive speech

---

## Vector Construction

For a given text segment:

1. Operators are detected
2. Each operator contributes a weighted force
3. Forces are aggregated per component
4. The result is normalized into MSV space

Simplified:


Normalization ensures:
- comparability across texts
- scale invariance
- translation robustness

---

## MSV Normalization

Each MSV is normalized to unit scale:


This allows:
- cosine similarity comparison
- cross-translation alignment
- regime classification

---

## MSV Similarity

To compare two MSVs:


Interpretation:
- **~1.0** → semantic invariance
- **~0.8–0.9** → mild interpretive variance
- **<0.7** → structural semantic divergence

This metric underlies:
- SHAİ (Ayat-Aligned Semantic Invariance)
- Translation drift analysis
- Operator stability testing

---

## MSV Regimes (Tau Classes)

Each MSV is classified into a **τ (tau) regime** based on operator balance:

- **A** → descriptive / narrative
- **C** → directive / intentional
- **AC** → mixed force
- **LOW_OPS** → weak operator presence
- **NOISE** → no reliable semantic signal

Tau classification is **not subjective**.
It is a deterministic function of MSV structure.

---

## Why MSV Is Not an Embedding

| Embeddings | MSV |
|-----------|-----|
| Latent | Explicit |
| Opaque | Interpretable |
| Probabilistic | Deterministic |
| Token-based | Operator-based |
| Model-dependent | Model-independent |

MSV can be computed without:
- training
- fine-tuning
- neural inference

---

## Phase-1 Scope

Phase-1 MSV is intentionally constrained.

It does **not** yet include:
- deep contextual memory
- cross-sentence dynamics
- B-component (information flow)

These are reserved for later phases.

---

## Summary

- MSV is a semantic state, not a guess
- It is built from operators, not tokens
- It enables measurement, not imitation
- It is invariant across language adapters
- It grounds NK-Ops in reproducible physics
