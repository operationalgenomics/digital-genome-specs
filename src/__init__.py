"""
Operational Genomics - Reference Implementation
"""

from .digital_genome_core import (
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    ComputationalRibosome,
    SafetyLevel,
    GeneStatus,
    ExecutionResult,
    make_uid
)

from .cognitive_core import (
    CognitiveSystem,
    ContextEvaluator,
    InferenceEngine,
    SimulationEngine,
    MerismEvolutionEngine,
    OracleSynthesizer,
    HighLevelIntent,
    ContextSnapshot
)

__version__ = "1.0.0"
__author__ = "Carlos Eduardo Favini"

