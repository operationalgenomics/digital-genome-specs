# Operational Genes — Technical Specification (v1.0)

## 1. Definition

An Operational Gene (__OG__) is a structured, coherent sequence of __Praxeological Codons__ that expresses a functional operational capability.

If codons are intention-atoms, then operational genes are action-proteins.

A gene defines:

* purpose-aligned behavior
* conditions for activation
* internal orchestration
* evaluation outputs
* inheritance rules
* safety guarantees

Genes are the fundamental units of operational meaning in the Digital Genome.
---
## 2. Gene Structure (canonical form)
   ```yaml
OperationalGene:
  id: <UUID or semantic label>
  purpose: <functional capability>
  activation_conditions:
    - <list of activation truths>
  codon_sequence:
    - <ordered list of codon IDs>
  branching_logic:
    - <conditional path selection>
  postconditions:
    - <expected truths after execution>
  exception_model:
    - <error propagation, recovery, escalation>
  evaluation_metrics:
    - <KPIs, performance, risk, stability indicators>
  metadata:
    context_tags: [<tags>]
    version: <semantic version>
    author: <entity>
   ```
---
## 3. Required Fields
### 3.1 purpose

A declarative description of what this gene accomplishes.

Examples:
* “Execute a safe emergency shutdown sequence.”
* “Stabilize pressure under abnormal load.”
* “Adjust pump flow to maintain optimal efficiency.”

### 3.2 activation_conditions

Conditions required for a gene to become active.

Types:
* Environmental
* Logical
* Temporal
* Severity or risk thresholds
* System state variables

### 3.3 codon_sequence

The ordered list of Praxeological Codons.

Constraints:
* Minimum: 2 codons
* Maximum: no fixed limit, but genes above 200 codons require special metadata
* Must be linear at the base, with optional branching logic

### 3.4 branching_logic

Genes support conditional branches, unlike codons.

Branching types:

* If / Else
* Threshold selection
* Risk-based branching
* Contextual mode switching

Example:
```lua
if vibration_level > threshold_critical:
    execute codon 'cooling_protocol'
else:
    execute codon 'load_reduction'
 ```
### 3.5 postconditions

Expected truths after execution.

They allow:
* validation
* auditing
* simulation
* introspection

### 3.6 exception_model

Defines how the gene reacts to failures:
* fallback genes
* alternative codon paths
* operator escalation
* safe-mode or shutdown mode

###  3.7 evaluation_metrics

Used by the Cognitive Core to:
* simulate
* select genes
* estimate outcomes
* evolve through Merism

Examples:
* energy efficiency
* variance stability
* failure probability
* response time
* operational coherence

---
## 4. Inheritance Model (Merism-Compatible)

Genes evolve through:
1. __Variation__ (structural change)
2. __Evaluation__ (testing outcomes)
3. __Selection__ (winning variant chosen)
4. __Inheritance__ (new version becomes canonical)

A child gene must preserve:
* the same purpose
* the same semantic identity
* upward compatibility
* safety invariants

---
## 5. Gene Validity Constraints

A valid Operational Gene must:

1. Contain at least 2 codons
2. Preserve semantic unity (single purpose)
3. Have at most 3 levels of branching
4. Not modify intent at the codon level
5. Expose clear pre/postconditions
6. Be audit-ready (black-box to white-box transparency)
7. Be selectable by the Cognitive Core
8. Be simulatable

---
## 6. Example — Emergency Shutdown Gene
```bash
OperationalGene:
  id: "og_emergency_shutdown_v1"
  purpose: "Execute a coordinated emergency shutdown in response to high vibration."
  activation_conditions:
    - "vibration_level > threshold_shutdown"
    - "operator_ack = true"
  codon_sequence:
    - "reduce_load_codon"
    - "activate_cooling_codon"
    - "engage_brake_codon"
  branching_logic:
    - "if cooling_failure → execute 'secondary_release_codon'"
  postconditions:
    - "equipment_status = 'shutdown'"
    - "temperature < safe_threshold"
  exception_model:
    - "if brake_failure → escalate 'manual_intervention_required'"
  evaluation_metrics:
    - "shutdown_safety_score"
    - "reaction_time"
    - "system_stability"
  metadata:
    context_tags: ["safety", "shutdown"]
    version: "1.0.0"
    author: "C.E. Favini"
```

---
## 7. Role of Genes in the Digital Genome

Genes define:
* macro-operational behavior
* safety-critical logic
* functional orchestration
* simulation units
* audit-ready operational knowledge
---
They are the middle layer between:
* 👉 atomic codons
* 👉 full Digital Genome structures
