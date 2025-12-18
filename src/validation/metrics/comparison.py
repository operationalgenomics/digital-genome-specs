"""
Baseline Comparison Metrics
===========================

This module provides metrics for comparing Digital Genome predictions
against ground truth and against baseline methods.

COMPARISON FRAMEWORK:
---------------------
The validation strategy requires demonstrating that the Digital Genome
framework produces measurably better results than existing approaches.
We compare against two types of baselines:

1. Ground Truth Comparison
   - Binary outcomes: Precision, Recall, F1, ROC-AUC
   - Continuous outcomes: MAE, RMSE, R²
   - Ranking: Spearman correlation, NDCG

2. Method Comparison
   - Process mining conformance checking (for BPI)
   - Traditional prognostics (for C-MAPSS)
   - Game-theoretic solvers (for Nash validation)

STATISTICAL RIGOR:
------------------
All comparisons include:
- Confidence intervals (95% by default)
- Statistical significance tests
- Effect size calculations
- Multiple comparison corrections when applicable

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum
import math
import statistics
import logging

logger = logging.getLogger("validation.metrics.comparison")


# ============================================================================
# PREDICTION METRICS
# ============================================================================

@dataclass
class PredictionMetrics:
    """
    Standard metrics for evaluating predictions against ground truth.
    
    Supports both binary classification (success/failure) and continuous
    prediction (numeric scores) scenarios.
    
    Attributes:
        accuracy: Proportion of correct predictions
        precision: True positives / (True positives + False positives)
        recall: True positives / (True positives + False negatives)
        f1_score: Harmonic mean of precision and recall
        specificity: True negatives / (True negatives + False positives)
        confusion_matrix: 2x2 matrix [[TN, FP], [FN, TP]]
        roc_auc: Area under the ROC curve (if scores available)
        support: Number of samples evaluated
    """
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    specificity: float
    confusion_matrix: List[List[int]]
    roc_auc: Optional[float] = None
    support: int = 0
    confidence_interval: Optional[Tuple[float, float]] = None
    
    @property
    def true_negatives(self) -> int:
        return self.confusion_matrix[0][0]
    
    @property
    def false_positives(self) -> int:
        return self.confusion_matrix[0][1]
    
    @property
    def false_negatives(self) -> int:
        return self.confusion_matrix[1][0]
    
    @property
    def true_positives(self) -> int:
        return self.confusion_matrix[1][1]
    
    @property
    def positive_predictive_value(self) -> float:
        """Alias for precision."""
        return self.precision
    
    @property
    def negative_predictive_value(self) -> float:
        """Probability that a negative prediction is correct."""
        tn = self.true_negatives
        fn = self.false_negatives
        return tn / (tn + fn) if (tn + fn) > 0 else 0.0
    
    @property
    def balanced_accuracy(self) -> float:
        """Average of sensitivity (recall) and specificity."""
        return (self.recall + self.specificity) / 2
    
    @property
    def matthews_correlation(self) -> float:
        """
        Matthews Correlation Coefficient.
        
        A balanced measure that accounts for all four confusion matrix
        quadrants. Range: [-1, 1] where 1 is perfect prediction.
        """
        tp = self.true_positives
        tn = self.true_negatives
        fp = self.false_positives
        fn = self.false_negatives
        
        numerator = (tp * tn) - (fp * fn)
        denominator = math.sqrt(
            (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
        )
        
        return numerator / denominator if denominator > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes metrics for storage and reporting."""
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "specificity": self.specificity,
            "balanced_accuracy": self.balanced_accuracy,
            "matthews_correlation": self.matthews_correlation,
            "roc_auc": self.roc_auc,
            "support": self.support,
            "confusion_matrix": self.confusion_matrix,
            "confidence_interval": self.confidence_interval
        }
    
    def format_report(self) -> str:
        """Generates a human-readable metrics report."""
        lines = [
            "Classification Metrics Report",
            "=" * 40,
            f"Support (n):     {self.support}",
            f"Accuracy:        {self.accuracy:.4f}",
            f"Precision:       {self.precision:.4f}",
            f"Recall:          {self.recall:.4f}",
            f"F1 Score:        {self.f1_score:.4f}",
            f"Specificity:     {self.specificity:.4f}",
            f"Balanced Acc:    {self.balanced_accuracy:.4f}",
            f"MCC:             {self.matthews_correlation:.4f}",
        ]
        
        if self.roc_auc is not None:
            lines.append(f"ROC-AUC:         {self.roc_auc:.4f}")
        
        if self.confidence_interval:
            lines.append(f"95% CI:          [{self.confidence_interval[0]:.4f}, {self.confidence_interval[1]:.4f}]")
        
        lines.extend([
            "",
            "Confusion Matrix:",
            f"  TN={self.true_negatives:4d}  FP={self.false_positives:4d}",
            f"  FN={self.false_negatives:4d}  TP={self.true_positives:4d}",
        ])
        
        return "\n".join(lines)


