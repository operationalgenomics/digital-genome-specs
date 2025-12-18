"""
Dataset Loaders for Empirical Validation
=========================================

This submodule provides data transformation utilities that convert raw benchmark
datasets into Praxeological Codons suitable for motor evaluation.

TRANSFORMATION PHILOSOPHY:
--------------------------
The critical insight of Operational Genomics is that raw data already contains
intentional structure — it merely needs to be recognized and codified. These
loaders do not impose external structure on data; they extract the inherent
praxeological structure that exists within purposeful human activities.

AVAILABLE LOADERS:
------------------
- BPILoader: Business Process Intelligence Challenge datasets
- CMAPSSLoader: NASA turbofan degradation simulation
- ASRSLoader: NASA Aviation Safety Reporting System

Each loader implements the BaseLoader interface, ensuring consistent
transformation pipelines across different data domains.
"""

from .base_loader import BaseLoader, LoaderConfig, TransformationResult
from .bpi_loader import BPILoader, BPIConfig

__all__ = [
    'BaseLoader',
    'LoaderConfig', 
    'TransformationResult',
    'BPILoader',
    'BPIConfig',
]
