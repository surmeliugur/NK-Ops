# NK-Ops
NK-Ops Phase-1: Language-Independent Operator Physics for Text

Overview

NK-Ops is an experimental framework for detecting, quantifying, and comparing semantic operators in natural language texts, independent of any specific language model or embedding system.

Instead of treating language as token sequences, NK-Ops models texts as the interaction of operators (negation, direction, anchoring, invocation, etc.) acting on a semantic field.
The framework is designed to be:

Language-independent at the operator level

Deterministic and rule-based

Empirically testable across heterogeneous corpora

This repository documents Phase-1 of NK-Ops: operator detection, aggregation, and classification.

Core Idea

Natural language meaning is not carried only by words, but by operators that shape intention, direction, certainty, and force.

NK-Ops assumes that:

Meaning emerges from operator configurations

Different texts can be compared by their operator signatures

Operator distributions are more stable than surface vocabulary

This allows meaningful comparison between:

Different translations of the same text

Religious, literary, and political corpora

Normative vs narrative language

Operator Set (Phase-1)

Phase-1 focuses on a minimal but expressive operator basis:

NEG — Negation

DAT / ACC — Direction and target

ANCHOR — Ontological assertion / certainty

INVOKE — Address / call / appeal

IMP — Imperative force

PAST / FUT / PROG — Temporal operators

EVID — Evidentiality

ABST — Abstraction

BARRIER — Prohibition / blocking

Operators are detected using explicit linguistic markers, not embeddings.

Tau Classification

Each text segment is assigned a τ (tau) type based on operator density and balance:

A — Meaning-dominant (low directional force)

C — Consciousness-oriented (address, invocation, agency)

AC — Mixed meaning–consciousness

LOW_OPS — Insufficient operator signal

NOISE — No reliable operator structure

This classification is empirical, reproducible, and corpus-agnostic.

Implemented Analyses

Phase-1 includes:

Single-verse multi-translation comparison

Full-author sweeps (entire works or translations)

Cross-corpus testing (religious, literary, narrative)

Operator density and variance statistics

Noise and low-signal diagnostics

Tested corpora include:

Multiple Qur’an translations (Turkish)

Literary prose (George Orwell, Nihal Atsız)

Repository Structure
NK-Ops/
├── scripts/            # Analysis scripts
├── scores/             # Generated CSV / JSON outputs
├── docs/               # Methodology notes
├── examples/           # Example runs
└── README.md

Relation to Token-to-Marble

NK-Ops is the operational layer of the broader Token-to-Marble paradigm.

While Token-to-Marble proposes a field-based alternative to token embeddings, NK-Ops provides a concrete, testable implementation of operator-based semantics.

See:
👉 https://github.com/surmeliugur/token-to-marble

Status

Current phase: Phase-1 (Operator Detection & Classification)

Stability: Experimental but reproducible

Next phase: Operator interaction dynamics (Phase-2)

Philosophy of the Project

NK-Ops intentionally avoids:

Neural embeddings

Black-box models

Probabilistic hallucination

The goal is semantic instrumentation, not language generation.

Meaning is treated as a measurable field, not an emergent illusion.

License

MIT License

Citation

If you reference this work, please cite the repository directly.
A formal paper is planned for a later phase.
