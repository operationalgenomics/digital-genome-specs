# Codon Index
### Comprehensive Index of All Codons in the Digital Genome Ecosystem

---

## 1. Purpose

The **Codon Index** provides a complete, structured catalog of every codon defined in the Digital Genome.  
Codons are the *atomic, indivisible units of praxeological action*—the smallest operational building blocks the Cognitive Core can execute or assemble into genes.

This index ensures:
- fast navigation,
- auditability,
- architectural clarity,
- consistency across all genes,
- standardized reuse across contexts.

It will expand automatically as additional codons are added to `specs/digital-genome/codons/`.

---

## 2. Codon Classification Model

Codons fall into *five canonical categories*, reflecting their functional role:

### 2.1 Action Codons
Perform a direct operational act.

### 2.2 Diagnostic Codons
Observe, measure, or analyze system or environmental states.

### 2.3 Safety Codons
Enforce safe states, mitigate hazards, or prepare secure conditions.

### 2.4 Governance Codons
Enforce policy, capture approvals, or maintain traceability.

### 2.5 Structural Codons
Define sequencing, branching, repetition, or context requirements inside genes.

---

## 3. Codon Index Table

The following is the *canonical baseline codon library* used by the Digital Genome architecture.  
As more codons are added, this table will be extended.

### **3.1 Action Codons**

| Codon ID | Name | Description |
|----------|------|-------------|
| COD-ACT-SET | Set Parameter | Sets an operational variable (flow, temp, pressure). |
| COD-ACT-INC | Increment Parameter | Increases a value by a defined delta. |
| COD-ACT-DEC | Decrement Parameter | Decreases a value by a defined delta. |
| COD-ACT-ACTUATE | Actuate Mechanism | Triggers a physical actuator or control signal. |
| COD-ACT-EXEC | Execute Routine | Performs a predefined routine or micro-action. |

---

### **3.2 Diagnostic Codons**

| Codon ID | Name | Description |
|----------|------|-------------|
| COD-DIAG-READ | Read Sensor | Reads a sensor value (temperature, vibration, etc.). |
| COD-DIAG-CHECK | Check Condition | Evaluates a boolean condition. |
| COD-DIAG-ANALYZE | Analyze Pattern | Performs a pattern or anomaly analysis. |
| COD-DIAG-VERIFY | Verify Preconditions | Confirms that an action is safe to execute. |
| COD-DIAG-COMPARE | Compare Values | Compares two or more operational values. |

---

### **3.3 Safety Codons**

| Codon ID | Name | Description |
|----------|------|-------------|
| COD-SAFE-STOP | Emergency Stop | Immediately halts unsafe operations. |
| COD-SAFE-ISOLATE | Isolate System | Separates equipment from operational load. |
| COD-SAFE-LIMIT | Enforce Limit | Enforces a hard safety boundary. |
| COD-SAFE-FALLBACK | Fallback to Safe State | Restores system to predefined safe configuration. |
| COD-SAFE-LOCK | Safety Lock | Prevents further actions until cleared. |

---

### **3.4 Governance Codons**

| Codon ID | Name | Description |
|----------|------|-------------|
| COD-GOV-LOG | Log Event | Creates a governance ledger entry. |
| COD-GOV-REQUEST | Request Approval | Requests human or governance validation. |
| COD-GOV-SIGN | Apply Signature | Applies cryptographic signature to an artifact. |
| COD-GOV-ANCHOR | Anchor to Ledger | Anchors the event to the immutable ledger. |
| COD-GOV-AUDIT | Audit Step | Enforces audit traceability requirements. |

---

### **3.5 Structural Codons**

| Codon ID | Name | Description |
|----------|------|-------------|
| COD-STR-SEQUENCE | Sequence | Defines ordered steps in a gene. |
| COD-STR-BRANCH | Branch | Creates a conditional branch. |
| COD-STR-LOOP | Loop | Repeats a codon or subroutine. |
| COD-STR-WAIT | Wait | Pauses execution until condition is met. |
| COD-STR-CONTEXT | Context Gate | Enforces context requirements before execution. |

---

## 4. Codon Metadata Fields

All codon definitions under `specs/digital-genome/codons/` follow this structure:

```ts
interface CodonMetadata {
  codonId: string;
  name: string;
  category: 'action' | 'diagnostic' | 'safety' | 'governance' | 'structural';
  description: string;
  parameters?: CodonParameter[];
  safetyImplications?: string[];
  preconditions?: string[];
  postconditions?: string[];
  exampleUsage?: string[];
  version: string;
}

interface CodonParameter {
  key: string;
  type: string;
  description: string;
  required: boolean;
}
```

This metadata schema ensures:
- consistent structure,
- predictable parsing by the Cognitive Core,
- complete traceability,
- easy validation for governance tools.

---

## 5. Codon Library Rules

### 5.1 Codons Must Be Atomic
A codon:
- cannot be subdivided,
- cannot contain multiple actions,
- cannot execute composite logic.

### 5.2 Codons Must Be Deterministic
Given the same input and context, a codon must always produce the same output.

### 5.3 Codons Must Be Explainable
Each codon must have a clear purpose and deterministic behavior.

### 5.4 Codons Must Remain Backward-Compatible
Codon behavior cannot change once deployed—only versioned extensions are permitted.

### 5.5 Codons Must Pass Safety Validation
Every codon must undergo:
- safety analysis,
- simulation validation,
- governance approval,
- version signing.

---

## 6. Adding New Codons

To add a codon:
1. Create a new file under `specs/digital-genome/codons/`
2. Follow the metadata schema
3. Place it in the correct category
4. Update this index
5. Ensure the Cognitive Core recognizes the new codon
6. Validate safety and governance rules

---

## 7. Summary

The **Codon Index** is the authoritative catalog of all atomic operational elements in the Digital Genome.  
It ensures clarity, structure, consistency, and auditability across the cognitive architecture.

This file must be updated whenever a new codon is introduced or an existing codon receives a version extension.

