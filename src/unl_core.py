"""
UNL Core - The Universal Neutral Language (v3.1 - Fix Syntax)
=======================================================================
Description:
    Implements the Ontology of UNL-0 ("Pre-sensory Perception").
    This module analyzes Signal Topology rather than semantic content.
    It acts as the "ears" of the system, interpreting raw signals.

PHILOSOPHY (The Flute Without Sound):
- Perfection is captured order, even if not understood.
- Lack of signal is Action (Stability/Void).
- Agency is inferred via Harmonic Signatures (Entropy, Periodicity, Volatility).

Reference: "The Ontology of UNL-0 and the Universal Epistemology of the Digital Genome"
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import logging
import math

# Setup Logging
logger = logging.getLogger("UNL_Core")

# --- UNL-0 PRIMITIVES ---
class OntologyType:
    MACHINE = "machine"       # High Repetition, Cyclic, Rigid Limits
    HUMAN = "human"           # Transactional, Bursty, Pareto Distribution
    NATURE = "nature"         # Fractal, Continuous, 1/f Noise
    ENTROPY = "pure_entropy"  # Randomness / Unknown
    VOID = "void"             # The "Lack of" -> Action of Non-Existence

class SemanticIntent:
    # Normalized intents based on signal direction
    EXECUTE = "execute"     # (Output/Emission)
    OBSERVE = "observe"     # (Input/Sensor)
    STABILIZE = "stabilize" # (Resistance to Change)

@dataclass
class HarmonicSignature:
    """The mathematical shape of the entity based on its signal topology."""
    periodicity: float  # 0.0 (Chaos) to 1.0 (Metronome)
    entropy: float      # Shannon Entropy of the signal
    volatility: float   # StdDev relative to Mean
    linearity: float    # R-squared of trend
    agency_type: str    # The inferred Ontology

class UNLEngine:
    def __init__(self):
        logger.info("UNL-0 Core Online. Listening to the Silent Flute...")

    def _calculate_entropy(self, signal: List[float]) -> float:
        """Calculates Shannon Entropy of a signal distribution."""
        if not signal or len(signal) < 2: return 0.0
        # Create histogram
        hist, _ = np.histogram(signal, bins=10, density=True)
        # Filter zeros to avoid log(0)
        hist = hist[hist > 0]
        return -np.sum(hist * np.log(hist))

    def _calculate_periodicity(self, signal: List[float]) -> float:
        """
        Uses FFT (Fast Fourier Transform) to detect dominant cycles.
        Heuristic: Machines hum (peaks); Nature flows; Humans stutter.
        """
        if len(signal) < 4: return 0.0
        
        # Remove DC component (mean)
        sig_array = np.array(signal)
        sig_array = sig_array - np.mean(sig_array)
        
        # FFT
        fft_vals = np.absolute(np.fft.rfft(sig_array))
        
        # Peak strength vs Background noise
        if np.sum(fft_vals) == 0: return 0.0
        peak = np.max(fft_vals)
        total = np.sum(fft_vals)
        
        # A pure sine wave has all energy in one peak (Ratio ~1.0)
        # White noise has energy spread everywhere (Ratio low)
        return peak / total

    def infer_agency_from_signal(self, signal_stream: List[float]) -> HarmonicSignature:
        """
        The Core Logic of UNL-0.
        Classifies a stream of numbers as Machine, Human, or Nature based on topology.
        """
        # 1. Handle "The Lack of" (Axiom 0)
        # If signal is empty or constant zero/null, it is a VOID action.
        if not signal_stream or all(v == 0 for v in signal_stream):
            return HarmonicSignature(0, 0, 0, 1, OntologyType.VOID)

        # 2. Analyze Topology
        sig_array = np.array(signal_stream)
        
        # Volatility (Coefficient of Variation)
        mean = np.mean(sig_array)
        std = np.std(sig_array)
        volatility = (std / mean) if mean != 0 else 0
        
        # Entropy (Information Density)
        entropy = self._calculate_entropy(signal_stream)
        
        # Periodicity (Rhythm)
        periodicity = self._calculate_periodicity(signal_stream)

        # 3. Infer Ontology based on Signatures
        # These thresholds are the "Ears" of the UNL-0.
        
        agency = OntologyType.ENTROPY # Default to Unknown
        
        # MACHINE SIGNATURE: High Rhythm, Low Entropy (Ordered)
        # Turbines vibrate at specific frequencies.
        if periodicity > 0.3 and entropy < 2.0:
            agency = OntologyType.MACHINE
            
        # HUMAN SIGNATURE: High Volatility, Low Rhythm (Bursty/Transactional)
        # Humans don't work in perfect cycles. They do big things, then wait.
        elif volatility > 0.5 and periodicity < 0.2:
            agency = OntologyType.HUMAN
            
        # NATURE SIGNATURE: Moderate Entropy, Low Volatility (Smooth), No Rhythm
        # Temperature/Pressure changes slowly and continuously.
        elif volatility < 0.1 and periodicity < 0.1:
            agency = OntologyType.NATURE
            
        return HarmonicSignature(periodicity, entropy, volatility, 0.0, agency)

    def process_gene_rna(self, gene_metadata: Dict, signal_sample: List[float]) -> str:
        """
        Main entry point.
        Receives metadata (Context) + Signal (Reality).
        Returns the Ontological Classification.
        """
        # 1. Try Signal Topology First (UNL-0 / Pre-sensory)
        # This is the "Flute without Sound" - pure math.
        if signal_sample and len(signal_sample) > 5:
            signature = self.infer_agency_from_signal(signal_sample)
            return signature.agency_type
            
        # 2. Fallback to Metadata Analysis (if no signal available)
        # Strictly for initialization or empty genes
        desc = gene_metadata.get("description", "").lower()
        src = gene_metadata.get("source_file", "").lower()
        
        if "turb" in desc or "engine" in desc or "sensor" in desc: return OntologyType.MACHINE
        if "user" in desc or "loan" in desc or "bpi" in src: return OntologyType.HUMAN
        if "rain" in desc or "weather" in desc: return OntologyType.NATURE
        
        return OntologyType.UNKNOWN