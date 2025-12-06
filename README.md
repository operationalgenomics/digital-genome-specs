# Operational Genomics — Technical Specifications & Implementation

> A framework that unifies **data, AI, intention and action** into coherent, evolutive, and explainable operational knowledge systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Overview

This repository contains both the **formal technical specification** and a **working reference implementation** of Operational Genomics — a discipline that applies biological genomic principles to operational knowledge management.

The core insight is simple but profound: **operational knowledge can be structured like biological DNA**, enabling systems that are:

- **Universal**: The same grammar represents processes across any industrial sector
- **Modular**: Operational genes can be combined and recombined
- **Evolutionary**: Mechanisms analogous to natural selection improve genes over time
- **Explainable**: Every decision traces back to atomic, inspectable units

---

## The Digital Genome Architecture

The architecture mirrors biology's elegant hierarchy:

```bash
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DIGITAL GENOME                                 │
│                    (Complete operational knowledge library)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐        │
│  │  OPERATIONAL GENE │  │  OPERATIONAL GENE │  │  OPERATIONAL GENE │  ...   │
│  │  (Functional unit)│  │  (Functional unit)│  │  (Functional unit)│        │
│  ├───────────────────┤  ├───────────────────┤  ├───────────────────┤        │
│  │ [Codon] [Codon]   │  │ [Codon] [Codon]   │  │ [Codon] [Codon]   │        │
│  │ [Codon] [Codon]   │  │ [Codon]           │  │ [Codon] [Codon]   │        │
│  └───────────────────┘  └───────────────────┘  └───────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            COGNITIVE CORE                                   │
│         (Reasoning engine: context → inference → simulation → decision)     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          [ COORDINATED ACTION ]
```

### The Praxeological Codon

The **smallest unit of operational meaning**. Every codon has three components:

```ts
[ Entity | Action | Target-State ]
```

Example: `[ Pump-401 | Stop | Isolated ]`

This isn't just an event record — it captures **intentional action**: an agent performed an action with a specific purpose.

### The Operational Gene

A **sequence of codons** that together express a complete functional capability. Genes include:

- **Preconditions**: What must be true before activation
- **Codon Sequence**: The ordered steps to execute
- **Postconditions**: What should be true after success
- **Exception Handlers**: What to do when things go wrong
- **Evaluation Metrics**: How to measure execution quality

### The Digital Genome

The **complete library of an organization's operational genes**, organized into:

- **Stems**: Thematic groupings (safety, maintenance, optimization)
- **Chromosomes**: Functional groupings (core, experimental, deprecated)

The genome is **alive**: it evolves through **Merism** (variation → evaluation → selection → inheritance).

---

## Repository Structure

