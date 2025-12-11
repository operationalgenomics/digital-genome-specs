# System Integration Contracts
### Cross-Layer APIs, Message Schemas, and Interoperability Rules for the Digital Genome Ecosystem

---

## 1. Purpose

The **System Integration Contracts** define the formal interfaces that connect all major subsystems of the Digital Genome Ecosystem:

- Universal Neutral Language (UNL)
- Cognitive Core
- Digital Genome
- Execution Layer
- Monitoring & Feedback Layer
- System Governance

These contracts specify:
- API boundaries
- message schemas
- interaction patterns
- versioning rules
- safety and governance hooks

Their goal is to ensure that all components can evolve independently while **remaining interoperable, safe, and explainable**.

---

## 2. Design Principles

### 2.1 Clear Boundaries
Each subsystem exposes a minimal, well-defined interface.

### 2.2 Contract-First Design
APIs are described as contracts **before** implementation.

### 2.3 Strong Typing and Validation
All messages must be validated against schemas.

### 2.4 Backward-Compatible Evolution
New versions of contracts must not break existing, approved behaviors.

### 2.5 Governance and Safety Integration
All critical calls must:
- pass through governance checks,
- respect safety constraints,
- be traceable.

---

## 3. High-Level Interaction Map

Primary integration flows:

1. **UNL → Cognitive Core** — intent submission
2. **Cognitive Core → UNL** — explanation and clarification
3. **Cognitive Core → Digital Genome** — gene queries and updates
4. **Cognitive Core → Execution** — execution plan dispatch
5. **Execution → Monitoring** — telemetry and events
6. **Monitoring → Feedback** — outcome evaluation, anomaly signals
7. **Feedback → Cognitive Core / Digital Genome** — fitness and evolution
8. **Governance → All** — policy enforcement and decision gating

Each of these flows is defined by explicit contracts below.

---

## 4. UNL ↔ Cognitive Core Contracts

### 4.1 Submit Intent (UNL → Cognitive Core)

```ts
// UNL → Cognitive Core
interface SendIntentRequest {
  intent: UNLIntent;
  context: UNLContext;
}

interface SendIntentResponse {
  ticketId: string;
  status: 'accepted' | 'rejected';
  reason?: string;
}
```

Usage:
- UNL sends a contextualized intent.
- Cognitive Core acknowledges and returns a ticket for traceability.

---

### 4.2 Request Explanation (UNL → Cognitive Core)

```ts
interface ExplanationRequest {
  ticketId: string;
  detailLevel: 'summary' | 'full' | 'debug';
}

interface ExplanationResponse {
  explanation: HumanExplanation;
}
```

Usage:
- Operator asks "Why?" or "What will happen?".
- UNL requests and renders an explanation.

---

## 5. Cognitive Core ↔ Digital Genome Contracts

### 5.1 Gene Query

```ts
interface GeneQueryRequest {
  intent: UNLIntent;
  context: UNLContext;
}

interface GeneQueryResponse {
  candidateGenes: GeneId[];
}
```

### 5.2 Gene Execution Plan Request

```ts
interface GenePlanRequest {
  geneId: GeneId;
  context: UNLContext;
}

interface GenePlanResponse {
  executionPlan: ExecutionPlan;
}
```

### 5.3 Genome Update Proposal

```ts
interface GenomeUpdateProposal {
  variants: GeneVariant[];
  antiGenes: AntiGene[];
  hypotheses: Hypothesis[];
}

interface GenomeUpdateDecision {
  approvedVariants: string[];
  approvedAntiGenes: string[];
  rejectedItems: string[];
}
```

All genome updates must be passed through **Governance** before application.

---

## 6. Cognitive Core ↔ Execution Layer Contracts

### 6.1 Dispatch Execution Plan

```ts
interface DispatchExecutionRequest {
  plan: ExecutionPlan;
}

interface DispatchExecutionResponse {
  executionId: string;
  status: 'scheduled' | 'rejected';
  reason?: string;
}
```

### 6.2 Execution Status Stream

```ts
interface ExecutionStatusEvent {
  executionId: string;
  planId: string;
  stepId?: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  metrics?: Record<string, unknown>;
  safetyFlags?: string[];
}
```

Execution status events are streamed to:
- Monitoring
- Cognitive Core
- Governance ledger (for critical actions)

---

## 7. Execution ↔ Monitoring Contracts

### 7.1 Telemetry Event

```ts
interface TelemetryEvent {
  timestamp: Timestamp;
  sourceSystem: string;
  entity: EntityId;
  state: string;
  metrics: Record<string, unknown>;
}
```

