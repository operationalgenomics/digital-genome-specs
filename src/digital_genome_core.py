"""
Digital Genome - Core Implementation v2.0
==========================================
Operational Genomics: A framework that unifies data, AI, intention and action
into coherent, evolutive, and explainable operational knowledge systems.

CRITICAL ARCHITECTURE PRINCIPLES:
1. DNA is not storage - DNA IS the neuron (knowledge IS the brain, not stored in it)
2. Four motors operate in PARALLEL, not sequentially
3. Craft Performance is a PRODUCT, not a weighted sum (zero = absolute veto)
4. Two truths: Foucauldian (registered, immutable) and Platonic (synthesized, approximate)
5. The Meta-Motor imagines what SHOULD exist, not just what does exist

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional, Set, Callable, Union
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
import hashlib
import time
import json
import uuid
import logging
import math

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DigitalGenome")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def compute_hash(*parts: bytes) -> str:
    """Computes a deterministic SHA-256 hash from multiple byte components."""
    hasher = hashlib.sha256()
    for part in parts:
        hasher.update(part)
    return hasher.hexdigest()


def make_uid(prefix: str, *components: str) -> str:
    """Creates a unique identifier based on a prefix and semantic components."""
    payload = f"{prefix}:{':'.join(components)}"
    return compute_hash(payload.encode())


# ============================================================================
# ENUMERATIONS
# ============================================================================
class SafetyLevel(Enum):
    """Safety classification for operational components"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class GeneStatus(Enum):
    """Lifecycle status of an operational gene"""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class TruthType(Enum):
    """
    The two types of truth in the Digital Genome:
    
    FOUCAULDIAN: Registered truth - crystallized in blockchain, immutable,
                 contextual ("this worked for this agent in this situation")
    
    PLATONIC: Synthesized truth - approximation of the ideal Form,
              calculated from Foucauldian truths, plastic, evolving
    """
    FOUCAULDIAN = "foucauldian"  # Registered, immutable, contextual
    PLATONIC = "platonic"        # Synthesized, approximate, universal


class VetoReason(Enum):
    """Reasons why a motor might issue an absolute veto (score = 0)"""
    INTENTION_VIOLATION = "intention_violation"
    STRATEGIC_INSTABILITY = "strategic_instability"
    CHAOS_CATASTROPHE = "chaos_catastrophe"
    PATTERN_VIOLATION = "pattern_violation"
    SAFETY_CRITICAL = "safety_critical"
    NO_VETO = "no_veto"


