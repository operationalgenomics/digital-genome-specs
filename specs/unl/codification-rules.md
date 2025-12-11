# UNL Codification Rules
### Structural, Semantic, and Praxeological Encoding Standards for the Universal Neutral Language

---

## 1. Purpose

The **UNL Codification Rules** define how all semantic content, contextual meaning, and multimodal expressions are encoded into **deterministic, machine-actionable structures** that the Cognitive Core can understand.

Codification ensures that every human input — regardless of language, modality, ambiguity, or operator style — is mapped into a unified, precise, interpretable representation.

These rules guarantee:
- semantic consistency,
- deterministic mapping,
- domain neutrality,
- safety compliance,
- compatibility with the Digital Genome architecture.

---

## 2. Design Principles

### 2.1 Deterministic Encoding
Given the same intent and the same context, codification must always produce the same encoded structure.

### 2.2 Minimal Information Principle
Only essential semantic components should be included:
- Entity,
- Action,
- Target-State,
- Modifiers,
- Constraints.

### 2.3 Praxeological Alignment
Every codified structure must reflect the universal action grammar:
```ts
[ Entity | Action | Target-State ]
```

### 2.4 Composability
Codified elements must be composable into:
- UNLIntent → Codon → Gene → Execution Plan.

### 2.5 Explainability
Encoded forms must be reversible into:
- natural language explanations,
- safety justification,
- operational reasoning.

---

## 3. Codification Pipeline

UNL codification is the final transformation step before intent is delivered to the Cognitive Core.

It works in three stages:

### Stage 1 — Semantic Normalization
Normalize raw expressions:
- resolve synonyms,
- convert natural language to canonical forms,
- align terms to ontology IDs.

### Stage 2 — Praxeological Structuring
Transform normalized meaning into:
- entity set,
- action verb,
- target-state,
- modifiers,
- constraints.

### Stage 3 — Codon-Level Encoding
For every atomic action:
```ts
Codon = {
  entity: EntityId,
  action: ActionId,
  targetState: StateId,
  parameters: {...},
  constraints: [...],
}
```

---

## 4. Core Encoding Rules

### 4.1 Entity Encoding
- Must reference canonical ontology entry.
- Must be unique within context.
- If multiple entities are selected → produce multiple codons.

### 4.2 Action Encoding
- Must map to canonical action ID.
- Synonyms resolved during normalization.
- Multimodal disambiguation prioritized (gesture > speech).

### 4.3 State Encoding
- Must map to canonical state ID.
- Inferred from:
  - explicit user request,
  - context model,
  - safety requirements.

### 4.4 Modifier Encoding
Modifiers must be encoded as key-value pairs:
```ts
modifier: {
  key: string,
  value: unknown,
  type: 'quantitative' | 'qualitative',
}
```

Examples:
- speed: "fast"
- precision: 0.8
- threshold: 120 psi

### 4.5 Constraint Encoding
Constraints provide operational boundaries.
```ts
constraint: {
  rule: string,
  severity: 'info' | 'warning' | 'critical',
  parameters?: Record<string, unknown>,
}
```

---

## 5. UNL Intent Encoding

After codification, a **UNLIntent** is fully deterministic:
```ts
interface UNLIntent {
  entities: EntityId[];
  action: ActionId;
  targetState?: StateId;
  modifiers?: Record<string, unknown>;
  constraints?: ConstraintSpec[];
  ambiguityLevel: number;
}
```

### 5.1 Focus Entity
If multiple entities appear but only one is gesturally indicated → gesture dominates.

### 5.2 Action Resolution
If natural language contains ambiguous action verbs → resolved via context and ontology.

### 5.3 Target-State Rules
If no state is given, derive it from:
1. Context model
2. Ontology state transitions
3. Safety constraints

---

## 6. Codon Encoding Rules

Every UNLIntent can be decomposed into one or more codons.

### 6.1 Single-Entity Intent → Single Codon
```ts
[ entity | action | target-state ]
```

### 6.2 Multi-Entity Intent → Multi-Codon Sequence
Examples:
- "Shut down pumps 3, 4, and 5" → 3 codons.

### 6.3 Nested Intent → Temporally Ordered Codons
Example:
- "Isolate and inspect" →
  1. isolate(entity)
  2. inspect(entity)

### 6.4 Safety-Insertion Codons
If safety requires pre-actions:
- auto-insert "isolate" before "inspect"
- auto-insert "confirm" before "execute critical action"

Codification must not violate safety invariants.

---

## 7. Multi-Modal Integration Rules

### 7.1 Gesture Dominance (Entity Selection)
Gesture → primary selector of entities.

### 7.2 Speech Dominance (Action Selection)
Speech → primary selector of verb/action.

### 7.3 Gaze Resolution
Used only during ambiguity.

### 7.4 Affective Signals
Affect may:
- elevate urgency,
- reduce ambiguity threshold,
- trigger additional safety confirmation.

---

## 8. Safety and Governance Rules

### 8.1 Forbidden Actions
Codification must prevent encoding:
- forbidden actions,
- forbidden entity combinations,
- forbidden sequences.

### 8.2 Mandatory Approvals
If governance mode = `review`, codification must:
- insert confirmation prompts.

### 8.3 Risk Threshold Enforcement
Codification must apply:
- emergency overrides,
- fail-safe substitutions,
- constraint expansion (e.g., require isolation).

---

## 9. Normalization Rules

### 9.1 Unit Normalization
Convert all quantitative values to canonical units.

### 9.2 Synonym Normalization
Map synonyms → canonical ontology term.

### 9.3 Structural Normalization
Rearrange:
- "check if pump is off" → (action: inspect, targetState: off)

---

## 10. Diagram Guidelines (PNG-ready)

### 10.1 Codification Pipeline Diagram
Raw Input → Normalization → Praxeological Structuring → Codon Encoding.

### 10.2 Multi-Entity Expansion Diagram
Intent → Multiple Codons.

### 10.3 Safety-Insertion Diagram
Intent → Safety Codons → Final Sequence.

---

## 11. Summary

The **UNL Codification Rules** provide the deterministic encoding framework that converts human expressions into praxeological structures ready for Cognitive Core reasoning.

They:
- ensure consistency,
- enforce safety,
- guarantee governance compliance,
- maintain semantic neutrality,
- and produce codons and intents suitable for Digital Genome integration.

Codification is the final step that transforms meaning into **actionable cognitive intelligence**.