```bash
digital-genome-specs/
├── specs/
│   ├── foundations/                #  PHILOSOPHICAL & ARCHITECTURAL FOUNDATIONS
│   │   ├── philosophical-foundations.md   # Why the system exists; epistemology
│   │   ├── truth-architecture.md          # Foucauldian vs Platonic truth
│   │   ├── neuron-ontology.md             # DNA as neurons; the distributed brain
│   │   └── information-lifecycle.md       # Complete flow from experience to wisdom
│   │
│   ├── cognitive-core/             # THE REASONING ENGINE
│   │   ├── specification.md               # Core architecture overview
│   │   ├── parallel-motors.md             # Four motors operating simultaneously
│   │   ├── craft-performance.md           # Convergence mathematics (product, not average)
│   │   ├── meta-motor-meristic.md         # The Platonic philosopher
│   │   ├── context-evaluator.md           # Context processing
│   │   ├── inference-engine.md            # Reasoning and selection
│   │   ├── simulation-engine.md           # Worldline/multiverse testing
│   │   ├── oracle-synthesizer.md          # Final decision synthesis
│   │   ├── merism-evolution.md            # Evolutionary mechanisms
│   │   └── governance-interface.md        # Safety and compliance
│   │
│   ├── digital-genome/             # THE KNOWLEDGE ORGANISM
│   │   └── specification.md               # Genome structure and operations
│   │
│   ├── unl/                        # UNIVERSAL NEUTRAL LANGUAGE
│   │   ├── specification.md
│   │   ├── semantic-ontology.md
│   │   ├── intent-mapping.md
│   │   ├── context-model.md
│   │   ├── codification-rules.md
│   │   ├── translation-engine.md
│   │   └── diagrams.md
│   │
│   └── system/                     # OPERATIONAL SPECIFICATIONS
│       ├── architecture-diagrams.md
│       ├── execution-model.md
│       ├── monitoring-model.md
│       ├── feedback-model.md
│       ├── governance-model.md
│       ├── integration-contracts.md
│       ├── operational-scenarios.md
│       ├── reliability-model.md
│       ├── deployment-model.md
│       ├── failure-modes.md
│       └── safety-invariants.md
│
├── codons/                         # Codon specifications
│   └── praxeological-codons.md
│
├── genes/                          # Gene specifications  
│   └── operational-genes.md
│
├── src/                            # Reference implementation
│   ├── digital_genome_core.py      # Core: Codons, Genes, Genome, Ribosome
│   └── cognitive_core.py           # Intelligence: Inference, Simulation, Oracle
│
├── examples/                       # Usage examples
│   └── demo.py
│
├── schemas/                        # JSON Schema definitions
│   └── digital-genome.schema.json
│
├── diagrams/
│   ├── foundations/                # PHILOSOPHICAL FOUNDATIONS (NEW)
│   │   ├── truth-architecture.mmd      # Foucauldian vs Platonic truth systems
│   │   ├── neuron-ontology.mmd         # DNA as neurons, distributed brain
│   │   └── information-lifecycle.mmd   # Complete flow from experience to wisdom
│   ├── sensory-cortex/             # SENSORY CORTEX (NEW)
│   │   ├── sensory-cortex-architecture.mmd  # Carrier->Pattern->Structure->Semantics
│   │   └── sensory-cortex-examples.mmd      # Processing examples across time horizons
│   ├── system/
│   │   ├── architecture/           # High-level view, technology stacks, cognitive loops
│   │   ├── execution/              # Orchestration layers, gateways, execution flows
│   │   ├── monitoring/             # Telemetry pipelines, anomaly detection, observability
│   │   ├── feedback/               # Feedback models, fitness loops, trigger mechanisms
│   │   ├── reliability/            # Redundancy models, recovery strategies, degraded modes
│   │   ├── failure/                # Failure pipelines, fallback trees, exception pathways
│   │   ├── deployment/             # Rollout strategies, isolation layers, containerization
│   │   ├── scenarios/              # Operational flows and scenario mapping
│   │   └── integration/            # Integration contracts and interoperability flows
│   ├── unl/
│   │   ├── architecture/           # UNL architecture and interaction with Core components
│   │   ├── flows/                  # Intent pipelines, encoding layers, translation paths
│   │   ├── semantic/               # Ontologies, knowledge graphs, praxeological structures
│   │   ├── context/                # Context layers, fusion mechanisms, contextual binding
│   │   └── interaction/            # Operator interaction models, ambiguity-resolution loops
│   ├── cognitive-core/  
│   │   ├── architecture/           # Layered architecture and internal cognitive cycles
│   │   ├── motors/                 # PARALLEL MOTORS (NEW)
│   │   │   ├── parallel-motors-architecture.mmd  # Four motors operating simultaneously
│   │   │   ├── craft-performance-calculation.mmd # CP as product, not sum
│   │   │   ├── motor-convergence.mmd             # How motors converge to decisions
│   │   │   └── meristic-meta-motor.mmd           # The Platonic philosopher
│   │   ├── inference/              # Inference pipelines, selection mechanisms
│   │   ├── simulation/             # Worldlines, multiverse modeling, safety funnels
│   │   ├── context/                # Context evaluation, contextual bindings
│   │   ├── evolution/              # Merism pipelines, mutation strategies, topology evolution
│   │   ├── oracle/                 # Synthesis flows, decision funnels, scoring frameworks
│   │   └── governance/             # Internal governance interfaces and control surfaces
│   ├── digital-genome/    
│   │   └── structure/              # Lifecycle, runtime stacks, federated components
│   ├── security/                   # Security architecture, DataSpaces, signature protocols
│   ├── docs/                       # High-level contextual diagrams
│   └── api/                        # API topologies and interaction flows
│
├── docs/                           # Supporting documentation
│   ├── abbreviations.md
│   ├── api-index.md
│   ├── architecture-summary.md
│   ├── changelog.md
│   ├── codon-index.md
│   ├── conventions-style-guide.md
│   ├── file-index.md
│   ├── gene-index.md
│   ├── glossary.md
│   ├── how-to-read-this-spec.md
│   ├── overview.md
│   ├── release-metadata.md
│   ├── security-principles.md
│   ├── system-context.md
│   └── versioning-policy.md
│
└── README.md
```

---

## Start Here: The Foundational Documents

If you are new to Operational Genomics, read the foundational documents in this order:

1. **[Philosophical Foundations](specs/foundations/philosophical-foundations.md)** — Why the system exists; the epistemological architecture
2. **[Truth Architecture](specs/foundations/truth-architecture.md)** — The dual truth system (registered vs synthesized)
3. **[Parallel Motors](specs/cognitive-core/parallel-motors.md)** — How four cognitive perspectives evaluate simultaneously
4. **[Craft Performance](specs/cognitive-core/craft-performance.md)** — The mathematics of convergence (product, not average)
5. **[Meristic Meta-Motor](specs/cognitive-core/meta-motor-meristic.md)** — The Platonic philosopher that imagines improvements
6. **[Neuron Ontology](specs/foundations/neuron-ontology.md)** — How DNA forms the distributed brain
7. **[Information Lifecycle](specs/foundations/information-lifecycle.md)** — The complete flow from experience to wisdom

These documents contain the **soul** of the system — the philosophical and architectural principles without which the technical specifications are mere mechanics.

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/operationalgenomics/digital-genome-specs.git
cd digital-genome-specs

