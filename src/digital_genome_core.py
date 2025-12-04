"""
Digital Genome - Core Implementation
=====================================
Operational Genomics: A framework that unifies data, AI, intention and action
into coherent, evolutive, and explainable operational knowledge systems.

This module implements the foundational components:
- Praxeological Codons: Atomic units of purposeful action (Entity-Action-State)
- Operational Genes: Composable sequences of codons expressing functional capabilities
- Digital Genome: The complete knowledge organism containing genes and evolution mechanisms
- Computational Ribosome: Translates genes into executable instructions

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional, Set, Callable
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
import hashlib
import time
import json
import uuid
import logging

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
    """
    Computes a deterministic SHA-256 hash from multiple byte components.
    Used to generate unique identifiers for genome components.
    """
    hasher = hashlib.sha256()
    for part in parts:
        hasher.update(part)
    return hasher.hexdigest()


def make_uid(prefix: str, *components: str) -> str:
    """
    Creates a unique identifier based on a prefix and semantic components.
    The UID is deterministic: same inputs always produce the same output.
    
    Args:
        prefix: Category identifier (e.g., "gene", "codon", "entity")
        components: Semantic parts that define the element
        
    Returns:
        A 64-character hexadecimal string
    """
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


class ExecutionResult(Enum):
    """Possible outcomes of gene execution"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    ABORTED = "aborted"


