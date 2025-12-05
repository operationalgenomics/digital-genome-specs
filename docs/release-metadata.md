# Release Metadata
### Authorship, Signatures, Version Bindings, Governance Approvals, and Cryptographic Anchoring for All Digital Genome Releases

---

## 1. Purpose

This **Release Metadata** file is the authoritative source of truth for:
- authorship information,
- governance approval chains,
- version bindings between subsystems,
- compatibility matrices,
- release-level cryptographic hashes,
- ledger anchoring records,
- human-readable release notes.

It complements the **Changelog** by describing properties of each *official release* of the Digital Genome Specification.

Every formal release **must** update this file.

---

## 2. Release Identification Schema

Each release is uniquely identified by:

```text
RELEASE-ID = SPEC-VERSION + GENOME-VERSION + CORE-VERSION + DEPLOYMENT-VERSION
```

Example:

```text
RELEASE-ID: SPEC-1.4.0 / GENOME-v1.7 / CORE-v1.5.4 / DEPLOY-v1.5.4
```

All four version domains must be explicitly declared.

---

## 3. Version Domains and Bindings

The Digital Genome Ecosystem consists of four coordinated version domains:

1. **SPEC** — documentation and architecture specification
2. **GENOME** — Digital Genome (genes, codons, ontologies)
3. **CORE** — Cognitive Core (reasoning, simulation, oracle)
4. **DEPLOY** — runtime deployment (containers, packages, orchestration)

### 3.1 Compatibility Matrix

| Component      | Version         | Compatibility Rule                             |
|----------------|-----------------|-----------------------------------------------|
| Specification  | SPEC-x.y.z      | GENOME major must match SPEC major            |
| Digital Genome | GENOME-a.b      | CORE major ≥ a and DEPLOY major ≥ a           |
| Cognitive Core | CORE-c.d.e      | Supports all GENOME versions with major ≤ c   |
| Deployment     | DEPLOY-f.g.h    | Built for CORE-f.g.h and compatible genomes   |

If these rules are violated, a release **cannot** be certified.

---

## 4. Release Metadata Structure

Every release is described by the following structure:

```ts
interface ReleaseMetadata {
  releaseId: string;
  specVersion: string;
  genomeVersion: string;
  coreVersion: string;
  deploymentVersion: string;

  releaseDate: string; // ISO 8601
  authors: string[];
  reviewers: string[];
  governanceSignatures: string[];

  compatibility: CompatibilityMatrix;
  hash: string;        // SHA-256 or stronger
  ledgerAnchor: string; // external anchor reference

  releaseNotes: string[];
}

interface CompatibilityMatrix {
  specToGenome: string;
  genomeToCore: string;
  coreToDeployment: string;
}
```

This is a **logical model**, not an enforced runtime schema.

---

## 5. Signature & Approval Requirements

Every release requires **three classes of signatures**:

1. **Authors** — certify correctness and intent.
2. **Reviewers** — certify clarity, completeness, and architectural coherence.
3. **Governance** — certify safety, compliance, and authorization for deployment.

A release is **invalid** without governance signatures.

---

## 6. Ledger Anchoring Requirements

Each release must be anchored to the immutable governance ledger, including:
- release metadata hash,
- all version identifiers,
- signature lineage,
- timestamp,
- anchor reference.

Anchor IDs follow:

```text
ANCHOR-<YYYYMMDD>-<unique-fragment>
```

---

## 7. Release Notes Guidelines

Release notes must:
- be concise but meaningful,
- explain why the change matters,
- describe impact on cognition, safety, or operation,
- reference key spec or subsystem changes.

Example entries:

- "Added multi-tenant DataSpaces enforcement in security model."
- "Expanded simulation engine to support multi-phase contextual evaluation."

---

# 8. Official Release Records

Below are example records for the initial evolution of the Digital Genome Specification.  
Additional releases must be appended chronologically.

---

## Release 1 — Digital Genome Specification **v1.0.0**

