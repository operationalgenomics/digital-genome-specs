"""
Craft Performance Calculation and Analysis
===========================================

This module provides utilities for calculating and analyzing Craft Performance
scores during validation experiments.

CRAFT PERFORMANCE FORMULA:
--------------------------
CP = M_P × M_C × M_N × M_M

Where:
- M_P: Praxeological Motor score (intention realization)
- M_C: Chaotic Motor score (robustness to perturbations)
- M_N: Nash Motor score (strategic equilibrium)
- M_M: Meristic Meta-Motor score (pattern universality)

CRITICAL PROPERTIES:
--------------------
1. Multiplicative: Any zero score produces CP = 0 (absolute veto)
2. Non-compensatory: High score in one motor cannot offset low score in another
3. Sensitive: Small changes in any motor propagate to final CP
4. Bounded: CP ∈ [0, 1] when all motors are in [0, 1]

These properties distinguish the Digital Genome approach from traditional
weighted-sum aggregation methods used in multi-criteria decision making.

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math
import statistics
import logging

logger = logging.getLogger("validation.metrics.cp")


# ============================================================================
# RESULT STRUCTURES
# ============================================================================

@dataclass
class CPResult:
    """
    The result of a Craft Performance calculation.
    
    This structure captures not just the final CP value but also the
    individual motor contributions and any veto conditions.
    
    Attributes:
        craft_performance: The final CP score [0, 1]
        motor_scores: Dictionary of individual motor scores
        is_vetoed: Whether any motor issued an absolute veto
        veto_motor: Name of the motor that issued veto (if any)
        veto_reason: Human-readable explanation of veto
        analysis: Additional analysis details
    """
    craft_performance: float
    motor_scores: Dict[str, float]
    is_vetoed: bool = False
    veto_motor: Optional[str] = None
    veto_reason: Optional[str] = None
    analysis: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_excellent(self) -> bool:
        """Returns True if CP suggests proximity to ideal Form (>0.9)."""
        return self.craft_performance > 0.9
    
    @property
    def is_acceptable(self) -> bool:
        """Returns True if CP is above minimum threshold (>0.5)."""
        return self.craft_performance > 0.5
    
    @property
    def weakest_motor(self) -> Tuple[str, float]:
        """Returns the motor with the lowest score."""
        if not self.motor_scores:
            return ("none", 0.0)
        return min(self.motor_scores.items(), key=lambda x: x[1])
    
    @property
    def strongest_motor(self) -> Tuple[str, float]:
        """Returns the motor with the highest score."""
        if not self.motor_scores:
            return ("none", 0.0)
        return max(self.motor_scores.items(), key=lambda x: x[1])
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes result for storage and logging."""
        return {
            "craft_performance": self.craft_performance,
            "motor_scores": self.motor_scores,
            "is_vetoed": self.is_vetoed,
            "veto_motor": self.veto_motor,
            "veto_reason": self.veto_reason,
            "analysis": self.analysis,
            "is_excellent": self.is_excellent,
            "is_acceptable": self.is_acceptable,
            "weakest_motor": self.weakest_motor,
            "strongest_motor": self.strongest_motor
        }