# ============================================================================
# PRAXEOLOGICAL CODON
# ============================================================================
@dataclass(frozen=True)
class PraxeologicalCodon:
    """
    The atomic, indivisible unit of purposeful operational knowledge.
    
    A codon encodes the fundamental structure of intentional action:
    Entity (who/what) → Action (operation) → Target State (desired result)
    
    This mirrors biological codons that encode amino acids, but here we
    encode units of operational meaning that can be composed into genes.
    
    Attributes:
        entity_id: Unique identifier of the entity being acted upon
        action_id: Unique identifier of the action to perform
        target_state_id: Unique identifier of the desired resulting state
        parameters: Optional domain-specific parameters for the action
        preconditions: Conditions that must be true before execution
        postconditions: Conditions expected to be true after execution
        safety_level: Risk classification of this codon
        context: Additional contextual information
    """
    entity_id: str
    action_id: str
    target_state_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    preconditions: Tuple[str, ...] = field(default_factory=tuple)
    postconditions: Tuple[str, ...] = field(default_factory=tuple)
    safety_level: SafetyLevel = SafetyLevel.INFO
    context: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def uid(self) -> str:
        """Generates a unique identifier for this codon"""
        return make_uid("codon", self.entity_id, self.action_id, self.target_state_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the codon to a dictionary"""
        return {
            "uid": self.uid,
            "entity_id": self.entity_id,
            "action_id": self.action_id,
            "target_state_id": self.target_state_id,
            "parameters": self.parameters,
            "preconditions": list(self.preconditions),
            "postconditions": list(self.postconditions),
            "safety_level": self.safety_level.value,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PraxeologicalCodon':
        """Deserializes a codon from a dictionary"""
        return cls(
            entity_id=data["entity_id"],
            action_id=data["action_id"],
            target_state_id=data["target_state_id"],
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
    A gene defines complete, purposeful behavior that can be activated,
    executed, and evaluated.
    
    Attributes:
        uid: Unique identifier for this gene
        name: Human-readable name
        purpose: Declarative description of what this gene accomplishes
        version: Semantic version string (e.g., "1.0.0")
        status: Current lifecycle status
        codons: Ordered sequence of praxeological codons
        activation_conditions: Conditions required for gene activation
        postconditions: Expected truths after successful execution
        exception_handlers: Fallback strategies for failure scenarios
        evaluation_metrics: KPIs for assessing execution quality
        metadata: Additional descriptive information
        fitness_scores: Historical performance data per context
        parent_genes: Lineage for evolutionary tracking (Merism)
        created_at: Timestamp of creation
        modified_at: Timestamp of last modification
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
    fitness_scores: Dict[str, float] = field(default_factory=dict)
    parent_genes: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    
    @classmethod
    def create(
        cls,
        name: str,
        purpose: str,
        executor: str,
        action: str,
        target: str,
        **metadata
    ) -> 'OperationalGene':
        """
        Factory method to create a new operational gene.
        
        Args:
            name: Human-readable name for the gene
            purpose: What this gene accomplishes
            executor: The agent/system that executes this gene
            action: The primary action performed
            target: The target of the action
            **metadata: Additional metadata key-value pairs
            
        Returns:
            A new OperationalGene instance
        """
        uid = make_uid("gene", executor, action, target, str(time.time()))
        return cls(
            uid=uid,
            name=name,
            purpose=purpose,
            metadata={"executor": executor, "action": action, "target": target, **metadata}
        )
    
    def add_codon(self, codon: PraxeologicalCodon) -> 'OperationalGene':
        """
        Adds a codon to the gene's sequence.
        Codons define the atomic steps of the gene's execution.
        
        Args:
            codon: The praxeological codon to add
            
        Returns:
            Self for method chaining
        """
        self.codons.append(codon)
        self.modified_at = time.time()
        return self
    
    def activate(self) -> 'OperationalGene':
        """Transitions the gene to active status"""
        if len(self.codons) < 1:
            raise ValueError("Cannot activate gene without codons")
        self.status = GeneStatus.ACTIVE
        self.modified_at = time.time()
        return self
    
    def deprecate(self, reason: str = "") -> 'OperationalGene':
        """Marks the gene as deprecated"""
        self.status = GeneStatus.DEPRECATED
        self.metadata["deprecation_reason"] = reason
        self.modified_at = time.time()
        return self
    
    def record_fitness(self, context_signature: str, score: float) -> None:
        """
        Records a fitness score for a specific context.
        Used by the Merism evolution engine to select superior variants.
        
        Args:
            context_signature: Hash identifying the execution context
            score: Performance score between 0.0 and 1.0
        """
        self.fitness_scores[context_signature] = score
        self.modified_at = time.time()
    
    def get_average_fitness(self) -> float:
        """Returns the average fitness across all recorded contexts"""
        if not self.fitness_scores:
            return 0.0
        return sum(self.fitness_scores.values()) / len(self.fitness_scores)
    
    @property
    def safety_level(self) -> SafetyLevel:
        """Returns the highest safety level among all codons"""
        if not self.codons:
            return SafetyLevel.INFO
        levels = [c.safety_level for c in self.codons]
        if SafetyLevel.CRITICAL in levels:
            return SafetyLevel.CRITICAL
        if SafetyLevel.WARNING in levels:
            return SafetyLevel.WARNING
        return SafetyLevel.INFO
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the gene to a dictionary"""
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
            "fitness_scores": self.fitness_scores,
            "parent_genes": self.parent_genes,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OperationalGene':
        """Deserializes a gene from a dictionary"""
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
            fitness_scores=data.get("fitness_scores", {}),
            parent_genes=data.get("parent_genes", []),
            created_at=data.get("created_at", time.time()),
            modified_at=data.get("modified_at", time.time())
        )
        for codon_data in data.get("codons", []):
            gene.codons.append(PraxeologicalCodon.from_dict(codon_data))
        return gene


