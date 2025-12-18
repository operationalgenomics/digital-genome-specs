"""
Digital Genome Core (v4.0 - The Vectorized Mind)
================================================
Operational Genomics: 100% Mathematical Representation.
Eliminates linguistic artifacts (Enums/Strings) from the core logic,
utilizing Holographic Identifiers and State Vectors.

PHILOSOPHY:
"The map is vectors. The territory is math."
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
import hashlib
import uuid
import json
import time
import logging
import math
import numpy as np
from pathlib import Path

# Setup Logging
logger = logging.getLogger("DigitalGenome")

# ============================================================================
# MATHEMATICAL PRIMITIVES
# ============================================================================

@dataclass(frozen=True)
class StateVector:
    """
    Represents a state as a multidimensional vector [0.0 - 1.0].
    Dimensions: [Intensity, Irreversibility, Scope]
    """
    coordinates: Tuple[float, ...]

    @staticmethod
    def distance(v1: 'StateVector', v2: 'StateVector') -> float:
        """Calculates Euclidean distance between two state vectors."""
        a = np.array(v1.coordinates)
        b = np.array(v2.coordinates)
        return np.linalg.norm(a - b)

    def to_list(self) -> List[float]:
        return list(self.coordinates)

    # --- ARCHETYPES (Mathematical Constants) ---
    # Replaces legacy "INFO", "WARNING", "CRITICAL" levels.
    # 0.0 = Low/Safe, 1.0 = High/Dangerous
    
    # [Intensity=0.1, Irreversibility=0.0, Scope=0.1]
    ARCHETYPE_NOMINAL = (0.1, 0.0, 0.1) 
    
    # [Intensity=0.5, Irreversibility=0.2, Scope=0.4]
    ARCHETYPE_DEVIATION = (0.5, 0.2, 0.4) 
    
    # [Intensity=0.9, Irreversibility=0.9, Scope=1.0]
    ARCHETYPE_ENTROPY_MAX = (0.9, 0.9, 1.0) 

# ============================================================================
# HELPER FUNCTIONS (Holographic IDs)
# ============================================================================
def compute_hash(*parts: str) -> str:
    hasher = hashlib.sha256()
    for part in parts:
        hasher.update(str(part).encode())
    return hasher.hexdigest()

def make_uid(prefix: str, *components: str) -> str:
    payload = f"{prefix}:{':'.join(str(c) for c in components)}"
    return compute_hash(payload)

# ============================================================================
# DNA STRUCTURES
# ============================================================================
@dataclass
class PraxeologicalCodon:
    """
    Atomic Unit. Uses StateVector for precise state definition.
    """
    entity_id: str      
    action_id: str      
    state_vector: StateVector 
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "action_id": self.action_id,
            "state_vector": self.state_vector.to_list(),
            "parameters": self.parameters
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PraxeologicalCodon':
        return cls(
            entity_id=data["entity_id"],
            action_id=data["action_id"],
            state_vector=StateVector(tuple(data["state_vector"])),
            parameters=data.get("parameters", {})
        )

@dataclass
class OperationalGene:
    """Sequence of Codons representing a complete operational concept."""
    uid: str
    name: str
    purpose: str
    codons: List[PraxeologicalCodon] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Execution State
    motor_scores: Dict[str, float] = field(default_factory=dict)
    craft_performance: float = 0.0
    
    is_vetoed_state: bool = False
    veto_source: str = "" 
    
    # Memory
    experience_count: int = 0 
    last_verdict: str = "UNKNOWN"
    created_at: float = field(default_factory=time.time)

    @classmethod
    def create(cls, name: str, purpose: str, executor: str, action: str, target: str, **metadata) -> 'OperationalGene':
        unique_signature = f"{executor}:{action}:{target}:{name}"
        uid = make_uid("gene", unique_signature)
        return cls(
            uid=uid,
            name=name,
            purpose=purpose,
            metadata={"executor": executor, "action": action, "target": target, **metadata}
        )

    def add_codon(self, codon: PraxeologicalCodon):
        self.codons.append(codon)

    def record_motor_scores(self, praxeological: float, nash: float, chaotic: float, meristic: float) -> None:
        self.motor_scores = {"praxeological": praxeological, "nash": nash, "chaotic": chaotic, "meristic": meristic}
        self.craft_performance = praxeological * nash * chaotic * meristic
        
        # Absolute Zero Veto Logic
        if self.craft_performance == 0:
            self.is_vetoed_state = True
            if praxeological == 0: self.veto_source = "P-Motor"
            elif nash == 0: self.veto_source = "N-Motor"
            elif chaotic == 0: self.veto_source = "C-Motor"
            elif meristic == 0: self.veto_source = "M-Motor"
        else:
            self.is_vetoed_state = False
            self.veto_source = ""

    def to_dict(self) -> Dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "purpose": self.purpose,
            "codons": [c.to_dict() for c in self.codons],
            "metadata": self.metadata,
            "motor_scores": self.motor_scores,
            "craft_performance": self.craft_performance,
            "is_vetoed_state": self.is_vetoed_state,
            "veto_source": self.veto_source,
            "experience_count": self.experience_count,
            "last_verdict": self.last_verdict,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'OperationalGene':
        gene = cls(
            uid=data["uid"],
            name=data["name"],
            purpose=data["purpose"],
            metadata=data.get("metadata", {}),
            motor_scores=data.get("motor_scores", {}),
            craft_performance=data.get("craft_performance", 0.0),
            is_vetoed_state=data.get("is_vetoed_state", False),
            veto_source=data.get("veto_source", ""),
            experience_count=data.get("experience_count", 0),
            last_verdict=data.get("last_verdict", "UNKNOWN"),
            created_at=data.get("created_at", time.time())
        )
        if "codons" in data:
            gene.codons = [PraxeologicalCodon.from_dict(c) for c in data["codons"]]
        return gene

# ============================================================================
# NEURAL STRUCTURE
# ============================================================================
@dataclass
class Neuron:
    uid: str
    gene: OperationalGene
    # Plasticity: 0.0 = Hard/Immutable (Foucauldian), 1.0 = Soft/Hypothetical (Platonic)
    plasticity: float 
    synapses: List[str] = field(default_factory=list)
    activation_level: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "uid": self.uid,
            "gene": self.gene.to_dict(),
            "plasticity": self.plasticity,
            "synapses": self.synapses,
            "activation_level": self.activation_level
        }

# ============================================================================
# THE GENOME
# ============================================================================
class DigitalGenome:
    def __init__(self, name: str, memory_path: str = "data/cortex/genome_memory.json"):
        self.name = name
        self.genes: Dict[str, OperationalGene] = {}
        self.neurons: Dict[str, Neuron] = {}
        self.memory_path = Path(memory_path)
        self.load_memory()

    def load_memory(self):
        if self.memory_path.exists():
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                loaded_genes = 0
                for gene_data in data.get("genes", []):
                    g = OperationalGene.from_dict(gene_data)
                    self.genes[g.uid] = g
                    loaded_genes += 1
                logger.info(f"🧠 CORTEX LOADED: {loaded_genes} concepts.")
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")
        else:
            logger.info("✨ NEW CORTEX CREATED.")
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)

    def save_memory(self):
        data = {
            "version": "v4.0",
            "timestamp": time.time(),
            "genes": [g.to_dict() for g in self.genes.values()]
        }
        try:
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"💾 MEMORY CONSOLIDATED: {len(self.genes)} genes.")
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def insert_gene_as_neuron(self, gene: OperationalGene, plasticity: float = 0.0) -> Tuple[Neuron, OperationalGene]:
        """
        Integrates a gene into the neural network.
        Returns both the Neuron object AND the Authoritative Gene from memory.
        """
        target_gene = gene
        
        # 1. Recognition (Does this gene exist in memory?)
        if gene.uid in self.genes:
            existing_gene = self.genes[gene.uid]
            existing_gene.experience_count += 1
            # Merge metadata (keep history, update context)
            existing_gene.metadata.update(gene.metadata)
            target_gene = existing_gene
        else:
            # 2. Learning (New concept)
            gene.experience_count = 1
            self.genes[gene.uid] = gene
            target_gene = gene

        # 3. Create Neuron (Synaptic Connection)
        neuron_id = make_uid("neuron", target_gene.uid, str(plasticity))
        neuron = Neuron(uid=neuron_id, gene=target_gene, plasticity=plasticity)
        self.neurons[neuron_id] = neuron
        
        return neuron, target_gene