# Praxeological Codons — Technical Specification (v1.0)

## 1. Definition
A Praxeological Codon (PC) is the atomic, indivisible unit of purposeful operational knowledge.

It encodes intention → conditions → instructions → exceptions as a minimal executable semantic block.
A codon is:
* composable
* inheritable
* context-aware
* deterministic under identical conditions
* explainable (fully inspectable state)

It is not a function, a rule, or a command; it is a semantic action genelet.

## 2. Codon Structure (canonical form)
Every codon must follow this canonical structure:

```yaml
Codon:
  id: <UUID or semantic label>
  intent: <description of the purposeful action>
  preconditions:
    - <list of required operational truths>
  instructions:
    - <ordered steps executed in sequence>
  exception_handling:
    - <fallback, safety, or alternative paths>
  metadata:
    context_tags: [<tags>]
    version: <semantic version>
    author: <person or system>
```

## 3. Required Fields
### 3.1 intent
A single declarative sentence describing why the codon exists. Examples:
* “Stabilize pump vibration before escalation.”
* “Ensure safe depressurization in emergency mode.”

### 3.2 preconditions
All truths that must hold before execution. Types of preconditions:
* Physical
* Logical
* Temporal
* Safety
* Risk or severity thresholds

### 3.3 instructions
Ordered steps that define the operational behavior. All steps must be:
* deterministic
* observable
* explainable

### 3.4 exception_handling
If-any-then rules for robustness. Types:
* retry
* fallback
* shutdown
* escalation
* human request

## 4. Metadata Requirements
Metadata enhances explainability and traceability.

Fields:
* context_tags: keywords (safety, shutdown, routine, calibration)
* version: explicit semantic versioning (ex: “1.2.3”)
* author: human or system entity
* timestamp (optional): recording of creation

## 5. Constraints and Validation Rules
A valid codon must:
* Contain all required fields
* Have one and only one intent
* Have deterministic instructions
* Contain no ambiguous natural language
* Be mappable to an Operational Gene
* Be auditable (state must be explainable after execution)

## 6. Codon Example (Emergency Shutdown)
```yaml
Codon:
  id: "emergency_shutdown_codon_v1"
  intent: "Safely transition equipment to shutdown mode in case of high vibration."
  preconditions:
    - "vibration_level > threshold_shutdown"
    - "operator_notified = true"
  instructions:
    - "reduce_load gradually"
    - "activate cooling system"
    - "engage mechanical brake"
  exception_handling:
    - "if cooling_failure → initiate secondary valve release"
    - "if brake_failure → send_alert('manual intervention required')"
  metadata:
    context_tags: ["safety", "shutdown", "emergency"]
    version: "1.0.0"
    author: "C.E. Favini"
```

## 7. Codon Composition
Codons do not branch. Genes branch. Codons must remain atomic.
Composition rules:
* A gene can contain 2 to 200 codons
* A codon cannot contain other codons
* Codons may inherit previous versions

## 8. Codon Inheritance (Merism-compatible)
Codons may evolve through:
* Variation
* Evaluation
* Selection
* Inheritance
* Inherited codons must maintain:
* the same intent
* backward compatibility
* preserved safety constraints

## 9. Purpose of Codons in the Digital Genome
Codons serve as:
* minimal units for simulation
* explainability atoms
* building blocks for cognitive action
* stable semantic anchors
* interoperable operational language
---
They form the lowest layer of the Digital Genome.