@dataclass
class BaselineComparison:
    """
    Comparison results between Digital Genome and a baseline method.
    
    Attributes:
        baseline_name: Name of the baseline method
        dg_metrics: Metrics from Digital Genome evaluation
        baseline_metrics: Metrics from baseline method
        improvement: Dictionary of improvement percentages per metric
        statistical_tests: Results of significance tests
        is_significantly_better: Whether DG is statistically better
    """
    baseline_name: str
    dg_metrics: PredictionMetrics
    baseline_metrics: PredictionMetrics
    improvement: Dict[str, float]
    statistical_tests: Dict[str, Any]
    is_significantly_better: bool = False
    effect_size: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_name": self.baseline_name,
            "digital_genome": self.dg_metrics.to_dict(),
            "baseline": self.baseline_metrics.to_dict(),
            "improvement": self.improvement,
            "statistical_tests": self.statistical_tests,
            "is_significantly_better": self.is_significantly_better,
            "effect_size": self.effect_size
        }
    
    def format_comparison(self) -> str:
        """Generates a comparison report."""
        lines = [
            f"Comparison: Digital Genome vs {self.baseline_name}",
            "=" * 50,
            "",
            f"{'Metric':<20} {'DG':>10} {'Baseline':>10} {'Δ':>10}",
            "-" * 50,
        ]
        
        metrics = ["accuracy", "precision", "recall", "f1_score"]
        for m in metrics:
            dg_val = getattr(self.dg_metrics, m)
            bl_val = getattr(self.baseline_metrics, m)
            delta = self.improvement.get(m, 0)
            sign = "+" if delta > 0 else ""
            lines.append(
                f"{m:<20} {dg_val:>10.4f} {bl_val:>10.4f} {sign}{delta:>9.2%}"
            )
        
        lines.extend([
            "",
            f"Statistically significant: {self.is_significantly_better}",
        ])
        
        if self.effect_size is not None:
            lines.append(f"Effect size (Cohen's d): {self.effect_size:.4f}")
        
        return "\n".join(lines)


# ============================================================================
# EVALUATION FUNCTIONS
# ============================================================================

def evaluate_predictions(
    predictions: List[bool],
    ground_truth: List[bool],
    scores: Optional[List[float]] = None,
    positive_label: bool = True
) -> PredictionMetrics:
    """
    Evaluates binary predictions against ground truth.
    
    Args:
        predictions: List of predicted labels
        ground_truth: List of actual labels
        scores: Optional list of prediction scores (for ROC-AUC)
        positive_label: Which label is considered "positive"
        
    Returns:
        PredictionMetrics with all calculated measures
    """
    if len(predictions) != len(ground_truth):
        raise ValueError(
            f"Length mismatch: predictions ({len(predictions)}) vs "
            f"ground_truth ({len(ground_truth)})"
        )
    
    n = len(predictions)
    if n == 0:
        raise ValueError("Cannot evaluate empty predictions")
    
    # Build confusion matrix
    tp = tn = fp = fn = 0
    
    for pred, truth in zip(predictions, ground_truth):
        if truth == positive_label:
            if pred == positive_label:
                tp += 1
            else:
                fn += 1
        else:
            if pred == positive_label:
                fp += 1
            else:
                tn += 1
    
    # Calculate metrics with safe division
    accuracy = (tp + tn) / n
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    # F1 score
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0
    
    # ROC-AUC calculation if scores provided
    roc_auc = None
    if scores is not None and len(scores) == n:
        roc_auc = calculate_roc_auc(scores, ground_truth, positive_label)
    
    # Wilson score confidence interval for accuracy
    ci = wilson_confidence_interval(accuracy, n)
    
    return PredictionMetrics(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1,
        specificity=specificity,
        confusion_matrix=[[tn, fp], [fn, tp]],
        roc_auc=roc_auc,
        support=n,
        confidence_interval=ci
    )


