"""
Cognitive Core - Intelligence Engine for Operational Genomics
=============================================================
The unified reasoning engine that evaluates context, interprets intent,
selects operational genes, and evolves the knowledge base through evidence.

This module implements:
- Context Evaluator: Transforms raw data into structured, actionable context
- Inference Engine: Matches intent + context to optimal genes
- Simulation Engine: Validates decisions across multiple scenarios
- Oracle Synthesizer: Produces final, safe, explainable decisions
- Merism Evolution Engine: Generates and tests gene variations

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
import random
import math
import logging

# Import core components
from digital_genome_core import (
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    ComputationalRibosome,
    SafetyLevel,
    GeneStatus,
    ExecutionResult,
    make_uid
)

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CognitiveCore")


# ============================================================================
# DATA STRUCTURES FOR COGNITIVE PROCESSING
# ============================================================================
@dataclass
class ContextSnapshot:
    """
    A structured, time-bound description of the operational world state.
    
    This is the input that the Cognitive Core uses to make decisions.
    It captures sensor data, system states, and environmental conditions.
    """
    snapshot_id: str
    captured_at: float
    source_systems: List[str]
    raw_data: Dict[str, Any]
    normalized_data: Dict[str, Any] = field(default_factory=dict)
    semantic_bindings: Dict[str, str] = field(default_factory=dict)
    integrity_score: float = 1.0
    safety_flags: List[str] = field(default_factory=list)
    features: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def create(cls, source_systems: List[str], data: Dict[str, Any]) -> 'ContextSnapshot':
        """Factory method to create a new context snapshot"""
        return cls(
            snapshot_id=make_uid("context", str(time.time()), str(random.random())),
            captured_at=time.time(),
            source_systems=source_systems,
            raw_data=data
        )
    
    def compute_context_score(self) -> float:
        """Computes a composite score representing context quality"""
        base_score = self.integrity_score
        penalty = len(self.safety_flags) * 0.1
        return max(0.0, min(1.0, base_score - penalty))


@dataclass
class HighLevelIntent:
    """
    Represents what an operator or system is trying to achieve.
    
    Intent is the starting point for all cognitive processing.
    It captures the goal, constraints, and priorities.
    """
    intent_id: str
    purpose: str
    target_entities: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"  # low, normal, high, critical
    operator_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    
    @classmethod
    def create(cls, purpose: str, **kwargs) -> 'HighLevelIntent':
        """Factory method to create a new intent"""
        return cls(
            intent_id=make_uid("intent", purpose, str(time.time())),
            purpose=purpose,
            **kwargs
        )


@dataclass
class CandidateGene:
    """A gene being considered for selection, with associated scores"""
    gene: OperationalGene
    safety_score: float = 1.0
    context_score: float = 0.0
    intent_alignment: float = 0.0
    fitness_score: float = 0.0
    composite_score: float = 0.0
    rationale: List[str] = field(default_factory=list)
    
    def compute_composite(
        self,
        w_safety: float = 0.4,
        w_context: float = 0.25,
        w_intent: float = 0.25,
        w_fitness: float = 0.1
    ) -> float:
        """
        Computes weighted composite score.
        Safety always has the highest weight.
        """
        self.composite_score = (
            w_safety * self.safety_score +
            w_context * self.context_score +
            w_intent * self.intent_alignment +
            w_fitness * self.fitness_score
        )
        return self.composite_score


@dataclass
class InferenceResult:
    """Result of the inference process"""
    selected_gene_uid: Optional[str]
    selected_gene_name: Optional[str]
    ranked_candidates: List[CandidateGene]
    explanation: Dict[str, Any]
    confidence: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class SimulationWorldline:
    """A single possible evolution path through a scenario"""
    worldline_id: str
    initial_state: Dict[str, Any]
    states: List[Dict[str, Any]]
    success: bool
    metrics: Dict[str, float]
    failure_point: Optional[int] = None


@dataclass 
class SimulationResult:
    """Result of multi-world simulation"""
    request_id: str
    gene_uid: str
    worldlines: List[SimulationWorldline]
    success_rate: float
    robustness_index: float
    worst_case_loss: float
    safety_flags: List[str]
    meta_robustness: Optional[float] = None


@dataclass
class EvolutionProposal:
    """A proposed modification to a gene"""
    proposal_id: str
    proposal_type: str  # "variation", "anti_gene", "parameter_tune"
    base_gene_uid: str
    modifications: Dict[str, Any]
    predicted_improvement: float
    rationale: str
    simulation_validated: bool = False


# ============================================================================
# CONTEXT EVALUATOR
# ============================================================================
class ContextEvaluator:
    """
    Transforms raw environmental information into structured, actionable context.
    
    The Context Evaluator is the bridge between heterogeneous data sources
    and the reasoning modules of the Cognitive Core. It normalizes, validates,
    and enriches data before it can be used for decision-making.
    """
    
    def __init__(self, genome: DigitalGenome):
        self.genome = genome
        self.validation_rules: List[Callable] = []
        self.normalization_functions: Dict[str, Callable] = {}
        
    def evaluate(self, raw_data: Dict[str, Any], sources: List[str]) -> ContextSnapshot:
        """
        Processes raw data into a validated context snapshot.
        
        Args:
            raw_data: Unprocessed data from various sources
            sources: List of source system identifiers
            
        Returns:
            A fully evaluated ContextSnapshot
        """
        snapshot = ContextSnapshot.create(sources, raw_data)
        
        # Step 1: Normalize data
        snapshot.normalized_data = self._normalize(raw_data)
        
        # Step 2: Bind to semantic entities
        snapshot.semantic_bindings = self._bind_semantics(snapshot.normalized_data)
        
        # Step 3: Validate integrity
        issues = self._validate(snapshot)
        if issues:
            snapshot.integrity_score = 1.0 - (len(issues) * 0.1)
            snapshot.safety_flags = issues
        
        # Step 4: Extract features
        snapshot.features = self._extract_features(snapshot)
        
        logger.info(
            f"Context evaluated: {len(raw_data)} inputs → "
            f"integrity={snapshot.integrity_score:.2f}, "
            f"features={len(snapshot.features)}"
        )
        
        return snapshot
    
    def _normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes raw data to standard formats"""
        normalized = {}
        
        for key, value in raw_data.items():
            # Apply registered normalization function if available
            if key in self.normalization_functions:
                normalized[key] = self.normalization_functions[key](value)
            else:
                # Default normalization
                if isinstance(value, (int, float)):
                    normalized[key] = float(value)
                elif isinstance(value, str):
                    normalized[key] = value.lower().strip()
                else:
                    normalized[key] = value
                    
        return normalized
    
    def _bind_semantics(self, normalized_data: Dict[str, Any]) -> Dict[str, str]:
        """Binds data fields to semantic entities in the genome"""
        bindings = {}
        
        for key in normalized_data:
            # Check entity registry
            for entity_id, entity_info in self.genome.entity_registry.items():
                if key.lower() in entity_info["name"].lower():
                    bindings[key] = entity_id
                    break
                    
        return bindings
    
    def _validate(self, snapshot: ContextSnapshot) -> List[str]:
        """Validates context for integrity and safety issues"""
        issues = []
        
        # Check for missing essential fields
        if not snapshot.normalized_data:
            issues.append("empty_context")
        
        # Check for contradictory states
        # (Simplified - real implementation would be more sophisticated)
        
        # Check safety thresholds
        for key, value in snapshot.normalized_data.items():
            if isinstance(value, (int, float)):
                if "temperature" in key.lower() and value > 100:
                    issues.append(f"high_temperature:{key}")
                if "pressure" in key.lower() and value > 1000:
                    issues.append(f"high_pressure:{key}")
                    
        return issues
    
    def _extract_features(self, snapshot: ContextSnapshot) -> Dict[str, float]:
        """Extracts high-level features from context"""
        features = {}
        
        # Compute risk level
        risk_indicators = len(snapshot.safety_flags)
        features["risk_level"] = min(1.0, risk_indicators * 0.2)
        
        # Compute data quality
        features["data_quality"] = snapshot.integrity_score
        
        # Compute operational load (simplified)
        numeric_values = [
            v for v in snapshot.normalized_data.values()
            if isinstance(v, (int, float))
        ]
        if numeric_values:
            features["operational_load"] = sum(numeric_values) / len(numeric_values) / 100
            
        return features


