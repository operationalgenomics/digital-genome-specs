"""
Praxeological Motor Validation Experiment
==========================================

This experiment validates the Praxeological Motor (M_P) of the Digital Genome
framework using the BPI Challenge 2017 dataset. The experiment tests whether
M_P can identify intention-realization failures in business process logs.

SCIENTIFIC HYPOTHESIS:
----------------------
H1: The Praxeological Motor can predict loan application outcomes (accepted/
    denied/withdrawn) with higher accuracy than traditional process mining
    conformance checking.

H0 (null): There is no significant difference between M_P predictions and
           random baseline or traditional conformance checking.

RATIONALE:
----------
Business processes encode intentional behavior. Each case (loan application)
represents an agent's intention to achieve a goal (obtain a loan). The process
either realizes this intention (loan granted) or fails to realize it (denied,
withdrawn, cancelled).

The Praxeological Motor evaluates whether actions align with their stated
intentions. In this context:
- High M_P score: Process activities are coherent and goal-directed
- Low M_P score: Process shows deviations, loops, or contradictions

If M_P correctly captures praxeological structure, cases with high M_P scores
should correlate with successful outcomes, while cases with low scores should
correlate with failures.

METHODOLOGY:
------------
1. Transform BPI 2017 event logs into Praxeological Codons and Genes
2. For each gene (loan case), calculate M_P score using:
   - Intent Alignment: Do activities progress toward the goal?
   - Means-End Coherence: Are the steps logically connected?
   - Completeness: Are all necessary steps present?
3. Binarize outcomes: success (offer accepted) vs failure (denied/cancelled)
4. Evaluate M_P as a predictor of outcome
5. Compare against baselines:
   - Random prediction (theoretical baseline)
   - Majority class prediction
   - Simple heuristic (case length > threshold)

METRICS:
--------
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC (using M_P score as continuous predictor)
- Comparison with baselines using McNemar's test

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from enum import Enum
import hashlib
import json
import time
import logging
import random
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from validation.datasets.bpi_loader import BPILoader, BPIConfig
from validation.datasets.base_loader import TransformationResult
from validation.metrics.craft_performance import (
    calculate_cp,
    CPResult,
    analyze_motor_contributions
)
from validation.metrics.comparison import (
    evaluate_predictions,
    PredictionMetrics,
    compare_with_baseline,
    BaselineComparison
)

logger = logging.getLogger("validation.experiments.praxeological")


# ============================================================================
# EXPERIMENT CONFIGURATION
# ============================================================================

class PraxeologicalHypothesis(Enum):
    """
    The hypotheses being tested in this experiment.
    """
    H1_PREDICTION = "M_P scores predict case outcomes better than random"
    H2_DISCRIMINATION = "M_P discriminates between success and failure cases"
    H3_BASELINE = "M_P outperforms traditional conformance metrics"


@dataclass
class ExperimentConfig:
    """
    Configuration for the Praxeological Motor validation experiment.
    
    Attributes:
        data_path: Path to BPI Challenge 2017 XES file
        output_dir: Directory for experiment outputs
        random_seed: Seed for reproducibility
        test_split: Proportion of data for testing (0-1)
        mp_threshold: Threshold for binarizing M_P predictions
        success_outcomes: Which outcome statuses count as "success"
        max_cases: Maximum cases to process (None = all)
    """
    data_path: Path
    output_dir: Path = Path("./results")
    random_seed: int = 42
    test_split: float = 0.2
    mp_threshold: float = 0.5
    success_outcomes: Tuple[str, ...] = ("accepted",)
    max_cases: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "data_path": str(self.data_path),
            "output_dir": str(self.output_dir),
            "random_seed": self.random_seed,
            "test_split": self.test_split,
            "mp_threshold": self.mp_threshold,
            "success_outcomes": list(self.success_outcomes),
            "max_cases": self.max_cases
        }


# ============================================================================
# PRAXEOLOGICAL SCORING FUNCTIONS
# ============================================================================

def calculate_intent_alignment(gene: Dict[str, Any]) -> float:
    """
    Calculates the Intent Alignment factor for a gene.
    
    Intent Alignment measures whether the sequence of activities progresses
    toward the stated goal. In BPI 2017 context:
    - Positive activities: A_Submitted, A_Accepted, O_Created, O_Accepted
    - Negative activities: A_Denied, A_Cancelled, O_Refused, O_Cancelled
    - Neutral activities: W_* (workflow activities)
    
    The score is based on the ratio of goal-directed activities to total
    activities, weighted by their position in the sequence.
    
    Args:
        gene: Gene dictionary with codons and metadata
        
    Returns:
        Intent alignment score [0, 1]
    """
    codons = gene.get("codons", [])
    if not codons:
        return 0.0
    
    # Activity classifications
    positive_prefixes = ("A_Create", "A_Submit", "A_Accept", "O_Create", "O_Accept", "O_Sent")
    negative_prefixes = ("A_Denied", "A_Cancel", "O_Refuse", "O_Cancel")
    
    positive_count = 0
    negative_count = 0
    total_relevant = 0
    
    for i, codon in enumerate(codons):
        activity = codon.get("action_id", "")
        
        # Weight later activities more (they indicate trajectory)
        position_weight = (i + 1) / len(codons)
        
        if any(activity.startswith(p) for p in positive_prefixes):
            positive_count += position_weight
            total_relevant += position_weight
        elif any(activity.startswith(p) for p in negative_prefixes):
            negative_count += position_weight
            total_relevant += position_weight
    
    if total_relevant == 0:
        # No relevant activities - neutral score
        return 0.5
    
    # Score based on positive ratio
    alignment = positive_count / (positive_count + negative_count) if (positive_count + negative_count) > 0 else 0.5
    
    return alignment


def calculate_means_end_coherence(gene: Dict[str, Any]) -> float:
    """
    Calculates the Means-End Coherence factor for a gene.
    
    Means-End Coherence measures whether the activities form a logical
    progression. Signs of incoherence include:
    - Loops (returning to earlier activities)
    - Missing steps (jumping over required activities)
    - Contradictory activities (accept then deny)
    
    Args:
        gene: Gene dictionary with codons and metadata
        
    Returns:
        Means-end coherence score [0, 1]
    """
    codons = gene.get("codons", [])
    if len(codons) < 2:
        return 1.0  # Single-step processes are trivially coherent
    
    activities = [c.get("action_id", "") for c in codons]
    
    # Detect loops (same activity appearing multiple times)
    unique_activities = set(activities)
    loop_ratio = len(unique_activities) / len(activities)
    
    # Penalize excessive loops (some repetition is normal)
    loop_penalty = max(0, 1 - (1 - loop_ratio) * 2)
    
    # Check for contradictions
    contradiction_penalty = 1.0
    
    # Accept followed by Deny is a contradiction
    if "A_Accepted" in activities and "A_Denied" in activities:
        accept_pos = activities.index("A_Accepted")
        deny_pos = activities.index("A_Denied")
        if accept_pos < deny_pos:
            contradiction_penalty = 0.5  # Significant penalty
    
    # Offer accepted then refused
    if "O_Accepted" in activities and "O_Refused" in activities:
        contradiction_penalty = 0.3
    
    # Check for logical progression
    # Expected order: Submit -> Validate -> Accept/Deny -> Offer -> Accept/Refuse
    expected_order = ["A_Submitted", "A_Accepted", "O_Created", "O_Accepted"]
    
    progression_score = 1.0
    last_expected_pos = -1
    
    for activity in activities:
        for i, expected in enumerate(expected_order):
            if activity.startswith(expected.split("_")[0]) and expected in activity:
                if i < last_expected_pos:
                    progression_score *= 0.9  # Out of order penalty
                else:
                    last_expected_pos = i
                break
    
    return loop_penalty * contradiction_penalty * progression_score


def calculate_completeness(gene: Dict[str, Any]) -> float:
    """
    Calculates the Completeness factor for a gene.
    
    Completeness measures whether all necessary steps are present.
    For loan applications, a complete successful process requires:
    - Application submitted
    - Application accepted
    - Offer created
    - Offer accepted
    
    An incomplete process (missing steps) suggests the intention
    was not fully realized.
    
    Args:
        gene: Gene dictionary with codons and metadata
        
    Returns:
        Completeness score [0, 1]
    """
    codons = gene.get("codons", [])
    activities = [c.get("action_id", "") for c in codons]
    activity_set = set(activities)
    
    # Required milestones for a complete successful process
    # Each milestone has a weight reflecting its importance
    milestones = {
        "A_Submitted": 0.2,    # Must start with submission
        "A_Accepted": 0.2,     # Application must be accepted
        "A_Complete": 0.1,     # Application completed
        "O_Created": 0.2,      # Offer must be created
        "O_Sent": 0.1,         # Offer sent to customer
        "O_Accepted": 0.2,     # Customer accepts offer
    }
    
    # Alternative completions (negative outcomes are also "complete")
    alternative_completions = {
        "A_Denied": 0.3,       # Denial is a valid completion
        "A_Cancelled": 0.3,    # Cancellation is a valid completion
        "O_Refused": 0.2,      # Refusal completes the offer phase
    }
    
    score = 0.0
    
    # Check positive milestones
    for milestone, weight in milestones.items():
        for activity in activity_set:
            if milestone in activity or activity.startswith(milestone):
                score += weight
                break
    
    # Check alternative completions
    has_alternative = False
    for alt, weight in alternative_completions.items():
        for activity in activity_set:
            if alt in activity or activity.startswith(alt):
                score += weight
                has_alternative = True
                break
    
    # Normalize to [0, 1]
    max_possible = sum(milestones.values())
    if has_alternative:
        max_possible = max(max_possible, sum(alternative_completions.values()) + 0.4)
    
    return min(1.0, score / max_possible) if max_possible > 0 else 0.0


def calculate_praxeological_score(gene: Dict[str, Any]) -> CPResult:
    """
    Calculates the complete Praxeological Motor score for a gene.
    
    The M_P score is the product of three factors:
    - Intent Alignment: Does the process move toward its goal?
    - Means-End Coherence: Are the steps logically connected?
    - Completeness: Are all necessary steps present?
    
    Formula: M_P = IntentAlignment × MeansEndCoherence × Completeness
    
    Args:
        gene: Gene dictionary with codons and metadata
        
    Returns:
        CPResult with M_P score and analysis
    """
    intent = calculate_intent_alignment(gene)
    coherence = calculate_means_end_coherence(gene)
    completeness = calculate_completeness(gene)
    
    # M_P is the product (multiplicative, like full CP)
    m_p = intent * coherence * completeness
    
    # Check for veto (any factor at zero)
    is_veto = m_p == 0 or intent == 0 or coherence == 0 or completeness == 0
    veto_reason = None
    
    if intent == 0:
        veto_reason = "Zero intent alignment - process contradicts its goal"
    elif coherence == 0:
        veto_reason = "Zero coherence - process contains fatal contradictions"
    elif completeness == 0:
        veto_reason = "Zero completeness - no progress toward goal"
    
    analysis = {
        "intent_alignment": intent,
        "means_end_coherence": coherence,
        "completeness": completeness,
        "case_length": len(gene.get("codons", [])),
        "outcome": gene.get("metadata", {}).get("outcome", {})
    }
    
    return CPResult(
        craft_performance=m_p,
        motor_scores={"praxeological": m_p},
        is_vetoed=is_veto,
        veto_motor="praxeological" if is_veto else None,
        veto_reason=veto_reason,
        analysis=analysis
    )


# ============================================================================
# EXPERIMENT CLASS
# ============================================================================

class PraxeologicalExperiment:
    """
    Scientific experiment to validate the Praxeological Motor.
    
    This class orchestrates the complete validation pipeline:
    1. Data loading and transformation
    2. Train/test split
    3. M_P score calculation for all cases
    4. Prediction evaluation against ground truth
    5. Baseline comparison
    6. Results generation
    
    The experiment is designed for full reproducibility. Given the same
    configuration and data, it produces identical results.
    """
    
    def __init__(self, config: ExperimentConfig):
        """
        Initializes the experiment with configuration.
        
        Args:
            config: ExperimentConfig with experiment parameters
        """
        self.config = config
        self.data: Optional[TransformationResult] = None
        self.genes: List[Dict[str, Any]] = []
        self.train_genes: List[Dict[str, Any]] = []
        self.test_genes: List[Dict[str, Any]] = []
        self.results: Dict[str, Any] = {}
        
        # Set random seed for reproducibility
        random.seed(config.random_seed)
        
        # Create output directory
        config.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized PraxeologicalExperiment with config: {config.to_dict()}")
    
    def load_data(self) -> None:
        """
        Loads and transforms the BPI Challenge 2017 dataset.
        """
        logger.info("Loading BPI Challenge 2017 dataset...")
        
        bpi_config = BPIConfig(
            data_path=self.config.data_path,
            max_records=self.config.max_cases * 50 if self.config.max_cases else None,
            include_incomplete_cases=True,  # Include all for analysis
            min_events_per_case=3  # Minimum meaningful process
        )
        
        loader = BPILoader(bpi_config)
        self.data = loader.transform()
        self.genes = self.data.genes
        
        logger.info(f"Loaded {len(self.genes)} genes (loan cases)")
    
    def split_data(self) -> None:
        """
        Splits genes into train and test sets.
        
        Uses stratified splitting to maintain outcome distribution.
        """
        logger.info("Splitting data into train/test sets...")
        
        # Separate by outcome for stratified split
        success_genes = []
        failure_genes = []
        
        for gene in self.genes:
            outcome = gene.get("metadata", {}).get("outcome", {}).get("status", "unknown")
            if outcome in self.config.success_outcomes:
                success_genes.append(gene)
            else:
                failure_genes.append(gene)
        
        logger.info(f"Success cases: {len(success_genes)}, Failure cases: {len(failure_genes)}")
        
        # Shuffle with fixed seed
        random.shuffle(success_genes)
        random.shuffle(failure_genes)
        
        # Split each class
        success_split = int(len(success_genes) * (1 - self.config.test_split))
        failure_split = int(len(failure_genes) * (1 - self.config.test_split))
        
        self.train_genes = (
            success_genes[:success_split] + 
            failure_genes[:failure_split]
        )
        self.test_genes = (
            success_genes[success_split:] + 
            failure_genes[failure_split:]
        )
        
        # Shuffle combined sets
        random.shuffle(self.train_genes)
        random.shuffle(self.test_genes)
        
        logger.info(f"Train set: {len(self.train_genes)}, Test set: {len(self.test_genes)}")
    
    def calculate_scores(
        self, 
        genes: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], CPResult]]:
        """
        Calculates M_P scores for a list of genes.
        
        Args:
            genes: List of gene dictionaries
            
        Returns:
            List of (gene, CPResult) tuples
        """
        results = []
        
        for gene in genes:
            score = calculate_praxeological_score(gene)
            results.append((gene, score))
        
        return results
    
    def get_ground_truth(
        self, 
        gene: Dict[str, Any]
    ) -> bool:
        """
        Extracts ground truth (success/failure) from gene metadata.
        
        Args:
            gene: Gene dictionary
            
        Returns:
            True if outcome is success, False otherwise
        """
        outcome = gene.get("metadata", {}).get("outcome", {}).get("status", "unknown")
        return outcome in self.config.success_outcomes
    
    def predict_from_score(
        self, 
        score: float, 
        threshold: Optional[float] = None
    ) -> bool:
        """
        Converts M_P score to binary prediction.
        
        Args:
            score: M_P score [0, 1]
            threshold: Decision threshold (default from config)
            
        Returns:
            True if score >= threshold (predict success)
        """
        if threshold is None:
            threshold = self.config.mp_threshold
        return score >= threshold
    
    def run_evaluation(self) -> PredictionMetrics:
        """
        Runs the main evaluation on test set.
        
        Returns:
            PredictionMetrics for M_P predictions
        """
        logger.info("Evaluating M_P predictions on test set...")
        
        scored = self.calculate_scores(self.test_genes)
        
        predictions = []
        ground_truth = []
        scores = []
        
        for gene, result in scored:
            predictions.append(self.predict_from_score(result.craft_performance))
            ground_truth.append(self.get_ground_truth(gene))
            scores.append(result.craft_performance)
        
        metrics = evaluate_predictions(
            predictions=predictions,
            ground_truth=ground_truth,
            scores=scores,
            positive_label=True
        )
        
        return metrics
    
    def run_baselines(self) -> Dict[str, BaselineComparison]:
        """
        Runs baseline comparisons.
        
        Baselines:
        1. Random: Random predictions
        2. Majority: Always predict majority class
        3. Length: Predict success if case length > median
        
        Returns:
            Dictionary of baseline names to comparison results
        """
        logger.info("Running baseline comparisons...")
        
        # Get M_P predictions and ground truth
        scored = self.calculate_scores(self.test_genes)
        
        mp_predictions = []
        ground_truth = []
        mp_scores = []
        case_lengths = []
        
        for gene, result in scored:
            mp_predictions.append(self.predict_from_score(result.craft_performance))
            ground_truth.append(self.get_ground_truth(gene))
            mp_scores.append(result.craft_performance)
            case_lengths.append(len(gene.get("codons", [])))
        
        comparisons = {}
        
        # Baseline 1: Random prediction
        random.seed(self.config.random_seed + 1)
        random_predictions = [random.random() > 0.5 for _ in ground_truth]
        
        comparisons["random"] = compare_with_baseline(
            dg_predictions=mp_predictions,
            baseline_predictions=random_predictions,
            ground_truth=ground_truth,
            baseline_name="Random Baseline",
            dg_scores=mp_scores
        )
        
        # Baseline 2: Majority class
        success_rate = sum(ground_truth) / len(ground_truth)
        majority_class = success_rate > 0.5
        majority_predictions = [majority_class] * len(ground_truth)
        
        comparisons["majority"] = compare_with_baseline(
            dg_predictions=mp_predictions,
            baseline_predictions=majority_predictions,
            ground_truth=ground_truth,
            baseline_name="Majority Class Baseline",
            dg_scores=mp_scores
        )
        
        # Baseline 3: Case length heuristic
        median_length = sorted(case_lengths)[len(case_lengths) // 2]
        length_predictions = [length > median_length for length in case_lengths]
        
        comparisons["length_heuristic"] = compare_with_baseline(
            dg_predictions=mp_predictions,
            baseline_predictions=length_predictions,
            ground_truth=ground_truth,
            baseline_name="Case Length Heuristic",
            dg_scores=mp_scores
        )
        
        return comparisons
    
    def analyze_score_distribution(self) -> Dict[str, Any]:
        """
        Analyzes the distribution of M_P scores across outcomes.
        
        Returns:
            Analysis dictionary with distributions and statistics
        """
        logger.info("Analyzing score distributions...")
        
        scored = self.calculate_scores(self.genes)
        
        success_scores = []
        failure_scores = []
        
        for gene, result in scored:
            if self.get_ground_truth(gene):
                success_scores.append(result.craft_performance)
            else:
                failure_scores.append(result.craft_performance)
        
        import statistics
        import math
        
        analysis = {
            "success": {
                "count": len(success_scores),
                "mean": statistics.mean(success_scores) if success_scores else 0,
                "median": statistics.median(success_scores) if success_scores else 0,
                "std": statistics.stdev(success_scores) if len(success_scores) > 1 else 0,
                "min": min(success_scores) if success_scores else 0,
                "max": max(success_scores) if success_scores else 0
            },
            "failure": {
                "count": len(failure_scores),
                "mean": statistics.mean(failure_scores) if failure_scores else 0,
                "median": statistics.median(failure_scores) if failure_scores else 0,
                "std": statistics.stdev(failure_scores) if len(failure_scores) > 1 else 0,
                "min": min(failure_scores) if failure_scores else 0,
                "max": max(failure_scores) if failure_scores else 0
            }
        }
        
        # Effect size (Cohen's d)
        if success_scores and failure_scores:
            pooled_std = math.sqrt(
                ((len(success_scores) - 1) * analysis["success"]["std"]**2 +
                 (len(failure_scores) - 1) * analysis["failure"]["std"]**2) /
                (len(success_scores) + len(failure_scores) - 2)
            )
            if pooled_std > 0:
                analysis["cohens_d"] = (
                    analysis["success"]["mean"] - analysis["failure"]["mean"]
                ) / pooled_std
            else:
                analysis["cohens_d"] = 0
        
        return analysis
    
    def run(self) -> Dict[str, Any]:
        """
        Executes the complete experiment.
        
        Returns:
            Dictionary containing all results
        """
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info("PRAXEOLOGICAL MOTOR VALIDATION EXPERIMENT")
        logger.info("=" * 60)
        
        # Load and prepare data
        self.load_data()
        self.split_data()
        
        # Run main evaluation
        logger.info("\nRunning main evaluation...")
        main_metrics = self.run_evaluation()
        
        # Run baseline comparisons
        logger.info("\nRunning baseline comparisons...")
        baselines = self.run_baselines()
        
        # Analyze score distributions
        logger.info("\nAnalyzing score distributions...")
        distribution = self.analyze_score_distribution()
        
        # Compile results
        elapsed = time.time() - start_time
        
        self.results = {
            "experiment": "Praxeological Motor Validation",
            "hypothesis": PraxeologicalHypothesis.H1_PREDICTION.value,
            "config": self.config.to_dict(),
            "data_statistics": self.data.statistics if self.data else {},
            "train_size": len(self.train_genes),
            "test_size": len(self.test_genes),
            "main_metrics": main_metrics.to_dict(),
            "baseline_comparisons": {
                name: comp.to_dict() for name, comp in baselines.items()
            },
            "score_distribution": distribution,
            "execution_time_seconds": round(elapsed, 2),
            "timestamp": time.time()
        }
        
        # Determine if hypothesis is supported
        self.results["hypothesis_supported"] = (
            main_metrics.f1_score > 0.5 and  # Better than random
            baselines["random"].is_significantly_better  # Statistically significant
        )
        
        return self.results
    
    def save_results(self) -> Path:
        """
        Saves results to output directory.
        
        Returns:
            Path to the saved results file
        """
        output_path = self.config.output_dir / "praxeological_validation_results.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Results saved to {output_path}")
        return output_path
    
    def print_report(self) -> None:
        """
        Prints a human-readable report of the results.
        """
        if not self.results:
            logger.warning("No results to report. Run experiment first.")
            return
        
        print("\n" + "=" * 70)
        print("PRAXEOLOGICAL MOTOR VALIDATION - EXPERIMENT REPORT")
        print("=" * 70)
        
        print(f"\nHypothesis: {self.results.get('hypothesis', PraxeologicalHypothesis.H1_PREDICTION.value)}")
        print(f"Dataset: {self.results.get('data_source', 'BPI Challenge 2017')}")
        print(f"Train samples: {self.results.get('train_size', len(self.train_genes))}")
        print(f"Test samples: {self.results.get('test_size', len(self.test_genes))}")
        
        print("\n" + "-" * 50)
        print("MAIN RESULTS (Test Set)")
        print("-" * 50)
        
        metrics = self.results.get('metrics', self.results.get('main_metrics', {}))
        print(f"Accuracy:    {metrics.get('accuracy', 0):.4f}")
        print(f"Precision:   {metrics.get('precision', 0):.4f}")
        print(f"Recall:      {metrics.get('recall', 0):.4f}")
        print(f"F1 Score:    {metrics.get('f1_score', 0):.4f}")
        if metrics.get('roc_auc'):
            print(f"ROC-AUC:     {metrics['roc_auc']:.4f}")
        
        print("\n" + "-" * 50)
        print("BASELINE COMPARISONS")
        print("-" * 50)
        
        baseline_comparisons = self.results.get('baseline_comparisons', {})
        for name, comparison in baseline_comparisons.items():
            dg_f1 = comparison['digital_genome']['f1_score']
            bl_f1 = comparison['baseline']['f1_score']
            improvement = comparison['improvement']['f1_score']
            significant = comparison['is_significantly_better']
            
            print(f"\nvs {comparison['baseline_name']}:")
            print(f"  DG F1: {dg_f1:.4f}, Baseline F1: {bl_f1:.4f}")
            print(f"  Improvement: {improvement:+.2%}")
            print(f"  Statistically significant: {significant}")
        
        print("\n" + "-" * 50)
        print("SCORE DISTRIBUTION ANALYSIS")
        print("-" * 50)
        
        dist = self.results.get('score_distribution', {})
        if dist:
            success_data = dist.get('success', {})
            failure_data = dist.get('failure', {})
            print(f"\nSuccess cases (n={success_data.get('count', 0)}):")
            print(f"  Mean M_P: {success_data.get('mean', 0):.4f} ± {success_data.get('std', 0):.4f}")
            print(f"\nFailure cases (n={failure_data.get('count', 0)}):")
            print(f"  Mean M_P: {failure_data.get('mean', 0):.4f} ± {failure_data.get('std', 0):.4f}")
            
            if 'cohens_d' in dist:
                print(f"\nEffect size (Cohen's d): {dist['cohens_d']:.4f}")
                if abs(dist['cohens_d']) > 0.8:
                    print("  Interpretation: LARGE effect")
                elif abs(dist['cohens_d']) > 0.5:
                    print("  Interpretation: MEDIUM effect")
                elif abs(dist['cohens_d']) > 0.2:
                    print("  Interpretation: SMALL effect")
                else:
                    print("  Interpretation: NEGLIGIBLE effect")
        
        print("\n" + "-" * 50)
        print("CONCLUSION")
        print("-" * 50)
        
        hypothesis_supported = self.results.get('hypothesis_supported', 
            metrics.get('f1_score', 0) > 0.5)
        
        if hypothesis_supported:
            print("\n✓ HYPOTHESIS SUPPORTED")
            print("The Praxeological Motor demonstrates predictive capability")
            print("for loan application outcomes that is statistically better")
            print("than random baseline.")
        else:
            print("\n✗ HYPOTHESIS NOT SUPPORTED")
            print("The Praxeological Motor did not demonstrate statistically")
            print("significant improvement over baselines.")
        
        exec_time = self.results.get('execution_time_seconds', 0)
        print(f"\nExecution time: {exec_time}s")
        print("\n" + "=" * 70)


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def run_praxeological_validation(
    data_path: str,
    output_dir: str = "./results",
    max_cases: Optional[int] = None
) -> Dict[str, Any]:
    """
    Convenience function to run the complete validation experiment.
    
    Args:
        data_path: Path to BPI Challenge 2017 XES file
        output_dir: Directory for output files
        max_cases: Maximum cases to process (None = all)
        
    Returns:
        Experiment results dictionary
    """
    config = ExperimentConfig(
        data_path=Path(data_path),
        output_dir=Path(output_dir),
        max_cases=max_cases
    )
    
    experiment = PraxeologicalExperiment(config)
    results = experiment.run()
    experiment.save_results()
    experiment.print_report()
    
    return results


# ============================================================================
# SYNTHETIC DATA FOR TESTING WITHOUT REAL DATASET
# ============================================================================

def generate_synthetic_genes(n_genes: int = 100, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Generates synthetic gene data for testing the experiment pipeline.
    
    This allows testing the experiment code without requiring the
    actual BPI Challenge dataset.
    
    Args:
        n_genes: Number of genes to generate
        seed: Random seed
        
    Returns:
        List of synthetic gene dictionaries
    """
    random.seed(seed)
    
    # Activity templates
    positive_activities = [
        "A_Submitted", "A_Create Application", "A_Complete",
        "A_Accepted", "O_Create Offer", "O_Created", "O_Sent", "O_Accepted"
    ]
    
    negative_activities = [
        "A_Denied", "A_Cancelled", "O_Refused", "O_Cancelled"
    ]
    
    workflow_activities = [
        "W_Handle leads", "W_Complete application", "W_Call after offers",
        "W_Validate application", "W_Call incomplete files"
    ]
    
    genes = []
    
    for i in range(n_genes):
        # Determine outcome (60% success, 40% failure for realistic imbalance)
        is_success = random.random() < 0.6
        
        # Generate activity sequence
        n_activities = random.randint(5, 20)
        activities = []
        
        # Start with submission
        activities.append("A_Submitted")
        
        # Add workflow activities
        for _ in range(random.randint(2, 8)):
            activities.append(random.choice(workflow_activities))
        
        if is_success:
            # Successful path
            activities.extend(["A_Accepted", "O_Created", "O_Sent"])
            if random.random() < 0.7:
                activities.append("O_Accepted")
        else:
            # Failure path
            if random.random() < 0.5:
                activities.append("A_Denied")
            else:
                activities.append("A_Cancelled")
        
        # Build codons
        codons = []
        for j, activity in enumerate(activities):
            codons.append({
                "uid": hashlib.sha256(f"{i}_{j}".encode()).hexdigest(),
                "entity_id": f"Resource_{random.randint(1, 10)}",
                "action_id": activity,
                "target_state_id": f"{activity}_complete",
                "timestamp": time.time() + j * 3600,
                "context": {"position": j}
            })
        
        gene = {
            "uid": hashlib.sha256(f"gene_{i}".encode()).hexdigest(),
            "name": f"SyntheticLoan_{i}",
            "purpose": "Process synthetic loan application",
            "codons": codons,
            "metadata": {
                "case_id": f"case_{i}",
                "outcome": {
                    "status": "accepted" if is_success else random.choice(["denied", "cancelled"]),
                    "application_accepted": is_success
                }
            }
        }
        
        genes.append(gene)
    
    return genes


