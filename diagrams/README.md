# Diagrams

Visual diagrams for the Operational Genomics specification. All diagrams are in Mermaid format (`.mmd`) for version control and can be rendered to SVG/PNG.

---

## Directory Structure

### `/foundations/` — Philosophical Foundations
Core epistemological and ontological concepts that underpin the entire system.

| Diagram | Description |
|---------|-------------|
| `truth-architecture.mmd` | The dual truth system: Registered Truth (Foucauldian, blockchain) vs Synthesized Truth (Platonic, DNA) |
| `neuron-ontology.mmd` | DNA blocks as neurons in a distributed brain; knowledge IS the brain, not stored in it |
| `information-lifecycle.mmd` | Complete journey: Experience → Registration → Motors → Synthesis → Integration → Expression |

### `/sensory-cortex/` — The Boundary Between World and Mind
How the system processes signals regardless of format, including formats that do not yet exist.

| Diagram | Description |
|---------|-------------|
| `sensory-cortex-architecture.mmd` | The abstraction hierarchy: Carrier → Pattern → Structure → Proto-Agency → Semantics |
| `sensory-cortex-examples.mmd` | Concrete examples: technical drawings (today), gestures (tomorrow), unknown signals (future) |

### `/cognitive-core/motors/` — The Four Parallel Motors
The heart of the cognitive architecture: four perspectives evaluating simultaneously.

| Diagram | Description |
|---------|-------------|
| `parallel-motors-architecture.mmd` | Praxeological, Nash, Chaotic, and Meristic motors operating in parallel |
| `craft-performance-calculation.mmd` | CP as PRODUCT (not sum): any zero = total zero (veto property) |
| `motor-convergence.mmd` | How motor convergence/divergence informs decisions |
| `meristic-meta-motor.mmd` | The Platonic philosopher: fractal patterns, cross-domain analogy, hypothesis generation |

### `/cognitive-core/architecture/` — Cognitive Core Structure
Layered architecture and decision cycles.

### `/cognitive-core/inference/` — Inference Pipeline
Gene selection through parallel motor evaluation.

### `/cognitive-core/simulation/` — Simulation Engine
Worldline, multiverse, and meta-multiverse testing.

### `/cognitive-core/evolution/` — Merism Evolution
Variation, selection, and integration mechanisms.

### `/cognitive-core/oracle/` — Oracle Synthesizer
Final decision synthesis and explanation generation.

### `/cognitive-core/governance/` — Governance Interface
Safety invariants and policy enforcement.

### `/system/` — System Operations
Architecture, execution, monitoring, feedback, reliability, failure handling, deployment, scenarios, integration.

### `/unl/` — Universal Neutral Language
Architecture, flows, semantics, context, interaction.

### `/digital-genome/` — Digital Genome Structure
Lifecycle and federated components.

### `/security/` — Security Architecture
DataSpaces, isolation, signature protocols.

### `/api/` — API Topology
Gateway flows and monitoring.

### `/docs/` — Documentation Context
C4 model diagrams for documentation structure.

---

## Key Conceptual Diagrams

For understanding the **soul** of the system, read these diagrams in order:

1. **`foundations/truth-architecture.mmd`** — The epistemological foundation
2. **`sensory-cortex/sensory-cortex-architecture.mmd`** — How the system perceives
3. **`cognitive-core/motors/parallel-motors-architecture.mmd`** — How the system thinks
4. **`cognitive-core/motors/craft-performance-calculation.mmd`** — How quality is measured
5. **`cognitive-core/motors/meristic-meta-motor.mmd`** — How the system imagines
6. **`foundations/neuron-ontology.mmd`** — How knowledge becomes structure
7. **`foundations/information-lifecycle.mmd`** — The complete cognitive loop

---

## Rendering

To render Mermaid diagrams to SVG:

```bash
# Using Mermaid CLI
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg

# Batch render all diagrams
find . -name "*.mmd" -exec sh -c 'npx @mermaid-js/mermaid-cli -i "$1" -o "${1%.mmd}.svg"' _ {} \;
```

---

## Conventions

- All text in **English (en-US)**
- Diagram type declared in first line (e.g., `graph TD`, `flowchart LR`)
- Header block with source file, repository path, and description
- Consistent color coding across related diagrams
- Annotations for critical concepts