@dataclass
class CPDistribution:
    """
    Statistical distribution of CP scores across a population.
    
    Used for analyzing the overall behavior of the system across
    many genes or cases.
    
    Attributes:
        scores: List of all CP scores
        motor_distributions: Per-motor score distributions
        veto_count: Number of absolute vetoes
        statistics: Computed statistical measures
    """
    scores: List[float]
    motor_distributions: Dict[str, List[float]]
    veto_count: int = 0
    statistics: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Computes statistics after initialization."""
        if self.scores and not self.statistics:
            self.statistics = self._compute_statistics()
    
    def _compute_statistics(self) -> Dict[str, float]:
        """Computes summary statistics for the distribution."""
        if not self.scores:
            return {}
        
        # Filter out vetoed (zero) scores for some statistics
        non_zero = [s for s in self.scores if s > 0]
        
        stats = {
            "count": len(self.scores),
            "mean": statistics.mean(self.scores),
            "median": statistics.median(self.scores),
            "stdev": statistics.stdev(self.scores) if len(self.scores) > 1 else 0,
            "min": min(self.scores),
            "max": max(self.scores),
            "veto_rate": self.veto_count / len(self.scores) if self.scores else 0,
            "excellent_rate": sum(1 for s in self.scores if s > 0.9) / len(self.scores),
            "acceptable_rate": sum(1 for s in self.scores if s > 0.5) / len(self.scores),
        }
        
        # Add non-zero statistics if there are any
        if non_zero:
            stats["mean_non_vetoed"] = statistics.mean(non_zero)
            stats["median_non_vetoed"] = statistics.median(non_zero)
        
        # Add percentiles
        sorted_scores = sorted(self.scores)
        n = len(sorted_scores)
        stats["p10"] = sorted_scores[int(n * 0.10)] if n > 10 else sorted_scores[0]
        stats["p25"] = sorted_scores[int(n * 0.25)] if n > 4 else sorted_scores[0]
        stats["p75"] = sorted_scores[int(n * 0.75)] if n > 4 else sorted_scores[-1]
        stats["p90"] = sorted_scores[int(n * 0.90)] if n > 10 else sorted_scores[-1]
        
        return stats
    
    def get_motor_statistics(self, motor_name: str) -> Dict[str, float]:
        """Returns statistics for a specific motor."""
        if motor_name not in self.motor_distributions:
            return {}
        
        scores = self.motor_distributions[motor_name]
        if not scores:
            return {}
        
        return {
            "mean": statistics.mean(scores),
            "median": statistics.median(scores),
            "stdev": statistics.stdev(scores) if len(scores) > 1 else 0,
            "min": min(scores),
            "max": max(scores),
            "zero_rate": sum(1 for s in scores if s == 0) / len(scores)
        }


# ============================================================================
# CP CALCULATION FUNCTIONS
# ============================================================================

def calculate_cp(
    m_p: float,
    m_c: float,
    m_n: float,
    m_m: float,
    veto_threshold: float = 0.0
) -> CPResult:
    """
    Calculates Craft Performance from the four motor scores.
    
    This is the core formula of the Digital Genome:
    
        CP = M_P × M_C × M_N × M_M
    
    The multiplicative structure ensures:
    1. A zero in any motor produces CP = 0 (absolute veto)
    2. All motors must agree for high CP
    3. The weakest motor dominates the result
    
    Args:
        m_p: Praxeological Motor score [0, 1]
        m_c: Chaotic Motor score [0, 1]
        m_n: Nash Motor score [0, 1]
        m_m: Meristic Meta-Motor score [0, 1]
        veto_threshold: Scores below this trigger veto (default 0)
        
    Returns:
        CPResult with full analysis
        
    Raises:
        ValueError: If any score is outside [0, 1]
    """
    # Validate inputs
    scores = {
        "praxeological": m_p,
        "chaotic": m_c,
        "nash": m_n,
        "meristic": m_m
    }
    
    for name, score in scores.items():
        if not 0 <= score <= 1:
            raise ValueError(
                f"Motor score must be in [0, 1], got {name}={score}"
            )
    
    # Check for veto conditions
    is_vetoed = False
    veto_motor = None
    veto_reason = None
    
    for name, score in scores.items():
        if score <= veto_threshold:
            is_vetoed = True
            veto_motor = name
            veto_reason = f"{name} motor issued absolute veto (score={score})"
            break
    
    # Calculate CP as product
    cp = m_p * m_c * m_n * m_m
    
    # Build analysis
    analysis = {
        "formula": "CP = M_P × M_C × M_N × M_M",
        "individual_contributions": {
            # Each motor's "contribution" to lowering CP from 1.0
            name: 1.0 - score for name, score in scores.items()
        },
        "geometric_mean": (m_p * m_c * m_n * m_m) ** 0.25,
        "arithmetic_mean": (m_p + m_c + m_n + m_m) / 4,
        "cp_vs_arithmetic_ratio": cp / ((m_p + m_c + m_n + m_m) / 4) if (m_p + m_c + m_n + m_m) > 0 else 0
    }
    
    return CPResult(
        craft_performance=cp,
        motor_scores=scores,
        is_vetoed=is_vetoed,
        veto_motor=veto_motor,
        veto_reason=veto_reason,
        analysis=analysis
    )


def calculate_cp_additive(
    m_p: float,
    m_c: float,
    m_n: float,
    m_m: float,
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculates a weighted-sum aggregation for comparison with CP.
    
    This implements the traditional multi-criteria approach:
    
        Score = w_P × M_P + w_C × M_C + w_N × M_N + w_M × M_M
    
    This is provided for baseline comparison to demonstrate the
    superiority of the multiplicative approach.
    
    Args:
        m_p, m_c, m_n, m_m: Motor scores [0, 1]
        weights: Optional weight dictionary (defaults to equal weights)
        
    Returns:
        Weighted sum score [0, 1]
    """
    if weights is None:
        weights = {
            "praxeological": 0.25,
            "chaotic": 0.25,
            "nash": 0.25,
            "meristic": 0.25
        }
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    normalized = {k: v / total_weight for k, v in weights.items()}
    
    return (
        normalized.get("praxeological", 0.25) * m_p +
        normalized.get("chaotic", 0.25) * m_c +
        normalized.get("nash", 0.25) * m_n +
        normalized.get("meristic", 0.25) * m_m
    )


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_motor_contributions(
    results: List[CPResult]
) -> Dict[str, Any]:
    """
    Analyzes the contribution of each motor across multiple results.
    
    This analysis helps understand which motors are most influential
    in determining CP and where the system's bottlenecks lie.
    
    Args:
        results: List of CPResult from multiple evaluations
        
    Returns:
        Dictionary with detailed contribution analysis
    """
    if not results:
        return {"error": "No results to analyze"}
    
    # Collect distributions
    cp_scores = [r.craft_performance for r in results]
    motor_names = ["praxeological", "chaotic", "nash", "meristic"]
    
    motor_distributions = {
        name: [r.motor_scores.get(name, 0) for r in results]
        for name in motor_names
    }
    
    veto_count = sum(1 for r in results if r.is_vetoed)
    
    # Build distribution object
    distribution = CPDistribution(
        scores=cp_scores,
        motor_distributions=motor_distributions,
        veto_count=veto_count
    )
    
    # Analyze veto patterns
    veto_by_motor = {name: 0 for name in motor_names}
    for r in results:
        if r.is_vetoed and r.veto_motor:
            veto_by_motor[r.veto_motor] = veto_by_motor.get(r.veto_motor, 0) + 1
    
    # Analyze correlation between motors and CP
    # (Simple correlation - for scientific papers, use proper statistical tests)
    correlations = {}
    for name in motor_names:
        motor_scores = motor_distributions[name]
        # Pearson correlation coefficient approximation
        if len(motor_scores) > 1:
            mean_motor = statistics.mean(motor_scores)
            mean_cp = statistics.mean(cp_scores)
            
            numerator = sum(
                (m - mean_motor) * (c - mean_cp)
                for m, c in zip(motor_scores, cp_scores)
            )
            
            denominator = math.sqrt(
                sum((m - mean_motor) ** 2 for m in motor_scores) *
                sum((c - mean_cp) ** 2 for c in cp_scores)
            )
            
            correlations[name] = numerator / denominator if denominator > 0 else 0
    
    # Identify bottleneck motor (most often the weakest)
    bottleneck_counts = {name: 0 for name in motor_names}
    for r in results:
        if r.motor_scores:
            weakest = min(r.motor_scores.items(), key=lambda x: x[1])
            bottleneck_counts[weakest[0]] += 1
    
    return {
        "distribution": distribution,
        "cp_statistics": distribution.statistics,
        "motor_statistics": {
            name: distribution.get_motor_statistics(name)
            for name in motor_names
        },
        "veto_analysis": {
            "total_vetoes": veto_count,
            "veto_rate": veto_count / len(results) if results else 0,
            "vetoes_by_motor": veto_by_motor
        },
        "correlation_with_cp": correlations,
        "bottleneck_analysis": {
            "counts": bottleneck_counts,
            "primary_bottleneck": max(bottleneck_counts.items(), key=lambda x: x[1])[0]
        }
    }