# ============================================================================
# INFERENCE ENGINE
# ============================================================================
class InferenceEngine:
    """
    The logical nucleus of the Cognitive Core.
    
    Evaluates intent and context, matches them to candidate genes,
    simulates potential outcomes, and ranks options to produce
    safe, explainable decisions.
    """
    
    def __init__(self, genome: DigitalGenome, context_evaluator: ContextEvaluator):
        self.genome = genome
        self.context_evaluator = context_evaluator
        self.safety_threshold = 0.6
        self.weights = {
            "safety": 0.4,
            "context": 0.25,
            "intent": 0.25,
            "fitness": 0.1
        }
        
    def infer(
        self,
        intent: HighLevelIntent,
        context: ContextSnapshot
    ) -> InferenceResult:
        """
        Main inference process: intent + context → selected gene.
        
        Args:
            intent: What the operator/system wants to achieve
            context: Current state of the operational environment
            
        Returns:
            InferenceResult with selected gene and explanation
        """
        logger.info(f"Starting inference for intent: {intent.purpose}")
        
        # Step 1: Find candidate genes
        candidates = self._find_candidates(intent, context)
        
        if not candidates:
            return InferenceResult(
                selected_gene_uid=None,
                selected_gene_name=None,
                ranked_candidates=[],
                explanation={"reason": "No suitable genes found"},
                confidence=0.0
            )
        
        # Step 2: Score candidates
        scored_candidates = self._score_candidates(candidates, intent, context)
        
        # Step 3: Apply safety filter
        safe_candidates = self._apply_safety_filter(scored_candidates)
        
        if not safe_candidates:
            return InferenceResult(
                selected_gene_uid=None,
                selected_gene_name=None,
                ranked_candidates=scored_candidates,
                explanation={"reason": "All candidates failed safety filter"},
                confidence=0.0
            )
        
        # Step 4: Rank and select
        ranked = sorted(safe_candidates, key=lambda c: c.composite_score, reverse=True)
        selected = ranked[0]
        
        # Build explanation
        explanation = {
            "selected_gene": selected.gene.name,
            "selection_reason": selected.rationale,
            "scores": {
                "safety": selected.safety_score,
                "context": selected.context_score,
                "intent_alignment": selected.intent_alignment,
                "fitness": selected.fitness_score,
                "composite": selected.composite_score
            },
            "alternatives_considered": len(ranked) - 1,
            "rejected_for_safety": len(scored_candidates) - len(safe_candidates)
        }
        
        logger.info(
            f"Inference complete: selected '{selected.gene.name}' "
            f"with confidence {selected.composite_score:.3f}"
        )
        
        return InferenceResult(
            selected_gene_uid=selected.gene.uid,
            selected_gene_name=selected.gene.name,
            ranked_candidates=ranked,
            explanation=explanation,
            confidence=selected.composite_score
        )
    
    def _find_candidates(
        self,
        intent: HighLevelIntent,
        context: ContextSnapshot
    ) -> List[CandidateGene]:
        """Finds genes that could potentially satisfy the intent"""
        candidates = []
        
        # Search by purpose/context keywords
        purpose_genes = self.genome.find_genes_by_context(intent.purpose)
        
        # Search by target entities
        for entity_id in intent.target_entities:
            entity_genes = self.genome.find_genes_by_context(entity_id)
            purpose_genes.extend(entity_genes)
        
        # Remove duplicates and create candidates
        seen_uids = set()
        for gene in purpose_genes:
            if gene.uid not in seen_uids and gene.status == GeneStatus.ACTIVE:
                candidates.append(CandidateGene(gene=gene))
                seen_uids.add(gene.uid)
        
        return candidates
    
    def _score_candidates(
        self,
        candidates: List[CandidateGene],
        intent: HighLevelIntent,
        context: ContextSnapshot
    ) -> List[CandidateGene]:
        """Scores each candidate on multiple dimensions"""
        for candidate in candidates:
            gene = candidate.gene
            
            # Safety score (based on gene's safety level)
            if gene.safety_level == SafetyLevel.CRITICAL:
                candidate.safety_score = 0.7
            elif gene.safety_level == SafetyLevel.WARNING:
                candidate.safety_score = 0.85
            else:
                candidate.safety_score = 1.0
            
            # Adjust for context safety flags
            if context.safety_flags:
                candidate.safety_score *= (1.0 - len(context.safety_flags) * 0.05)
            
            # Context score (how well gene fits current context)
            context_score = context.compute_context_score()
            candidate.context_score = context_score
            
            # Intent alignment (keyword matching - simplified)
            purpose_lower = intent.purpose.lower()
            gene_purpose_lower = gene.purpose.lower()
            
            # Count matching words
            purpose_words = set(purpose_lower.split())
            gene_words = set(gene_purpose_lower.split())
            overlap = len(purpose_words & gene_words)
            candidate.intent_alignment = min(1.0, overlap / max(len(purpose_words), 1) * 2)
            
            # Fitness score (historical performance)
            candidate.fitness_score = gene.get_average_fitness()
            if candidate.fitness_score == 0:
                candidate.fitness_score = 0.5  # Default for new genes
            
            # Compute composite
            candidate.compute_composite(**self.weights)
            
            # Build rationale
            candidate.rationale = [
                f"Safety: {candidate.safety_score:.2f}",
                f"Context fit: {candidate.context_score:.2f}",
                f"Intent match: {candidate.intent_alignment:.2f}",
                f"Historical fitness: {candidate.fitness_score:.2f}"
            ]
        
        return candidates
    
    def _apply_safety_filter(
        self,
        candidates: List[CandidateGene]
    ) -> List[CandidateGene]:
        """Removes candidates that don't meet safety requirements"""
        return [c for c in candidates if c.safety_score >= self.safety_threshold]


