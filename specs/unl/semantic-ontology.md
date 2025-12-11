# UNL Semantic Ontology
### Semantic Foundations, Entity Structures, Action Grammars and State Taxonomies for the Universal Neutral Language

---

## 1. Purpose

The **UNL Semantic Ontology** defines the universal conceptual structures that allow the UNL to:

- interpret human intent consistently,
- map natural expressions to praxeological codons and genes,
- maintain semantic coherence across contexts, domains and languages,
- ensure all Cognitive Core inputs obey a unified grammar,
- support explainability by linking cognitive decisions back to neutral concepts.

This ontology is the **semantic backbone** of the UNL. Without it, intent mapping would produce inconsistent, ambiguous or invalid praxeological structures.

---

## 2. Design Principles

### 2.1 Neutral, Domain-Agnostic Semantics
All UNL semantic classes must be:
- independent of natural language,
- independent of culture,
- independent of technical domain.

### 2.2 Minimal Conceptual Kernel
The ontology uses a compact universal kernel:
- **Entity** — what acts or is acted upon
- **Action** — what operation is intended
- **State** — what condition is desired or described
- **Modifier** — quantitative or qualitative refinement
- **Constraint** — rules, limits, obligations

### 2.3 Operational Grounding
Every concept ultimately must be mappable to a **codon**:
```
[ Entity | Action | Target-State ]
```

### 2.4 Deterministic Composition
Semantic nodes combine deterministically into praxeological structures used by the Cognitive Core.

### 2.5 Explainability
Each semantic element must:
- have a clear human-readable gloss,
- support reversible translation back into explanations.

---

## 3. Core Semantic Model

The UNL Ontology defines **five fundamental semantic classes**.

### 3.1 Entity Class
Represents objects, agents, systems, subsystems, locations, or resources.

Examples:
- machines, humans, sensors
- subsystems, assemblies
- virtual or informational entities

```ts
interface EntitySemantic {
  id: EntityId;
  label: string;
  type: 'physical' | 'logical' | 'agent' | 'resource' | 'composite';
  attributes?: Record<string, unknown>;
  ontologyRefs?: string[];
}
```

---

### 3.2 Action Class
Represents transformations, operations, or influences performed by or on entities.

Actions are neutral verbs such as:
- start
- stop
- isolate
- inspect
- activate
- move
- configure
- measure

```ts
interface ActionSemantic {
  id: ActionId;
  label: string;
  category: 'operational' | 'informational' | 'safety' | 'diagnostic';
  parameters?: ParameterSpec[];
  allowedStates?: StateId[];
}
```

---

### 3.3 State Class
Represents stable or transitional conditions of an entity.

Common categories:
- operational states
- safety states
- transitional states
- readiness states
- diagnostic states

```ts
interface StateSemantic {
  id: StateId;
  label: string;
  category: 'operational' | 'safety' | 'intermediate' | 'diagnostic';
  constraints?: ConstraintSpec[];
}
```

---

### 3.4 Modifier Class
Modifiers refine the meaning of an action or state.

Examples:
- speed: fast, slow
- intensity: high, medium, low
- precision levels
- quantitative thresholds

```ts
interface ModifierSemantic {
  key: string;
  value: unknown;
  type: 'quantitative' | 'qualitative';
}
```

---

### 3.5 Constraint Class
Constraints define boundary conditions of intents.

Examples:
- safety requirements
- governance restrictions
- time limits
- environmental conditions

```ts
interface ConstraintSpec {
  rule: string;
  severity: 'info' | 'warning' | 'critical';
  parameters?: Record<string, unknown>;
}
```

---

## 4. Semantic Graph Structure

The ontology is represented as a **semantic graph**.

### 4.1 Nodes
- Entities
- Actions
- States
- Modifiers
- Constraints

### 4.2 Edges
- Entity → Action (what can act on what)
- Action → State (what states an action can lead to)
- Entity → State (which states belong to the entity)
- Action → Constraint (limits on an action)
- State → Constraint (conditions required for state)

### 4.3 Graph Properties
- acyclic for baseline operational logic
- supports composite nodes
- supports inheritance and categorization

---

## 5. Semantic Normalization Rules

### 5.1 Entity Normalization
Rules:
- prefer canonical names
- avoid synonyms
- enforce unique identifiers

### 5.2 Action Normalization
Rules:
- reduce natural language to universal verbs
- apply category classification

### 5.3 State Normalization
Rules:
- map domain-specific states to universal categories
- enforce one state = one unambiguous condition

### 5.4 Modifier Normalization
Rules:
- convert qualitative inputs into known scales
- standardize quantitative units

### 5.5 Constraint Normalization
Rules:
- rewrite natural instructions into logical expressions
- ensure explicit severity levels

---

## 6. Semantic Compatibility Rules

A mapped intent is **semantically valid** only if:

### 6.1 Entity–Action Compatibility
Action must be defined as executable on the entity.

### 6.2 Action–State Compatibility
Action must be capable of producing the target state.

### 6.3 Constraint Satisfaction
Action or state must not violate:
- governance rules
- safety rules
- operational constraints

### 6.4 Contextual Boundaries
Context may invalidate:
- actions
- states
- modifiers

This ensures the Cognitive Core receives only *valid* praxeological intents.

---

## 7. Ontology Extension Mechanisms

UNL supports controlled extension of the ontology.

### 7.1 New Entities
Allowed when:
- description is provided
- class/type declared
- constraints defined

### 7.2 New Actions
Allowed when:
- action semantics mapped
- domain implications known

### 7.3 New States
Allowed when:
- state category defined
- constraints declared

### 7.4 Governance Compliance
All new ontology entries require governance approval.

---

## 8. Integration with Intent Mapping

The ontology provides the canonical structures used during intent mapping:

- semantic frames resolve to ontology nodes
- UNLIntent uses ontology IDs
- ambiguity resolution relies on ontology relationships

Without ontology grounding, UNLIntent cannot be deterministic.

---

## 9. Cognitive Core Integration

The Cognitive Core relies on the ontology to:
- validate actions
- check context compatibility
- support gene selection
- interpret constraints
- ensure praxeological consistency

Ontology = the Cognitive Core’s reference language.

---

## 10. Diagram Guidelines (PNG-ready)

### 10.1 Semantic Graph
Nodes: Entities, Actions, States
Edges: allowed transitions and compatibilities

### 10.2 Ontology Kernel
Diagram of the five classes: Entity, Action, State, Modifier, Constraint

### 10.3 Compatibility Matrix
Matrix of allowed combinations (Entity × Action × State)

---

## 11. Summary

The **UNL Semantic Ontology** is the universal conceptual framework that ensures clarity, determinism, coherence and safety across all human–machine interaction. It:

- normalizes meaning,
- resolves ambiguity,
- grounds intent,
- structures praxeological mapping,
- supports Cognitive Core reasoning.

It is the shared semantic language through which humans, machines and operational genes can communicate with precision, neutrality and explainability.
