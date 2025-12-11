# Conventions & Style Guide
### Standards for Structure, Writing, Formatting, Naming, Versioning, and Documentation Across the Entire Digital Genome Ecosystem

---

## 1. Purpose

The **Conventions & Style Guide** establishes the rules and standards governing **how specifications are written**, **how files are structured**, **how naming works**, and **how documentation must remain consistent** across all layers of the Digital Genome Ecosystem.

This ensures:
- structural uniformity,
- readability,
- long-term maintainability,
- predictable formatting,
- consistent terminology,
- and smooth onboarding for contributors.

This document **must be followed for all future contributions** to maintain the integrity of the specification.

---

## 2. Language and Formatting Conventions

### 2.1 Language
- All documents must be written in **English (en-US)**.
- Avoid regionalisms, slang, or ambiguous expressions.
- Use precise, technical terminology.

### 2.2 Sentence and Paragraph Style
- Prefer short, direct sentences.
- One concept per paragraph.
- No rhetorical language in specification files.

### 2.3 Markdown Formatting Rules
- Headers follow the hierarchy `H1 → H2 → H3 → H4`.
- No skipping header levels.
- Code blocks use triple backticks.
- Lists use `-` for unordered and numbers for ordered.

### 2.4 File Encoding
- UTF-8 without BOM.
- Use Unix-style line endings (LF).

---

## 3. Naming Conventions

### 3.1 File Naming
All filenames:
- use **kebab-case**,
- use **lowercase-only**,
- must reflect the content,
- must match references in documentation.

Examples:
```bash
execution-model.md
context-model.md
oracle-synthesizer.md
system-context.md
```

### 3.2 Folder Naming
Folders follow:
```bash
specs/
docs/
```
No uppercase, no spaces.

### 3.3 Identifier Naming in Code Blocks
- Interfaces: **PascalCase**  
- Fields: **camelCase**  
- Enum-like strings: **lowercase-with-hyphens**

Example:
```ts
interface ExecutionPlan {
  stepId: string;
  action: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
}
```

---

## 4. Structural Conventions for Specification Files

Every `.md` file under `specs/` must follow the structure below.

### 4.1 Mandatory Header
```ts
# <Title>
### <Short Description>
```

### 4.2 Mandatory Sections
Each spec file must include:
1. **Purpose** — why the subsystem exists
2. **Design Principles** — the philosophy behind it
3. **Architecture / Components** — internal structure
4. **Data Structures or Typings** — TypeScript-style interfaces
5. **Flows or Algorithms** — how it operates
6. **Diagrams (PNG-ready)** — list of diagram filenames
7. **Summary** — recap of the subsystem purpose

### 4.3 Allowed Optional Sections
- Notes
- Examples
- Edge cases
- Additional constraints

### 4.4 Forbidden Elements
- Inline images
- Unreferenced tables
- Non-technical narrative language
- Speculative design (must be grounded in architecture)

---

## 5. Documentation Conventions

### 5.1 Document Types
There are two categories:
- **Specification Documents** (`specs/`) — formal, binding architecture
- **Documentation Files** (`docs/`) — contextual, explanatory, and navigational

### 5.2 Documentation File Structure
Each file in `docs/` must contain:
1. clear title,
2. purpose section,
3. structured headings,
4. summary.

### 5.3 Cross-Referencing Rules
- Use relative references (e.g., `specs/unl/specification.md`).
- Do not embed URLs in technical specs.
- Always reference diagram filenames without links.

---

## 6. Versioning Rules

### 6.1 Semantic Versioning
The Digital Genome Spec follows:
```ts
MAJOR.MINOR.PATCH
```

- **MAJOR** — breaking changes to architecture
- **MINOR** — backward-compatible improvements
- **PATCH** — fixes or clarifications

### 6.2 Genome Versioning
Genome versions are tracked separately from spec versions:
```ts
GENOME-v<major>.<minor>
```

### 6.3 Change Tracking
Every change must include:
- rationale,
- timestamp,
- author signature.

Changes are logged in `docs/changelog.md`.

---

## 7. Safety and Governance in Documentation

### 7.1 No Ambiguous Language
Safety requires precision — avoid vague expressions.

### 7.2 Explicit Risk and Constraint References
Where relevant, reference:
- safety invariants,
- governance policies,
- forbidden transitions.

### 7.3 Explanation Requirements
Every cognitive or execution reference must be explainable.

---

## 8. Visual Diagram Conventions

### 8.1 Diagram Filenames
Use the format:
```ts
<system>-<concept>.png
```
Example:
```ts
system-deployment-architecture.png
unl-context-flow.png
```

### 8.2 No Embedded Images
Specifications contain **references only**, not inline diagrams.

### 8.3 Diagram Indexing
Every reference should list diagrams at the end of a file under:
```
## Diagram Guidelines
```

---

## 9. Quality Standards

### 9.1 Clarity
Documents must be easy to read.

### 9.2 Consistency
No contradictory definitions or overlapping concepts.

### 9.3 Completeness
Every subsystem must be fully specified.

### 9.4 Non-Redundancy
No duplicated content across files.

### 9.5 Traceability
All architectural decisions should be traceable through:
- design principles,
- diagrams,
- flows,
- explanations.

---

## 10. Summary

This **Conventions & Style Guide** ensures that all contributors to the Digital Genome Ecosystem maintain a consistent writing style, formatting standard, naming approach, and documentation structure.

It guarantees that the entire specification remains:
- readable,
- coherent,
- standardized,
- maintainable.
  
These conventions must be applied to every file in the project — past, present, and future.

