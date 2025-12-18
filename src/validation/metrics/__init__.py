"""
Metrics Module for Empirical Validation
========================================

This submodule provides quantitative measures for evaluating the Digital Genome
framework against baselines and ground truth.

METRIC CATEGORIES:
------------------

1. Craft Performance Metrics
   - CP calculation validation
   - Motor score distributions
   - Veto frequency analysis

2. Comparison Metrics
   - Precision, Recall, F1 against ground truth
   - ROC-AUC for outcome prediction
   - Baseline method comparison

3. Statistical Significance
   - Confidence intervals
   - Hypothesis testing
   - Effect size calculation

SCIENTIFIC STANDARDS:
---------------------
All metrics follow established standards for machine learning evaluation:
- Proper train/test splits to avoid data leakage
- Cross-validation for robust estimates
- Multiple random seeds for variance estimation
- Clear reporting of all hyperparameters
"""

from .craft_performance import (
    calculate_cp,
    CPResult,
    CPDistribution,
    analyze_motor_contributions
)

from .comparison import (
    evaluate_predictions,
    PredictionMetrics,
    compare_with_baseline,
    BaselineComparison
)

__all__ = [
    'calculate_cp',
    'CPResult',
    'CPDistribution',
    'analyze_motor_contributions',
    'evaluate_predictions',
    'PredictionMetrics',
    'compare_with_baseline',
    'BaselineComparison',
]