# No external dependencies required for core functionality
# Optional: install for full features
pip install numpy matplotlib  # For advanced analytics
```

### Basic Usage

```python
from src.digital_genome_core import (
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    ComputationalRibosome,
    SafetyLevel,
    make_uid
)

# Create a genome
genome = DigitalGenome(name="Industrial Operations")

# Register entities, actions, and states
pump_id = genome.register_entity(
    make_uid("entity", "pump", "401"),
    name="Pump 401",
    entity_type="physical"
)

stop_action = genome.register_action(
    make_uid("action", "stop"),
    name="Stop",
    category="operational"
)

isolated_state = genome.register_state(
    make_uid("state", "isolated"),
    name="Isolated",
    category="safety"
)

# Create an operational gene
shutdown_gene = OperationalGene.create(
    name="Emergency Shutdown",
    purpose="Safely stop equipment in emergency",
    executor="safety_system",
    action="emergency_stop",
    target="pump_401"
)

# Add codons (atomic action steps)
shutdown_gene.add_codon(PraxeologicalCodon(
    entity_id=pump_id,
    action_id=stop_action,
    target_state_id=isolated_state,
    safety_level=SafetyLevel.CRITICAL,
    preconditions=("equipment_running",),
    postconditions=("equipment_isolated",)
))

# Activate and insert into genome
shutdown_gene.activate()
genome.insert_gene(shutdown_gene, stem="safety", chromosome="critical")

# Translate and execute
ribosome = ComputationalRibosome(genome)
plan = ribosome.translate_gene(shutdown_gene.uid)
result = ribosome.execute_plan(plan, dry_run=True)

print(f"Execution: {result['overall_status'].value}")
```

### Using the Cognitive Core

```python
from src.cognitive_core import CognitiveSystem

# Initialize with genome
system = CognitiveSystem(genome)

# Process high-level objective
result = system.process_objective(
    objective="Execute emergency shutdown procedure",
    context_data={"temperature": 95, "vibration": 8.5},
    dry_run=True
)

if result["decision"]["success"]:
    print(f"Selected: {result['decision']['selected_gene']['name']}")
    print(f"Confidence: {result['decision']['explanation']['inference']['scores']['composite']:.2f}")
```

---

## Core Concepts

### Praxeological Foundation

The term **praxeological** comes from praxeology — the study of human action. Every codon represents not just a physical transformation, but an **intentional action** performed by an agent with purpose.

This distinction is crucial: the system captures **intent**, not just occurrence.

### Merism: Evolutionary Cognition

Merism is the evolutionary mechanism that allows the genome to improve over time:

1. **Variation**: Generate modified versions of existing genes
2. **Evaluation**: Test variants through simulation
3. **Selection**: Choose variants that outperform originals
4. **Inheritance**: Incorporate successful variants into the genome

This creates a system that **learns from experience** without requiring explicit reprogramming.

### The Cognitive Core

The reasoning engine that turns knowledge into action:

- **Context Evaluator**: Transforms raw data into structured, validated context
- **Inference Engine**: Matches intent + context to optimal genes
- **Simulation Engine**: Validates decisions across multiple scenarios (worldlines)
- **Oracle Synthesizer**: Produces final, safe, explainable decisions
- **Governance Interface**: Ensures compliance with safety and policy constraints

---

## Validation Results

The framework has been validated through extensive testing:

| Metric | Result | Target |
|--------|--------|--------|
| Autopoiesis Score | 0.847 | > 0.7 |
| Cognitive Emergence | 0.761 | > 0.7 |
| Success Rate (50 scenarios) | 84.2% | > 80% |
| Average Processing Time | 3.7s | < 5s |
| Scalability Degradation | 24% | < 30% |

Emergent behaviors detected during validation:

- **Predictive Self-Diagnosis**: System detected performance degradation before failure
- **Cross-Domain Synthesis**: Spontaneous recombination of genes from different domains
- **Adaptive Resilience**: Creation of "survival modes" under extreme stress

---

## Applications

Operational Genomics is designed for complex industrial environments:

- **Manufacturing**: Process optimization, quality control, predictive maintenance
- **Healthcare**: Clinical protocols, patient flow, resource allocation
- **Energy**: Grid management, predictive maintenance, safety systems
- **Logistics**: Supply chain orchestration, fleet management, warehouse operations
- **Construction**: BIM integration, safety compliance, resource coordination

---

## Related Resources

### Publications

- **Book (EN)**: [The Digital Genome](https://a.co/d/ciFwzqM) — Amazon
- **Book (PT-BR)**: [Fundamentos da Genômica Operacional](https://a.co/d/a4PRANJ) — Amazon

### White Papers

- [White Papers Repository](https://github.com/operationalgenomics/whitepapers)

---

## Contributing

Contributions are welcome. Please read the specification documents before proposing changes to ensure alignment with the theoretical foundations.

Areas where contributions are especially valuable:

- Additional domain-specific gene libraries
- Performance optimizations
- Visualization tools
- Integration adapters for industrial systems

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Carlos Eduardo Favini**

Creator of Operational Genomics and author of *The Digital Genome*.

---

*"You cannot integrate what you do not understand. The Digital Genome provides the grammar that makes understanding — and therefore true integration — possible."*
