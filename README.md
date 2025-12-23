# NK-Ops
NK-Ops Phase-1: Language-Independent Operator Physics for Text

## Overview

NK-Ops is an experimental framework for detecting, quantifying, and comparing semantic operators in natural language texts, independent of any specific language model or embedding system.

Instead of treating language as token sequences, NK-Ops models texts as the interaction of operators (negation, direction, anchoring, invocation, etc.) acting on a semantic field.

The framework is designed to be:

- Language-independent at the operator level  
- Deterministic and rule-based  
- Empirically testable across heterogeneous corpora  

This repository documents **Phase-1** of NK-Ops: operator detection, aggregation, and classification.

## Core Idea

Natural language meaning is not carried only by words, but by **operators** that shape intention, direction, certainty, and force.

NK-Ops assumes that:

- Meaning emerges from operator configurations  
- Different texts can be compared by their operator signatures  
- Operator distributions are more stable than surface vocabulary  

## Operator Set (Phase-1)

Phase-1 focuses on a minimal but expressive operator basis:

NEG, DAT/ACC, ANCHOR, INVOKE, IMP, PAST/FUT/PROG, EVID, ABST, BARRIER

Operators are detected using explicit linguistic markers, not embeddings.

## Tau Classification

A, C, AC, LOW_OPS, NOISE

## Quick Start

NK-Ops is a measurement framework, not a black-box model.

### Input

CSV with one semantic unit per row and a `text` column.

### Run

python nk_ops_text_sweep.py --csv input.csv --text_col text --outdir results --msv_version 0.1.3

## Outputs

Phase-1 produces:
- MSV vectors (per segment)
- τ (tau) classifications
- Summary statistics and diagnostics

See:
- results/extremes_table.md (tau + operator extremes across authors)
- results/extreme_meals.json (machine-readable extremes)
- results/*.csv (author index + operator averages)


## License

MIT License
