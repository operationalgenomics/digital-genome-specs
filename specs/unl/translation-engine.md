# UNL Translation Engine
### Bidirectional Semantic Rendering, Cognitive Explanation, and Natural-Language Realization for the Universal Neutral Language

---

## 1. Purpose

The **UNL Translation Engine** is responsible for converting:

1. **UNL → Natural Language** (explanations, summaries, operational guidance)
2. **Natural Language → UNL** (interpretations, questions, clarifications)
3. **Cognitive Core Outputs → Human-Readable Narratives**

Its purpose is to ensure that every interaction between humans and the Digital Genome ecosystem is:
- clear,
- consistent,
- linguistically neutral,
- semantically faithful,
- safe,
- fully explainable.

Unlike Intent Mapping (which interprets the operator), the Translation Engine focuses on **expression** — rendering meaning back into natural or multimodal communication.

---

## 2. Design Principles

### 2.1 Semantic Fidelity
The output must precisely reflect the cognitive structure, without distortion.

### 2.2 Deterministic Mapping
The same UNL structure must generate consistent translations.

### 2.3 Safety-Aware Rendering
Language must not:
- downplay risk,
- hide required constraints,
- misrepresent safety flags.

### 2.4 Universality
Translations must be independent of:
- operator language,
- cultural context,
- technical domain.

### 2.5 Multi-Format Rendering
The engine renders:
- text,
- structured messages,
- voice prompts,
- visual highlights,
- operator guidance sequences.

---

## 3. Functional Overview

The Translation Engine performs six core functions:

1. **Parsing of UNL structures** — codons, intents, constraints.
2. **Semantic rendering** — natural language realization.
3. **Risk communication** — translating safety concerns.
4. **Trace explanation** — converting cognitive reasoning into narratives.
5. **Strategy summarization** — expressing selected genes and pathways.
6. **Multimodal output** — adapting the explanation to required channels.

---

## 4. Input Structures

The Translation Engine receives formal objects from the Cognitive Core:

```ts
interface CognitiveResponse {
  selectedGene: GeneId;
  codonSequence: PraxeologicalCodon[];
  explanation: ExplanationArtifact;
  risks?: string[];
  alternatives?: string[];
  constraints?: ConstraintSpec[];
}
```

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

## 5. Translation Pipeline

Translation occurs in four stages.

### Stage 1 — Semantic Decomposition
Break structures into linguistic primitives:
- actors (entities)
- verbs (actions)
- state transitions
- constraints
- sequence order
- causal links

### Stage 2 — Template Selection
Choose rendering pattern based on:
- action category
- risk level
- operator skill level
- governance mode

### Stage 3 — Narrative Assembly
Build human-readable text:
- clear main sentence,
- ordered operational steps,
- explanations,
- safety instructions.

### Stage 4 — Format Adaptation
Output adapted for:
- UI text,
- speech synthesis,
- notification cards,
- summarized briefings.

---

## 6. Rendering Rules

### 6.1 Entity Rendering
Entities are always named using their canonical label.

Example:
```ts
"Pump-401" → "Pump 401"
```

### 6.2 Action Rendering
Actions use simple, unambiguous verbs:
```ts
activate, stop, isolate, inspect, configure
```

### 6.3 State Rendering
States convert into descriptive adjectives or clauses:
```ts
"isolated" → "in isolated mode"
"safe_halt" → "in safe halt condition"
```

### 6.4 Constraint Rendering
Constraints must always be expressed explicitly.

Example:
```ts
Constraint: { rule: "safety_zone_required" }
→ "Ensure all personnel are outside the safety zone."
```

### 6.5 Risk Rendering
If risks exist, they must be:
- highlighted,
- explicit,
- severity-labeled.

Example:
```ts
"High risk: vibration levels exceed threshold."
```

### 6.6 Sequence Rendering
Codons must be described in execution order.
Example:
1. "Isolate Pump 401."
2. "Stop Pump 401."
3. "Inspect Pump 401 for anomalies."

---

## 7. Explanation Generation

The Translation Engine produces **cognitive explanations** using the ExplanationArtifact structure.

### 7.1 Structure of an Explanation
```ts
interface ExplanationArtifact {
  reasoningSteps: string[];
  selectionCriteria: string[];
  rejectedAlternatives: string[];
  contextFactors: string[];
}
```

### 7.2 Explanation Rendering Rules
Rendered explanations must:
- describe why the gene was selected,
- reveal safety considerations,
- show critical context factors,
- list rejected alternatives with reasons.

### Example Output
```ts
"Gene G-EMERGENCY-STOP was selected because vibration levels exceeded the critical threshold. Safer alternatives were unavailable due to active alarms."
```

---

## 8. Bidirectional Translation

### 8.1 Natural Language → UNL
When the operator asks:
```ts
"Why did you choose this action?"
```
The engine must:
- interpret the intent,
- trigger explanation request,
- deliver full reasoning.

### 8.2 UNL → Natural Language
When the Cognitive Core responds:
```ts
selectedGene: "GEN-001"
```
The engine must produce:
```ts
"Executing Gene GEN-001: System will isolate, stop, and inspect Pump 401." 
```

---

## 9. Safety and Governance Rendering

### 9.1 Mandatory Disclosures
The engine must disclose:
- forbidden actions,
- restricted steps,
- required human approvals.

### 9.2 Governance Mode Rendering
If governance mode = `review`:
```ts
"Operator approval required before execution."
```
If forbidden:
```ts
"This action cannot be performed under current governance policy."
```

---

## 10. Multimodal Output Rules

### 10.1 Voice Output
Must prioritize clarity and avoid overloaded phrasing.

### 10.2 UI Text Output
Must provide:
- key message first,
- detailed steps below,
- risks highlighted.

### 10.3 Visual Output
Can include:
- entity highlighting,
- state transitions diagrams,
- workflow paths.

---

## 11. Integration with Context Model

The Translation Engine adjusts explanations based on context:
- operator skill level,
- urgency,
- active alarms,
- governance restrictions.

Advanced operators receive more technical detail.
Novices receive simplified explanations.

---

## 12. Diagram Guidelines (PNG-ready)

### 12.1 Translation Flow Diagram
UNLIntent → Cognitive Response → Narrative + Codons + Risks.

### 12.2 Explanation Rendering Diagram
ReasoningSteps → Narrative Explanation.

### 12.3 Governance Output Diagram
Governance Mode → Required Actions → Rendered Notifications.

---

## 13. Summary

The **UNL Translation Engine** is the expressive layer of the Universal Neutral Language.  
It transforms cognitive intelligence into clear, contextual, safe, and actionable communication for operators.

It ensures:
- linguistic clarity,
- semantic fidelity,
- transparency of reasoning,
- correct risk communication,
- and full alignment with safety and governance.

It is the bridge through which the system **speaks back to humans** with precision, confidence, and responsibility.

