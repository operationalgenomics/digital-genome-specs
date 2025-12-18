"""
Experiments Module for Empirical Validation
============================================

This submodule contains the scientific experiments that validate the
Digital Genome framework against benchmark datasets.

EXPERIMENT STRUCTURE:
---------------------
Each experiment follows a standardized structure:

1. Hypothesis: Clear statement of what is being tested
2. Dataset: Which benchmark data is used
3. Methodology: Step-by-step procedure
4. Metrics: How success is measured
5. Baselines: What methods are compared against
6. Results: Reproducible outputs

AVAILABLE EXPERIMENTS:
----------------------

exp_praxeological.py
    Validates the Praxeological Motor using BPI Challenge 2017.
    Tests whether M_P correctly identifies intention-realization failures
    in business process logs.

exp_chaotic.py (planned)
    Validates the Chaotic Motor using NASA C-MAPSS.
    Tests whether M_C improves remaining useful life prediction.

exp_nash.py (planned)
    Validates the Nash Motor using market/traffic data.
    Tests whether M_N identifies strategic instabilities.

exp_integrated.py (planned)
    Validates the complete Craft Performance formula.
    Tests whether multiplicative aggregation outperforms additive.

REPRODUCIBILITY:
----------------
All experiments are designed for full reproducibility:
- Random seeds are fixed and documented
- All hyperparameters are versioned
- Data splits are deterministic
- Results include confidence intervals
"""

from .exp_praxeological import (
    PraxeologicalExperiment,
    PraxeologicalHypothesis,
    run_praxeological_validation
)

__all__ = [
    'PraxeologicalExperiment',
    'PraxeologicalHypothesis',
    'run_praxeological_validation',
]