def compare_multiplicative_vs_additive(
    results: List[CPResult]
) -> Dict[str, Any]:
    """
    Compares multiplicative CP with additive aggregation.
    
    This analysis demonstrates the behavioral differences between
    the Digital Genome approach and traditional methods.
    
    Key differences to highlight:
    1. Multiplicative is more conservative (lower scores on average)
    2. Multiplicative has higher variance (more sensitive to weak motors)
    3. Multiplicative produces more vetoes
    4. Multiplicative is non-compensatory
    
    Args:
        results: List of CPResult from evaluations
        
    Returns:
        Comparison analysis dictionary
    """
    if not results:
        return {"error": "No results to analyze"}
    
    multiplicative_scores = []
    additive_scores = []
    
    for r in results:
        multiplicative_scores.append(r.craft_performance)
        
        # Calculate additive equivalent
        additive = calculate_cp_additive(
            r.motor_scores.get("praxeological", 0),
            r.motor_scores.get("chaotic", 0),
            r.motor_scores.get("nash", 0),
            r.motor_scores.get("meristic", 0)
        )
        additive_scores.append(additive)
    
    # Calculate statistics for comparison
    mult_mean = statistics.mean(multiplicative_scores)
    add_mean = statistics.mean(additive_scores)
    
    mult_std = statistics.stdev(multiplicative_scores) if len(multiplicative_scores) > 1 else 0
    add_std = statistics.stdev(additive_scores) if len(additive_scores) > 1 else 0
    
    # Calculate correlation between the two methods
    if len(multiplicative_scores) > 1:
        mean_m = mult_mean
        mean_a = add_mean
        
        numerator = sum(
            (m - mean_m) * (a - mean_a)
            for m, a in zip(multiplicative_scores, additive_scores)
        )
        
        denominator = math.sqrt(
            sum((m - mean_m) ** 2 for m in multiplicative_scores) *
            sum((a - mean_a) ** 2 for a in additive_scores)
        )
        
        correlation = numerator / denominator if denominator > 0 else 0
    else:
        correlation = 0
    
    # Count disagreements (where multiplicative vetoes but additive doesn't)
    disagreements = sum(
        1 for m, a in zip(multiplicative_scores, additive_scores)
        if m == 0 and a > 0.25  # Multiplicative vetoed, additive still acceptable
    )
    
    return {
        "multiplicative": {
            "mean": mult_mean,
            "std": mult_std,
            "min": min(multiplicative_scores),
            "max": max(multiplicative_scores),
            "zero_count": sum(1 for s in multiplicative_scores if s == 0)
        },
        "additive": {
            "mean": add_mean,
            "std": add_std,
            "min": min(additive_scores),
            "max": max(additive_scores),
            "zero_count": sum(1 for s in additive_scores if s == 0)
        },
        "comparison": {
            "mean_difference": add_mean - mult_mean,
            "std_ratio": mult_std / add_std if add_std > 0 else float('inf'),
            "correlation": correlation,
            "disagreement_count": disagreements,
            "disagreement_rate": disagreements / len(results) if results else 0
        },
        "interpretation": {
            "multiplicative_more_conservative": mult_mean < add_mean,
            "multiplicative_more_variable": mult_std > add_std,
            "significant_disagreement": disagreements / len(results) > 0.1 if results else False
        }
    }


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == "__main__":
    """Test the CP calculation and analysis functions."""
    
    print("=" * 60)
    print("CRAFT PERFORMANCE METRICS TEST")
    print("=" * 60)
    
    # Test basic CP calculation
    print("\n1. Basic CP Calculation")
    print("-" * 40)
    
    result = calculate_cp(0.9, 0.8, 0.85, 0.9)
    print(f"   M_P=0.9, M_C=0.8, M_N=0.85, M_M=0.9")
    print(f"   CP = {result.craft_performance:.4f}")
    print(f"   Excellent: {result.is_excellent}")
    print(f"   Weakest motor: {result.weakest_motor}")
    
    # Test veto behavior
    print("\n2. Veto Behavior")
    print("-" * 40)
    
    result_veto = calculate_cp(0.9, 0.0, 0.85, 0.9)
    print(f"   M_P=0.9, M_C=0.0, M_N=0.85, M_M=0.9")
    print(f"   CP = {result_veto.craft_performance:.4f}")
    print(f"   Vetoed: {result_veto.is_vetoed}")
    print(f"   Veto motor: {result_veto.veto_motor}")
    
    # Test comparison with additive
    print("\n3. Multiplicative vs Additive")
    print("-" * 40)
    
    scores = (0.9, 0.4, 0.85, 0.9)
    cp_mult = calculate_cp(*scores).craft_performance
    cp_add = calculate_cp_additive(*scores)
    
    print(f"   Motors: P=0.9, C=0.4, N=0.85, M=0.9")
    print(f"   Multiplicative CP: {cp_mult:.4f}")
    print(f"   Additive (equal weights): {cp_add:.4f}")
    print(f"   Difference: {cp_add - cp_mult:.4f}")
    
    # Test analysis
    print("\n4. Distribution Analysis")
    print("-" * 40)
    
    test_results = [
        calculate_cp(0.9, 0.8, 0.85, 0.9),
        calculate_cp(0.7, 0.6, 0.75, 0.8),
        calculate_cp(0.5, 0.9, 0.6, 0.7),
        calculate_cp(0.8, 0.0, 0.9, 0.85),  # Vetoed
        calculate_cp(0.95, 0.92, 0.88, 0.91),
    ]
    
    analysis = analyze_motor_contributions(test_results)
    print(f"   Samples: {len(test_results)}")
    print(f"   Mean CP: {analysis['cp_statistics']['mean']:.4f}")
    print(f"   Veto rate: {analysis['veto_analysis']['veto_rate']:.2%}")
    print(f"   Bottleneck: {analysis['bottleneck_analysis']['primary_bottleneck']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
