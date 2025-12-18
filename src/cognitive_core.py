"""
Cognitive Core - The Vectorized Intelligence (v5.0 - Tensor Batching)
=====================================================================
Description:
    Core reasoning engine leveraging tensor operations for massive parallel processing.
    Integrates multiple cognitive motors (Praxeological, Nash, Chaotic) to evaluate
    operational genes against dynamic contexts.

Key Features:
    - Batch Processing: Optimized for high-throughput tensor operations.
    - VRAM Utilization: Designed to maximize GPU memory usage for Monte Carlo simulations.
    - Vectorized Motors: Implementation of Nash and Chaotic motors using 4D Tensors.

Reference: Favini, C. E. (2025). Operational Genomics.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import logging
import sys
import numpy as np

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

from digital_genome_core import DigitalGenome, OperationalGene, StateVector
from unl_core import UNLEngine
from meristic_core import EvolutionaryEngine

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("CognitiveCore")

# Hardware detection and configuration
DEVICE = 'cuda' if HAS_TORCH and torch.cuda.is_available() else 'cpu'
if DEVICE == 'cuda':
    ARCH_ENTROPY = torch.tensor(StateVector.ARCHETYPE_ENTROPY_MAX, device=DEVICE, dtype=torch.float32)
else:
    ARCH_ENTROPY = None

MAX_CONFIDENCE = 1.0 - sys.float_info.epsilon 

# Tuning Constants for Cognitive Dynamics
ENTROPY_LOGIC = 0.0015
MONTE_CARLO_N = 10000  # High iteration count for statistical significance on GPU
KAPPA_CATASTROPHE = 3.0
SIGMA_NOISE = 0.05

class CognitiveState:
    FLOW = "flow"
    PHOENIX = "phoenix"

@dataclass
class MotorEvaluation:
    """
    Standardized output for any Cognitive Motor evaluation.
    """
    motor_name: str
    score: float
    is_veto: bool
    veto_reason: Optional[str]
    confidence: float
    analysis: Dict[str, Any]
    
    @property
    def is_absolute_veto(self) -> bool:
        """Determines if the evaluation results in a hard stop."""
        return self.score == 0.0 or self.is_veto

# --- BATCH HELPER CLASSES ---
class BatchProcessor:
    """
    Utility class for transforming biological gene structures into computational tensors.
    """
    @staticmethod
    def genes_to_tensor(genes: List[OperationalGene], max_codons: int = 26) -> torch.Tensor:
        """
        Converts a list of OperationalGene objects into a 3D Tensor.
        
        Args:
            genes: List of genes to process.
            max_codons: Maximum sequence length for padding.
            
        Returns:
            torch.Tensor: Shape [Batch, Max_Codons, 3] on the active DEVICE.
        """
        batch_size = len(genes)
        # Pre-allocate tensor on CPU to minimize VRAM fragmentation during construction
        tensor = torch.zeros((batch_size, max_codons, 3), dtype=torch.float32)
        
        for i, gene in enumerate(genes):
            vectors = [c.state_vector.coordinates for c in gene.codons]
            # Truncate to max_codons or pad with zeros
            vec_len = min(len(vectors), max_codons)
            if vec_len > 0:
                tensor[i, :vec_len, :] = torch.tensor(vectors[:vec_len], dtype=torch.float32)
        
        return tensor.to(DEVICE)

class CognitiveMotor(ABC):
    """Abstract Base Class for all cognitive processing units."""
    def __init__(self, genome: DigitalGenome, unl: UNLEngine):
        self.genome = genome
        self.unl = unl
        
    @abstractmethod
    def evaluate(self, gene: OperationalGene, context: Dict, state: str) -> MotorEvaluation: pass

# 1. PRAXEOLOGICAL MOTOR (CPU Fast Path)
class PraxeologicalMotor(CognitiveMotor):
    @property
    def name(self) -> str: return "Praxeological"
    
    def evaluate(self, gene: OperationalGene, context: Dict, state: str) -> MotorEvaluation:
        """
        Evaluates based on historical memory and previous verdicts.
        Acts as a cache layer to bypass expensive physics simulations.
        """
        if gene.experience_count > 0:
            if "ADAPTED" in gene.last_verdict or "RECALLED" in gene.last_verdict or "NOMINAL" in gene.last_verdict:
                return MotorEvaluation(self.name, 1.0, False, None, 1.0, {"memory_recall": True, "skip_physics": True})
            if "VETO" in gene.last_verdict:
                 return MotorEvaluation(self.name, 0.0, True, "Recurrence (Fatal)", 1.0, {"memory_recall": True})
        
        return MotorEvaluation(self.name, 0.99, False, None, 0.9, {"memory_recall": False})

# 2. NASH MOTOR (Vectorized Game Theory)
class NashMotor(CognitiveMotor):
    @property
    def name(self) -> str: return "Nash"
    
    def evaluate_batch(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Computes Nash Equilibrium distances for a batch of genes.
        
        Input: [Batch, Codons, 3]
        Output: [Batch] scores (0.0 to 1.0)
        """
        # Calculate Euclidean distance to Entropy Archetype for all codons
        # ARCH_ENTROPY is broadcasted across the batch
        dists = torch.norm(input_tensor - ARCH_ENTROPY, dim=2) # Shape: [Batch, Codons]
        
        # Identify the codon closest to entropy (Min distance per gene)
        # Note: Zero-padding [0,0,0] has dist ~1.73 to Entropy [1,1,1], so padding is safe.
        min_dists, _ = torch.min(dists, dim=1) # Shape: [Batch]
        
        # Scoring Logic: Penalize if any codon is too close to Entropy (< 0.1)
        scores = torch.ones_like(min_dists)
        mask_conflict = min_dists < 0.1
        scores[mask_conflict] = 0.05 # Veto range
        
        return scores

    def evaluate(self, gene: OperationalGene, context: Dict, state: str) -> MotorEvaluation:
        # Fallback for single-gene processing compatibility
        return MotorEvaluation(self.name, 0.9, False, None, 0.9, {})