### 7.2 Anomaly Event

```ts
interface AnomalyEvent {
  timestamp: Timestamp;
  entity: EntityId;
  anomalyType: 'state' | 'metric' | 'behavioral' | 'cognitive';
  severity: 'low' | 'medium' | 'high' | 'critical';
  details: string;
}
```

Monitoring aggregates these events and emits **OutcomeEvaluations** to the Feedback system.

---

## 8. Monitoring ↔ Feedback Contracts

### 8.1 Outcome Evaluation Message

```ts
interface OutcomeEvaluation {
  planId: string;
  executionId: string;
  success: boolean;
  classification: 'success' | 'partial' | 'safeFailure' | 'unsafeFailure';
  deviations?: string[];
  anomalyScore?: number;
  safetyIncidents?: string[];
}
```

### 8.2 Feedback Broadcast

```ts
interface FeedbackBroadcast {
  evaluation: OutcomeEvaluation;
  metrics?: Record<string, unknown>;
}
```

Feedback is consumed by:
- Cognitive Core (learning)
- Digital Genome (fitness updates)
- Governance (compliance)

---

## 9. Feedback ↔ Cognitive Core / Digital Genome Contracts

### 9.1 Fitness Update Message

```ts
interface FitnessUpdate {
  geneId: GeneId;
  delta: number;
  reason: string;
  metrics?: Record<string, unknown>;
}
```

### 9.2 Evolution Trigger

```ts
interface EvolutionTrigger {
  geneId: GeneId;
  triggerType: 'failurePattern' | 'performancePlateau' | 'contextShift' | 'safetyEvent';
  evidence: Record<string, unknown>;
}
```

These messages feed the **Merism Evolution Engine**.

---

## 10. Governance ↔ All Subsystems Contracts

### 10.1 Governance Check (Generic)

```ts
interface GovernanceCheckRequest {
  actorId: string;
  eventType: 'intent' | 'decision' | 'execution' | 'update' | 'evolution';
  payload: Record<string, unknown>;
}

interface GovernanceCheckResponse {
  mode: 'auto' | 'review' | 'forbidden';
  appliedPolicies: string[];
  safetyFlags?: string[];
  rationale: string;
}
```

### 10.2 Governance Log Entry

```ts
interface GovernanceLogEntry {
  timestamp: Timestamp;
  actor: string;
  eventType: string;
  payloadSummary: Record<string, unknown>;
  decision: GovernanceDecision;
  signature?: string;
}
```

All critical events must produce a GovernanceLogEntry.

---

## 11. Versioning and Compatibility Rules

### 11.1 Semantic Versioning
All contracts follow:
```ts
MAJOR.MINOR.PATCH
```

- MAJOR: breaking changes
- MINOR: backward-compatible extensions
- PATCH: bugfixes and clarifications

### 11.2 Backward Compatibility
New versions must:
- accept older message formats when possible,
- preserve meaning of existing fields,
- deprecate before removal.

### 11.3 Contract Registry
A central registry tracks:
- contract name,
- version,
- owner subsystem,
- changelog,
- deprecation status.

---

## 12. Error Handling and Resilience

### 12.1 Standard Error Envelope

```ts
interface ErrorEnvelope {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  retriable: boolean;
}
```

### 12.2 Retry and Backoff
Certain calls (e.g., telemetry, feedback) may be retried with exponential backoff.

### 12.3 Circuit Breakers
If a subsystem becomes unstable, governance may:
- trip circuit breakers,
- restrict certain contracts,
- route to safe fallbacks.

---

## 13. Diagram Guidelines (PNG-ready)

### 13.1 Integration Overview (`system-integration-overview.png`)
Shows all subsystems and contract calls.

### 13.2 Message Flow Diagrams (`system-integration-flows-*.png`)
Separate diagrams for:
- UNL ↔ Cognitive Core
- Cognitive Core ↔ Digital Genome
- Cognitive Core ↔ Execution
- Execution ↔ Monitoring ↔ Feedback
- Governance ↔ All

### 13.3 Contract Registry Diagram (`system-contract-registry.png`)
Shows how contracts are versioned and managed.

---

## 14. Summary

The **System Integration Contracts** define the formal communication backbone of the Digital Genome Ecosystem.

They ensure that:
- subsystems remain loosely coupled but strongly aligned,
- all interactions are typed, validated, and governed,
- safety and governance are embedded in every critical call,
- evolution is possible without breaking the system.

With these contracts, the architecture becomes **implementable, testable, and evolvable** in a real-world engineering environment.

