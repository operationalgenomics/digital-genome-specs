# UNL Intent Mapping
### Semantic Convergence Between Human Multimodal Input and Cognitive Codon/Gene Structures

---

## 1. Purpose

The **Intent Mapping Layer** of the UNL is responsible for converting human multimodal expressions into **structured, deterministic, praxeological intents** suitable for processing by the Cognitive Core.

Its mission is to:
- detect intent from ambiguous or natural human expression,
- normalize linguistic, gestural and contextual cues,
- map meaning onto the Digital Genome’s fundamental triad (Entity → Action → State),
- attach constraints, modifiers and priorities,
- ensure all mapped intents conform to safety and governance policies.

The Intent Mapping Layer is the *semantic heart* of the UNL.

---

## 2. Design Principles

### 2.1 Universality
All human expressions — verbal, gestural, textual, contextual — must map to the same internal representation.

### 2.2 Determinism
A given input + context must always produce the same mapped intent.

### 2.3 Minimal Semantics
Every mapped intent must reduce to:
- **Entities** (who/what)
- **Action** (what operation)
- **Target-State** (desired resulting condition)

### 2.4 Contextual Enrichment
UNL may enrich the intent with context-derived:
- constraints
- modifiers
- inferred missing details

### 2.5 Governance-Aware Mapping
The mapping process must:
- reject unsafe intents,
- require confirmation when policies demand it,
- enforce operator permissions.

---

## 3. Intent Processing Pipeline

### **Step 1 — Input Reception**
Raw multimodal input arrives as **RawInputEnvelope**.

### **Step 2 — Semantic Parsing**
The parser extracts:
- entities
- actions
- states
- modifiers
- constraints
- intent type indicators

### **Step 3 — Ambiguity Detection**
The system evaluates ambiguity in:
- entities
- actions
- states
- constraints

If ambiguity > threshold → trigger clarification loop.

### **Step 4 — Contextual Binding**
The UNL binds parsed items to:
- known entities from the Digital Genome
- operational domain ontologies

### **Step 5 — Praxeological Encoding**
The mapped intent is encoded into **UNLIntent**:
- entityId[]
- actionId
- targetStateId
- constraints[]
- modifiers{}
- ambiguityLevel

### **Step 6 — Governance Pre-Check**
Before sending to the Cognitive Core, UNL:
- checks authorization rules
- enforces forbidden actions
- pauses for human approval when required

### **Step 7 — Intent Dispatch**
The finalized intent is delivered to the Cognitive Core.

---

## 4. Intent Mapping Model

UNL uses a **three-tier semantic abstraction model**.

### 4.1 Tier 1 — Natural Expression
Direct human input:
- “Shut down pump 04”
- gesture pointing at a machine
- emergency button press
- voice: “Lower this pressure now”

### 4.2 Tier 2 — Semantic Frame
Neutral abstraction such as:
```json
{
  "entities": ["pump_04"],
  "actions": ["shutdown"],
  "states": ["inactive"],
  "modifiers": {},
  "constraints": ["immediate"]
}
```

### 4.3 Tier 3 — Praxeological Intent (UNLIntent)
Machine-actionable form:
```json
{
  "entities": ["pump_04"],
  "action": "stop",
  "targetState": "isolated",
  "constraints": ["immediate"],
  "modifiers": {},
  "ambiguityLevel": 0
}
```

---

## 5. Data Structures

### 5.1 Parsed Semantic Frame
```ts
interface SemanticFrame {
  entities: string[];
  actions: string[];
  states: string[];
  modifiers?: Record<string, unknown>;
  constraints?: string[];
  intentType: string;
  confidence: number;
}
```

### 5.2 Mapped Praxeological Intent
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

---

## 6. Mapping Rules

### 6.1 Entity Mapping
Resolution process:
1. Match direct names.
2. Use disambiguation if multiple matches.
3. Apply contextual hints (e.g., proximity, operator viewpoint).
4. Default to highest-confidence entity.

### 6.2 Action Mapping
Actions must map to the Digital Genome action registry.

Natural expressions → canonical actions:
- “Kill”, “Turn off”, “Stop immediately” → **stop**
- “Start”, “Activate”, “Begin cycle” → **start**
- “Check”, “Inspect”, “Verify” → **inspect**

### 6.3 Target-State Mapping
Derived from:
- explicit operator request
- domain defaults
- safety policies

E.g. “Shut down” may map to:
- `stopped`
- `isolated`
- `safe_halt`

depending on rules.

### 6.4 Constraint Mapping
Constraints give nuance:
- timing
- safety
- priority
- resource usage

### 6.5 Modifier Mapping
Modifiers refine:
- intensity
- speed
- precision
- thresholds

---

## 7. Ambiguity Resolution Logic

### 7.1 Ambiguity Score
Ambiguity is calculated from:
- number of candidate entities
- conflicting actions
- inconsistent states
- insufficient context
- vague natural-language expressions

### 7.2 Clarification Loop
If `ambiguityLevel > threshold`:
- UNL generates a clarification question
- operator selects or responds
- the intent is refined

### 7.3 Safety-Driven Clarification
If an interpretation could lead to unsafe action:
UNL must enforce clarification even below normal thresholds.

---

## 8. Cognitive Core Integration

UNLIntent is delivered through:
```ts
sendIntent(intent: UNLIntent): Promise<CognitiveResponse>;
```

The Cognitive Core responds with:
- selected gene
- action plan
- risks
- alternatives
- explanation trace

UNL reformats this for the operator.

---

## 9. Example Mapping Scenarios

### 9.1 Speech + Context
Human says: “Turn it off!” while pointing at a machine.

UNL:
- uses gesture to identify entity
- parses “turn off” → action: stop
- context → targetState: isolated

### 9.2 Text Command
"Prepare crane A for lift operation."

UNL →
- entity: crane_A
- action: prepare
- state: ready_for_lift

### 9.3 Emergency Gesture
Operator slams emergency panel.

UNL →
- action: emergency_stop
- constraints: immediate
- entity: global_scope

---

## 10. Diagram Guidelines (PNG-ready)

### 10.1 Intent Abstraction Funnel
Natural Input → Semantic Frame → UNLIntent → Cognitive Core

### 10.2 Ambiguity Loop
Input → Uncertainty → Clarification → Final Intent

### 10.3 Mapping Schema
Entities, Actions, States → Unified Praxeological Intent

---

## 11. Summary

The **Intent Mapping Layer** is the mechanism that transforms messy, ambiguous, multimodal human expression into precise, deterministic, safe, and actionable semantic structures. It ensures that humans can express what they want naturally, while the system interprets with rigor, predictability and alignment with the Digital Genome.

