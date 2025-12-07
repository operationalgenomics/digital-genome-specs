"""
Cognitive Core - Four Parallel Motors Architecture
===================================================
The reasoning engine that transforms intent and context into decisions
through four motors operating SIMULTANEOUSLY, not sequentially.

CRITICAL ARCHITECTURE:
- Motors are PARALLEL, not sequential
- Each motor asks a fundamental question
- Each motor can issue ABSOLUTE VETO (score = 0)
- Craft Performance = PRODUCT of all motors (not sum, not average)
- The Meta-Motor imagines what SHOULD exist (Platonic function)

THE FOUR MOTORS:
1. Praxeological Motor: "Does this action realize its intention?"
2. Nash Motor: "Does this action produce strategic equilibrium?"
3. Chaotic Motor: "Is this action robust to perturbations?"
4. Meristic Meta-Motor: "Does this reflect universal patterns? What should exist?"

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
import concurrent.futures

from digital_genome_core import (
    DigitalGenome,
    OperationalGene,
    PraxeologicalCodon,
    DNANeuron,
    FoucauldianTruth,
    PlatonicApproximation,
    SafetyLevel,
    GeneStatus,
    TruthType,
    VetoReason,
    make_uid
)

# ============================================================================
# LOGGING
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CognitiveCore")


# ============================================================================
# MOTOR EVALUATION RESULT
# ============================================================================
@dataclass
class MotorEvaluation:
    """
    The result of a single motor's evaluation.
    
    Each motor produces a score in [0, 1] where:
    - 0 = absolute veto (this action MUST NOT happen)
    - 1 = perfect alignment with the motor's criterion
    - Between = degree of alignment
    
    The score is NOT a probability. It's a measure of how close
    the action is to the ideal Form according to this motor's perspective.
    """
    motor_name: str
    score: float  # [0, 1]
    is_veto: bool
    veto_reason: Optional[str]
    confidence: float  # How certain the motor is
    analysis: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    
    @property
    def is_absolute_veto(self) -> bool:
        """Returns True if this is an absolute veto (score = 0)."""
        return self.score == 0.0 or self.is_veto


# ============================================================================
# ABSTRACT MOTOR BASE CLASS
# ============================================================================
class CognitiveMotor(ABC):
    """
    Abstract base class for all cognitive motors.
    
    Each motor operates independently and in parallel with others.
    Each asks a fundamental question about the action being evaluated.
    Each can issue an absolute veto.
    """
    
    def __init__(self, genome: DigitalGenome):
        self.genome = genome
        self.evaluation_history: List[MotorEvaluation] = []
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The motor's identifier."""
        pass
    
    @property
    @abstractmethod
    def fundamental_question(self) -> str:
        """The question this motor asks about every action."""
        pass
    
    @abstractmethod
    def evaluate(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> MotorEvaluation:
        """
        Evaluates a gene in the given context.
        Returns a MotorEvaluation with score [0, 1].
        """
        pass
    
    def _record_evaluation(self, evaluation: MotorEvaluation) -> None:
        """Records an evaluation in history."""
        self.evaluation_history.append(evaluation)


# ============================================================================
# PRAXEOLOGICAL MOTOR
# ============================================================================
class PraxeologicalMotor(CognitiveMotor):
    """
    The motor that evaluates INTENTION REALIZATION.
    
    Fundamental Question: "Does this action realize its intention?"
    
    Based on praxeology - the study of human action. Every action
    has a purpose, and this motor evaluates whether the action
    achieves that purpose.
    
    Veto conditions:
    - The action contradicts its stated intention
    - The action cannot logically achieve its goal
    - The action's preconditions cannot be satisfied
    """
    
    @property
    def name(self) -> str:
        return "Praxeological"
    
    @property
    def fundamental_question(self) -> str:
        return "Does this action realize its intention?"
    
    def evaluate(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> MotorEvaluation:
        """
        Evaluates intention realization.
        
        Score formula:
        Score_P = (IntentAlignment × PreconditionSatisfaction × LogicalCoherence)
        """
        analysis = {
            "intent_stated": intent.get("purpose", gene.purpose),
            "codons_analyzed": len(gene.codons),
            "factors": {}
        }
        
        # Factor 1: Intent alignment
        # Does the gene's purpose align with the stated intent?
        intent_alignment = self._calculate_intent_alignment(gene, intent)
        analysis["factors"]["intent_alignment"] = intent_alignment
        
        # Factor 2: Precondition satisfaction
        # Can the preconditions be satisfied in the current context?
        precondition_satisfaction = self._check_preconditions(gene, context)
        analysis["factors"]["precondition_satisfaction"] = precondition_satisfaction
        
        # Factor 3: Logical coherence
        # Do the codons logically lead to the intended outcome?
        logical_coherence = self._assess_logical_coherence(gene)
        analysis["factors"]["logical_coherence"] = logical_coherence
        
        # Calculate score (product of factors)
        score = intent_alignment * precondition_satisfaction * logical_coherence
        
        # Check for veto conditions
        is_veto = False
        veto_reason = None
        
        if intent_alignment < 0.1:
            is_veto = True
            veto_reason = "Action contradicts stated intention"
            score = 0.0
        elif logical_coherence < 0.1:
            is_veto = True
            veto_reason = "Action cannot logically achieve its goal"
            score = 0.0
        elif precondition_satisfaction == 0:
            is_veto = True
            veto_reason = "Preconditions cannot be satisfied"
            score = 0.0
        
        evaluation = MotorEvaluation(
            motor_name=self.name,
            score=score,
            is_veto=is_veto,
            veto_reason=veto_reason,
            confidence=0.85,
            analysis=analysis
        )
        
        self._record_evaluation(evaluation)
        return evaluation
    
    def _calculate_intent_alignment(self, gene: OperationalGene, intent: Dict[str, Any]) -> float:
        """Calculates how well the gene aligns with the intent."""
        intent_purpose = intent.get("purpose", "").lower()
        gene_purpose = gene.purpose.lower()
        
        # Simple keyword overlap (in production, use semantic similarity)
        intent_words = set(intent_purpose.split())
        gene_words = set(gene_purpose.split())
        
        if not intent_words:
            return 0.5  # No intent specified, neutral
        
        overlap = len(intent_words & gene_words)
        alignment = min(1.0, overlap / len(intent_words) * 2)
        
        return max(0.1, alignment)  # Minimum 0.1 unless veto
    
    def _check_preconditions(self, gene: OperationalGene, context: Dict[str, Any]) -> float:
        """Checks how many preconditions can be satisfied."""
        if not gene.activation_conditions:
            return 1.0  # No preconditions = satisfied
        
        # Simplified: in production, evaluate actual conditions
        satisfied = 0
        for condition in gene.activation_conditions:
            # Check if condition appears satisfiable from context
            condition_key = condition.split()[0].lower() if condition else ""
            if condition_key in [k.lower() for k in context.keys()]:
                satisfied += 1
            else:
                satisfied += 0.5  # Unknown = partial credit
        
        return satisfied / len(gene.activation_conditions)
    
    def _assess_logical_coherence(self, gene: OperationalGene) -> float:
        """Assesses logical coherence of the codon sequence."""
        if not gene.codons:
            return 0.0
        
        # Check that codons form a logical sequence
        # (In production, this would be much more sophisticated)
        coherence = 1.0
        
        for i, codon in enumerate(gene.codons):
            # Each codon should have an entity and action
            if not codon.entity_id or not codon.action_id:
                coherence *= 0.5
            
            # Postconditions should enable next codon's preconditions
            if i > 0:
                prev_codon = gene.codons[i-1]
                if not set(prev_codon.postconditions) & set(codon.preconditions):
                    coherence *= 0.9  # Minor penalty for unclear chain
        
        return coherence


# ============================================================================
# NASH MOTOR
# ============================================================================
class NashMotor(CognitiveMotor):
    """
    The motor that evaluates STRATEGIC EQUILIBRIUM.
    
    Fundamental Question: "Does this action produce equilibrium between agents?"
    
    Based on Nash equilibrium from game theory. In multi-agent systems,
    an action is stable only if no agent can improve their outcome
    by unilaterally changing their behavior.
    
    Veto conditions:
    - The action creates destructive feedback loops
    - No stable equilibrium exists given the action
    - The action exploits agents in ways that trigger retaliation
    - The action requires irrational behavior from others
    """
    
    @property
    def name(self) -> str:
        return "Nash"
    
    @property
    def fundamental_question(self) -> str:
        return "Does this action produce strategic equilibrium?"
    
    def evaluate(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> MotorEvaluation:
        """
        Evaluates strategic stability.
        
        Score formula:
        Score_N = EquilibriumProximity × StabilityFactor × MultiAgentCoherence
        """
        analysis = {
            "agents_identified": [],
            "equilibrium_type": None,
            "factors": {}
        }
        
        # Identify agents involved
        agents = self._identify_agents(gene, context)
        analysis["agents_identified"] = agents
        
        # Factor 1: Equilibrium proximity
        equilibrium_proximity = self._calculate_equilibrium_proximity(gene, agents, context)
        analysis["factors"]["equilibrium_proximity"] = equilibrium_proximity
        
        # Factor 2: Stability factor
        stability = self._assess_stability(gene, agents)
        analysis["factors"]["stability"] = stability
        
        # Factor 3: Multi-agent coherence
        coherence = self._assess_multi_agent_coherence(gene, agents)
        analysis["factors"]["multi_agent_coherence"] = coherence
        
        # Calculate score
        score = equilibrium_proximity * stability * coherence
        
        # Check for veto conditions
        is_veto = False
        veto_reason = None
        
        if stability < 0.1:
            is_veto = True
            veto_reason = "Action creates destructive feedback loops"
            score = 0.0
        elif len(agents) > 1 and equilibrium_proximity < 0.1:
            is_veto = True
            veto_reason = "No stable equilibrium exists"
            score = 0.0
        
        # Determine equilibrium type
        if score > 0.8:
            analysis["equilibrium_type"] = "Pareto optimal"
        elif score > 0.5:
            analysis["equilibrium_type"] = "Nash equilibrium"
        else:
            analysis["equilibrium_type"] = "Unstable"
        
        evaluation = MotorEvaluation(
            motor_name=self.name,
            score=score,
            is_veto=is_veto,
            veto_reason=veto_reason,
            confidence=0.80,
            analysis=analysis
        )
        
        self._record_evaluation(evaluation)
        return evaluation
    
    def _identify_agents(self, gene: OperationalGene, context: Dict[str, Any]) -> List[str]:
        """Identifies agents affected by or affecting the action."""
        agents = set()
        
        # Extract from gene metadata
        if "executor" in gene.metadata:
            agents.add(gene.metadata["executor"])
        if "target" in gene.metadata:
            agents.add(gene.metadata["target"])
        
        # Extract from codons
        for codon in gene.codons:
            agents.add(codon.entity_id)
        
        # Extract from context
        if "agents" in context:
            agents.update(context["agents"])
        
        return list(agents)
    
    def _calculate_equilibrium_proximity(
        self,
        gene: OperationalGene,
        agents: List[str],
        context: Dict[str, Any]
    ) -> float:
        """Calculates how close the action brings the system to equilibrium."""
        if len(agents) <= 1:
            return 1.0  # Single agent = always in equilibrium with self
        
        # Simplified: in production, solve actual game-theoretic model
        # Here we use heuristics based on gene structure
        
        # Check if action benefits all agents or exploits some
        benefit_distribution = 0.8  # Assume reasonable distribution
        
        # Check for reciprocity in codons
        has_reciprocity = any(
            "response" in c.action_id.lower() or "feedback" in c.action_id.lower()
            for c in gene.codons
        )
        if has_reciprocity:
            benefit_distribution += 0.1
        
        return min(1.0, benefit_distribution)
    
    def _assess_stability(self, gene: OperationalGene, agents: List[str]) -> float:
        """Assesses whether the equilibrium is stable."""
        # Check for exception handlers (indicates awareness of instability)
        exception_coverage = len(gene.exception_handlers) / max(len(agents), 1)
        
        stability = 0.7 + min(0.3, exception_coverage * 0.3)
        return stability
    
    def _assess_multi_agent_coherence(self, gene: OperationalGene, agents: List[str]) -> float:
        """Assesses coherence across multiple agents."""
        if len(agents) <= 1:
            return 1.0
        
        # Check if gene considers multiple perspectives
        coherence = 0.8
        
        if gene.postconditions:
            coherence += 0.1  # Has defined outcomes
        if gene.evaluation_metrics:
            coherence += 0.1  # Has metrics for evaluation
        
        return min(1.0, coherence)


# ============================================================================
# CHAOTIC MOTOR
# ============================================================================
class ChaoticMotor(CognitiveMotor):
    """
    The motor that evaluates ROBUSTNESS TO PERTURBATIONS.
    
    Fundamental Question: "Is this action robust to chaos?"
    
    Based on chaos theory and dynamical systems. Many systems exhibit
    sensitive dependence on initial conditions. An action that works
    perfectly under ideal conditions but fails with minor perturbations
    is not truly reliable.
    
    Veto conditions:
    - Action operates near a bifurcation point
    - Basin of attraction is too small
    - Action amplifies perturbations instead of damping them
    - Failure modes include irreversible catastrophes
    """
    
    @property
    def name(self) -> str:
        return "Chaotic"
    
    @property
    def fundamental_question(self) -> str:
        return "Is this action robust to perturbations?"
    
    def evaluate(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> MotorEvaluation:
        """
        Evaluates robustness to chaos.
        
        Score formula:
        Score_C = (1 - NormalizedLyapunov) × BasinSize × PerturbationTolerance
        """
        analysis = {
            "sensitivity_class": None,
            "failure_modes": [],
            "factors": {}
        }
        
        # Factor 1: Lyapunov-like sensitivity
        lyapunov_estimate = self._estimate_sensitivity(gene, context)
        normalized_lyapunov = min(1.0, lyapunov_estimate)
        sensitivity_factor = 1.0 - normalized_lyapunov
        analysis["factors"]["sensitivity"] = sensitivity_factor
        
        # Factor 2: Basin of attraction size
        basin_size = self._estimate_basin_size(gene, context)
        analysis["factors"]["basin_size"] = basin_size
        
        # Factor 3: Perturbation tolerance
        perturbation_tolerance = self._assess_perturbation_tolerance(gene)
        analysis["factors"]["perturbation_tolerance"] = perturbation_tolerance
        
        # Identify failure modes
        failure_modes = self._identify_failure_modes(gene)
        analysis["failure_modes"] = failure_modes
        
        # Calculate score
        score = sensitivity_factor * basin_size * perturbation_tolerance
        
        # Check for veto conditions
        is_veto = False
        veto_reason = None
        
        if any(fm.get("catastrophic", False) for fm in failure_modes):
            is_veto = True
            veto_reason = "Failure mode includes irreversible catastrophe"
            score = 0.0
        elif sensitivity_factor < 0.1:
            is_veto = True
            veto_reason = "Extreme sensitivity to initial conditions"
            score = 0.0
        elif basin_size < 0.1:
            is_veto = True
            veto_reason = "Basin of attraction too small for real-world noise"
            score = 0.0
        
        # Classify sensitivity
        if score > 0.8:
            analysis["sensitivity_class"] = "Stable attractor"
        elif score > 0.5:
            analysis["sensitivity_class"] = "Limit cycle"
        elif score > 0.2:
            analysis["sensitivity_class"] = "Near bifurcation"
        else:
            analysis["sensitivity_class"] = "Chaotic regime"
        
        evaluation = MotorEvaluation(
            motor_name=self.name,
            score=score,
            is_veto=is_veto,
            veto_reason=veto_reason,
            confidence=0.75,
            analysis=analysis
        )
        
        self._record_evaluation(evaluation)
        return evaluation
    
    def _estimate_sensitivity(self, gene: OperationalGene, context: Dict[str, Any]) -> float:
        """Estimates Lyapunov-like sensitivity measure."""
        sensitivity = 0.2  # Base sensitivity
        
        # More codons = more places for perturbations to accumulate
        sensitivity += len(gene.codons) * 0.05
        
        # Critical safety level increases sensitivity concern
        if gene.safety_level == SafetyLevel.CRITICAL:
            sensitivity += 0.2
        
        # Lack of exception handlers increases sensitivity
        if not gene.exception_handlers:
            sensitivity += 0.15
        
        return min(1.0, sensitivity)
    
    def _estimate_basin_size(self, gene: OperationalGene, context: Dict[str, Any]) -> float:
        """Estimates the basin of attraction size."""
        basin = 0.8  # Start optimistic
        
        # Each strict precondition narrows the basin
        for condition in gene.activation_conditions:
            if ">" in condition or "<" in condition or "=" in condition:
                basin -= 0.1  # Strict numeric condition
            else:
                basin -= 0.05  # Qualitative condition
        
        return max(0.1, basin)
    
    def _assess_perturbation_tolerance(self, gene: OperationalGene) -> float:
        """Assesses tolerance to perturbations."""
        tolerance = 0.7
        
        # Exception handlers indicate perturbation awareness
        tolerance += len(gene.exception_handlers) * 0.05
        
        # Postconditions indicate defined success criteria
        if gene.postconditions:
            tolerance += 0.1
        
        return min(1.0, tolerance)
    
    def _identify_failure_modes(self, gene: OperationalGene) -> List[Dict[str, Any]]:
        """Identifies potential failure modes."""
        failure_modes = []
        
        for codon in gene.codons:
            if codon.safety_level == SafetyLevel.CRITICAL:
                failure_modes.append({
                    "codon": str(codon),
                    "type": "critical_failure",
                    "catastrophic": True
                })
        
        if not gene.exception_handlers:
            failure_modes.append({
                "type": "unhandled_exception",
                "catastrophic": False
            })
        
        return failure_modes


# ============================================================================
# MERISTIC META-MOTOR
# ============================================================================
class MeristicMetaMotor(CognitiveMotor):
    """
    The motor that IMAGINES what should exist.
    
    Fundamental Question: "Does this reflect universal patterns? What SHOULD exist?"
    
    This is the Platonic motor - it doesn't just evaluate what IS,
    it imagines what the ideal Form would be. It operates at multiple
    scales (micro, meso, macro) and sees patterns that span domains.
    
    Like Plato's allegory of the cave: while other motors look at shadows,
    the Meta-Motor tries to perceive the Forms that cast those shadows.
    
    The Meta-Motor is CONSULTATIVE - it proposes, never decides.
    It suggests possibilities that don't yet exist in the genome.
    
    Four types of output:
    1. Variants: Modified versions of existing genes
    2. Anti-Genes: Fundamentally different approaches
    3. Hypotheses: Untested possibilities worth exploring
    4. Paradigms: New frameworks for understanding
    """
    
    @property
    def name(self) -> str:
        return "Meristic"
    
    @property
    def fundamental_question(self) -> str:
        return "Does this reflect universal patterns? What should exist?"
    
    def evaluate(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> MotorEvaluation:
        """
        Evaluates pattern universality and imagines improvements.
        
        Score formula:
        Score_M = PatternUniversality × ScaleCoherence × PotentialForImprovement
        """
        analysis = {
            "patterns_detected": [],
            "scale_analysis": {},
            "imagined_improvements": [],
            "factors": {}
        }
        
        # Factor 1: Pattern universality
        patterns = self._detect_patterns(gene)
        analysis["patterns_detected"] = patterns
        pattern_score = self._score_pattern_universality(patterns)
        analysis["factors"]["pattern_universality"] = pattern_score
        
        # Factor 2: Scale coherence (micro/meso/macro)
        scale_analysis = self._analyze_across_scales(gene, context)
        analysis["scale_analysis"] = scale_analysis
        scale_score = scale_analysis.get("coherence", 0.7)
        analysis["factors"]["scale_coherence"] = scale_score
        
        # Factor 3: Potential for improvement
        improvements = self._imagine_improvements(gene, context, intent)
        analysis["imagined_improvements"] = improvements
        
        # If we can imagine significantly better, current is far from Form
        if improvements:
            best_improvement = max(i.get("expected_gain", 0) for i in improvements)
            improvement_penalty = min(0.3, best_improvement * 0.5)
        else:
            improvement_penalty = 0
        
        potential_score = 1.0 - improvement_penalty
        analysis["factors"]["proximity_to_form"] = potential_score
        
        # Calculate score
        score = pattern_score * scale_score * potential_score
        
        # The Meta-Motor rarely vetoes - it prefers to suggest alternatives
        is_veto = False
        veto_reason = None
        
        if pattern_score < 0.1:
            is_veto = True
            veto_reason = "Action violates fundamental patterns"
            score = 0.0
        
        evaluation = MotorEvaluation(
            motor_name=self.name,
            score=score,
            is_veto=is_veto,
            veto_reason=veto_reason,
            confidence=0.70,  # Lower confidence - we're imagining
            analysis=analysis
        )
        
        self._record_evaluation(evaluation)
        return evaluation
    
    def _detect_patterns(self, gene: OperationalGene) -> List[Dict[str, Any]]:
        """Detects patterns in the gene structure."""
        patterns = []
        
        # Check for common operational patterns
        if len(gene.codons) >= 2:
            # Sequential pattern
            patterns.append({
                "name": "sequential_execution",
                "type": "structural",
                "universality": 0.9
            })
        
        if gene.exception_handlers:
            # Error handling pattern
            patterns.append({
                "name": "defensive_execution",
                "type": "safety",
                "universality": 0.85
            })
        
        if gene.postconditions:
            # Goal-directed pattern
            patterns.append({
                "name": "goal_directed",
                "type": "intentional",
                "universality": 0.95
            })
        
        # Check for feedback loops
        codon_entities = [c.entity_id for c in gene.codons]
        if len(codon_entities) != len(set(codon_entities)):
            patterns.append({
                "name": "feedback_loop",
                "type": "control",
                "universality": 0.8
            })
        
        return patterns
    
    def _score_pattern_universality(self, patterns: List[Dict[str, Any]]) -> float:
        """Scores how universal the detected patterns are."""
        if not patterns:
            return 0.5  # No patterns = uncertain
        
        avg_universality = sum(p["universality"] for p in patterns) / len(patterns)
        return avg_universality
    
    def _analyze_across_scales(
        self,
        gene: OperationalGene,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyzes the gene across micro, meso, and macro scales."""
        analysis = {
            "micro": {"score": 0.8, "notes": "Individual codon integrity"},
            "meso": {"score": 0.75, "notes": "Gene-level coherence"},
            "macro": {"score": 0.7, "notes": "System-level impact"},
            "coherence": 0.75
        }
        
        # Micro: Each codon is well-formed
        micro_score = 1.0
        for codon in gene.codons:
            if not codon.entity_id or not codon.action_id:
                micro_score -= 0.2
        analysis["micro"]["score"] = max(0, micro_score)
        
        # Meso: Codons work together
        meso_score = 0.8 if gene.postconditions else 0.6
        analysis["meso"]["score"] = meso_score
        
        # Macro: Gene fits in larger context
        macro_score = 0.7
        if gene.metadata.get("domain"):
            macro_score += 0.1
        analysis["macro"]["score"] = macro_score
        
        # Overall coherence
        analysis["coherence"] = (
            analysis["micro"]["score"] * 0.3 +
            analysis["meso"]["score"] * 0.4 +
            analysis["macro"]["score"] * 0.3
        )
        
        return analysis
    
    def _imagine_improvements(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Imagines potential improvements to the gene.
        This is the Platonic function - seeing what SHOULD exist.
        """
        improvements = []
        
        # Imagine variant
        if len(gene.codons) > 2:
            improvements.append({
                "type": "variant",
                "description": "Reorder codons for better parallelization",
                "expected_gain": 0.15,
                "confidence": 0.6
            })
        
        # Imagine anti-gene if exceptions are frequent
        if len(gene.exception_handlers) > 3:
            improvements.append({
                "type": "anti_gene",
                "description": "Fundamentally different approach to avoid exceptions",
                "expected_gain": 0.25,
                "confidence": 0.4
            })
        
        # Imagine hypothesis
        if not gene.evaluation_metrics:
            improvements.append({
                "type": "hypothesis",
                "description": "Add metrics to measure actual vs intended outcome",
                "expected_gain": 0.1,
                "confidence": 0.7
            })
        
        return improvements
    
    def generate_proposal(
        self,
        gene: OperationalGene,
        proposal_type: str
    ) -> Dict[str, Any]:
        """
        Generates a concrete proposal for gene improvement.
        
        The Meta-Motor is CONSULTATIVE - it proposes, never decides.
        All proposals must be validated before implementation.
        """
        proposal = {
            "proposal_id": make_uid("proposal", gene.uid, str(time.time())),
            "type": proposal_type,
            "base_gene": gene.uid,
            "status": "proposed",
            "requires_validation": True,
            "created_at": time.time()
        }
        
        if proposal_type == "variant":
            proposal["modifications"] = {
                "type": "codon_optimization",
                "changes": "Reorder for parallel execution"
            }
        elif proposal_type == "anti_gene":
            proposal["modifications"] = {
                "type": "complete_redesign",
                "changes": "Alternative approach to same goal"
            }
        elif proposal_type == "hypothesis":
            proposal["modifications"] = {
                "type": "experimental",
                "changes": "Untested possibility worth exploring"
            }
        elif proposal_type == "paradigm":
            proposal["modifications"] = {
                "type": "framework_shift",
                "changes": "New way of understanding the problem"
            }
        
        logger.info(f"Meta-Motor generated {proposal_type} proposal for {gene.name}")
        return proposal


# ============================================================================
# PARALLEL MOTOR ORCHESTRATOR
# ============================================================================
@dataclass
class CraftPerformanceResult:
    """
    The result of parallel motor evaluation.
    
    Craft Performance is the PRODUCT of all motor scores.
    This means any zero = total zero (absolute veto).
    
    CP is not a probability. It's a measure of how close
    the action is to the ideal Platonic Form.
    
    Between 0 and 1 there are infinite values - not binary,
    it's fractal, quantum-like. 0 is error, 1 is absolute truth.
    """
    gene_uid: str
    evaluations: Dict[str, MotorEvaluation]
    craft_performance: float
    is_vetoed: bool
    veto_motor: Optional[str]
    veto_reason: Optional[str]
    timestamp: float = field(default_factory=time.time)
    
    @property
    def individual_scores(self) -> Dict[str, float]:
        return {name: e.score for name, e in self.evaluations.items()}
    
    def explain(self) -> str:
        """Returns a human-readable explanation of the result."""
        lines = [
            f"Craft Performance: {self.craft_performance:.4f}",
            f"",
            f"Motor Scores (PRODUCT formula - any zero = total zero):",
        ]
        
        for name, evaluation in self.evaluations.items():
            veto_mark = " [VETO]" if evaluation.is_absolute_veto else ""
            lines.append(f"  • {name}: {evaluation.score:.3f}{veto_mark}")
        
        lines.append(f"")
        
        if self.is_vetoed:
            lines.append(f" VETOED by {self.veto_motor}: {self.veto_reason}")
        else:
            if self.craft_performance > 0.9:
                lines.append(f"✓ Approaching Platonic Form")
            elif self.craft_performance > 0.5:
                lines.append(f"○ Acceptable but improvable")
            else:
                lines.append(f"△ Significant concerns")
        
        return "\n".join(lines)


class ParallelMotorOrchestrator:
    """
    Orchestrates the four motors running in PARALLEL.
    
    The motors do not run sequentially. They evaluate simultaneously
    and independently, then their scores are combined as a PRODUCT.
    
    This is like four GPS satellites triangulating a position -
    each gives its own measurement, and together they locate
    the action in the space of possibilities.
    """
    
    def __init__(self, genome: DigitalGenome):
        self.genome = genome
        
        # Initialize the four parallel motors
        self.praxeological = PraxeologicalMotor(genome)
        self.nash = NashMotor(genome)
        self.chaotic = ChaoticMotor(genome)
        self.meristic = MeristicMetaMotor(genome)
        
        self.evaluation_history: List[CraftPerformanceResult] = []
    
    def evaluate_gene(
        self,
        gene: OperationalGene,
        context: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> CraftPerformanceResult:
        """
        Evaluates a gene using all four motors IN PARALLEL.
        
        Returns the Craft Performance as a PRODUCT of all scores.
        """
        logger.info(f"Parallel evaluation starting for: {gene.name}")
        
        # Run all four motors (in production, use actual parallelism)
        # Here we simulate parallel execution
        evaluations = {}
        
        # Motor 1: Praxeological
        evaluations["Praxeological"] = self.praxeological.evaluate(gene, context, intent)
        
        # Motor 2: Nash
        evaluations["Nash"] = self.nash.evaluate(gene, context, intent)
        
        # Motor 3: Chaotic
        evaluations["Chaotic"] = self.chaotic.evaluate(gene, context, intent)
        
        # Motor 4: Meristic
        evaluations["Meristic"] = self.meristic.evaluate(gene, context, intent)
        
        # Calculate Craft Performance as PRODUCT
        craft_performance = 1.0
        is_vetoed = False
        veto_motor = None
        veto_reason = None
        
        for name, evaluation in evaluations.items():
            craft_performance *= evaluation.score
            
            if evaluation.is_absolute_veto and not is_vetoed:
                is_vetoed = True
                veto_motor = name
                veto_reason = evaluation.veto_reason
                craft_performance = 0.0
        
        result = CraftPerformanceResult(
            gene_uid=gene.uid,
            evaluations=evaluations,
            craft_performance=craft_performance,
            is_vetoed=is_vetoed,
            veto_motor=veto_motor,
            veto_reason=veto_reason
        )
        
        # Record motor scores in the gene
        gene.record_motor_scores(
            praxeological=evaluations["Praxeological"].score,
            nash=evaluations["Nash"].score,
            chaotic=evaluations["Chaotic"].score,
            meristic=evaluations["Meristic"].score
        )
        
        self.evaluation_history.append(result)
        
        logger.info(f"Craft Performance: {craft_performance:.4f} (vetoed={is_vetoed})")
        return result
    
    def get_meta_motor_proposals(
        self,
        gene: OperationalGene
    ) -> List[Dict[str, Any]]:
        """Gets improvement proposals from the Meta-Motor."""
        proposals = []
        
        for proposal_type in ["variant", "hypothesis"]:
            proposal = self.meristic.generate_proposal(gene, proposal_type)
            proposals.append(proposal)
        
        return proposals


# ============================================================================
# COGNITIVE SYSTEM - The Complete Brain
# ============================================================================
class CognitiveSystem:
    """
    The unified cognitive system integrating all components.
    
    This is the complete distributed brain:
    - The Digital Genome is the neural structure
    - The four motors are emergent properties of neural activation
    - Decisions emerge from parallel evaluation and convergence
    """
    
    def __init__(self, genome: DigitalGenome = None):
        self.genome = genome or DigitalGenome(name="Cognitive System")
        self.orchestrator = ParallelMotorOrchestrator(self.genome)
        self.decision_history: List[Dict[str, Any]] = []
        
        logger.info("Cognitive System initialized with four parallel motors")
    
    def process_intent(
        self,
        intent: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Processes an intent through the complete cognitive pipeline.
        
        1. Find candidate genes
        2. Evaluate each in parallel through four motors
        3. Select best non-vetoed option
        4. Return decision with full explanation
        """
        context = context or {}
        intent_dict = {"purpose": intent}
        
        decision = {
            "decision_id": make_uid("decision", intent, str(time.time())),
            "intent": intent,
            "context": context,
            "timestamp": time.time(),
            "candidates": [],
            "selected": None,
            "craft_performance": 0.0,
            "explanation": {},
            "meta_motor_proposals": []
        }
        
        # Find candidate genes
        candidates = self.genome.find_genes_by_context(intent)
        
        if not candidates:
            decision["explanation"]["error"] = "No suitable genes found"
            self.decision_history.append(decision)
            return decision
        
        # Evaluate each candidate
        best_result = None
        best_gene = None
        
        for gene in candidates:
            result = self.orchestrator.evaluate_gene(gene, context, intent_dict)
            
            decision["candidates"].append({
                "gene_uid": gene.uid,
                "gene_name": gene.name,
                "craft_performance": result.craft_performance,
                "is_vetoed": result.is_vetoed,
                "individual_scores": result.individual_scores
            })
            
            # Select best non-vetoed candidate
            if not result.is_vetoed:
                if best_result is None or result.craft_performance > best_result.craft_performance:
                    best_result = result
                    best_gene = gene
        
        if best_gene:
            decision["selected"] = {
                "gene_uid": best_gene.uid,
                "gene_name": best_gene.name,
                "purpose": best_gene.purpose
            }
            decision["craft_performance"] = best_result.craft_performance
            decision["explanation"] = {
                "selection_reason": "Highest Craft Performance among non-vetoed candidates",
                "motor_analysis": {
                    name: {
                        "score": e.score,
                        "confidence": e.confidence,
                        "analysis_summary": list(e.analysis.get("factors", {}).keys())
                    }
                    for name, e in best_result.evaluations.items()
                },
                "cp_explanation": best_result.explain()
            }
            
            # Get Meta-Motor proposals for improvement
            proposals = self.orchestrator.get_meta_motor_proposals(best_gene)
            decision["meta_motor_proposals"] = proposals
        else:
            decision["explanation"]["error"] = "All candidates were vetoed"
            
            # Find veto reasons
            veto_reasons = []
            for cand in decision["candidates"]:
                if cand["is_vetoed"]:
                    veto_reasons.append(f"{cand['gene_name']}: vetoed")
            decision["explanation"]["veto_details"] = veto_reasons
        
        self.decision_history.append(decision)
        return decision
    
    def get_statistics(self) -> Dict[str, Any]:
        """Returns system statistics."""
        return {
            "genome": self.genome.get_statistics(),
            "total_decisions": len(self.decision_history),
            "successful_decisions": sum(
                1 for d in self.decision_history 
                if d.get("selected") is not None
            ),
            "motor_evaluations": {
                "praxeological": len(self.orchestrator.praxeological.evaluation_history),
                "nash": len(self.orchestrator.nash.evaluation_history),
                "chaotic": len(self.orchestrator.chaotic.evaluation_history),
                "meristic": len(self.orchestrator.meristic.evaluation_history)
            }
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================
def demonstration():
    """Demonstrates the four parallel motors architecture."""
    print("\n" + "=" * 70)
    print("COGNITIVE CORE - FOUR PARALLEL MOTORS DEMONSTRATION")
    print("CP = Praxeological × Nash × Chaotic × Meristic")
    print("=" * 70)
    
    # Create genome with example gene
    genome = DigitalGenome(name="Demo Genome")
    
    # Register ontology
    pump_id = genome.register_entity(make_uid("entity", "pump", "401"), "Pump 401", "physical")
    valve_id = genome.register_entity(make_uid("entity", "valve", "302"), "Valve 302", "physical")
    stop_action = genome.register_action(make_uid("action", "stop"), "Stop", "operational")
    close_action = genome.register_action(make_uid("action", "close"), "Close", "operational")
    isolated_state = genome.register_state(make_uid("state", "isolated"), "Isolated", "safety")
    closed_state = genome.register_state(make_uid("state", "closed"), "Closed", "safety")
    
    # Create a well-formed gene for emergency shutdown
    gene = OperationalGene.create(
        name="Emergency Pump Shutdown",
        purpose="Safely stop pump emergency shutdown procedure",
        executor="safety_system",
        action="emergency_shutdown",
        target="pump_401",
        domain="safety"
    )
    
    # Add codons with proper chain
    gene.add_codon(PraxeologicalCodon(
        entity_id=pump_id,
        action_id=stop_action,
        target_state_id=isolated_state,
        safety_level=SafetyLevel.WARNING,
        preconditions=("pump_running",),
        postconditions=("pump_stopped", "ready_for_isolation")
    ))
    
    gene.add_codon(PraxeologicalCodon(
        entity_id=valve_id,
        action_id=close_action,
        target_state_id=closed_state,
        safety_level=SafetyLevel.WARNING,
        preconditions=("ready_for_isolation",),
        postconditions=("valve_closed", "system_isolated")
    ))
    
    gene.activation_conditions = ["emergency", "pressure > 800"]
    gene.postconditions = ["pump_stopped", "system_isolated", "safe_state"]
    gene.exception_handlers = {
        "timeout": "force_shutdown",
        "comm_failure": "local_override",
        "valve_stuck": "manual_intervention"
    }
    gene.evaluation_metrics = ["shutdown_time_ms", "equipment_integrity"]
    gene.activate()
    
    genome.insert_gene_as_neuron(gene, TruthType.PLATONIC, "safety", "critical")
    
    # Initialize cognitive system
    print("\n Initializing Cognitive System with four parallel motors...")
    system = CognitiveSystem(genome)
    
    # Directly evaluate the gene to show motor scores
    print("\n Direct evaluation of 'Emergency Pump Shutdown' gene")
    print("   Context: emergency=True, pressure=850")
    
    context = {"emergency": True, "pressure": 850, "temperature": 95}
    intent = {"purpose": "emergency shutdown procedure"}
    
    result = system.orchestrator.evaluate_gene(gene, context, intent)
    
    # Display results
    print("\n PARALLEL MOTOR EVALUATION RESULTS:")
    print("-" * 50)
    print(result.explain())
    
    # Show analysis details
    print("\n🔍 MOTOR ANALYSIS DETAILS:")
    for motor_name, evaluation in result.evaluations.items():
        print(f"\n   {motor_name} Motor:")
        print(f"      Score: {evaluation.score:.3f}")
        print(f"      Confidence: {evaluation.confidence:.2f}")
        if evaluation.analysis.get("factors"):
            print(f"      Factors: {evaluation.analysis['factors']}")
    
    # Get Meta-Motor proposals
    print("\n🔮 META-MOTOR PROPOSALS (Platonic imagination):")
    proposals = system.orchestrator.get_meta_motor_proposals(gene)
    for prop in proposals:
        print(f"   • {prop['type'].upper()}: {prop['modifications'].get('changes', 'N/A')}")
    
    # Demonstrate absolute veto
    print("\n" + "-" * 50)
    print(" DEMONSTRATING ABSOLUTE VETO:")
    print("-" * 50)
    
    # Create gene that will be vetoed (no exception handlers = chaotic veto potential)
    vetoed_gene = OperationalGene.create(
        name="Dangerous Unprotected Action",
        purpose="Action without safety measures",
        executor="system",
        action="dangerous",
        target="target"
    )
    vetoed_gene.add_codon(PraxeologicalCodon(
        entity_id="entity",
        action_id="action",
        target_state_id="state",
        safety_level=SafetyLevel.CRITICAL  # Critical but no handlers!
    ))
    # NO exception handlers, NO postconditions - should score poorly
    vetoed_gene.activate()
    
    vetoed_result = system.orchestrator.evaluate_gene(
        vetoed_gene,
        {"chaos_level": 0.9},
        {"purpose": "dangerous action"}
    )
    
    print(f"\n   Gene: {vetoed_gene.name}")
    print(f"   Has exception handlers: {bool(vetoed_gene.exception_handlers)}")
    print(f"   Has postconditions: {bool(vetoed_gene.postconditions)}")
    print(f"\n   Motor Scores:")
    for name, score in vetoed_result.individual_scores.items():
        print(f"      {name}: {score:.3f}")
    print(f"\n   Craft Performance: {vetoed_result.craft_performance:.4f}")
    print(f"   Vetoed: {vetoed_result.is_vetoed}")
    if vetoed_result.is_vetoed:
        print(f"   Veto by: {vetoed_result.veto_motor}")
        print(f"   Reason: {vetoed_result.veto_reason}")
    
    # Final statistics
    print("\n SYSTEM STATISTICS:")
    stats = system.get_statistics()
    print(f"   Total Motor Evaluations: {sum(stats['motor_evaluations'].values())}")
    for motor, count in stats['motor_evaluations'].items():
        print(f"      • {motor}: {count}")
    
    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    return system


if __name__ == "__main__":
    system = demonstration()