def run_synthetic_test():
    """
    Runs the experiment with synthetic data for testing.
    """
    print("\n" + "=" * 70)
    print("SYNTHETIC DATA TEST")
    print("Testing experiment pipeline without real dataset")
    print("=" * 70)
    
    # Generate synthetic data
    genes = generate_synthetic_genes(n_genes=500, seed=42)
    print(f"\nGenerated {len(genes)} synthetic genes")
    
    # Create a minimal experiment
    config = ExperimentConfig(
        data_path=Path("/tmp/synthetic"),  # Not used for synthetic
        output_dir=Path("/tmp/results"),
        random_seed=42
    )
    
    experiment = PraxeologicalExperiment(config)
    experiment.genes = genes
    experiment.split_data()
    
    # Run evaluation
    print("\nRunning evaluation on synthetic data...")
    metrics = experiment.run_evaluation()
    
    print("\n" + "-" * 50)
    print("SYNTHETIC DATA RESULTS")
    print("-" * 50)
    print(metrics.format_report())
    
    # Analyze distribution
    distribution = experiment.analyze_score_distribution()
    
    print("\n" + "-" * 50)
    print("SCORE DISTRIBUTION")
    print("-" * 50)
    print(f"Success mean: {distribution['success']['mean']:.4f}")
    print(f"Failure mean: {distribution['failure']['mean']:.4f}")
    if 'cohens_d' in distribution:
        print(f"Cohen's d: {distribution['cohens_d']:.4f}")
    
    print("\n✓ Synthetic test completed successfully")
    print("The experiment pipeline is functional.")
    print("To run with real data, provide path to BPI_Challenge_2017.xes.gz")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Command-line interface for the experiment.
    
    Usage:
        python exp_praxeological.py <path_to_xes_file> [max_cases]
        python exp_praxeological.py --synthetic  # Run with synthetic data
    """
    import math  # Needed for effect size calculation
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python exp_praxeological.py <path_to_xes_file> [max_cases]")
        print("  python exp_praxeological.py --synthetic")
        print("\nExamples:")
        print("  python exp_praxeological.py ./BPI_Challenge_2017.xes.gz")
        print("  python exp_praxeological.py ./BPI_Challenge_2017.xes.gz 1000")
        print("  python exp_praxeological.py --synthetic")
        sys.exit(1)
    
    if sys.argv[1] == "--synthetic":
        run_synthetic_test()
    else:
        data_path = sys.argv[1]
        max_cases = int(sys.argv[2]) if len(sys.argv) > 2 else None
        
        run_praxeological_validation(data_path, max_cases=max_cases)
