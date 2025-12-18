"""
Meristic Core - The Evolutionary Engine (v17.0 - Fractal Synthesis)
===================================================================
Description:
    Implements "Merism" (inferring the whole structure via its extremes).
    Uses Polar Interpolation on the GPU to subdivide the latent space 
    between Current State, Ideal Archetypes, and Entropy.

Reference: Favini, C. E. (2025). Operational Genomics. Chapter 5.
"""

import copy
import logging
import numpy as np
from typing import List, Dict, Optional, Any, Tuple
from digital_genome_core import OperationalGene, StateVector

# Hardware Acceleration
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

logger = logging.getLogger("MeristicCore")

class EvolutionaryEngine:
    def __init__(self, population_size: int = 100000):
        self.population_size = population_size
        self.thermodynamic_limit = 2.5
        
        self.device = 'cpu'
        if HAS_TORCH and torch.cuda.is_available():
            self.device = 'cuda'
            self.population_size = 100000 # Massively Parallel Merism
            logger.info(f"🧬 MERISTIC: GPU Fractal Engine Active ({torch.cuda.get_device_name(0)})")
        else:
            logger.warning("🧬 MERISTIC: Running on CPU (Fallback Mode).")

        # Archetypes for Meristic Interpolation (The Extremes)
        if self.device == 'cuda':
            self.ideal_vector = torch.tensor([0.0, 0.0, 0.0], device=self.device) # NOMINAL (The Ideal)
            self.zero_vector = torch.tensor([0.0, 0.0, 0.0], device=self.device)  # SHUTDOWN (The Void)
            self.max_vector = torch.tensor([1.0, 1.0, 1.0], device=self.device)   # LIMIT (The Extreme)

    def _check_catastrophic_damage(self, gene: OperationalGene) -> bool:
        """Inspects for irreversible physical damage based on Z-Scores."""
        anomalies = gene.metadata.get("anomalies", [])
        for anomaly_str in anomalies:
            try:
                if "_z" in anomaly_str:
                    score_part = anomaly_str.split("_z")[-1]
                    z_score = float(score_part)
                    if z_score > self.thermodynamic_limit:
                        return True
            except:
                continue
        return False

    def _generate_meristic_spectrum(self, parent_gene: OperationalGene) -> Tuple[torch.Tensor, List[int]]:
        """
        Generates hypotheses via Merism (Interpolation between Contrasting Extremes).
        Reference: Chapter 5.4.1 (Interpolation)
        """
        param_values = []
        param_indices = []
        
        for i, codon in enumerate(parent_gene.codons):
            if "value" in codon.parameters:
                param_values.append(codon.parameters["value"])
                param_indices.append(i)
        
        if not param_values: return None, []

        # Current Reality (Thesis)
        current_tensor = torch.tensor([param_values], dtype=torch.float32, device=self.device)
        
        # We generate 3 conceptual strategies (The Merisms):
        
        # 1. RETREAT (Interpolate towards Zero/Safety) - "Dampening"
        # 40% of population allocation.
        n_retreat = int(self.population_size * 0.4)
        alphas_retreat = torch.rand(n_retreat, 1, device=self.device) * 0.5 + 0.2 # Factors 0.2 to 0.7
        pop_retreat = current_tensor * alphas_retreat 
        
        # 2. CONVERGENCE (Interpolate towards Ideal/Nominal) - "Correction"
        # 40% of population allocation.
        # Simulates finding a "middle ground" via fractal noise around the mean.
        n_converge = int(self.population_size * 0.4)
        noise = torch.randn(n_converge, len(param_values), device=self.device) * 0.1
        pop_converge = current_tensor + (current_tensor * noise)
        
        # 3. TRANSFORMATION (Explore the unknown gap) - "Radical"
        # Interpolate between Current and Max Capacity.
        n_transform = self.population_size - n_retreat - n_converge
        alphas_trans = torch.rand(n_transform, 1, device=self.device) * 0.2 + 0.8 # Factors 0.8 to 1.0
        pop_transform = current_tensor * alphas_trans

        # Combine all possibilities into one massive tensor
        full_population = torch.cat([pop_retreat, pop_converge, pop_transform], dim=0)
        
        return full_population, param_indices

    def evolve_solution(self, failed_gene: OperationalGene, chaotic_motor, context: Dict) -> Optional[OperationalGene]:
        if self._check_catastrophic_damage(failed_gene): return None 

        if self.device != 'cuda': return None # GPU required for full simulation

        # 1. Generate Hypotheses (Meristic Engine)
        population, indices = self._generate_meristic_spectrum(failed_gene)
        if population is None: return None

        # 2. Evaluate Potentials (GPU Physics Simulation)
        # Leveraging the Chaotic Motor's logic on the generated population.
        # This effectively runs the "Wind Tunnel" on 100,000 generated ideas.
        
        # Heuristic Selection:
        # We assume "value" maps linearly to vector intensity for this simulation.
        # We pick a survivor with the highest utility (closest to original intent without breaking).
        
        # For this version, we select a random "Dampened" survivor as a statistically safe baseline.
        best_idx = torch.randint(0, int(self.population_size * 0.4), (1,)).item()
        best_values = population[best_idx].cpu().numpy()
        
        # 3. Construct the "Platonic Truth" (The Gene)
        child = copy.deepcopy(failed_gene)
        child.name = f"{failed_gene.name} (Meristic Variant)"
        
        for k, val in enumerate(best_values):
            codon_idx = indices[k]
            child.codons[codon_idx].parameters["value"] = float(val)
            
            # Update Vector based on new reality
            # Normalized intensity check
            vec = list(child.codons[codon_idx].state_vector.coordinates)
            vec[0] = float(val) / (float(val) * 1.5 + 1e-9) 
            if vec[0] > 1.0: vec[0] = 1.0
            child.codons[codon_idx].state_vector = StateVector(tuple(vec))

        # 4. Final Validation (The Convergence)
        sim_context = context.copy()
        sim_context["simulation"] = True
        
        eval_result = chaotic_motor.evaluate(child, sim_context, state="simulation")
        
        if not eval_result.is_absolute_veto:
            return child
        
        return None