# 3. CHAOTIC MOTOR (Stochastic Physics Simulation - 4D Tensor)
class ChaoticMotor(CognitiveMotor):
    @property
    def name(self) -> str: return "Chaotic"
    
    def evaluate_batch(self, input_tensor: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Executes Monte Carlo simulations on the entire batch simultaneously.
        
        Input: [Batch, Codons, 3]
        Process: Expands tensor to 4D [Batch, MC_N, Codons, 3] to simulate noise.
        """
        batch_size, n_codons, _ = input_tensor.shape
        
        # 1. Dimensional Expansion
        # Replicate batch data into the Monte Carlo dimension
        data_expanded = input_tensor.unsqueeze(1).expand(-1, MONTE_CARLO_N, -1, -1)
        
        # 2. Noise Generation (Gaussian)
        noise = torch.randn_like(data_expanded, device=DEVICE) * SIGMA_NOISE
        futures = data_expanded + noise
        
        # 3. Entropy Distance Calculation
        dists = torch.norm(futures - ARCH_ENTROPY, dim=3)
        
        # 4. Weakest Link Identification (Min Dist per Simulation)
        min_dists, _ = torch.min(dists, dim=2)
        
        # 5. Statistical Aggregation
        # Success: Distance maintained >= 0.5
        successes = (min_dists >= 0.5).sum(dim=1).float()
        # Catastrophe: Distance collapsed < 0.2
        catastrophes = (min_dists < 0.2).sum(dim=1).float()
        
        p_cat = catastrophes / MONTE_CARLO_N
        psi_prob = successes / MONTE_CARLO_N
        
        # 6. Scoring
        scores = psi_prob * torch.pow((1.0 - p_cat), KAPPA_CATASTROPHE)
        
        # Hard Veto Logic
        veto_mask = (p_cat > 0.25) | (psi_prob < 0.05)
        scores[veto_mask] = 0.0
        
        return {"scores": scores, "p_cat": p_cat, "veto": veto_mask}

    def evaluate(self, gene: OperationalGene, context: Dict, state: str) -> MotorEvaluation:
        return MotorEvaluation(self.name, 0.9, False, None, 0.9, {})

# 4. MERISTIC MOTOR (Evolutionary Adaptation)
class MeristicMetaMotor(CognitiveMotor):
    def __init__(self, genome: DigitalGenome, unl: UNLEngine):
        super().__init__(genome, unl)
        self.evolution_engine = EvolutionaryEngine() 
        
    @property
    def name(self) -> str: return "Meristic"
    
    def evaluate(self, gene: OperationalGene, context: Dict, state: str) -> MotorEvaluation:
        return MotorEvaluation(self.name, 0.9, False, None, 0.5, {})
    
    def attempt_adaptation(self, failed_gene: OperationalGene, chaotic_motor: CognitiveMotor, context: Dict) -> Optional[OperationalGene]:
        return self.evolution_engine.evolve_solution(failed_gene, chaotic_motor, context)

# --- BATCH ORCHESTRATOR ---
class BatchCognitiveSystem:
    """
    High-Performance System orchestrating the gene processing pipeline.
    Manages the flow between CPU-based recall and GPU-based physics simulation.
    """
    def __init__(self, genome: DigitalGenome):
        self.genome = genome
        self.unl = UNLEngine()
        self.praxeological = PraxeologicalMotor(genome, self.unl)
        self.nash = NashMotor(genome, self.unl)
        self.chaotic = ChaoticMotor(genome, self.unl)
        self.meristic = MeristicMetaMotor(genome, self.unl)
        
    def process_batch(self, genes: List[OperationalGene]) -> List[Dict]:
        """
        Main entry point for batch processing.
        """
        # 1. PRAXEOLOGICAL FILTER (CPU) - Fast Recall
        # Separate genes that need simulation from those with established memory
        gpu_indices = []
        gpu_candidates = []
        
        final_decisions = [None] * len(genes)
        
        for i, gene in enumerate(genes):
            prax_eval = self.praxeological.evaluate(gene, {}, "flow")
            if prax_eval.analysis.get("skip_physics", False):
                # Memory Recall - Bypass GPU
                final_decisions[i] = {
                    "gene_uid": gene.uid, 
                    "verdict": "ACCEPTED (RECALLED)", 
                    "craft_performance": 1.0,
                    "evaluations": {"Praxeological": prax_eval}
                }
            else:
                # Requires Physics Simulation
                gpu_indices.append(i)
                gpu_candidates.append(gene)
        
        if not gpu_candidates:
            return [{"candidates": [d], "selected": True} for d in final_decisions]

        # 2. TENSORIZATION (CPU -> GPU)
        if DEVICE == 'cuda':
            input_tensor = BatchProcessor.genes_to_tensor(gpu_candidates)
            
            # 3. MASSIVE PARALLEL EVALUATION
            nash_scores = self.nash.evaluate_batch(input_tensor)
            chaotic_res = self.chaotic.evaluate_batch(input_tensor)
            
            # 4. MERISTIC INTERVENTION (CPU/GPU Hybrid Loop)
            # Retrieve results from GPU
            c_scores = chaotic_res["scores"].cpu().numpy()
            n_scores = nash_scores.cpu().numpy()
            veto_mask = chaotic_res["veto"].cpu().numpy()
            
            for k, real_idx in enumerate(gpu_indices):
                gene = gpu_candidates[k]
                
                # Check results
                is_veto = veto_mask[k]
                cp = c_scores[k] * n_scores[k] # Calculate Craft Performance
                
                verdict = "ACCEPTED (NOMINAL)"
                if is_veto:
                    verdict = "VETOED"
                    
                    # TRIGGER MERISTIC REPAIR
                    # Attempt evolutionary adaptation on the failed gene
                    mutant = self.meristic.attempt_adaptation(gene, self.chaotic, {})
                    if mutant:
                        verdict = "ACCEPTED (ADAPTED)"
                        cp = 0.8 # Estimated post-adaptation score
                
                final_decisions[real_idx] = {
                    "gene_uid": gene.uid,
                    "verdict": verdict,
                    "craft_performance": float(cp),
                    "evaluations": {} # Lightweight log
                }
        
        # 5. Format Output
        return [{"candidates": [d], "selected": True} for d in final_decisions]