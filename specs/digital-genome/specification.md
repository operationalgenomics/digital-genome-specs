# 7 — Digital Genome Specification

> (Top-Level Architecture Specification)

## 7.1 Purpose and Scope

The __Digital Genome__ is the canonical, organization-wide representation of __operational knowledge as living, evolutionary structure,__ not just static documentation or code. 
It encodes ***intentional action*** as composable units (codons and genes) and exposes them to the __Cognitive Core__ for reasoning and to the ***Universal Neutral Language (UNL)*** for human interaction.

This specification defines, at the highest architectural level:

1. The __conceptual model_ (***codons → genes → genome***).
2. The __abstract data model__ (***key types, relationships, invariants***).
3. The __interaction contracts__ with:
    * Cognitive Core (_read / write / evolve_).
    * UNL (_intent → codons / codons → feedback_).
4. The governance and lifecycle of the Digital Genome.

#### Implementation details (persistence, specific DBs, frameworks) are out of scope and left to lower-level design.
---
## 7.2 Design Principles

### 7.2.1 Intention-First
Every artifact in the genome must represent intentional action (praxeology), not just raw events or measurements.

### 7.2.2 Minimal Universal Grammar
All operational knowledge is reducible to combinations of three primitives: Entities, Actions, States, structured as praxeological codons.

### 7.2.3 Composability and Heredity
Genes are sequences of codons; genomes are libraries of genes. Both must support versioning, recombination, and inheritance (Merism) across time, systems and organizations.

### 7.2.4 Technology-Agnostic Core
The conceptual and logical model must be independent of programming language or database technology. Code examples are binding illustrations, not mandatory implementations.

### 7.2.5 Cognitive First-Class Integration
The genome is designed to be readable and writable by the Cognitive Core as a first-class citizen, not as an afterthought (no “middleware cemetery”).

### 7.2.6 Human-Centric Interface
The UNL must be able to map human multimodal intent directly into codons / genes and back, without exposing internal technical details to operators.

---
## 7.3 Conceptual Model

### 7.3.1 Core Concepts
  * __Entity__  
        A thing that can act or be acted upon in the operational world.
        Examples: _Pump-401, Patient-ID123, Crane-03, Conveyor-Line-A._
  * __Action__  
        An intentional operation applied to an entity.
        Examples: _Start, Stop, Medicate, Lift, Isolate, Evacuate._
  * __State__  
        A meaningful condition or status of an entity that matters for decision-making.
        Examples: _Operational, Standby, Critical, In Transit, Isolated._
  * __Praxeological Codon__  
        The smallest unit of operational intent:
        > __[ Entity | Action | Target-State ]__
        Example: ```[Pump-401 | Stop | Isolated]```.
        This is the “atom” of Operational Genomics.
  * __Operational Gene__  
      A __sequenced, validated__ set of codons plus structural metadata that accomplishes a full _intentional function_ in the real world (e.g., emergency shutdown, sepsis protocol, multi-crane lift). It includes __preconditions, postconditions, exception handling, and context hooks.__
  * __Digital Genome__  
      The complete, versioned, governed library of operational genes of an organization (or federated ecosystem). It is __alive__: it evolves via Merism (variation, selection, inheritance).
  * __Context Snapshot__  
        A structured, time-bound description of the world state when a gene is evaluated or executed (sensors, topology, constraints, risk levels, etc.).
  * __Merism Artifacts__  
        Structures that capture variants, anti-genes, fitness scores, and evolution history of genes.

---
## 7.4 Logical Data Model (Abstract)

> __Note:__ Pseudo-TypeScript used for clarity. This is a logical model; physical models may differ.

