# UNL Specification
### Universal Neutral Language — Multimodal Intent, Semantic Abstraction and Cognitive Interfacing

---

## 1. Purpose

The **Universal Neutral Language (UNL)** is the human–machine interface layer of the Digital Genome ecosystem.  
Its mission is to convert *human multimodal intent* into *machine-actionable cognitive structures* and to translate *cognitive explanations* back into human-readable form.

UNL serves as:
- the **linguistic substrate** of the Cognitive Core,
- the **semantic bridge** between humans, machines and operational genes,
- the **neutral grammar** enabling domain-agnostic communication,
- the **explainability layer** translating cognitive reasoning back to the operator.

UNL is not a natural language, nor a programming language.  
It is a **semantic, praxeological interface** designed for clarity, universality, neutrality and operational consistency.

---

## 2. Design Principles

### 2.1 Multimodal by Default
UNL accepts:
- speech
- text
- gesture
- haptics
- visual selections
- contextual signals
- affective annotations

### 2.2 Neutrality & Universality
UNL abstracts away:
- human languages
- operator skill level
- domain specifics
- cultural variations

### 2.3 Intent-First Interpretation
UNL interprets *what the user wants*, not merely what they say.

### 2.4 Semantic Minimalism
All statements reduce to:
- **Entities**
- **Actions**
- **States**
- **Modifiers**
- **Constraints**
- **Contextual anchors**

### 2.5 Deterministic Mapping
Every human input must map to a **deterministic semantic structure** consumed by the Cognitive Core.

### 2.6 Full Explainability
Every cognitive output must be translated back into:
- clear natural-language explanations
- operator-friendly summaries
- multimodal clarification options

---

## 3. Functional Overview

UNL performs six essential functions:

1. **Intent Capture** — receive human input in any modality.
2. **Semantic Parsing** — convert signal into structured meaning.
3. **Praxeological Encoding** — map meaning to codons/genes.
4. **Ambiguity Resolution** — interactively refine unclear intents.
5. **Cognitive Interface** — pass structured input to the Cognitive Core.
6. **Human Explanation Layer** — translate cognitive output into natural expression.

---

## 4. UNL Architecture

The architecture is composed of four logical layers.

### 4.1 Multimodal Capture Layer
Handles:
- speech-to-text
- gesture analysis
- gaze selection
- keyboard/text input
- contextual metadata

Outputs **RawInputEnvelope**.

### 4.2 Semantic Parser
Transforms raw input into neutral structures:
- tokenization
- syntactic role labeling
- semantic frame extraction
- domain alignment

Outputs **SemanticFrame**.

### 4.3 Praxeological Mapper
Maps semantic frames into praxeological components:
- Entity
- Action
- Target-State
- Constraints
- Modifiers

Outputs **UNLIntent**.

### 4.4 Explanation & Rendering Engine
Translates cognitive outputs back into:
- natural sentences
- visual summaries
- step-by-step narratives
- risk justification

Outputs **HumanExplanation**.

---

## 5. UNL Core Data Structures

```ts
interface RawInputEnvelope {
  modality: 'speech' | 'text' | 'gesture' | 'visual' | 'mixed';
  content: any;
  timestamp: Timestamp;
  metadata?: Record<string, unknown>;
}

interface SemanticFrame {
  intentType: string;
  entities: string[];
  actions: string[];
  states: string[];
  modifiers?: Record<string, unknown>;
  constraints?: string[];
  confidence: number;
}

interface UNLIntent {
  entities: EntityId[];
  action: ActionId;
  targetState?: StateId;
  modifiers?: Record<string, unknown>;
  constraints?: ConstraintSpec[];
  ambiguityLevel: number;
}

interface HumanExplanation {
  title: string;
  summary: string;
  steps: string[];
  risks?: string[];
  alternatives?: string[];
}
```

---

## 6. UNL → Cognitive Core Flow

### **Step 1 — Input Capture**
UNL receives multimodal signals.

### **Step 2 — Semantic Parsing**
UNL extracts meaning-independent-of-language.

### **Step 3 — Praxeological Mapping**
UNL maps meaning to:
- entity
- action
- state
- intent type

### **Step 4 — Intent Packaging**
Produces a **UNLIntent** and sends it to the Cognitive Core.

### **Step 5 — Cognitive Evaluation**
The Cognitive Core:
- evaluates intent
- identifies candidate genes
- selects the optimal option

### **Step 6 — Explanation Return**
UNL translates the full decision trace into:
- friendly explanation
- operator-facing narrative
- multimodal cues

---

## 7. Ambiguity Resolution

UNL provides dynamic clarification dialogs to reduce ambiguity.

### 7.1 Ambiguity Classes
- **Entity Ambiguity** (“Which pump?”)
- **Action Ambiguity** (“Do you mean stop or isolate?”)
- **State Ambiguity** (“What level of shutdown?”)
- **Constraint Ambiguity** (“Any safety restrictions?”)

### 7.2 Resolution Methods
- natural language questioning
- highlight/gesture selection
- context-aware suggestions
- disambiguation menus

---

## 8. Explanation Engine

UNL produces:

### 8.1 Narrative Explanation
Clear paragraphs describing:
- what will happen
- why it was chosen
- what was rejected
- risks involved

### 8.2 Codon-Level Explanation
For advanced operators:
- show codons
- show gene structure
- show transitions

### 8.3 Safety Explanation
Important for governance:
- safety checks
- risk thresholds
- constraints satisfied

---

## 9. Compliance & Safety Requirements

UNL must enforce:

### 9.1 Identity Awareness
Certain intents can only be issued by:
- certified operators
- authorized agents
- specific roles

### 9.2 Safety Constraints
UNL cannot phrase an intent that violates safety.

### 9.3 Governance Hooks
UNL must:
- check approval mode (auto/review/forbidden)
- pause when required
- prompt operator confirmation

### 9.4 Immutable Logging
Every input → output pair must be logged.

---

## 10. Integration Contracts

### 10.1 UNL → Cognitive Core
```ts
sendIntent(intent: UNLIntent): Promise<CognitiveResponse>;
```

### 10.2 Cognitive Core → UNL
```ts
formatExplanation(response: CognitiveResponse): Promise<HumanExplanation>;
```

### 10.3 UNL → Operator
Rendered via:
- natural language
- icons/diagrams
- highlighted risk summaries
- alternative suggestions

---

## 11. Diagram Guidelines (PNG-ready)

### 11.1 UNL Architecture Diagram
Multimodal Input → Parser → Mapper → Cognitive Core → Explanation Engine → Human

### 11.2 Intent Flow
Raw Input → Semantic Frame → UNLIntent → Cognitive Core → Explanation → Operator

### 11.3 Ambiguity Resolution
Intent → Ambiguity → Clarification Loop → Resolved Intent

### 11.4 Explanation Rendering
Cognitive Output → Narrative + Codons + Risks + Alternatives

---

## 12. Summary

The **Universal Neutral Language (UNL)** is the semantic backbone of human-AI interaction within the Digital Genome ecosystem. It:

- captures human intention,
- interprets it neutrally,
- converts it into actionable cognitive structures,
- receives cognitive decisions,
- translates them into human-understandable explanations.

UNL forms the **interface of trust** between humans and the Cognitive Core, ensuring clarity, neutrality, safety and full explainability.