# ============================================================================
# SIMULATION ENGINE
# ============================================================================
class SimulationEngine:
    """
    Creates synthetic futures and validates decisions before execution.
    
    The Simulation Engine is the only component capable of evaluating
    decisions under both known uncertainty and paradigm-shifting scenarios.
    It produces worldlines representing complete possible evolutions.
    """
    
    def __init__(self, genome: DigitalGenome):
        self.genome = genome
        self.default_worldline_count = 10
        self.chaos_levels = [0.0, 0.3, 0.6, 0.9]
        
    def simulate(
        self,
        gene: OperationalGene,
        context: ContextSnapshot,
        worldline_count: int = None,
        max_chaos: float = 0.6
    ) -> SimulationResult:
        """
        Simulates gene execution across multiple possible futures.
        
        Args:
            gene: The gene to simulate
            context: Starting context
            worldline_count: Number of worldlines to generate
            max_chaos: Maximum chaos level to test
            
        Returns:
            SimulationResult with statistics across all worldlines
        """
        worldline_count = worldline_count or self.default_worldline_count
        worldlines = []
        
        logger.info(f"Simulating gene '{gene.name}' across {worldline_count} worldlines")
        
        for i in range(worldline_count):
            # Determine chaos level for this worldline
            chaos = random.uniform(0, max_chaos)
            
            # Generate worldline
            worldline = self._generate_worldline(gene, context, chaos, i)
            worldlines.append(worldline)
        
        # Compute aggregate metrics
        successes = sum(1 for w in worldlines if w.success)
        success_rate = successes / len(worldlines)
        
        # Robustness: variance in success across chaos levels
        success_by_chaos = defaultdict(list)
        for w in worldlines:
            chaos_bucket = round(w.metrics.get("chaos_level", 0), 1)
            success_by_chaos[chaos_bucket].append(1 if w.success else 0)
        
        variances = [
            sum(v) / len(v) for v in success_by_chaos.values() if v
        ]
        robustness = 1.0 - (max(variances) - min(variances)) if len(variances) > 1 else 1.0
        
        # Worst case loss
        all_losses = [w.metrics.get("loss", 0) for w in worldlines]
        worst_case = max(all_losses) if all_losses else 0
        
        # Safety flags
        safety_flags = []
        if success_rate < 0.5:
            safety_flags.append("low_success_rate")
        if worst_case > 0.8:
            safety_flags.append("high_worst_case_loss")
        if robustness < 0.5:
            safety_flags.append("low_robustness")
        
        result = SimulationResult(
            request_id=make_uid("sim", gene.uid, str(time.time())),
            gene_uid=gene.uid,
            worldlines=worldlines,
            success_rate=success_rate,
            robustness_index=robustness,
            worst_case_loss=worst_case,
            safety_flags=safety_flags
        )
        
        logger.info(
            f"Simulation complete: success_rate={success_rate:.2f}, "
            f"robustness={robustness:.2f}, flags={len(safety_flags)}"
        )
        
        return result
    
    def _generate_worldline(
        self,
        gene: OperationalGene,
        context: ContextSnapshot,
        chaos: float,
        index: int
    ) -> SimulationWorldline:
        """Generates a single simulated worldline"""
        worldline_id = make_uid("worldline", gene.uid, str(index), str(chaos))
        
        initial_state = {
            "context_score": context.compute_context_score(),
            "gene_fitness": gene.get_average_fitness(),
            "chaos_level": chaos
        }
        
        states = [initial_state]
        success = True
        failure_point = None
        
        # Simulate each codon execution
        for i, codon in enumerate(gene.codons):
            # Probability of success decreases with chaos
            base_success_prob = 0.95 - (chaos * 0.4)
            
            # Adjust for safety level
            if codon.safety_level == SafetyLevel.CRITICAL:
                base_success_prob *= 0.9
            
            # Random outcome
            step_success = random.random() < base_success_prob
            
            state = {
                "step": i + 1,
                "codon": str(codon),
                "success": step_success,
                "cumulative_success": success and step_success
            }
            states.append(state)
            
            if not step_success:
                success = False
                if failure_point is None:
                    failure_point = i + 1
        
        # Compute metrics
        metrics = {
            "chaos_level": chaos,
            "steps_completed": len([s for s in states if s.get("success", True)]),
            "total_steps": len(gene.codons),
            "loss": 0 if success else (1.0 - (failure_point / len(gene.codons)) if failure_point else 1.0)
        }
        
        return SimulationWorldline(
            worldline_id=worldline_id,
            initial_state=initial_state,
            states=states,
            success=success,
            metrics=metrics,
            failure_point=failure_point
        )