### 7.4.1 Identities and Basic Types
```ts
type EntityId = string;      // e.g., "Pump-401"
type ActionId = string;      // e.g., "Stop"
type StateId = string;       // e.g., "Isolated"
type GeneId = string;        // e.g., "GEN-EMERGENCY-STOP-V3"
type GenomeId = string;      // organizational / federated identifier
type UserId = string;        // human or system agent
type Timestamp = string;     // ISO-8601
type Locale = string;        // e.g., "en-US", "pt-BR"

interface Tagged<T> {
  value: T;
  tags?: string[];
}
```
### 7.4.2 Praxeological Codon
```ts
interface PraxeologicalCodon {
  id: string;                     // Unique codon identifier (within a gene or library)
  entity: EntityId;               // Target entity
  action: ActionId;               // Intentional operation
  targetState: StateId;           // Desired resulting state

  parameters?: Record<string, unknown>; // Domain-specific args (e.g., torque, dosage)
  preConditions?: ConditionExpression[]; // Must be true before applying codon
  postConditions?: ConditionExpression[]; // Expected to be true after execution

  // Semantic hooks
  ontologyRefs?: string[];        // Links to domain ontologies / standards
  safetyLevel?: 'info' | 'warning' | 'critical';
}
```
### 7.4.3 Operational Gene
```ts
interface OperationalGene {
  id: GeneId;
  name: string;                   // Human-readable label
  description?: string;

  version: string;                // e.g., "3.1.0"
  status: 'draft' | 'active' | 'deprecated';

  // Structure
  codons: PraxeologicalCodon[];
  preConditions?: ConditionExpression[];     // For the whole gene
  postConditions?: ConditionExpression[];    // For the whole gene
  exceptionPolicies?: GeneExceptionPolicy[];

  // Context & applicability
  applicableContexts?: ContextFilter[];      // Where this gene is valid
  riskProfile?: RiskProfile;
  estimatedDuration?: number;                // ms or domain unit

  // Governance & audit
  createdBy: UserId;
  createdAt: Timestamp;
  lastModifiedBy: UserId;
  lastModifiedAt: Timestamp;

  // Evolution
  parentGenes?: GeneId[];                    // For Merism genealogy
  antiGenes?: GeneId[];                      // Competing / alternative strategies
  fitnessScores?: FitnessScore[];            // Per context / scenario
}
```
### 7.4.4 Digital Genome
```ts
interface DigitalGenome {
  id: GenomeId;
  name: string;
  ownerOrg: string;             // legal / operational owner
  description?: string;

  genes: Record<GeneId, OperationalGene>;
  entities: Record<EntityId, EntityDescriptor>;
  actions: Record<ActionId, ActionDescriptor>;
  states: Record<StateId, StateDescriptor>;

  // Ontology & semantics
  ontologyRefs?: string[];      // External ontologies, taxonomies, standards
  version: string;

  // Governance
  governancePolicyId: string;   // Link to Governance Matrix
  changeLog: GenomeChangeEvent[];

  // Federation
  federationScopes?: FederationScope[];
}
```
### 7.4.5 Context and Conditions (Simplified)
```ts
interface ContextSnapshot {
  id: string;
  capturedAt: Timestamp;
  sourceSystemIds: string[];    // SCADA, EMR, WMS, etc.
  data: Record<string, unknown>; // Abstract; domain-specific schemas downstream
}

interface ContextFilter {
  // Minimal structure: predicates over context keys
  expression: ConditionExpression;
  priority?: number;
}

interface ConditionExpression {
  // Logical expression in a safe, declarative mini-language
  // Example: "sensor.vibration < 3.0 && pump.status == 'running'"
  expr: string;
  description?: string;
}
```
### 7.4.6 Merism Artifacts (Evolution)
```ts
interface FitnessScore {
  contextSignature: string; // e.g., hash of salient context dimensions
  score: number;            // 0..1 or domain-specific
  samples: number;          // number of observations
  lastUpdated: Timestamp;
}

interface GeneExceptionPolicy {
  onCondition: ConditionExpression;  // What kind of failure / anomaly
  fallbackGeneId?: GeneId;          // Which alternative gene to use
  escalationPolicy?: EscalationPolicy;
}

interface GenomeChangeEvent {
  id: string;
  geneId: GeneId;
  changeType: 'create' | 'update' | 'deprecate' | 'merge' | 'split';
  author: UserId;
  timestamp: Timestamp;
  rationale?: string;
  diffSummary?: string;
}
```
---
## 7.5 Interaction Contracts

> This section defines, at top level, how __Cognitive Core__ and __UNL__ will interact with the Digital Genome. Detailed APIs and protocols will be specified in subsequent steps (Cognitive Core spec and UNL spec).

### 7.5.1 Cognitive Core ↔ Digital Genome

The Cognitive Core is the reasoning engine that reads, evaluates, and writes genes.

Core responsibilities of Cognitive Core regarding the Genome:

1. Read
    * Query genes applicable to a given __ContextSnapshot__.
    * Retrieve codons and constraints for simulation and planning.
2. Evaluate
    * Simulate gene execution under multiple hypothetical contexts.
    * Assign / update __FitnessScore__ based on observed outcomes.
3. Write / Evolve
    * Propose new genes (variations, anti-genes).
    * Update existing genes (parameters, sequences, policies).
    * Mark genes as deprecated / unsafe when necessary.
4. Explain
    * Provide decision traces relating a chosen action back to the genes (for audit / governance).

#### Top-Level Contract (Logical):
```ts
interface CognitiveCoreGenomePort {
  // Query candidate genes for a given context and intent
  findCandidateGenes(
    intent: HighLevelIntent,
    context: ContextSnapshot
  ): Promise<OperationalGene[]>;

  // Record outcome for Merism
  recordExecutionOutcome(
    geneId: GeneId,
    context: ContextSnapshot,
    outcome: ExecutionOutcome
  ): Promise<void>;

  // Propose gene variations (subject to Governance Matrix)
  proposeGeneVariation(
    baseGene: OperationalGene,
    variation: GeneVariationProposal
  ): Promise<GeneId>;
}
```

