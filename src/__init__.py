"""
Operational Genomics - Digital Genome v2.0
==========================================
A framework that unifies data, AI, intention and action
into coherent, evolutive, and explainable operational knowledge systems.

CRITICAL ARCHITECTURE:
- DNA IS the neuron (knowledge IS the brain, not stored in it)
- Four motors operate in PARALLEL (Praxeological, Nash, Chaotic, Meristic)
- Craft Performance is a PRODUCT, not sum (any zero = absolute veto)
- Two truths: Foucauldian (immutable) and Platonic (plastic)

Author: Carlos Eduardo Favini
"""

from .digital_genome_core import (
    # Core classes
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    DNANeuron,
    FoucauldianTruth,
    PlatonicApproximation,
    
    # Enums
    SafetyLevel,
    GeneStatus,
    TruthType,
    VetoReason,
    
    # Utilities
    make_uid,
    compute_hash
)

from .cognitive_core import (
    # System
    CognitiveSystem,
    ParallelMotorOrchestrator,
    CraftPerformanceResult,
    
    # Motors
    CognitiveMotor,
    PraxeologicalMotor,
    NashMotor,
    ChaoticMotor,
    MeristicMetaMotor,
    
    # Data structures
    MotorEvaluation
)

__version__ = "1.1.0"
__author__ = "Carlos Eduardo Favini"