# ============================================================================
# MERISM EVOLUTION ENGINE
# ============================================================================
class MerismEvolutionEngine:
    """
    The evolutionary subsystem of the Cognitive Core.
    
    Merism explores, proposes, validates, and governs new possibilities
    that don't exist yet in the Digital Genome. It operates as a
    consultative layer, never enforcing changes without validation.
    
    Evolution follows: variation → evaluation → selection → inheritance
    """
    
    def __init__(self, genome: DigitalGenome, simulation_engine: SimulationEngine):
        self.genome = genome
        self.simulation_engine = simulation_engine
        self.mutation_rate = 0.1
        self.improvement_threshold = 0.1
        self.proposal_history: List[EvolutionProposal] = []
        
    def generate_variations(
        self,
        base_gene: OperationalGene,
        context: ContextSnapshot,
        count: int = 3
    ) -> List[EvolutionProposal]:
        """
        Generates variation proposals for a gene.
        
        Args:
            base_gene: The gene to create variations of
            context: Current context informing variations
            count: Number of variations to generate
            
        Returns:
            List of EvolutionProposals
        """
        proposals = []
        
        for i in range(count):
            variation_type = random.choice([
                "parameter_adjustment",
                "codon_reordering",
                "threshold_modification",
                "exception_enhancement"
            ])
            
            modifications = self._generate_modification(base_gene, variation_type)
            predicted_improvement = random.uniform(-0.1, 0.3)  # Simplified prediction
            
            proposal = EvolutionProposal(
                proposal_id=make_uid("proposal", base_gene.uid, str(i), str(time.time())),
                proposal_type="variation",
                base_gene_uid=base_gene.uid,
                modifications={
                    "type": variation_type,
                    "changes": modifications
                },
                predicted_improvement=predicted_improvement,
                rationale=f"Variation based on {variation_type} to improve {base_gene.name}"
            )
            proposals.append(proposal)
        
        logger.info(f"Generated {len(proposals)} variation proposals for '{base_gene.name}'")
        return proposals
    
    def _generate_modification(
        self,
        gene: OperationalGene,
        modification_type: str
    ) -> Dict[str, Any]:
        """Generates specific modifications based on type"""
        if modification_type == "parameter_adjustment":
            return {
                "target": "metadata",
                "adjustment": random.uniform(0.9, 1.1)
            }
        elif modification_type == "codon_reordering":
            return {
                "target": "codon_sequence",
                "swap_positions": [
                    random.randint(0, max(0, len(gene.codons) - 1)),
                    random.randint(0, max(0, len(gene.codons) - 1))
                ]
            }
        elif modification_type == "threshold_modification":
            return {
                "target": "activation_conditions",
                "threshold_change": random.uniform(-0.1, 0.1)
            }
        else:
            return {
                "target": "exception_handlers",
                "enhancement": "add_fallback"
            }
    
    def generate_anti_gene(
        self,
        base_gene: OperationalGene,
        reason: str
    ) -> EvolutionProposal:
        """
        Generates an anti-gene: a disruptive alternative that takes
        a fundamentally different approach to achieving the same purpose.
        
        Args:
            base_gene: The gene to create an alternative for
            reason: Why an anti-gene is needed
            
        Returns:
            An EvolutionProposal for the anti-gene
        """
        proposal = EvolutionProposal(
            proposal_id=make_uid("antigene", base_gene.uid, str(time.time())),
            proposal_type="anti_gene",
            base_gene_uid=base_gene.uid,
            modifications={
                "approach": "inverse_logic",
                "original_codons": len(base_gene.codons),
                "restructure": True
            },
            predicted_improvement=random.uniform(0.1, 0.4),
            rationale=f"Anti-gene for '{base_gene.name}': {reason}"
        )
        
        self.proposal_history.append(proposal)
        logger.info(f"Generated anti-gene proposal for '{base_gene.name}'")
        
        return proposal
    
    def validate_proposal(
        self,
        proposal: EvolutionProposal,
        context: ContextSnapshot
    ) -> bool:
        """
        Validates a proposal through simulation.
        
        Args:
            proposal: The proposal to validate
            context: Context for simulation
            
        Returns:
            True if the proposal passes validation
        """
        base_gene = self.genome.get_gene(proposal.base_gene_uid)
        if not base_gene:
            return False
        
        # Simulate the base gene for comparison
        base_result = self.simulation_engine.simulate(base_gene, context, worldline_count=5)
        
        # For now, we approve if predicted improvement is positive
        # In a real implementation, we would create and simulate the variant
        passes = (
            proposal.predicted_improvement > self.improvement_threshold and
            base_result.success_rate > 0.5
        )
        
        proposal.simulation_validated = passes
        
        logger.info(
            f"Proposal validation: {proposal.proposal_id[:16]}... "
            f"{'PASSED' if passes else 'FAILED'}"
        )
        
        return passes
    
    def apply_evolution(
        self,
        proposal: EvolutionProposal
    ) -> Optional[OperationalGene]:
        """
        Applies a validated proposal to create a new gene version.
        
        Args:
            proposal: A validated EvolutionProposal
            
        Returns:
            The new gene if successful, None otherwise
        """
        if not proposal.simulation_validated:
            logger.warning("Cannot apply unvalidated proposal")
            return None
        
        base_gene = self.genome.get_gene(proposal.base_gene_uid)
        if not base_gene:
            return None
        
        # Create new version
        new_version = self._increment_version(base_gene.version)
        
        new_gene = OperationalGene(
            uid=make_uid("gene", base_gene.uid, new_version, str(time.time())),
            name=f"{base_gene.name} (v{new_version})",
            purpose=base_gene.purpose,
            version=new_version,
            status=GeneStatus.DRAFT,
            codons=list(base_gene.codons),  # Copy codons
            activation_conditions=list(base_gene.activation_conditions),
            postconditions=list(base_gene.postconditions),
            exception_handlers=dict(base_gene.exception_handlers),
            evaluation_metrics=list(base_gene.evaluation_metrics),
            metadata=dict(base_gene.metadata),
            parent_genes=[base_gene.uid]
        )
        
        # Apply modifications (simplified)
        new_gene.metadata["evolution_applied"] = proposal.proposal_id
        new_gene.metadata["evolution_type"] = proposal.proposal_type
        
        logger.info(f"Evolution applied: created '{new_gene.name}'")
        
        return new_gene
    
    def _increment_version(self, version: str) -> str:
        """Increments semantic version"""
        parts = version.split(".")
        if len(parts) == 3:
            parts[2] = str(int(parts[2]) + 1)
        return ".".join(parts)