The __Governance Matrix__ (already outlined in the book) defines which proposals from the Core are auto-accepted, which require human review, and which are forbidden.

### 7.5.2 UNL ↔ Digital Genome

The __Universal Neutral__ Language (UNL) is the human interface layer that captures __multimodal intent__ (speech, gesture, text, context) and maps it to __praxeological codons and genes__, and back.

  ***Core responsibilities of UNL regarding the Genome:***  
  1. __Intent → Codons / Genes__
    * Interpret human input and produce a set of candidate codons or genes representing the requested action.
  2. __Codons / Genes → Explanations__  
    * Translate selected genes back into human-readable narratives, in the operator’s language and modality.
  3. __Feedback Collection__  
    * Capture operator corrections / overrides as signals for gene evolution and fitness updates.

__Top-Level Contract (Logical):__
```ts
interface UNLGenomePort {
  // Map human intent to codons / genes
  interpretIntent(
    rawInput: MultimodalInput,
    context: ContextSnapshot
  ): Promise<IntentInterpretationResult>;

  // Generate human explanation for a given gene
  explainGene(
    geneId: GeneId,
    locale: Locale
  ): Promise<HumanExplanation>;

  // Capture operator feedback after execution
  recordOperatorFeedback(
    geneId: GeneId,
    feedback: OperatorFeedback
  ): Promise<void>;
}
```
---
## 7.6 Governance and Safety Invariants

The Digital Genome must respect the **Governance Matrix** and **safety nets** defined in the broader architecture (governança evolutiva, soberania digital, etc.).

### Top-Level Invariants (informal)

1. **Semantic Coherence**  
   - Every codon must reference valid `EntityId`, `ActionId`, `StateId` present in the genome’s ontological registry.  
   - Genes with missing or inconsistent references are invalid and cannot be executed.

2. **Typed Context**  
   - Gene applicability must be explicitly constrained by `ContextFilter`.  
   - A gene cannot be executed in contexts where it is not declared valid.

3. **Governed Evolution**  
   - Any change to an active gene must:  
     - Be recorded as a `GenomeChangeEvent`.  
     - Pass through the appropriate governance policy (automatic, human review, or forbidden).

4. **Auditability**  
   - For every operational action derived from the genome, it must be possible to reconstruct:  
     - Which gene was applied.  
     - Under which context snapshot.  
     - Which decisions the Cognitive Core made.

5. **Safety Priority**  
   - In case of conflict between multiple candidate genes:  
     - Genes with higher safety level (e.g., critical safety) must have precedence, subject to governance rules.

---

## 7.7 Non-Functional Requirements (Top-Level)

1. **Scalability**  
   - Support thousands of genes and millions of codon instances across large industrial ecosystems.

2. **Federation**  
   - Allow multiple genomes (per plant / organization / sector) to interoperate via federated sharing of genes, respecting sovereignty and IP constraints.

3. **Interoperability**  
   - Provide neutral representations (e.g., JSON / Protobuf / RDF) to be consumed by existing systems (SCADA, MES, EMR, WMS, etc.) without forcing a full replacement.

4. **Resilience**  
   - Degradation mode: if the Cognitive Core is partially unavailable, the system must still be able to execute validated, safe genes using last-known fitness data.

5. **Traceability**  
   - Full trace from:  
     - Human intent → UNL interpretation → gene selection → codon execution → outcomes → evolution.

---

## 7.8 Diagram Guidelines (for the PNGs later)

For the next step (“Cognitive Core → UNL → Diagrams PNG → Publicação adicional”), here is a **minimal set of diagrams**:

1. **Diagram 7.1 – Digital Genome Layer Stack (PNG)**  
   - Layers: Sensors/Data → Context Snapshot → Digital Genome → Cognitive Core → Orchestration / Physical Action.  
   - Highlight codons, genes, and their position between raw data and physical execution.

2. **Diagram 7.2 – Operational Gene Lifecycle (PNG)**  
   - States: Draft → Active → Monitored → Evolving → Deprecated.  
   - Arrows showing Merism (variations), governance gates, and feedback loops from outcomes.

3. **Diagram 7.3 – Intent Flow (UNL ↔ Cognitive Core ↔ Genome) (PNG)**  
   - Human operator (voice/gesture) → UNL → “Intent Interpretation” → Candidate Genes → Cognitive Core selection → Execution → Explanation back to human.

4. **Diagram 7.4 – Federated Genomes (PNG)**  
   - Multiple organizations with their own genomes, sharing selected genes via a federated bus, under governance and sovereignty constraints.
