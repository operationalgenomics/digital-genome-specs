#!/usr/bin/env python3
"""
Operational Genomics - Complete System Demonstration
====================================================
This script demonstrates the full capabilities of the Digital Genome
framework, from atomic codons to intelligent cognitive decisions.

Run: python demo.py

Author: Carlos Eduardo Favini
License: MIT
"""

import sys
import json
import time
from typing import Dict, Any

# Import core components
from digital_genome_core import (
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    ComputationalRibosome,
    SafetyLevel,
    GeneStatus,
    make_uid,
    create_example_genome
)

from cognitive_core import (
    CognitiveSystem,
    HighLevelIntent,
    ContextSnapshot
)


def print_header(title: str):
    """Prints a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_subheader(title: str):
    """Prints a formatted subsection header"""
    print(f"\n  ▸ {title}")
    print(f"  {'-'*60}")


def demonstrate_codons():
    """Demonstrates Praxeological Codons - the atomic units"""
    print_header("PART 1: PRAXEOLOGICAL CODONS")
    
    print("""
  Codons are the atomic, indivisible units of operational meaning.
  Each codon captures: Entity → Action → Target State
  
  This mirrors biological codons that encode amino acids, but here
  we encode units of intentional action.
    """)
    
    # Create example codons
    codon1 = PraxeologicalCodon(
        entity_id="pump-401",
        action_id="stop",
        target_state_id="isolated",
        safety_level=SafetyLevel.CRITICAL,
        preconditions=("pump_running", "operator_authorized"),
        postconditions=("pump_stopped", "flow_halted"),
        parameters={"timeout_seconds": 30}
    )
    
    codon2 = PraxeologicalCodon(
        entity_id="valve-302",
        action_id="close",
        target_state_id="sealed",
        safety_level=SafetyLevel.WARNING,
        preconditions=("valve_open",),
        postconditions=("valve_closed", "path_blocked")
    )
    
    print_subheader("Example Codons Created")
    print(f"    Codon 1: {codon1}")
    print(f"             UID: {codon1.uid[:32]}...")
    print(f"             Safety: {codon1.safety_level.value}")
    print(f"             Preconditions: {codon1.preconditions}")
    
    print(f"\n    Codon 2: {codon2}")
    print(f"             UID: {codon2.uid[:32]}...")
    print(f"             Safety: {codon2.safety_level.value}")
    
    print_subheader("Serialization")
    print("    Codons serialize to JSON for persistence and transmission:")
    print(f"    {json.dumps(codon1.to_dict(), indent=2)[:200]}...")
    
    return [codon1, codon2]


def demonstrate_genes(codons):
    """Demonstrates Operational Genes - functional units"""
    print_header("PART 2: OPERATIONAL GENES")
    
    print("""
  Genes are sequences of codons that together express a complete
  functional capability. They include activation conditions,
  exception handlers, and evaluation metrics.
    """)
    
    # Create a gene
    gene = OperationalGene.create(
        name="Emergency Isolation Sequence",
        purpose="Safely isolate equipment section in emergency conditions",
        executor="safety_controller",
        action="emergency_isolate",
        target="section_alpha",
        domain="safety",
        priority="critical"
    )
    
    # Add codons
    for codon in codons:
        gene.add_codon(codon)
    
    # Configure gene
    gene.activation_conditions = [
        "emergency_signal_received",
        "section_pressure > critical_threshold",
        "operator_authorization = valid"
    ]
    gene.postconditions = [
        "section_isolated",
        "all_equipment_stopped",
        "incident_logged"
    ]
    gene.exception_handlers = {
        "valve_stuck": "escalate_to_manual",
        "communication_timeout": "activate_local_shutdown",
        "sensor_failure": "assume_worst_case"
    }
    gene.evaluation_metrics = [
        "isolation_time_ms",
        "equipment_integrity_score",
        "compliance_index"
    ]
    
    # Activate
    gene.activate()
    
    print_subheader("Gene Created")
    print(f"    Name: {gene.name}")
    print(f"    Purpose: {gene.purpose}")
    print(f"    UID: {gene.uid[:32]}...")
    print(f"    Version: {gene.version}")
    print(f"    Status: {gene.status.value}")
    print(f"    Codons: {len(gene.codons)}")
    print(f"    Safety Level: {gene.safety_level.value}")
    
    print_subheader("Gene Structure")
    print(f"    Activation Conditions:")
    for cond in gene.activation_conditions:
        print(f"      • {cond}")
    print(f"    Exception Handlers:")
    for exc, handler in gene.exception_handlers.items():
        print(f"      • {exc} → {handler}")
    
    return gene


def demonstrate_genome(gene):
    """Demonstrates the Digital Genome - the knowledge repository"""
    print_header("PART 3: DIGITAL GENOME")
    
    print("""
  The Digital Genome is the complete library of operational genes,
  organized into thematic stems and functional chromosomes.
  It's a living structure that evolves through Merism.
    """)
    
    # Create genome
    genome = DigitalGenome(name="Industrial Operations Genome")
    
    # Register ontology
    genome.register_entity(make_uid("entity", "pump", "401"), "Pump 401", "physical", location="Section A")
    genome.register_entity(make_uid("entity", "valve", "302"), "Valve 302", "physical", location="Section A")
    genome.register_entity(make_uid("entity", "sensor", "101"), "Temperature Sensor 101", "sensor", type="temperature")
    
    genome.register_action(make_uid("action", "stop"), "Stop", "operational")
    genome.register_action(make_uid("action", "close"), "Close", "operational")
    genome.register_action(make_uid("action", "inspect"), "Inspect", "diagnostic")
    
    genome.register_state(make_uid("state", "isolated"), "Isolated", "safety")
    genome.register_state(make_uid("state", "running"), "Running", "operational")
    genome.register_state(make_uid("state", "stopped"), "Stopped", "operational")
    
    # Insert the gene
    genome.insert_gene(gene, stem="safety", chromosome="critical_operations")
    
    # Create additional genes
    inspection_gene = OperationalGene.create(
        name="Routine Inspection Protocol",
        purpose="Perform scheduled equipment inspection",
        executor="maintenance_system",
        action="inspect",
        target="all_equipment"
    )
    inspection_gene.add_codon(PraxeologicalCodon(
        entity_id=make_uid("entity", "pump", "401"),
        action_id=make_uid("action", "inspect"),
        target_state_id=make_uid("state", "running"),
        safety_level=SafetyLevel.INFO
    ))
    inspection_gene.activate()
    genome.insert_gene(inspection_gene, stem="maintenance", chromosome="routine_operations")
    
    print_subheader("Genome Statistics")
    stats = genome.get_statistics()
    for key, value in stats.items():
        if key not in ["created_at", "modified_at", "genome_id"]:
            print(f"    • {key.replace('_', ' ').title()}: {value}")
    
    print_subheader("Ontology Registry")
    print(f"    Entities: {len(genome.entity_registry)}")
    for eid, info in list(genome.entity_registry.items())[:3]:
        print(f"      • {info['name']} ({info['type']})")
    print(f"    Actions: {len(genome.action_registry)}")
    print(f"    States: {len(genome.state_registry)}")
    
    print_subheader("Search Capabilities")
    results = genome.find_genes_by_context("emergency")
    print(f"    Search 'emergency': {len(results)} genes found")
    for g in results:
        print(f"      • {g.name}")
    
    return genome


def demonstrate_ribosome(genome):
    """Demonstrates the Computational Ribosome - gene translation"""
    print_header("PART 4: COMPUTATIONAL RIBOSOME")
    
    print("""
  The Ribosome translates genes into executable instructions,
  just as biological ribosomes translate mRNA into proteins.
    """)
    
    ribosome = ComputationalRibosome(genome)
    
    # Find a gene to translate
    genes = genome.find_genes_by_context("emergency")
    if genes:
        gene = genes[0]
        
        print_subheader("Translation")
        print(f"    Translating: {gene.name}")
        
        plan = ribosome.translate_gene(gene.uid)
        
        print(f"    Steps Generated: {plan.total_steps}")
        print(f"    Safety Level: {plan.safety_level.value}")
        print(f"    Estimated Duration: {plan.estimated_duration_ms}ms")
        
        print_subheader("Execution (Dry Run)")
        result = ribosome.execute_plan(plan, dry_run=True)
        
        print(f"    Status: {result['overall_status'].value}")
        print(f"    Steps Executed: {result['steps_executed']}")
        print(f"    Steps Successful: {result['steps_successful']}")
        print(f"    Duration: {result['duration_ms']:.2f}ms")
    
    return ribosome


def demonstrate_cognitive_system(genome):
    """Demonstrates the Cognitive Core - intelligent decision making"""
    print_header("PART 5: COGNITIVE CORE")
    
    print("""
  The Cognitive Core is the reasoning engine that transforms
  intent and context into safe, validated, explainable decisions.
  
  It integrates:
    • Context Evaluator - validates environmental data
    • Inference Engine - matches intent to genes
    • Simulation Engine - tests decisions across scenarios
    • Oracle Synthesizer - produces final decisions
    • Merism Engine - evolves genes over time
    """)
    
    system = CognitiveSystem(genome)
    
    print_subheader("System Initialized")
    status = system.get_status()
    print(f"    Genes Available: {status['genome_statistics']['total_genes']}")
    print(f"    Active Genes: {status['genome_statistics']['active_genes']}")
    
    print_subheader("Processing Objectives")
    
    test_cases = [
        {
            "objective": "Isolate equipment due to high pressure",
            "context": {"pressure": 850, "temperature": 75, "status": "warning"}
        },
        {
            "objective": "Perform scheduled maintenance inspection",
            "context": {"schedule": "weekly", "last_inspection": "7_days_ago"}
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n    Test {i}: {test['objective']}")
        print(f"    Context: {test['context']}")
        
        result = system.process_objective(
            test["objective"],
            test["context"],
            dry_run=True
        )
        
        decision = result["decision"]
        if decision.get("success"):
            print(f"    ✓ Decision: Execute '{decision['selected_gene']['name']}'")
            print(f"      Confidence: {decision['explanation']['inference']['scores']['composite']:.2f}")
            print(f"      Steps: {decision['execution_plan']['total_steps']}")
        else:
            reason = decision.get("explanation", {}).get("reason", "Unknown")
            print(f"    ✗ No suitable gene found: {reason}")
    
    print_subheader("Final Statistics")
    final_status = system.get_status()
    print(f"    Decisions Processed: {final_status['total_decisions']}")
    print(f"    Success Rate: {final_status['success_rate']:.1%}")
    print(f"    Avg Duration: {final_status['average_duration_ms']:.2f}ms")
    
    return system


def demonstrate_persistence(genome):
    """Demonstrates genome serialization and persistence"""
    print_header("PART 6: PERSISTENCE & INTEROPERABILITY")
    
    print("""
  The Digital Genome can be serialized to JSON for:
    • Persistent storage
    • Network transmission
    • Federation between systems
    • Version control
    """)
    
    print_subheader("JSON Export")
    json_str = genome.to_json()
    print(f"    Serialized size: {len(json_str):,} characters")
    print(f"    Preview:\n    {json_str[:300]}...")
    
    print_subheader("Roundtrip Test")
    # Export and re-import
    exported = genome.to_dict()
    reimported = DigitalGenome.from_dict(exported)
    
    print(f"    Original genes: {len(genome.genes)}")
    print(f"    Reimported genes: {len(reimported.genes)}")
    print(f"    Integrity: {'✓ Preserved' if len(genome.genes) == len(reimported.genes) else '✗ Lost'}")


def main():
    """Main demonstration entry point"""
    print("\n" + "=" * 70)
    print("  OPERATIONAL GENOMICS - COMPLETE FRAMEWORK DEMONSTRATION")
    print("  Unifying Data, AI, Intention, and Action")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run demonstrations
    codons = demonstrate_codons()
    gene = demonstrate_genes(codons)
    genome = demonstrate_genome(gene)
    ribosome = demonstrate_ribosome(genome)
    system = demonstrate_cognitive_system(genome)
    demonstrate_persistence(genome)
    
    # Summary
    duration = time.time() - start_time
    
    print_header("DEMONSTRATION COMPLETE")
    print(f"""
  The Operational Genomics framework provides:
  
    ✓ Atomic knowledge units (Codons) encoding intentional action
    ✓ Composable functional capabilities (Genes)
    ✓ Organized knowledge repository (Digital Genome)
    ✓ Translation to executable instructions (Ribosome)
    ✓ Intelligent decision making (Cognitive Core)
    ✓ Evolutionary improvement (Merism)
    ✓ Full persistence and interoperability
  
  Total demonstration time: {duration:.2f} seconds
  
  For more information:
    • Specifications: specs/
    • Source code: src/
    • Documentation: README.md
    """)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