# ============================================================================
# TRUTH ARCHITECTURE
# ============================================================================
@dataclass(frozen=True)
class FoucauldianTruth:
    """
    A registered truth - an experience crystallized in the blockchain.
    
    Like light that traveled billions of years without changing,
    Foucauldian truths are immutable records of what actually happened.
    They make no claim to universality - only to authenticity.
    
    "This action worked for this agent in this situation at this time."
    """
    truth_id: str
    agent_id: str
    action_signature: str
    context_hash: str
    outcome: Dict[str, Any]
    timestamp: float
    block_hash: str  # Reference to blockchain block
    
    @classmethod
    def register(
        cls,
        agent_id: str,
        action: str,
        context: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> 'FoucauldianTruth':
        """Registers a new truth in the system."""
        context_hash = compute_hash(json.dumps(context, sort_keys=True).encode())
        truth_id = make_uid("truth", agent_id, action, context_hash, str(time.time()))
        block_hash = compute_hash(truth_id.encode(), str(time.time()).encode())
        
        return cls(
            truth_id=truth_id,
            agent_id=agent_id,
            action_signature=action,
            context_hash=context_hash,
            outcome=outcome,
            timestamp=time.time(),
            block_hash=block_hash
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "truth_id": self.truth_id,
            "truth_type": TruthType.FOUCAULDIAN.value,
            "agent_id": self.agent_id,
            "action_signature": self.action_signature,
            "context_hash": self.context_hash,
            "outcome": self.outcome,
            "timestamp": self.timestamp,
            "block_hash": self.block_hash
        }


@dataclass
class PlatonicApproximation:
    """
    A synthesized truth - an approximation of the ideal Platonic Form.
    
    Unlike Foucauldian truths which are immutable, Platonic approximations
    are plastic - they can change when better evidence emerges.
    
    The journey from Foucault to Plato:
    1. Experiences are registered (Foucauldian truths)
    2. Motors evaluate patterns across experiences
    3. Meta-Motor imagines improvements
    4. Validated improvements become new Platonic approximations
    
    A single verified truth can replace millions of perceived truths.
    This is science, not democracy.
    """
    approximation_id: str
    source_truths: List[str]  # UIDs of Foucauldian truths that contributed
    synthesized_pattern: Dict[str, Any]
    craft_performance: float  # CP score [0, 1]
    confidence: float
    version: int
    created_at: float
    supersedes: Optional[str] = None  # UID of previous approximation if evolved
    
    @property
    def is_approaching_form(self) -> bool:
        """Returns True if CP suggests proximity to the ideal Form."""
        return self.craft_performance > 0.9
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "approximation_id": self.approximation_id,
            "truth_type": TruthType.PLATONIC.value,
            "source_truths": self.source_truths,
            "synthesized_pattern": self.synthesized_pattern,
            "craft_performance": self.craft_performance,
            "confidence": self.confidence,
            "version": self.version,
            "created_at": self.created_at,
            "supersedes": self.supersedes
        }


# ============================================================================
# PRAXEOLOGICAL CODON - The Atomic Unit
# ============================================================================
@dataclass(frozen=True)
class PraxeologicalCodon:
    """
    The atomic, indivisible unit of purposeful operational knowledge.
    
    A codon encodes the fundamental structure of intentional action:
    Entity (who/what) → Action (operation) → Target State (desired result)
    
    This is not just an event record - it captures INTENT.
    The praxeological foundation means every codon represents
    purposeful human action, not mere occurrence.
    """
    entity_id: str
    action_id: str
    target_state_id: str
    intent_signature: str = ""  # Hash of the original intent
    parameters: Dict[str, Any] = field(default_factory=dict)
    preconditions: Tuple[str, ...] = field(default_factory=tuple)
    postconditions: Tuple[str, ...] = field(default_factory=tuple)
    safety_level: SafetyLevel = SafetyLevel.INFO
    context: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def uid(self) -> str:
        """Generates a unique identifier for this codon."""
        return make_uid("codon", self.entity_id, self.action_id, self.target_state_id)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "entity_id": self.entity_id,
            "action_id": self.action_id,
            "target_state_id": self.target_state_id,
            "intent_signature": self.intent_signature,
            "parameters": self.parameters,
            "preconditions": list(self.preconditions),
            "postconditions": list(self.postconditions),
            "safety_level": self.safety_level.value,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PraxeologicalCodon':
        return cls(
            entity_id=data["entity_id"],
            action_id=data["action_id"],
            target_state_id=data["target_state_id"],
            intent_signature=data.get("intent_signature", ""),
            parameters=data.get("parameters", {}),
            preconditions=tuple(data.get("preconditions", [])),
            postconditions=tuple(data.get("postconditions", [])),
            safety_level=SafetyLevel(data.get("safety_level", "info")),
            context=data.get("context", {})
        )
    
    def __str__(self) -> str:
        return f"[{self.entity_id} | {self.action_id} | {self.target_state_id}]"


