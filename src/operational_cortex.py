"""
DIGITAL GENOME | VOLUME II | OPERATIONAL CORTEX
===============================================
Purpose: High-Frequency Inference Engine (Day 2 Operations)
Input: Real-time sensor stream (Simulated)
Memory: Loads 'synaptic_weights.json' (The Archetypes)
Hardware: Utilizes GPU for instant similarity search (Nash Distance).
"""

import json
import torch
import time
import numpy as np
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# CONFIGURATION
MEMORY_PATH = Path("data/cortex/synaptic_weights.json")
SIMILARITY_THRESHOLD = 0.05 
MOCK_STREAM_SIZE = 1000     # Simulate 1000 new sensor readings

def load_cortex():
    print(f"{Fore.CYAN}[BOOT] Loading Operational Cortex...{Style.RESET_ALL}")
    
    if not MEMORY_PATH.exists():
        # Fallback search
        alt_path = Path("src/data/cortex/synaptic_weights.json")
        if alt_path.exists():
            path = alt_path
        else:
            print(f"{Fore.RED}[FATAL] 'synaptic_weights.json' not found. Execute REM Sleep cycle first.{Style.RESET_ALL}")
            return None, None
    else:
        path = MEMORY_PATH

    t0 = time.time()
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    genes = data['genes']
    # Vectorize Archetypes
    vectors = []
    metadata = []
    
    # Peek dimensions
    first_vec = []
    for c in genes[0]['codons']: first_vec.extend(c['state_vector'])
    vec_dim = len(first_vec)

    for g in genes:
        v = []
        for c in g['codons']: v.extend(c['state_vector'])
        if len(v) == vec_dim:
            vectors.append(v)
            # Store lightweight metadata for fast retrieval
            metadata.append({
                "uid": g['uid'],
                "verdict": g['last_verdict'],
                "count": g['metadata'].get('experience_count', 1)
            })
    
    # Move to GPU if available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        tensor = torch.tensor(vectors, dtype=torch.float32, device=device)
        print(f"{Fore.GREEN}[HARDWARE] Cortex loaded in VRAM (GPU): {len(vectors)} Archetypes.{Style.RESET_ALL}")
    else:
        device = torch.device("cpu")
        tensor = torch.tensor(vectors, dtype=torch.float32)
        print(f"{Fore.YELLOW}[HARDWARE] Cortex loaded on CPU (Compatibility Mode).{Style.RESET_ALL}")

    print(f"   >>> Boot Time: {time.time() - t0:.4f}s")
    return tensor, metadata

def simulate_stream(archetype_tensor, metadata):
    if archetype_tensor is None: return

    device = archetype_tensor.device
    vec_dim = archetype_tensor.shape[1]
    
    print(f"\n{Fore.CYAN}[STREAM] Simulating influx of {MOCK_STREAM_SIZE} turbine signals...{Style.RESET_ALL}")
    
    # Create random mock data (some close to archetypes, some noise)
    random_indices = torch.randint(0, len(archetype_tensor), (MOCK_STREAM_SIZE,))
    base_signals = archetype_tensor[random_indices]
    noise = torch.randn_like(base_signals) * 0.03 # Add small noise to simulate realism
    
    incoming_stream = base_signals + noise
    
    # --- THE INFERENCE LOOP (High Frequency) ---
    print(f"{Fore.YELLOW}[OPERATIONAL] Starting Real-Time Inference...{Style.RESET_ALL}")
    start_time = time.time()
    
    # 1. Calculate Distances against Wisdom (Broadcasting)
    # Stream vs Archetypes Matrix Calculation
    dists = torch.cdist(incoming_stream, archetype_tensor)
    
    # 2. Find nearest archetype
    min_dists, best_indices = torch.min(dists, dim=1)
    
    # 3. Decision Logic (GPU)
    matches_mask = min_dists < SIMILARITY_THRESHOLD
    
    # Sync to CPU for reporting
    total_time = time.time() - start_time
    matches_count = matches_mask.sum().item()
    anomalies_count = MOCK_STREAM_SIZE - matches_count
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"OPERATIONAL REPORT (DAY 2)")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"Processed Signals:       {MOCK_STREAM_SIZE}")
    print(f"Total Time:              {total_time:.4f} seconds")
    print(f"Throughput:              {MOCK_STREAM_SIZE / total_time:.0f} verdicts/second")
    print(f"{'-'*60}")
    print(f"✅ Recognized (Recalled):   {matches_count} ({(matches_count/MOCK_STREAM_SIZE)*100:.1f}%)")
    print(f"⚠️ Anomalies (New):        {anomalies_count}")
    
    # Example Decision
    idx = 0
    if matches_mask[idx]:
        arch_idx = best_indices[idx].item()
        meta = metadata[arch_idx]
        print(f"\nInstant Decision Example (Signal #0):")
        print(f"   Input: ... (Sensor Vector)")
        print(f"   Match: {meta['uid']}")
        print(f"   Action: {meta['verdict']} (Based on {meta['count']} past experiences)")
    
if __name__ == "__main__":
    memory, meta = load_cortex()
    simulate_stream(memory, meta)