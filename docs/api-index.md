# API Index
### Complete Index of All Interfaces, Interaction Contracts, and API Schemas in the Digital Genome Ecosystem

---

## 1. Purpose

The **API Index** provides a unified directory of all interfaces, message schemas, integration contracts, and API endpoints defined across the Digital Genome Ecosystem.

This document is essential for:
- integrators,
- system architects,
- developers,
- governance auditors,
- cognitive-core maintainers.

It enables rapid discovery of how subsystems communicate, what data structures they exchange, and which interfaces are stable, versioned, and governed.

---

## 2. Categories of APIs in the Ecosystem

All APIs fall into one of the following canonical categories:

### 2.1 UNL APIs
Interfaces for communication between humans and the system.

### 2.2 Cognitive Core APIs
Internal reasoning, simulation, evaluation, and decision interfaces.

### 2.3 Digital Genome APIs
Gene and codon retrieval, lineage access, and genome-version queries.

### 2.4 System Layer APIs
Execution, monitoring, feedback, governance, and safety interfaces.

### 2.5 Governance & Ledger APIs
Multi-signature approval, audit retrieval, and ledger anchoring.

---

## 3. API Index Table (By Subsystem)

Below is the reference list of all canonical API structures defined in the specification.  
Each entry includes:
- **API Name**
- **File Location**
- **Purpose**
- **Primary Interfaces/Schemas**

---

## 3.1 UNL APIs

| API | File | Purpose |
|-----|------|---------|
| UNL Parsing API | `specs/unl/specification.md` | Converts input text/multimodal signals into UNL structures. |
| Intent Mapping API | `specs/unl/intent-mapping.md` | Maps tokens to structured intents. |
| Context Evaluation API | `specs/unl/context-model.md` | Applies situational context to intents. |
| Translation API | `specs/unl/translation-engine.md` | Converts UNL structures back to human language. |

---

## 3.2 Cognitive Core APIs

| API | File | Purpose |
|-----|------|---------|
| Inference Engine API | `specs/cognitive-core/inference-engine.md` | Produces decisions from UNL inputs. |
| Simulation Engine API | `specs/cognitive-core/simulation-engine.md` | Runs predictive simulations for validation. |
| Oracle Synthesizer API | `specs/cognitive-core/oracle-synthesizer.md` | Forecasts consequences of alternative decisions. |
| Context Evaluator API | `specs/cognitive-core/context-evaluator.md` | Provides environment-aware reasoning support. |
| Evolution Engine API | `specs/cognitive-core/merism-evolution.md` | Generates and evaluates gene variants. |
| Governance Interface API | `specs/cognitive-core/governance-interface.md` | Enforces governance rules inside cognition. |

---

## 3.3 Digital Genome APIs

| API | File | Purpose |
|-----|------|---------|
| Genome Access API | `specs/digital-genome/specification.md` | Retrieves genes, codons, lineages, metadata. |
| Gene Retrieval API | `specs/digital-genome/genes/*.md` | Provides gene definitions and metadata. |
| Codon Retrieval API | `specs/digital-genome/codons/*.md` | Provides codon definitions and metadata. |
| Genome Structure API | `specs/digital-genome/genome-structure.md` | Defines domain-wide gene/codon composition. |

---

## 3.4 System Layer APIs

| API | File | Purpose |
|-----|------|---------|
| Execution API | `specs/system/execution-model.md` | Executes decision plans and codon sequences. |
| Monitoring API | `specs/system/monitoring-model.md` | Streams telemetry, anomalies, and state data. |
| Feedback API | `specs/system/feedback-model.md` | Processes outcomes and informs cognitive updates. |
| Integration Contracts API | `specs/system/integration-contracts.md` | Defines external system communication contracts. |
| Safety Envelope API | `specs/system/safety-invariants.md` | Enforces safety constraints during execution. |
| Failure Mode API | `specs/system/failure-modes.md` | Standard classification for failure-handling logic. |
| Reliability API | `specs/system/reliability-model.md` | Ensures redundancy, fault tolerance, and continuity. |
| Deployment API | `specs/system/deployment-model.md` | Controls distribution, rollout, and runtime isolation. |

---

## 3.5 Governance & Ledger APIs

| API | File | Purpose |
|-----|------|---------|
| Governance Decision API | `specs/system/governance-model.md` | Evaluates and approves/denies operations. |
| Audit & Logging API | `specs/system/governance-model.md` | Writes audit logs into the ledger. |
| Multi-Signature Approval API | `docs/security-principles.md` | Enforces distributed approval for critical actions. |
| Ledger Anchoring API | `docs/security-principles.md` | Anchors actions/decisions into immutable ledger. |
| Identity & Lineage API | `docs/security-principles.md` | Manages identity signatures and lineage proofs. |

---

## 4. API Stability Levels

Every API in the ecosystem is tagged with a **stability level**, indicating maturity and backward compatibility guarantees:

### 4.1 Stable
- Will not change in a breaking way.
- Only backward-compatible additions allowed.

### 4.2 Evolving
- Active improvements ongoing.
- Potential for minor breaking changes.

### 4.3 Experimental
- Early-stage API.
- Not guaranteed for production usage.

Stability levels are documented directly in the specification files.

---

## 5. API Versioning

All APIs follow the versioning rules defined in `docs/versioning-policy.md`:
- SemVer for interface changes
- Genome/Core alignment requirements
- Governance-approved schema evolution

APIs must include:
- version tag,
- change log entry,
- signature lineage (for sensitive interfaces).

---

## 6. Diagram References (PNG-Ready)

### 6.1 API Topology Diagram
`api-topology-overview.png`  
Shows subsystem interactions and message flows.

### 6.2 Cognitive Core API Interactions
`api-cognitive-core-flow.png`  
Illustrates inference → simulation → governance → execution.

### 6.3 UNL Pipeline API Map
`api-unl-pipeline.png`  
End-to-end transformation from human expression to structured intent.

### 6.4 Governance & Ledger API Flow
`api-governance-ledger-flow.png`  
Displays multi-signature approval, anchoring, and audit retrieval.

### 6.5 Execution & Monitoring API Diagram
`api-execution-monitoring.png`  
Shows how execution updates monitoring and feeds back into cognition.

---

## 7. Summary

The **API Index** is the authoritative reference for all communication flows, interfaces, message schemas, and integration contracts in the Digital Genome Ecosystem.

It enables:
- fast discovery of subsystem boundaries,
- correct integration with external systems,
- governance and auditability of interface evolution,
- consistent architecture-wide communication.

This file must be updated whenever new APIs are introduced or existing ones evolve.

