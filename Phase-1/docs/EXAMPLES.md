# Examples

This document presents concrete examples of NK-Ops Phase-1 applied to different text types.

All examples use:
- the same operator set
- the same thresholds
- the same MSV version

Only the input text changes.

---

## 1. Scriptural Text (Qur’an – Multi-Meal)

### Example: Surah 2, Verse 6 (Multiple Translations)

**Observation**
- High variation in surface wording
- Strong consistency in operator structure

**Result**
- Dominant τ-class: AC
- High x_cos across translators
- Meaning State Vectors remain tightly clustered

**Interpretation**
The verse exhibits stable structural meaning despite linguistic variation.

This is a case of **Meaning Invariance under Translation**.

---

### Example: Surah 4, Verse 75

**Observation**
- Clear invocation and directionality
- Imperative and target-oriented operators dominate

**Result**
- Dominant τ-class: C
- High v_cos consistency
- Low NOISE incidence across meals

**Interpretation**
This verse expresses explicit action orientation.
Operator dominance is unambiguous.

---

## 2. Single-Author Full Corpus (Yaşar Nuri Öztürk)

### Scope
- Entire Qur’an translation by a single author
- 6,236 segments

**Aggregate Results**
- LOW_OPS is the largest class
- A and AC follow
- C remains rare but stable

**Key Insight**
LOW_OPS is not noise.
It represents structurally calm, descriptive, or connective segments.

This validates LOW_OPS as a necessary class, not a residual bin.

---

## 3. Literary Narrative (Atsız – *Bozkurtların Ölümü*)

### Observation
- High narrative density
- Temporal and accusative operators dominate
- Minimal invocation or directive force

**Result**
- τ distribution:
  - A ≈ 50%
  - NOISE ≈ 50%
- Almost no C or AC dominance

**Interpretation**
Narrative prose carries structure, but not directive or invocative force.

NK-Ops correctly distinguishes narration from instruction.

---

## 4. Political Fiction (George Orwell – *1984*)

### Observation
- Strong negation and abstraction
- Heavy past tense usage
- Minimal explicit direction or invocation

**Result**
- Dominant τ-class: A (~98%)
- Very low NOISE
- LOW_OPS nearly absent

**Interpretation**
The text is structurally assertive and descriptive.
It does not instruct directly; it frames reality.

NK-Ops captures this without semantic interpretation.

---

## 5. Cross-Domain Comparison

| Text Type        | Dominant τ | Structural Character |
|------------------|-----------|----------------------|
| Qur’an (multi)   | AC / C    | Directive + Meaning  |
| Qur’an (single)  | LOW_OPS   | Calm structural flow |
| Narrative novel  | A / NOISE | Temporal narration   |
| Political fiction| A         | Assertive framing    |

**Key Result**
The same operator system produces coherent differentiation
across radically different text genres.

---

## 6. What These Examples Show

- NK-Ops does not rely on vocabulary
- Style changes do not confuse the system
- Structure persists across translation
- Genre differences emerge naturally

No model was trained.
No labels were learned.

---

## 7. What These Examples Do NOT Claim

- They do not claim truth
- They do not judge correctness
- They do not infer author intent

They demonstrate **structural measurement**, nothing more.

---

## Closing Note

If meaning has structure,
structure should be measurable.

These examples show that it is.