# ============================================================================
# OPERATIONAL GENE
# ============================================================================
@dataclass
class OperationalGene:
    """
    A structured, coherent sequence of Praxeological Codons that expresses
    a functional operational capability.
    
    If codons are intention-atoms, then operational genes are action-proteins.
    """
    uid: str
    name: str
    purpose: str
    version: str = "1.0.0"
    status: GeneStatus = GeneStatus.DRAFT
    codons: List[PraxeologicalCodon] = field(default_factory=list)
    activation_conditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    exception_handlers: Dict[str, str] = field(default_factory=dict)
    evaluation_metrics: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Motor scores - these are filled by parallel evaluation
    motor_scores: Dict[str, float] = field(default_factory=dict)
    craft_performance: float = 0.0
    veto_status: VetoReason = VetoReason.NO_VETO
    
    # Evolution tracking
    parent_genes: List[str] = field(default_factory=list)
    source_truths: List[str] = field(default_factory=list)  # Foucauldian truths that informed this gene
    
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    
    @classmethod
    def create(cls, name: str, purpose: str, executor: str, action: str, target: str, **metadata) -> 'OperationalGene':
        uid = make_uid("gene", executor, action, target, str(time.time()))
        return cls(
            uid=uid,
            name=name,
            purpose=purpose,
            metadata={"executor": executor, "action": action, "target": target, **metadata}
        )
    
    def add_codon(self, codon: PraxeologicalCodon) -> 'OperationalGene':
        self.codons.append(codon)
        self.modified_at = time.time()
        return self
    
    def activate(self) -> 'OperationalGene':
        if len(self.codons) < 1:
            raise ValueError("Cannot activate gene without codons")
        self.status = GeneStatus.ACTIVE
        self.modified_at = time.time()
        return self
    
    def record_motor_scores(
        self,
        praxeological: float,
        nash: float,
        chaotic: float,
        meristic: float
    ) -> None:
        """
        Records scores from all four parallel motors and computes CP.
        
        CRITICAL: CP is computed as PRODUCT, not sum.
        If any motor gives zero, CP is zero (absolute veto).
        
        The yen example: if I have 1 million yen and you have 0,
        our "average" of 500k is a lie. You still starve.
        The product captures reality: 1,000,000 × 0 = 0.
        """
        self.motor_scores = {
            "praxeological": praxeological,
            "nash": nash,
            "chaotic": chaotic,
            "meristic": meristic
        }
        
        # CP is the PRODUCT of all motor scores
        self.craft_performance = praxeological * nash * chaotic * meristic
        
        # Check for veto conditions
        if praxeological == 0:
            self.veto_status = VetoReason.INTENTION_VIOLATION
        elif nash == 0:
            self.veto_status = VetoReason.STRATEGIC_INSTABILITY
        elif chaotic == 0:
            self.veto_status = VetoReason.CHAOS_CATASTROPHE
        elif meristic == 0:
            self.veto_status = VetoReason.PATTERN_VIOLATION
        else:
            self.veto_status = VetoReason.NO_VETO
        
        self.modified_at = time.time()
    
    @property
    def is_vetoed(self) -> bool:
        """Returns True if any motor has issued an absolute veto."""
        return self.veto_status != VetoReason.NO_VETO
    
    @property
    def safety_level(self) -> SafetyLevel:
        if not self.codons:
            return SafetyLevel.INFO
        levels = [c.safety_level for c in self.codons]
        if SafetyLevel.CRITICAL in levels:
            return SafetyLevel.CRITICAL
        if SafetyLevel.WARNING in levels:
            return SafetyLevel.WARNING
        return SafetyLevel.INFO
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "purpose": self.purpose,
            "version": self.version,
            "status": self.status.value,
            "codons": [c.to_dict() for c in self.codons],
            "activation_conditions": self.activation_conditions,
            "postconditions": self.postconditions,
            "exception_handlers": self.exception_handlers,
            "evaluation_metrics": self.evaluation_metrics,
            "metadata": self.metadata,
            "motor_scores": self.motor_scores,
            "craft_performance": self.craft_performance,
            "veto_status": self.veto_status.value,
            "parent_genes": self.parent_genes,
            "source_truths": self.source_truths,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OperationalGene':
        gene = cls(
            uid=data["uid"],
            name=data["name"],
            purpose=data["purpose"],
            version=data.get("version", "1.0.0"),
            status=GeneStatus(data.get("status", "draft")),
            activation_conditions=data.get("activation_conditions", []),
            postconditions=data.get("postconditions", []),
            exception_handlers=data.get("exception_handlers", {}),
            evaluation_metrics=data.get("evaluation_metrics", []),
            metadata=data.get("metadata", {}),
            motor_scores=data.get("motor_scores", {}),
            craft_performance=data.get("craft_performance", 0.0),
            veto_status=VetoReason(data.get("veto_status", "no_veto")),
            parent_genes=data.get("parent_genes", []),
            source_truths=data.get("source_truths", []),
            created_at=data.get("created_at", time.time()),
            modified_at=data.get("modified_at", time.time())
        )
        for codon_data in data.get("codons", []):
            gene.codons.append(PraxeologicalCodon.from_dict(codon_data))
        return gene


