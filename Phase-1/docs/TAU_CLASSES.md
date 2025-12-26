# Tau Classes — Semantic Activity Regimes

In NK-Ops, every textual segment is assigned to a **tau-class**.
Tau-classes do not represent meaning itself, but the **mode of semantic activity** detected in the segment.

They answer the question:

> *What kind of semantic work is this text performing?*

Phase-1 defines five tau-classes:
A, C, AC, LOW_OPS, and NOISE.

This document formally locks their definitions, with special emphasis on the **NOISE vs. LOW_OPS distinction**.

---

## A — Assertive / Descriptive Regime

**Definition:**  
Segments dominated by anchoring and descriptive operators, without strong direction, invocation, or barriers.

**Characteristics:**
- High anchor presence
- Temporal or evidential operators may exist
- No explicit semantic push toward an external target

**Interpretation:**  
The text *states*, *describes*, or *reports*.

Typical examples:
- Narrative prose
- Historical description
- Explanatory statements

---

## C — Directive / Invocative Regime

**Definition:**  
Segments where semantic force is directed toward an addressee or target.

**Characteristics:**
- Presence of invocation, direction (DAT/ACC), or barrier operators
- Meaning is *aimed*, not merely stated

**Interpretation:**  
The text *calls*, *requests*, *commands*, or *addresses*.

---

## AC — Coupled Regime

**Definition:**  
Segments that simultaneously stabilize meaning (A) and direct it (C).

**Characteristics:**
- Strong anchoring combined with direction or invocation
- High semantic coherence across translations

**Interpretation:**  
The text *states* while *acting*.

This is the most semantically dense regime in Phase-1.

---

## LOW_OPS — Weakly Operative Regime

**Definition:**  
Segments that contain **detectable operators**, but **below the activation threshold** required for a stable A or C classification.

**Key Properties:**
- Operators are present but sparse, weak, or non-coupled
- Semantic activity exists, but is **incomplete or underpowered**
- Not random, not meaningless

**Critical Distinction:**  
LOW_OPS is **not noise**.

It represents **latent or minimal semantic operation**.

Typical causes:
- Short verses or sentences
- Elliptical constructions
- Transitions between semantic regimes
- Implicit anchoring without direction

LOW_OPS segments are **eligible for reclassification** in later phases as operator sensitivity increases.

---

## NOISE — Non-Operative Regime

**Definition:**  
Segments where **no meaningful semantic operators** are detected.

**Key Properties:**
- Absence of anchoring, direction, invocation, or barrier operators
- Operator detections (if any) are incidental or below noise floor
- No coherent semantic force vector can be constructed

**Typical Causes:**
- Pure narrative filler
- Descriptive scenery without semantic intent
- Structural or stylistic fragments
- Token-level matches without functional meaning

**Critical Rule:**  
NOISE is **not low meaning** — it is **no detectable semantic operation**.

---

## NOISE vs. LOW_OPS — Formal Lock

This distinction is foundational.

| Property | LOW_OPS | NOISE |
|--------|--------|-------|
| Operators detected | Yes | No |
| Semantic intent | Weak / incomplete | None detectable |
| Eligible for future reclassification | Yes | No |
| Considered semantic activity | Minimal | Absent |

**Formal Rule (Phase-1):**

> If at least one core operator is detected with functional validity,  
> the segment **cannot** be classified as NOISE.

Conversely:

> Absence of functional operators implies NOISE, regardless of perceived meaning by a human reader.

---

## Phase-1 Scope Limitation

Phase-1 intentionally accepts **false LOW_OPS positives** over false NOISE negatives.

This bias ensures:
- Preservation of borderline semantic activity
- Avoidance of premature dismissal of weakly operative segments

Later phases may subdivide LOW_OPS,  
but **NOISE is terminal**.

---

## Summary

- **NOISE** = no semantic operation detected
- **LOW_OPS** = weak but real semantic operation
- The distinction is **algorithmic, not interpretive**
- This separation is **non-negotiable in Phase-1**
