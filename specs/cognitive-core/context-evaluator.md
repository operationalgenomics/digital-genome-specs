# Cognitive Core — Context Evaluator
### Semantic Processing and Environmental Understanding for Operational Reasoning

---

## 1. Purpose

The **Context Evaluator** is the subsystem responsible for transforming raw environmental information into structured, coherent, and actionable context for the Cognitive Core.  
It acts as the bridge between heterogeneous data sources (sensors, digital twins, industrial systems, human annotations) and the reasoning modules of the Cognitive Core.

This document defines:

- The conceptual role of the Context Evaluator  
- Context ingestion, normalization, and semantic binding  
- Safety and integrity validation  
- Context scoring mechanisms  
- Interfaces with the Inference Engine and Digital Genome  
- Internal data structures used for reasoning  

---

## 2. Design Principles

### 2.1 Context as First-Class Citizen  
Reasoning only begins after a complete, validated `ContextSnapshot` is produced.

### 2.2 Multi-Source Integration  
The evaluator must unify information from:
- Real-time sensor streams  
- System logs  
- Operator annotations  
- Digital twin simulations  
- Historical archive data  

### 2.3 Structured Abstraction  
Raw data is abstracted into meaningful contextual features (e.g., risk indicators, operational states, anomalies).

### 2.4 Semantic Binding  
Every entity, action, and state referenced in the context must be aligned with Digital Genome ontologies.

### 2.5 Safety and Consistency Validation  
The Context Evaluator filters out inconsistent, corrupted, or unsafe context before it reaches the Inference Engine.

---

## 3. Responsibilities

The Context Evaluator performs six core functions:

### 3.1 Context Ingestion  
Receives raw/unified data from:
- SCADA/PLC  
- MES/WMS/EMS  
- EMR/EHR (when in health systems)  
- Industrial IoT platforms  
- Human operators via UNL  

### 3.2 Context Normalization  
Standardizes the input into a unified structure:
- Data type alignment  
- Unit normalization (e.g., Pa → kPa, °C → K)  
- Temporal alignment  
- Removal of duplicated or outdated data  

### 3.3 Semantic Entity Binding  
Matches data inputs to Digital Genome `EntityId`, `ActionId`, and `StateId` definitions.

This ensures:
- Referential integrity  
- Ontology alignment  
- Avoidance of “rogue entities”  

### 3.4 Context Integrity Validation  
The evaluator flags or rejects contexts that exhibit:
- Missing essential fields  
- Logical contradictions  
- Unsafe state combinations  
- Device failure indicators  
- Stale timestamps  

### 3.5 Derived Feature Computation  
Computes higher-level contextual indicators, such as:
- Risk scores  
- Operational stress levels  
- System bottlenecks  
- Safety threshold violations  
- Temporal patterns  

### 3.6 Context Scoring  
Generates a composite score used to rank genes by contextual suitability.

---

## 4. Context Processing Pipeline

The context undergoes a layered transformation:

1. **Raw Data Layer**  
   - Direct data from sensors and systems.

2. **Normalization Layer**  
   - Cleansing, reformatting, unit standardization.

3. **Semantic Layer**  
   - Mapping to genome entities and states.

4. **Integrity Layer**  
   - Validation of coherence and completeness.

5. **Feature Layer**  
   - Computation of derived, high-level features.

6. **Context Snapshot Assembly**  
   - Final structure consumed by the Inference Engine.

---

## 5. Internal Architecture

### 5.1 Ingestion Module  
Defines adapters for each data source class.  
Adapters standardize:
- Timestamping  
- Source identification  
- Quality metrics  

### 5.2 Normalizer  
Applies transformations:
- Unit conversion  
- Value smoothing  
- Outlier handling  
- Missing value resolution  

### 5.3 Semantic Binder  
Match rules (logical-level):
- Entity Recognition  
- Action/State Alignment  
- Topology mapping  
- Ontology tag insertion  

### 5.4 Integrity Validator  
Validation rules include:
- `NoEntityWithoutState`  
- `NoContradictoryStates`  
- `ChronologicalCoherence`  
- `SafetyLevelConsistency`  

### 5.5 Feature Extractor  
Models include:
- Threshold-based indicators  
- Multivariate risk models  
- Contextual embeddings  
- System load models  

### 5.6 Composite Scoring Engine  
Produces the `ContextScore` used by the Inference Engine.

---

## 6. Data Structures (Logical-Level)

```ts
interface ContextSnapshot {
  id: string;
  capturedAt: Timestamp;
  sourceSystemIds: string[];
  rawData: Record<string, unknown>;
  normalizedData: Record<string, unknown>;
  semanticMap: SemanticBinding[];
  integrity: ContextIntegrity;
  features: ContextFeatures;
  contextScore: number;
}

interface SemanticBinding {
  entityId?: EntityId;
  stateId?: StateId;
  actionId?: ActionId;
  sourceKey: string;
  confidence: number;
}

interface ContextIntegrity {
  isValid: boolean;
  issues: ContextIssue[];
  safetyFlags?: string[];
}

interface ContextFeatures {
  riskLevel?: number;
  operationalLoad?: number;
  anomalyScore?: number;
  derivedSignals?: Record<string, unknown>;
}

interface ContextIssue {
  code: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
}
```
---
## 7. Validation Rules

### 7.1 Essential Fields
A valid context must include:

- Timestamp  
- At least one entity reference  
- System state information  
- Integrity score  

### 7.2 Coherence Checks
Examples:

- A pump cannot be simultaneously “Running” and “Stopped”.  
- A machine cannot show future timestamps relative to evaluator time.  
- Pressure cannot be negative unless explicitly allowed by specification.  

### 7.3 Safety Preconditions
If a context violates critical safety indicators:

- The entire inference cycle must halt  
- The operator must be notified via UNL  
- The Digital Genome must log the event  

---

## 8. Outputs

The Context Evaluator produces:

### 8.1 ContextSnapshot
The final structured, validated, semantically-rich context object.

### 8.2 ContextScore
Used by the Inference Engine to match and rank genes.

### 8.3 Integrity Flags
Transported to:

- Governance layer  
- Safety modules  
- Evolution engine (Merism)  

---

## 9. Integration Contracts

### 9.1 With Inference Engine
The Context Evaluator must provide:

- Final ContextSnapshot  
- Composite context score  
- Integrity report  
- Feature vector  

### 9.2 With Digital Genome
The evaluator relies on:

- Entity/Action/State registries  
- Ontology references  
- Context validation rules  

### 9.3 With UNL
Operator annotations (qualitative context) are included in semantic binding.

---

## 10. Diagram Guidelines (for future PNGs)

### 10.1 Context Processing Pipeline Diagram
Depict the path:

- Raw Data → Normalization → Semantics → Validation → Features → Snapshot  

### 10.2 Semantic Binding Map
Mapping raw inputs to Digital Genome entities.

### 10.3 Context Integrity Matrix
Table showing validation checks and severity flags.

---

## 11. Summary

The Context Evaluator is the component that transforms a chaotic mix of operational data into a coherent, semantically-aligned, reliable representation of the world.  
It ensures that all cognitive reasoning is grounded in validated, safe, meaningful context — forming the substrate on which the Inference Engine and entire Cognitive Core operate.