# ============================================================================
# DNA NEURON - The Fundamental Unit of the Cognitive Architecture
# ============================================================================
@dataclass
class DNANeuron:
    """
    A DNA block that functions as a plastic neuron in the distributed brain.
    
    CRITICAL INSIGHT: Knowledge is not stored IN the brain.
    Knowledge IS the brain. Each DNA block is a neuron.
    When a new truth crystallizes, the brain grows a new neuron.
    
    The Digital Genome's brain is morphogenic - it literally constructs
    itself as it learns. Each validated experience, each proven CODON,
    each crystallized Foucauldian truth adds matter to the brain.
    
    Synapses are the relationships between DNA-neurons.
    The motors are not separate modules - they are emergent properties
    of how DNA-neurons connect and fire together.
    """
    neuron_id: str
    gene: OperationalGene
    truth_type: TruthType
    source_block: Optional[str] = None  # Blockchain reference for Foucauldian
    synapses: List[str] = field(default_factory=list)  # Connected neuron IDs
    activation_level: float = 0.0
    plasticity: float = 1.0  # How much this neuron can change (Foucauldian = 0, Platonic = 1)
    
    def __post_init__(self):
        if self.truth_type == TruthType.FOUCAULDIAN:
            self.plasticity = 0.0  # Immutable
        else:
            self.plasticity = 1.0  # Plastic
    
    def connect_to(self, other_neuron_id: str) -> None:
        """Creates a synapse to another neuron."""
        if other_neuron_id not in self.synapses:
            self.synapses.append(other_neuron_id)
    
    def activate(self, signal_strength: float) -> float:
        """
        Activates this neuron with a signal.
        Returns the output activation level.
        """
        # Simple sigmoid activation
        self.activation_level = 1 / (1 + math.exp(-signal_strength))
        return self.activation_level
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "neuron_id": self.neuron_id,
            "gene": self.gene.to_dict(),
            "truth_type": self.truth_type.value,
            "source_block": self.source_block,
            "synapses": self.synapses,
            "activation_level": self.activation_level,
            "plasticity": self.plasticity
        }