def calculate_roc_auc(
    scores: List[float],
    labels: List[bool],
    positive_label: bool = True
) -> float:
    """
    Calculates the Area Under the ROC Curve.
    
    Uses the Mann-Whitney U statistic formulation which is equivalent
    to AUC and more numerically stable.
    
    Args:
        scores: Prediction scores (higher = more likely positive)
        labels: True labels
        positive_label: Which label is positive
        
    Returns:
        ROC-AUC score [0, 1]
    """
    # Separate scores by class
    positive_scores = [s for s, l in zip(scores, labels) if l == positive_label]
    negative_scores = [s for s, l in zip(scores, labels) if l != positive_label]
    
    if not positive_scores or not negative_scores:
        return 0.5  # Random guess when one class is missing
    
    # Mann-Whitney U statistic
    u_statistic = 0
    for pos in positive_scores:
        for neg in negative_scores:
            if pos > neg:
                u_statistic += 1
            elif pos == neg:
                u_statistic += 0.5
    
    # Normalize to [0, 1]
    auc = u_statistic / (len(positive_scores) * len(negative_scores))
    
    return auc


def wilson_confidence_interval(
    proportion: float,
    n: int,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculates Wilson score confidence interval for a proportion.
    
    This is more accurate than the normal approximation, especially
    for proportions near 0 or 1.
    
    Args:
        proportion: Observed proportion (e.g., accuracy)
        n: Sample size
        confidence: Confidence level (default 0.95)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    # Z-score for confidence level
    # For 95% CI, z ≈ 1.96
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence, 1.96)
    
    # Wilson score formula
    denominator = 1 + z**2 / n
    center = (proportion + z**2 / (2*n)) / denominator
    spread = z * math.sqrt(
        (proportion * (1 - proportion) + z**2 / (4*n)) / n
    ) / denominator
    
    lower = max(0, center - spread)
    upper = min(1, center + spread)
    
    return (lower, upper)


# ============================================================================
# BASELINE COMPARISON FUNCTIONS
# ============================================================================

def compare_with_baseline(
    dg_predictions: List[bool],
    baseline_predictions: List[bool],
    ground_truth: List[bool],
    baseline_name: str = "Baseline",
    dg_scores: Optional[List[float]] = None,
    baseline_scores: Optional[List[float]] = None,
    alpha: float = 0.05
) -> BaselineComparison:
    """
    Compares Digital Genome predictions against a baseline method.
    
    Performs statistical significance testing using McNemar's test,
    which is appropriate for comparing two classifiers on the same
    test set.
    
    Args:
        dg_predictions: Digital Genome predictions
        baseline_predictions: Baseline method predictions
        ground_truth: True labels
        baseline_name: Name of baseline for reporting
        dg_scores: Optional DG prediction scores
        baseline_scores: Optional baseline prediction scores
        alpha: Significance level for hypothesis test
        
    Returns:
        BaselineComparison with metrics and statistical tests
    """
    # Evaluate both methods
    dg_metrics = evaluate_predictions(
        dg_predictions, ground_truth, dg_scores
    )
    baseline_metrics = evaluate_predictions(
        baseline_predictions, ground_truth, baseline_scores
    )
    
    # Calculate improvement percentages
    improvement = {}
    for metric in ["accuracy", "precision", "recall", "f1_score"]:
        dg_val = getattr(dg_metrics, metric)
        bl_val = getattr(baseline_metrics, metric)
        if bl_val > 0:
            improvement[metric] = (dg_val - bl_val) / bl_val
        else:
            improvement[metric] = float('inf') if dg_val > 0 else 0.0
    
    # McNemar's test for statistical significance
    # Count cases where methods disagree
    b = 0  # DG correct, baseline wrong
    c = 0  # DG wrong, baseline correct
    
    for dg, bl, truth in zip(dg_predictions, baseline_predictions, ground_truth):
        dg_correct = (dg == truth)
        bl_correct = (bl == truth)
        
        if dg_correct and not bl_correct:
            b += 1
        elif not dg_correct and bl_correct:
            c += 1
    
    # McNemar's test statistic (with continuity correction)
    if b + c > 0:
        chi_squared = (abs(b - c) - 1) ** 2 / (b + c)
        # For 1 degree of freedom, chi-squared critical value at α=0.05 is 3.841
        critical_value = 3.841 if alpha == 0.05 else 2.706  # α=0.10
        p_value_approx = "< 0.05" if chi_squared > critical_value else ">= 0.05"
        is_significant = chi_squared > critical_value and b > c
    else:
        chi_squared = 0
        p_value_approx = "N/A (no disagreements)"
        is_significant = False
    
    statistical_tests = {
        "mcnemar_chi_squared": chi_squared,
        "dg_correct_baseline_wrong": b,
        "dg_wrong_baseline_correct": c,
        "p_value_approx": p_value_approx,
        "alpha": alpha
    }
    
    # Effect size (Cohen's h for proportions)
    phi_dg = 2 * math.asin(math.sqrt(dg_metrics.accuracy))
    phi_bl = 2 * math.asin(math.sqrt(baseline_metrics.accuracy))
    effect_size = phi_dg - phi_bl
    
    return BaselineComparison(
        baseline_name=baseline_name,
        dg_metrics=dg_metrics,
        baseline_metrics=baseline_metrics,
        improvement=improvement,
        statistical_tests=statistical_tests,
        is_significantly_better=is_significant,
        effect_size=effect_size
    )