# ============================================================================
# DIGITAL GENOME
# ============================================================================
class DigitalGenome:
    """
    The complete, versioned, governed library of operational genes.
    
    The Digital Genome is the central repository of operational knowledge,
    organized into thematic clusters (stems) and functional groups (chromosomes).
    It supports versioning, evolution tracking, and contextual search.
    
    This is a "living" structure that evolves through Merism:
    variation → evaluation → selection → inheritance
    """
    
    def __init__(self, genome_id: str = None, name: str = "Default Genome"):
        """
        Initializes a new Digital Genome.
        
        Args:
            genome_id: Unique identifier (auto-generated if not provided)
            name: Human-readable name for this genome
        """
        self.genome_id = genome_id or make_uid("genome", name, str(time.time()))
        self.name = name
        self.genes: Dict[str, OperationalGene] = {}
        self.stems: Dict[str, List[str]] = defaultdict(list)  # Thematic groupings
        self.chromosomes: Dict[str, List[str]] = defaultdict(list)  # Functional groupings
        self.evolution_history: List[Dict[str, Any]] = []
        self.entity_registry: Dict[str, Dict[str, Any]] = {}
        self.action_registry: Dict[str, Dict[str, Any]] = {}
        self.state_registry: Dict[str, Dict[str, Any]] = {}
        self.created_at = time.time()
        self.modified_at = time.time()
        
        logger.info(f"Digital Genome initialized: {self.name} ({self.genome_id[:16]}...)")
    
    def register_entity(self, entity_id: str, name: str, entity_type: str, **attributes) -> str:
        """
        Registers an entity in the genome's ontology.
        
        Args:
            entity_id: Unique identifier for the entity
            name: Human-readable name
            entity_type: Classification (physical, logical, agent, resource)
            **attributes: Additional attributes
            
        Returns:
            The entity_id
        """
        self.entity_registry[entity_id] = {
            "name": name,
            "type": entity_type,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return entity_id
    
    def register_action(self, action_id: str, name: str, category: str, **attributes) -> str:
        """
        Registers an action in the genome's ontology.
        
        Args:
            action_id: Unique identifier for the action
            name: Human-readable name
            category: Classification (operational, informational, safety, diagnostic)
            **attributes: Additional attributes
            
        Returns:
            The action_id
        """
        self.action_registry[action_id] = {
            "name": name,
            "category": category,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return action_id
    
    def register_state(self, state_id: str, name: str, category: str, **attributes) -> str:
        """
        Registers a state in the genome's ontology.
        
        Args:
            state_id: Unique identifier for the state
            name: Human-readable name
            category: Classification (operational, safety, intermediate, diagnostic)
            **attributes: Additional attributes
            
        Returns:
            The state_id
        """
        self.state_registry[state_id] = {
            "name": name,
            "category": category,
            "attributes": attributes,
            "registered_at": time.time()
        }
        return state_id
    
    def insert_gene(
        self,
        gene: OperationalGene,
        stem: str = "default",
        chromosome: str = "primary"
    ) -> None:
        """
        Inserts a gene into the genome.
        
        Args:
            gene: The operational gene to insert
            stem: Thematic grouping (e.g., "safety", "optimization", "diagnostics")
            chromosome: Functional grouping (e.g., "core", "experimental")
        """
        self.genes[gene.uid] = gene
        self.stems[stem].append(gene.uid)
        self.chromosomes[chromosome].append(gene.uid)
        self.modified_at = time.time()
        
        # Record evolution event
        self.evolution_history.append({
            "timestamp": time.time(),
            "event_type": "insertion",
            "gene_uid": gene.uid,
            "gene_name": gene.name,
            "stem": stem,
            "chromosome": chromosome
        })
        
        logger.info(f"Gene inserted: {gene.name} ({gene.uid[:16]}...) → stem='{stem}', chromosome='{chromosome}'")
    
    def get_gene(self, gene_uid: str) -> Optional[OperationalGene]:
        """Retrieves a gene by its UID"""
        return self.genes.get(gene_uid)
    
    def find_genes_by_context(self, context: str) -> List[OperationalGene]:
        """
        Finds genes related to a specific context.
        Searches through gene names, purposes, and metadata.
        
        Args:
            context: Search term or context description
            
        Returns:
            List of matching genes, sorted by relevance
        """
        context_lower = context.lower()
        matches = []
        
        for gene in self.genes.values():
            relevance = 0
            
            # Check name
            if context_lower in gene.name.lower():
                relevance += 3
            
            # Check purpose
            if context_lower in gene.purpose.lower():
                relevance += 2
            
            # Check metadata
            for key, value in gene.metadata.items():
                if context_lower in str(value).lower():
                    relevance += 1
            
            if relevance > 0:
                matches.append((relevance, gene))
        
        # Sort by relevance (descending) and return genes only
        matches.sort(key=lambda x: x[0], reverse=True)
        return [gene for _, gene in matches]
    
    def find_genes_by_stem(self, stem: str) -> List[OperationalGene]:
        """Returns all genes in a specific thematic stem"""
        gene_uids = self.stems.get(stem, [])
        return [self.genes[uid] for uid in gene_uids if uid in self.genes]
    
    def find_genes_by_chromosome(self, chromosome: str) -> List[OperationalGene]:
        """Returns all genes in a specific functional chromosome"""
        gene_uids = self.chromosomes.get(chromosome, [])
        return [self.genes[uid] for uid in gene_uids if uid in self.genes]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Returns comprehensive statistics about the genome"""
        total_codons = sum(len(gene.codons) for gene in self.genes.values())
        active_genes = sum(1 for g in self.genes.values() if g.status == GeneStatus.ACTIVE)
        avg_fitness = sum(g.get_average_fitness() for g in self.genes.values()) / max(len(self.genes), 1)
        
        return {
            "genome_id": self.genome_id[:16] + "...",
            "name": self.name,
            "total_genes": len(self.genes),
            "active_genes": active_genes,
            "total_codons": total_codons,
            "stems": len(self.stems),
            "chromosomes": len(self.chromosomes),
            "evolution_events": len(self.evolution_history),
            "entities_registered": len(self.entity_registry),
            "actions_registered": len(self.action_registry),
            "states_registered": len(self.state_registry),
            "average_fitness": round(avg_fitness, 3),
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the entire genome to a dictionary"""
        return {
            "genome_id": self.genome_id,
            "name": self.name,
            "genes": {uid: gene.to_dict() for uid, gene in self.genes.items()},
            "stems": dict(self.stems),
            "chromosomes": dict(self.chromosomes),
            "evolution_history": self.evolution_history,
            "entity_registry": self.entity_registry,
            "action_registry": self.action_registry,
            "state_registry": self.state_registry,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Serializes the genome to a JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DigitalGenome':
        """Deserializes a genome from a dictionary"""
        genome = cls(genome_id=data["genome_id"], name=data["name"])
        
        for gene_data in data.get("genes", {}).values():
            gene = OperationalGene.from_dict(gene_data)
            genome.genes[gene.uid] = gene
        
        genome.stems = defaultdict(list, data.get("stems", {}))
        genome.chromosomes = defaultdict(list, data.get("chromosomes", {}))
        genome.evolution_history = data.get("evolution_history", [])
        genome.entity_registry = data.get("entity_registry", {})
        genome.action_registry = data.get("action_registry", {})
        genome.state_registry = data.get("state_registry", {})
        genome.created_at = data.get("created_at", time.time())
        genome.modified_at = data.get("modified_at", time.time())
        
        return genome


# ============================================================================
# COMPUTATIONAL RIBOSOME
# ============================================================================
@dataclass
class ExecutionStep:
    """Represents a single step in gene execution"""
    order: int
    codon: PraxeologicalCodon
    status: ExecutionResult = ExecutionResult.SUCCESS
    output: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class ExecutionPlan:
    """Complete execution plan for a gene"""
    gene_uid: str
    gene_name: str
    steps: List[ExecutionStep]
    total_steps: int
    safety_level: SafetyLevel
    estimated_duration_ms: float
    created_at: float = field(default_factory=time.time)


class ComputationalRibosome:
    """
    Translates operational genes into executable instructions.
    
    Just as biological ribosomes translate mRNA into proteins,
    the Computational Ribosome translates genes into action sequences
    that can be executed in the operational environment.
    """
    
    def __init__(self, genome: DigitalGenome):
        """
        Initializes the ribosome with a reference to the genome.
        
        Args:
            genome: The Digital Genome containing genes to translate
        """
        self.genome = genome
        self.translation_cache: Dict[str, ExecutionPlan] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def translate_gene(self, gene_uid: str) -> ExecutionPlan:
        """
        Translates a gene into an executable plan.
        
        Args:
            gene_uid: The unique identifier of the gene to translate
            
        Returns:
            An ExecutionPlan containing all steps to execute
            
        Raises:
            ValueError: If the gene is not found or is not active
        """
        # Check cache first
        if gene_uid in self.translation_cache:
            logger.debug(f"Using cached translation for gene {gene_uid[:16]}...")
            return self.translation_cache[gene_uid]
        
        gene = self.genome.get_gene(gene_uid)
        if not gene:
            raise ValueError(f"Gene not found: {gene_uid}")
        
        if gene.status != GeneStatus.ACTIVE:
            raise ValueError(f"Gene is not active: {gene.name} (status: {gene.status.value})")
        
        # Build execution steps from codons
        steps = []
        for i, codon in enumerate(gene.codons):
            step = ExecutionStep(
                order=i + 1,
                codon=codon,
                status=ExecutionResult.SUCCESS,  # Will be updated during execution
                output={}
            )
            steps.append(step)
        
        # Create execution plan
        plan = ExecutionPlan(
            gene_uid=gene_uid,
            gene_name=gene.name,
            steps=steps,
            total_steps=len(steps),
            safety_level=gene.safety_level,
            estimated_duration_ms=len(steps) * 100  # Rough estimate
        )
        
        # Cache the translation
        self.translation_cache[gene_uid] = plan
        
        logger.info(f"Translated gene '{gene.name}' → {len(steps)} execution steps")
        return plan
    
    def execute_plan(
        self,
        plan: ExecutionPlan,
        context: Dict[str, Any] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a translated plan.
        
        Args:
            plan: The execution plan to run
            context: Runtime context and parameters
            dry_run: If True, simulates execution without side effects
            
        Returns:
            Execution result with status, outputs, and metrics
        """
        context = context or {}
        start_time = time.time()
        
        result = {
            "gene_uid": plan.gene_uid,
            "gene_name": plan.gene_name,
            "dry_run": dry_run,
            "steps_executed": 0,
            "steps_successful": 0,
            "steps_failed": 0,
            "step_results": [],
            "overall_status": ExecutionResult.SUCCESS,
            "start_time": start_time,
            "end_time": None,
            "duration_ms": 0
        }
        
        for step in plan.steps:
            step_start = time.time()
            
            try:
                # Validate preconditions
                preconditions_met = self._check_preconditions(step.codon, context)
                
                if not preconditions_met:
                    step.status = ExecutionResult.ABORTED
                    step.error = "Preconditions not met"
                    result["steps_failed"] += 1
                else:
                    # Execute the step (simulated in this implementation)
                    if not dry_run:
                        step.output = self._execute_codon(step.codon, context)
                    step.status = ExecutionResult.SUCCESS
                    result["steps_successful"] += 1
                    
            except Exception as e:
                step.status = ExecutionResult.FAILURE
                step.error = str(e)
                result["steps_failed"] += 1
                logger.error(f"Step {step.order} failed: {e}")
            
            step.duration_ms = (time.time() - step_start) * 1000
            result["steps_executed"] += 1
            result["step_results"].append({
                "order": step.order,
                "codon": str(step.codon),
                "status": step.status.value,
                "duration_ms": step.duration_ms,
                "error": step.error
            })
            
            # Stop on critical failure
            if step.status == ExecutionResult.FAILURE and step.codon.safety_level == SafetyLevel.CRITICAL:
                result["overall_status"] = ExecutionResult.ABORTED
                break
        
        # Determine overall status
        if result["steps_failed"] > 0:
            if result["steps_successful"] > 0:
                result["overall_status"] = ExecutionResult.PARTIAL
            else:
                result["overall_status"] = ExecutionResult.FAILURE
        
        result["end_time"] = time.time()
        result["duration_ms"] = (result["end_time"] - start_time) * 1000
        
        # Record in history
        self.execution_history.append(result)
        
        logger.info(
            f"Execution complete: {plan.gene_name} → "
            f"{result['overall_status'].value} "
            f"({result['steps_successful']}/{result['steps_executed']} steps, "
            f"{result['duration_ms']:.2f}ms)"
        )
        
        return result
    
    def _check_preconditions(self, codon: PraxeologicalCodon, context: Dict[str, Any]) -> bool:
        """
        Validates that all preconditions for a codon are met.
        In a real implementation, this would check actual system state.
        """
        # Simplified: always return True for demonstration
        # In production, this would validate against real context
        return True
    
    def _execute_codon(self, codon: PraxeologicalCodon, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a single codon.
        In a real implementation, this would interface with actual systems.
        """
        # Simulated execution
        return {
            "entity": codon.entity_id,
            "action_performed": codon.action_id,
            "resulting_state": codon.target_state_id,
            "timestamp": time.time()
        }
    
    def invalidate_cache(self, gene_uid: str = None) -> None:
        """
        Invalidates translation cache.
        
        Args:
            gene_uid: Specific gene to invalidate, or None for all
        """
        if gene_uid:
            self.translation_cache.pop(gene_uid, None)
        else:
            self.translation_cache.clear()


# ============================================================================
# EXAMPLE USAGE AND DEMONSTRATION
# ============================================================================
def create_example_genome() -> DigitalGenome:
    """
    Creates an example genome with sample genes demonstrating
    the core concepts of Operational Genomics.
    """
    # Initialize genome
    genome = DigitalGenome(name="Industrial Operations Genome")
    
    # Register entities
    pump_id = genome.register_entity(
        make_uid("entity", "pump", "401"),
        name="Pump 401",
        entity_type="physical",
        location="Building A",
        criticality="high"
    )
    
    valve_id = genome.register_entity(
        make_uid("entity", "valve", "302"),
        name="Valve 302",
        entity_type="physical",
        location="Building A",
        criticality="medium"
    )
    
    # Register actions
    start_action = genome.register_action(
        make_uid("action", "start"),
        name="Start",
        category="operational"
    )
    
    stop_action = genome.register_action(
        make_uid("action", "stop"),
        name="Stop",
        category="operational"
    )
    
    isolate_action = genome.register_action(
        make_uid("action", "isolate"),
        name="Isolate",
        category="safety"
    )
    
    inspect_action = genome.register_action(
        make_uid("action", "inspect"),
        name="Inspect",
        category="diagnostic"
    )
    
    # Register states
    running_state = genome.register_state(
        make_uid("state", "running"),
        name="Running",
        category="operational"
    )
    
    stopped_state = genome.register_state(
        make_uid("state", "stopped"),
        name="Stopped",
        category="operational"
    )
    
    isolated_state = genome.register_state(
        make_uid("state", "isolated"),
        name="Isolated",
        category="safety"
    )
    
    # Create an Emergency Shutdown Gene
    shutdown_gene = OperationalGene.create(
        name="Emergency Pump Shutdown",
        purpose="Safely transition pump to shutdown mode in case of anomaly",
        executor="safety_system",
        action="emergency_shutdown",
        target="pump_401",
        domain="safety",
        priority="critical"
    )
    
    # Add codons to the gene
    shutdown_gene.add_codon(PraxeologicalCodon(
        entity_id=pump_id,
        action_id=stop_action,
        target_state_id=stopped_state,
        safety_level=SafetyLevel.CRITICAL,
        preconditions=("pump_running",),
        postconditions=("pump_stopped",)
    ))
    
    shutdown_gene.add_codon(PraxeologicalCodon(
        entity_id=valve_id,
        action_id=isolate_action,
        target_state_id=isolated_state,
        safety_level=SafetyLevel.CRITICAL,
        preconditions=("valve_open",),
        postconditions=("valve_isolated",)
    ))
    
    shutdown_gene.add_codon(PraxeologicalCodon(
        entity_id=pump_id,
        action_id=inspect_action,
        target_state_id=stopped_state,
        safety_level=SafetyLevel.WARNING,
        preconditions=("pump_stopped", "valve_isolated"),
        postconditions=("inspection_complete",)
    ))
    
    # Configure gene
    shutdown_gene.activation_conditions = [
        "vibration_level > threshold",
        "temperature > safe_limit",
        "operator_authorization = true"
    ]
    shutdown_gene.postconditions = [
        "equipment_status = 'safe_shutdown'",
        "inspection_log_created = true"
    ]
    shutdown_gene.exception_handlers = {
        "valve_stuck": "escalate_to_manual_intervention",
        "communication_failure": "activate_local_shutdown"
    }
    shutdown_gene.evaluation_metrics = [
        "shutdown_time_ms",
        "safety_compliance_score",
        "equipment_integrity"
    ]
    shutdown_gene.activate()
    
    # Insert into genome
    genome.insert_gene(shutdown_gene, stem="safety", chromosome="critical_operations")
    
    # Create a Routine Inspection Gene
    inspection_gene = OperationalGene.create(
        name="Routine Equipment Inspection",
        purpose="Perform standard inspection procedures on equipment",
        executor="maintenance_system",
        action="routine_inspection",
        target="general_equipment",
        domain="maintenance",
        priority="normal"
    )
    
    inspection_gene.add_codon(PraxeologicalCodon(
        entity_id=pump_id,
        action_id=inspect_action,
        target_state_id=running_state,
        safety_level=SafetyLevel.INFO,
        context={"inspection_type": "visual"}
    ))
    
    inspection_gene.activate()
    genome.insert_gene(inspection_gene, stem="maintenance", chromosome="routine_operations")
    
    return genome


def demonstration():
    """
    Demonstrates the core functionality of the Digital Genome framework.
    """
    print("\n" + "=" * 70)
    print("OPERATIONAL GENOMICS - DIGITAL GENOME DEMONSTRATION")
    print("Framework for Coherent, Evolutive Operational Knowledge Systems")
    print("=" * 70)
    
    # Create genome with example data
    print("\n📦 Creating Digital Genome...")
    genome = create_example_genome()
    
    # Display statistics
    stats = genome.get_statistics()
    print(f"\n📊 Genome Statistics:")
    print(f"   • Name: {stats['name']}")
    print(f"   • Total Genes: {stats['total_genes']}")
    print(f"   • Active Genes: {stats['active_genes']}")
    print(f"   • Total Codons: {stats['total_codons']}")
    print(f"   • Stems: {stats['stems']}")
    print(f"   • Chromosomes: {stats['chromosomes']}")
    print(f"   • Entities Registered: {stats['entities_registered']}")
    print(f"   • Actions Registered: {stats['actions_registered']}")
    print(f"   • States Registered: {stats['states_registered']}")
    
    # Initialize ribosome
    print(f"\n🔬 Initializing Computational Ribosome...")
    ribosome = ComputationalRibosome(genome)
    
    # Find and execute a gene
    print(f"\n🔍 Searching for safety-related genes...")
    safety_genes = genome.find_genes_by_context("shutdown")
    
    if safety_genes:
        gene = safety_genes[0]
        print(f"   Found: {gene.name}")
        print(f"   Purpose: {gene.purpose}")
        print(f"   Codons: {len(gene.codons)}")
        print(f"   Safety Level: {gene.safety_level.value}")
        
        # Translate gene
        print(f"\n⚙️  Translating gene to execution plan...")
        plan = ribosome.translate_gene(gene.uid)
        print(f"   Steps: {plan.total_steps}")
        print(f"   Estimated Duration: {plan.estimated_duration_ms}ms")
        
        # Execute (dry run)
        print(f"\n▶️  Executing gene (dry run)...")
        result = ribosome.execute_plan(plan, dry_run=True)
        print(f"   Status: {result['overall_status'].value}")
        print(f"   Steps Executed: {result['steps_executed']}")
        print(f"   Steps Successful: {result['steps_successful']}")
        print(f"   Duration: {result['duration_ms']:.2f}ms")
    
    # Export genome
    print(f"\n💾 Genome can be exported to JSON for persistence")
    print(f"   Use: genome.to_json() or genome.to_dict()")
    
    print("\n" + "=" * 70)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    return genome, ribosome


if __name__ == "__main__":
    genome, ribosome = demonstration()