```json
{
  "releaseId": "SPEC-1.0.0 / GENOME-v1.0 / CORE-v1.0.0 / DEPLOY-v1.0.0",
  "specVersion": "1.0.0",
  "genomeVersion": "v1.0",
  "coreVersion": "v1.0.0",
  "deploymentVersion": "v1.0.0",

  "releaseDate": "2025-01-01",
  "authors": ["C.E.F.", "Architectural AI Assistant"],
  "reviewers": ["<reviewer-signature>"],
  "governanceSignatures": ["<governance-signature>"],

  "compatibility": {
    "specToGenome": "GENOME major = SPEC major",
    "genomeToCore": "CORE major ≥ GENOME major",
    "coreToDeployment": "DEPLOY matches CORE"
  },

  "hash": "<pending>",
  "ledgerAnchor": "ANCHOR-20250101-<pending>",

  "releaseNotes": [
    "Initialized core directories and architectural baseline.",
    "Defined Digital Genome structure, Cognitive Core specification, and UNL foundations.",
    "Established initial System Layer architecture (execution, monitoring, governance)."
  ]
}
```

---

## Release 2 — Digital Genome Specification **v1.1.0**

```json
{
  "releaseId": "SPEC-1.1.0 / GENOME-v1.3 / CORE-v1.2.0 / DEPLOY-v1.2.0",
  "specVersion": "1.1.0",
  "genomeVersion": "v1.3",
  "coreVersion": "v1.2.0",
  "deploymentVersion": "v1.2.0",

  "releaseDate": "2025-01-07",
  "authors": ["C.E.F."],
  "reviewers": ["<reviewer-signature>"],
  "governanceSignatures": ["<governance-signature>"],

  "compatibility": {
    "specToGenome": "GENOME minor extended but compatible with SPEC-1.x",
    "genomeToCore": "CORE supports new genome constraints and metadata fields",
    "coreToDeployment": "DEPLOY artifacts aligned with CORE-v1.2.0"
  },

  "hash": "<pending>",
  "ledgerAnchor": "ANCHOR-20250107-<pending>",

  "releaseNotes": [
    "Added Conventions & Style Guide for all specification files.",
    "Expanded documentation structure and navigation aids.",
    "Refined versioning policy and cross-layer index documents."
  ]
}
```

---

## Release 3 — Digital Genome Specification **v1.2.0**

```json
{
  "releaseId": "SPEC-1.2.0 / GENOME-v1.4 / CORE-v1.3.0 / DEPLOY-v1.3.0",
  "specVersion": "1.2.0",
  "genomeVersion": "v1.4",
  "coreVersion": "v1.3.0",
  "deploymentVersion": "v1.3.0",

  "releaseDate": "2025-01-10",
  "authors": ["C.E.F."],
  "reviewers": ["<reviewer-signature>"],
  "governanceSignatures": ["<governance-signature>"],

  "compatibility": {
    "specToGenome": "GENOME updated to include security-aware praxeological extensions.",
    "genomeToCore": "CORE-v1.3.0 includes security hooks and DataSpaces awareness.",
    "coreToDeployment": "DEPLOY-v1.3.0 introduces hardened containers and segmented runtime zones."
  },

  "hash": "<pending>",
  "ledgerAnchor": "ANCHOR-20250110-<pending>",

  "releaseNotes": [
    "Expanded Security Principles with RBAC + ABAC, DataSpaces, and ledger anchoring.",
    "Aligned Cognitive Core and System Layer with new security requirements.",
    "Prepared architecture for multi-tenant, governance-enforced deployments."
  ]
}
```

---

## 9. Future Releases

Future releases must:
- append new JSON blocks following the patterns above,
- respect the version and compatibility rules,
- include full signature and governance metadata,
- ensure ledger anchors are resolvable.

---

## 10. Summary

This **Release Metadata** file links the Digital Genome Specification to concrete, governance-approved releases.  
It encodes authorship, signatures, version bindings, compatibility rules, and ledger anchors, ensuring every release is:
- traceable,
- auditable,
- cryptographically verifiable,
- safe to deploy in mission-critical environments.