# ============================================================================
# ORACLE SYNTHESIZER
# ============================================================================
class OracleSynthesizer:
    """
    The apex component of the Cognitive Core.
    
    Unifies inference, simulation, context evaluation, and evolutionary
    hypotheses into a single integrated decision. The Oracle ensures
    every decision is safe, robust, and fully explainable.
    """
    
    def __init__(
        self,
        genome: DigitalGenome,
        context_evaluator: ContextEvaluator,
        inference_engine: InferenceEngine,
        simulation_engine: SimulationEngine,
        evolution_engine: MerismEvolutionEngine
    ):
        self.genome = genome
        self.context_evaluator = context_evaluator
        self.inference_engine = inference_engine
        self.simulation_engine = simulation_engine
        self.evolution_engine = evolution_engine
        self.ribosome = ComputationalRibosome(genome)
        self.decision_history: List[Dict[str, Any]] = []
        
    def synthesize_decision(
        self,
        intent: HighLevelIntent,
        raw_context: Dict[str, Any],
        context_sources: List[str]
    ) -> Dict[str, Any]:
        """
        Synthesizes a complete, validated decision from intent and context.
        
        This is the main entry point for cognitive processing.
        
        Args:
            intent: What the operator/system wants to achieve
            raw_context: Raw data from operational environment
            context_sources: List of data source identifiers
            
        Returns:
            Complete decision with execution plan and explanation
        """
        start_time = time.time()
        
        logger.info(f"Oracle synthesizing decision for: {intent.purpose}")
        
        decision = {
            "decision_id": make_uid("decision", intent.intent_id, str(start_time)),
            "intent": intent.purpose,
            "timestamp": start_time,
            "stages": [],
            "selected_gene": None,
            "execution_plan": None,
            "explanation": {},
            "success": False
        }
        
        try:
            # Stage 1: Context Evaluation
            context = self.context_evaluator.evaluate(raw_context, context_sources)
            decision["stages"].append({
                "stage": "context_evaluation",
                "success": True,
                "integrity_score": context.integrity_score,
                "safety_flags": context.safety_flags
            })
            
            # Stage 2: Inference
            inference_result = self.inference_engine.infer(intent, context)
            decision["stages"].append({
                "stage": "inference",
                "success": inference_result.selected_gene_uid is not None,
                "candidates_evaluated": len(inference_result.ranked_candidates),
                "confidence": inference_result.confidence
            })
            
            if not inference_result.selected_gene_uid:
                decision["explanation"] = inference_result.explanation
                return decision
            
            # Stage 3: Simulation Validation
            selected_gene = self.genome.get_gene(inference_result.selected_gene_uid)
            simulation_result = self.simulation_engine.simulate(
                selected_gene, context, worldline_count=10
            )
            decision["stages"].append({
                "stage": "simulation",
                "success": simulation_result.success_rate >= 0.6,
                "success_rate": simulation_result.success_rate,
                "robustness": simulation_result.robustness_index,
                "safety_flags": simulation_result.safety_flags
            })
            
            # Check simulation results
            if simulation_result.success_rate < 0.6:
                decision["explanation"] = {
                    "reason": "Gene failed simulation validation",
                    "success_rate": simulation_result.success_rate
                }
                
                # Consider evolution
                proposals = self.evolution_engine.generate_variations(
                    selected_gene, context
                )
                decision["evolution_triggered"] = True
                decision["proposals_generated"] = len(proposals)
                
                return decision
            
            # Stage 4: Translation and Execution Plan
            execution_plan = self.ribosome.translate_gene(selected_gene.uid)
            decision["stages"].append({
                "stage": "translation",
                "success": True,
                "steps": execution_plan.total_steps
            })
            
            # Build final decision
            decision["selected_gene"] = {
                "uid": selected_gene.uid,
                "name": selected_gene.name,
                "purpose": selected_gene.purpose,
                "codons": len(selected_gene.codons),
                "safety_level": selected_gene.safety_level.value
            }
            decision["execution_plan"] = {
                "total_steps": execution_plan.total_steps,
                "estimated_duration_ms": execution_plan.estimated_duration_ms,
                "safety_level": execution_plan.safety_level.value
            }
            decision["explanation"] = {
                "inference": inference_result.explanation,
                "simulation": {
                    "success_rate": simulation_result.success_rate,
                    "robustness": simulation_result.robustness_index
                }
            }
            decision["success"] = True
            
        except Exception as e:
            logger.error(f"Oracle error: {e}")
            decision["error"] = str(e)
            
        finally:
            decision["duration_ms"] = (time.time() - start_time) * 1000
            self.decision_history.append(decision)
        
        logger.info(
            f"Oracle decision: {'SUCCESS' if decision['success'] else 'FAILED'} "
            f"in {decision['duration_ms']:.2f}ms"
        )
        
        return decision
    
    def execute_decision(
        self,
        decision: Dict[str, Any],
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Executes a synthesized decision.
        
        Args:
            decision: A decision from synthesize_decision()
            dry_run: If True, simulates execution without side effects
            
        Returns:
            Execution result
        """
        if not decision.get("success"):
            return {"error": "Cannot execute failed decision"}
        
        gene_uid = decision["selected_gene"]["uid"]
        plan = self.ribosome.translate_gene(gene_uid)
        
        return self.ribosome.execute_plan(plan, dry_run=dry_run)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Returns operational statistics"""
        successful_decisions = sum(1 for d in self.decision_history if d.get("success"))
        
        return {
            "total_decisions": len(self.decision_history),
            "successful_decisions": successful_decisions,
            "success_rate": successful_decisions / max(len(self.decision_history), 1),
            "average_duration_ms": sum(
                d.get("duration_ms", 0) for d in self.decision_history
            ) / max(len(self.decision_history), 1),
            "genome_statistics": self.genome.get_statistics(),
            "evolution_proposals": len(self.evolution_engine.proposal_history)
        }


# ============================================================================
# INTEGRATED COGNITIVE SYSTEM
# ============================================================================
class CognitiveSystem:
    """
    Unified cognitive system integrating all components.
    
    This is the main entry point for using the Operational Genomics
    framework. It provides high-level methods for common operations.
    """
    
    def __init__(self, genome: DigitalGenome = None):
        """
        Initializes the complete cognitive system.
        
        Args:
            genome: Optional pre-configured genome. If None, creates empty one.
        """
        self.genome = genome or DigitalGenome(name="Cognitive System Genome")
        self.context_evaluator = ContextEvaluator(self.genome)
        self.inference_engine = InferenceEngine(self.genome, self.context_evaluator)
        self.simulation_engine = SimulationEngine(self.genome)
        self.evolution_engine = MerismEvolutionEngine(
            self.genome, self.simulation_engine
        )
        self.oracle = OracleSynthesizer(
            self.genome,
            self.context_evaluator,
            self.inference_engine,
            self.simulation_engine,
            self.evolution_engine
        )
        
        logger.info("Cognitive System initialized")
    
    def process_objective(
        self,
        objective: str,
        context_data: Dict[str, Any] = None,
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        High-level method to process an objective from intent to execution.
        
        Args:
            objective: Natural language description of what to achieve
            context_data: Current environmental data
            dry_run: If True, simulates without side effects
            
        Returns:
            Complete result including decision and execution
        """
        context_data = context_data or {}
        
        # Create intent
        intent = HighLevelIntent.create(objective)
        
        # Synthesize decision
        decision = self.oracle.synthesize_decision(
            intent,
            context_data,
            ["system_input"]
        )
        
        result = {
            "objective": objective,
            "decision": decision
        }
        
        # Execute if successful
        if decision.get("success"):
            execution = self.oracle.execute_decision(decision, dry_run=dry_run)
            result["execution"] = execution
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Returns complete system status"""
        return self.oracle.get_statistics()


# ============================================================================
# DEMONSTRATION
# ============================================================================
def demonstration():
    """Demonstrates the Cognitive Core capabilities"""
    print("\n" + "=" * 70)
    print("COGNITIVE CORE - OPERATIONAL GENOMICS DEMONSTRATION")
    print("Intelligent Decision Engine for Digital Genome")
    print("=" * 70)
    
    # Import and create example genome
    from digital_genome_core import create_example_genome
    genome = create_example_genome()
    
    # Initialize cognitive system
    print("\n🧠 Initializing Cognitive System...")
    cognitive_system = CognitiveSystem(genome)
    
    # Display initial status
    status = cognitive_system.get_status()
    print(f"\n📊 System Status:")
    print(f"   • Genes in Genome: {status['genome_statistics']['total_genes']}")
    print(f"   • Active Genes: {status['genome_statistics']['active_genes']}")
    print(f"   • Decisions Made: {status['total_decisions']}")
    
    # Test objectives
    test_cases = [
        ("Execute emergency shutdown procedure", {"temperature": 85, "vibration": 7.5}),
        ("Perform routine equipment inspection", {"status": "normal", "schedule": "weekly"}),
        ("Optimize pump performance", {"efficiency": 0.75, "target": 0.90})
    ]
    
    print(f"\n🎯 Processing {len(test_cases)} objectives...")
    
    for objective, context in test_cases:
        print(f"\n   Objective: {objective}")
        
        result = cognitive_system.process_objective(objective, context, dry_run=True)
        decision = result["decision"]
        
        if decision.get("success"):
            print(f"   ✅ Success: Gene '{decision['selected_gene']['name']}'")
            print(f"   📝 Steps: {decision['execution_plan']['total_steps']}")
            print(f"   ⏱️  Duration: {decision['duration_ms']:.2f}ms")
        else:
            print(f"   ❌ Failed: {decision.get('explanation', {}).get('reason', 'Unknown')}")
    
    # Final statistics
    final_status = cognitive_system.get_status()
    print(f"\n📈 Final Statistics:")
    print(f"   • Total Decisions: {final_status['total_decisions']}")
    print(f"   • Success Rate: {final_status['success_rate']:.1%}")
    print(f"   • Avg Duration: {final_status['average_duration_ms']:.2f}ms")
    print(f"   • Evolution Proposals: {final_status['evolution_proposals']}")
    
    print("\n" + "=" * 70)
    print("✅ COGNITIVE CORE DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    return cognitive_system


if __name__ == "__main__":
    system = demonstration()