# ============================================================================
# DIGITAL GENOME - The Distributed Brain
# ============================================================================
class DigitalGenome:
    """
    The complete, versioned, governed library of operational genes.
    
    But more than a library - this IS the brain. The Digital Genome
    is a distributed cognitive organ where:
    - Each gene is a neuron
    - Stems and chromosomes are brain regions
    - Synapses are relationships between genes
    - Motors emerge from activation patterns
    
    The genome is morphogenic: it grows new neurons as it learns.
    It is federated: each node has its own brain that can donate
    cells to other nodes when evolution occurs.
    """
    
    def __init__(self, genome_id: str = None, name: str = "Default Genome"):
        self.genome_id = genome_id or make_uid("genome", name, str(time.time()))
        self.name = name
        
        # Neural architecture
        self.neurons: Dict[str, DNANeuron] = {}
        self.genes: Dict[str, OperationalGene] = {}
        
        # Brain regions
        self.stems: Dict[str, List[str]] = defaultdict(list)  # Thematic regions
        self.chromosomes: Dict[str, List[str]] = defaultdict(list)  # Functional regions
        
        # Truth registries
        self.foucauldian_truths: Dict[str, FoucauldianTruth] = {}
        self.platonic_approximations: Dict[str, PlatonicApproximation] = {}
        
        # Ontology registries
        self.entity_registry: Dict[str, Dict[str, Any]] = {}
        self.action_registry: Dict[str, Dict[str, Any]] = {}
        self.state_registry: Dict[str, Dict[str, Any]] = {}
        
        # Evolution tracking
        self.evolution_history: List[Dict[str, Any]] = []
        
        self.created_at = time.time()
        self.modified_at = time.time()
        
        logger.info(f"Digital Genome initialized: {self.name} ({self.genome_id[:16]}...)")
    
    def register_foucauldian_truth(
        self,
        agent_id: str,
        action: str,
        context: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> FoucauldianTruth:
        """
        Registers an experience as immutable truth.
        This is like light that traveled without changing - 
        it records what actually happened.
        """
        truth = FoucauldianTruth.register(agent_id, action, context, outcome)
        self.foucauldian_truths[truth.truth_id] = truth
        
        logger.info(f"Foucauldian truth registered: {truth.truth_id[:16]}...")
        return truth
    
    def synthesize_platonic_approximation(
        self,
        source_truth_ids: List[str],
        pattern: Dict[str, Any],
        craft_performance: float,
        confidence: float
    ) -> PlatonicApproximation:
        """
        Synthesizes a Platonic approximation from multiple Foucauldian truths.
        This is the journey from experience to wisdom.
        """
        approximation = PlatonicApproximation(
            approximation_id=make_uid("platonic", str(time.time())),
            source_truths=source_truth_ids,
            synthesized_pattern=pattern,
            craft_performance=craft_performance,
            confidence=confidence,
            version=1,
            created_at=time.time()
        )
        self.platonic_approximations[approximation.approximation_id] = approximation
        
        logger.info(f"Platonic approximation synthesized: CP={craft_performance:.3f}")
        return approximation
    
    def insert_gene_as_neuron(
        self,
        gene: OperationalGene,
        truth_type: TruthType,
        stem: str = "default",
        chromosome: str = "primary",
        source_block: Optional[str] = None
    ) -> DNANeuron:
        """
        Inserts a gene into the genome as a neuron.
        The brain grows a new cell.
        """
        self.genes[gene.uid] = gene
        self.stems[stem].append(gene.uid)
        self.chromosomes[chromosome].append(gene.uid)
        
        # Create the neuron
        neuron = DNANeuron(
            neuron_id=make_uid("neuron", gene.uid),
            gene=gene,
            truth_type=truth_type,
            source_block=source_block
        )
        self.neurons[neuron.neuron_id] = neuron
        
        self.modified_at = time.time()
        
        # Record evolution event
        self.evolution_history.append({
            "timestamp": time.time(),
            "event_type": "neuron_growth",
            "gene_uid": gene.uid,
            "neuron_id": neuron.neuron_id,
            "truth_type": truth_type.value,
            "stem": stem,
            "chromosome": chromosome
        })
        
        logger.info(f"Neuron grown: {gene.name} → {stem}/{chromosome}")
        return neuron
    
    def create_synapse(self, neuron_id_1: str, neuron_id_2: str) -> None:
        """Creates a bidirectional synapse between two neurons."""
        if neuron_id_1 in self.neurons and neuron_id_2 in self.neurons:
            self.neurons[neuron_id_1].connect_to(neuron_id_2)
            self.neurons[neuron_id_2].connect_to(neuron_id_1)
            logger.debug(f"Synapse created: {neuron_id_1[:16]} ↔ {neuron_id_2[:16]}")
    
    def register_entity(self, entity_id: str, name: str, entity_type: str, **attributes) -> str:
        self.entity_registry[entity_id] = {
            "name": name,
            "type": entity_type,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return entity_id
    
    def register_action(self, action_id: str, name: str, category: str, **attributes) -> str:
        self.action_registry[action_id] = {
            "name": name,
            "category": category,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return action_id
    
    def register_state(self, state_id: str, name: str, category: str, **attributes) -> str:
        self.state_registry[state_id] = {
            "name": name,
            "category": category,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return state_id
    
    def get_gene(self, gene_uid: str) -> Optional[OperationalGene]:
        return self.genes.get(gene_uid)
    
    def get_neuron(self, neuron_id: str) -> Optional[DNANeuron]:
        return self.neurons.get(neuron_id)
    
    def find_genes_by_context(self, context: str) -> List[OperationalGene]:
        """Finds genes related to a specific context using word matching."""
        context_words = set(context.lower().split())
        matches = []
        
        for gene in self.genes.values():
            relevance = 0
            
            # Check name words
            name_words = set(gene.name.lower().split())
            name_overlap = len(context_words & name_words)
            relevance += name_overlap * 3
            
            # Check purpose words
            purpose_words = set(gene.purpose.lower().split())
            purpose_overlap = len(context_words & purpose_words)
            relevance += purpose_overlap * 2
            
            # Check metadata
            for key, value in gene.metadata.items():
                value_words = set(str(value).lower().split())
                meta_overlap = len(context_words & value_words)
                relevance += meta_overlap
            
            if relevance > 0:
                matches.append((relevance, gene))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        return [gene for _, gene in matches]
    
    def get_statistics(self) -> Dict[str, Any]:
        total_codons = sum(len(gene.codons) for gene in self.genes.values())
        active_genes = sum(1 for g in self.genes.values() if g.status == GeneStatus.ACTIVE)
        vetoed_genes = sum(1 for g in self.genes.values() if g.is_vetoed)
        
        avg_cp = 0
        if self.genes:
            avg_cp = sum(g.craft_performance for g in self.genes.values()) / len(self.genes)
        
        return {
            "genome_id": self.genome_id[:16] + "...",
            "name": self.name,
            "total_neurons": len(self.neurons),
            "total_genes": len(self.genes),
            "active_genes": active_genes,
            "vetoed_genes": vetoed_genes,
            "total_codons": total_codons,
            "foucauldian_truths": len(self.foucauldian_truths),
            "platonic_approximations": len(self.platonic_approximations),
            "stems": len(self.stems),
            "chromosomes": len(self.chromosomes),
            "total_synapses": sum(len(n.synapses) for n in self.neurons.values()),
            "average_craft_performance": round(avg_cp, 4),
            "evolution_events": len(self.evolution_history)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "genome_id": self.genome_id,
            "name": self.name,
            "genes": {uid: gene.to_dict() for uid, gene in self.genes.items()},
            "neurons": {nid: n.to_dict() for nid, n in self.neurons.items()},
            "stems": dict(self.stems),
            "chromosomes": dict(self.chromosomes),
            "foucauldian_truths": {tid: t.to_dict() for tid, t in self.foucauldian_truths.items()},
            "platonic_approximations": {aid: a.to_dict() for aid, a in self.platonic_approximations.items()},
            "entity_registry": self.entity_registry,
            "action_registry": self.action_registry,
            "state_registry": self.state_registry,
            "evolution_history": self.evolution_history,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ============================================================================
# DEMONSTRATION
# ============================================================================
def demonstration():
    """Demonstrates the core Digital Genome architecture."""
    print("\n" + "=" * 70)
    print("DIGITAL GENOME v2.0 - CORE ARCHITECTURE DEMONSTRATION")
    print("Knowledge IS the brain, not stored in it")
    print("=" * 70)
    
    # Create genome
    print("\n Creating Digital Genome (distributed brain)...")
    genome = DigitalGenome(name="Industrial Cognitive Genome")
    
    # Register ontology
    pump_id = genome.register_entity(make_uid("entity", "pump", "401"), "Pump 401", "physical")
    stop_action = genome.register_action(make_uid("action", "stop"), "Stop", "operational")
    isolated_state = genome.register_state(make_uid("state", "isolated"), "Isolated", "safety")
    
    # Register a Foucauldian truth (immutable experience)
    print("\n Registering Foucauldian truth (immutable experience)...")
    truth = genome.register_foucauldian_truth(
        agent_id="operator_001",
        action="emergency_stop_pump_401",
        context={"temperature": 95, "vibration": 8.5, "pressure": 850},
        outcome={"success": True, "time_ms": 450, "equipment_intact": True}
    )
    print(f"   Truth registered: {truth.truth_id[:32]}...")
    print(f"   Block hash: {truth.block_hash[:32]}...")
    
    # Create an operational gene
    print("\n Creating operational gene...")
    gene = OperationalGene.create(
        name="Emergency Pump Shutdown",
        purpose="Safely stop pump in emergency conditions",
        executor="safety_system",
        action="emergency_shutdown",
        target="pump_401"
    )
    
    gene.add_codon(PraxeologicalCodon(
        entity_id=pump_id,
        action_id=stop_action,
        target_state_id=isolated_state,
        safety_level=SafetyLevel.CRITICAL,
        intent_signature=make_uid("intent", "emergency", "safety")
    ))
    
    # Record motor scores (PRODUCT, not sum!)
    print("\n Recording parallel motor scores...")
    gene.record_motor_scores(
        praxeological=0.92,  # Intention realization
        nash=0.85,          # Strategic equilibrium
        chaotic=0.88,       # Robustness to perturbations
        meristic=0.90       # Pattern universality
    )
    
    print(f"   Praxeological Motor: {gene.motor_scores['praxeological']:.2f}")
    print(f"   Nash Motor: {gene.motor_scores['nash']:.2f}")
    print(f"   Chaotic Motor: {gene.motor_scores['chaotic']:.2f}")
    print(f"   Meristic Motor: {gene.motor_scores['meristic']:.2f}")
    print(f"   Craft Performance (PRODUCT): {gene.craft_performance:.4f}")
    print(f"   Veto Status: {gene.veto_status.value}")
    
    # Demonstrate veto
    print("\n Demonstrating absolute veto (zero in any motor)...")
    vetoed_gene = OperationalGene.create(
        name="Unstable Action",
        purpose="Action that fails strategic equilibrium",
        executor="system",
        action="unstable",
        target="target"
    )
    vetoed_gene.record_motor_scores(
        praxeological=0.95,
        nash=0.0,  # ZERO - absolute veto!
        chaotic=0.90,
        meristic=0.85
    )
    print(f"   Motors: P=0.95, N=0.0, C=0.90, M=0.85")
    print(f"   Craft Performance: {vetoed_gene.craft_performance:.4f}")
    print(f"   Vetoed: {vetoed_gene.is_vetoed} ({vetoed_gene.veto_status.value})")
    
    # Insert gene as neuron
    print("\n Growing neuron in the distributed brain...")
    gene.activate()
    neuron = genome.insert_gene_as_neuron(
        gene,
        truth_type=TruthType.PLATONIC,
        stem="safety",
        chromosome="critical_operations"
    )
    print(f"   Neuron ID: {neuron.neuron_id[:32]}...")
    print(f"   Plasticity: {neuron.plasticity} (Platonic = plastic)")
    
    # Statistics
    print("\n Genome Statistics:")
    stats = genome.get_statistics()
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    return genome


if __name__ == "__main__":
    genome = demonstration()