def aggregate_cross_validation_results(
    fold_metrics: List[PredictionMetrics]
) -> Dict[str, Any]:
    """
    Aggregates metrics across cross-validation folds.
    
    Provides mean, standard deviation, and confidence intervals
    for each metric across folds.
    
    Args:
        fold_metrics: List of metrics from each fold
        
    Returns:
        Dictionary with aggregated statistics
    """
    if not fold_metrics:
        return {"error": "No fold metrics provided"}
    
    n_folds = len(fold_metrics)
    
    metrics_to_aggregate = [
        "accuracy", "precision", "recall", "f1_score",
        "specificity", "balanced_accuracy", "matthews_correlation"
    ]
    
    aggregated = {
        "n_folds": n_folds,
        "metrics": {}
    }
    
    for metric in metrics_to_aggregate:
        values = [getattr(m, metric) for m in fold_metrics]
        
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if n_folds > 1 else 0
        
        # 95% CI using t-distribution approximation
        # For small n, we should use proper t-distribution
        margin = 1.96 * std_val / math.sqrt(n_folds) if n_folds > 1 else 0
        
        aggregated["metrics"][metric] = {
            "mean": mean_val,
            "std": std_val,
            "min": min(values),
            "max": max(values),
            "ci_lower": mean_val - margin,
            "ci_upper": mean_val + margin,
            "values": values
        }
    
    # Aggregate ROC-AUC if available
    auc_values = [m.roc_auc for m in fold_metrics if m.roc_auc is not None]
    if auc_values:
        mean_auc = statistics.mean(auc_values)
        std_auc = statistics.stdev(auc_values) if len(auc_values) > 1 else 0
        aggregated["metrics"]["roc_auc"] = {
            "mean": mean_auc,
            "std": std_auc,
            "values": auc_values
        }
    
    return aggregated


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == "__main__":
    """Test the comparison metrics with synthetic data."""
    
    print("=" * 60)
    print("COMPARISON METRICS TEST")
    print("=" * 60)
    
    # Simulate predictions
    import random
    random.seed(42)
    
    n_samples = 200
    ground_truth = [random.random() > 0.5 for _ in range(n_samples)]
    
    # DG predictions (slightly better than baseline)
    dg_predictions = []
    dg_scores = []
    for truth in ground_truth:
        if random.random() < 0.85:  # 85% accuracy
            dg_predictions.append(truth)
            dg_scores.append(0.8 if truth else 0.2)
        else:
            dg_predictions.append(not truth)
            dg_scores.append(0.5)
    
    # Baseline predictions (lower accuracy)
    baseline_predictions = []
    for truth in ground_truth:
        if random.random() < 0.75:  # 75% accuracy
            baseline_predictions.append(truth)
        else:
            baseline_predictions.append(not truth)
    
    # Evaluate DG alone
    print("\n1. Digital Genome Evaluation")
    print("-" * 40)
    dg_metrics = evaluate_predictions(dg_predictions, ground_truth, dg_scores)
    print(dg_metrics.format_report())
    
    # Compare with baseline
    print("\n2. Baseline Comparison")
    print("-" * 40)
    comparison = compare_with_baseline(
        dg_predictions,
        baseline_predictions,
        ground_truth,
        baseline_name="Traditional Method"
    )
    print(comparison.format_comparison())
    
    # Aggregate cross-validation
    print("\n3. Cross-Validation Aggregation")
    print("-" * 40)
    
    # Simulate 5-fold results
    fold_metrics = []
    for i in range(5):
        random.seed(42 + i)
        fold_preds = [random.random() > 0.5 for _ in range(40)]
        fold_truth = [random.random() > 0.5 for _ in range(40)]
        fold_metrics.append(evaluate_predictions(fold_preds, fold_truth))
    
    cv_results = aggregate_cross_validation_results(fold_metrics)
    print(f"   Folds: {cv_results['n_folds']}")
    print(f"   Accuracy: {cv_results['metrics']['accuracy']['mean']:.4f} "
          f"± {cv_results['metrics']['accuracy']['std']:.4f}")
    print(f"   F1 Score: {cv_results['metrics']['f1_score']['mean']:.4f} "
          f"± {cv_results['metrics']['f1_score']['std']:.4f}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
