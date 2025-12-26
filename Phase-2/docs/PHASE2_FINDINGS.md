# Phase-2 Findings — Operator Interaction Graphs

This document summarizes the core empirical findings of **NK-Ops Phase-2**.
Phase-2 investigates how linguistic operators interact as a semantic field,
beyond individual operator frequencies.

------------------------------------------------------------

## Objective

The primary objective of Phase-2 is to determine whether meaning structure
is carried by **individual operators** or by **stable interaction patterns**
between operators.

To test this, we construct operator interaction graphs and perform
systematic **ablation experiments**.

------------------------------------------------------------

## Method Summary

Input:
- Segment-level operator presence (binary)
- 44 Turkish Quran translations (authors)
- ~270k aligned segments

Steps:
1. Build operator co-occurrence matrices per segment
2. Normalize interactions using NPMI
3. Aggregate graphs globally and per author
4. Measure edge invariance across authors
5. Perform ablations by removing dominant operators

------------------------------------------------------------

## Ablation Experiments

### 1. CASE.DAT Removal
Result:
- Global interaction structure remains largely stable
- Core operator pairs persist across authors

Interpretation:
CASE.DAT acts as a high-frequency carrier, but is not load-bearing
for semantic structure.

------------------------------------------------------------

### 2. VOICE.PASS Removal
Result:
- Interaction graph remains coherent
- Invariant edges preserved
- Slight reduction in overall density

Interpretation:
VOICE.PASS contributes stylistic modulation rather than structural meaning.

------------------------------------------------------------

### 3. CASE.ABL Removal
Result:
- Severe collapse of interaction graph
- Loss of invariant edges
- Fragmentation across authors

Interpretation:
CASE.ABL is a **load-bearing operator**.
Its removal destabilizes the semantic field.

------------------------------------------------------------

## Invariant Core Edges

Edges that remain present across nearly all authors include:

- CASE.ABL ↔ PAST.DI
- CASE.ABL ↔ EVID.MIS
- CASE.ABL ↔ NEG.MA
- ABST.LIK ↔ CASE.ABL
- NEG ↔ PAST ↔ EVID triads

These edges define the **semantic backbone** of the corpus.

------------------------------------------------------------

## Key Insight

Meaning does not reside in isolated operators.
It emerges from **persistent interaction patterns**.

Operators such as CASE.ABL function as structural joints,
while others act as surface-level modifiers.

------------------------------------------------------------

## Status

Phase-2 core analysis: Completed  
Phase-2 interpretation & write-up: Ongoing

------------------------------------------------------------

## Next Steps

- Formalize results into a standalone paper
- Extend analysis to non-religious corpora
- Integrate findings into Token-to-Marble modeling
