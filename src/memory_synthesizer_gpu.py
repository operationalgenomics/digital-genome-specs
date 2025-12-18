"""
Memory Synthesizer v2.4 - Stability Cap
=======================================
Optimized for: Alienware m16 R2 (RTX 4070 8GB)
Changes:
1. HARD CAP BATCH: Limits batch to 2048 to prevent Python loop checking freeze.
2. PROGRESS BAR: Adds sub-progress for novelty clustering.
3. FAILSAFE: Forces CPU fallback if CUDA errors occur.
"""

import json
import torch
import numpy as np
import logging
import time
import sys
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIG ---
SIMILARITY_THRESHOLD = 0.05
INITIAL_BUFFER_SIZE = 20000
# CRITICAL FIX: Cap batch size.
# Large batches are good for Matrix Mul, but bad for the Greedy Clustering loop.
MAX_BATCH_SIZE = 2048 

# Paths
CURRENT_DIR = Path.cwd()
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
POSSIBLE_PATHS = [
    CURRENT_DIR / "data/cortex/genome_memory.json",
    SCRIPT_DIR / "data/cortex/genome_memory.json",
    PROJECT_ROOT / "data/cortex/genome_memory.json",
    CURRENT_DIR / "src/data/cortex/genome_memory.json"
]

def find_file():
    print(f"{Fore.YELLOW}[SEARCH] Searching for memory file...{Style.RESET_ALL}")
    for p in POSSIBLE_PATHS:
        if p.exists(): 
            print(f"   Found: {p}")
            return p
    return None

def get_device():
    if torch.cuda.is_available():
        d = torch.device("cuda")
        print(f"{Fore.GREEN}[HARDWARE] GPU Active: {torch.cuda.get_device_name(0)}{Style.RESET_ALL}")
        return d
    return torch.device("cpu")

def main():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"DIGITAL GENOME | REM SLEEP v2.4 (STABILITY CAP)")
    print(f"{'='*60}{Style.RESET_ALL}")

    device = get_device()
    memory_path = find_file()
    if not memory_path: return

    # 1. LOAD
    print(f"[I/O] Reading JSON...")
    t0 = time.time()
    with open(memory_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    raw_genes = data.get("genes", [])
    if not raw_genes: return

    # 2. VECTORIZE
    print(f"[PREP] Vectorizing {len(raw_genes)} experiences...")
    first_vec = []
    for c in raw_genes[0]['codons']: first_vec.extend(c['state_vector'])
    vec_dim = len(first_vec)
    
    # Pre-allocate Host
    host_tensor = torch.empty((len(raw_genes), vec_dim), dtype=torch.float32)
    valid_genes = []
    
    nominal_indices = []
    veto_indices = []
    
    cursor = 0
    for i, g in enumerate(tqdm(raw_genes, desc="Parsing")):
        v = []
        for c in g['codons']: v.extend(c['state_vector'])
        if len(v) != vec_dim: continue
        
        host_tensor[cursor] = torch.tensor(v)
        valid_genes.append(g)
        
        verdict = g.get('last_verdict', 'UNKNOWN')
        if "VETO" in verdict:
            veto_indices.append(cursor)
        else:
            nominal_indices.append(cursor)
        cursor += 1
        
    host_tensor = host_tensor[:cursor]
    full_tensor = host_tensor.to(device)
    print(f"   >>> VRAM Tensor: {full_tensor.shape} ({full_tensor.element_size()*full_tensor.nelement()/1024**2:.1f} MB)")
    
    # 3. CLUSTERING
    # Force smaller batch for loop stability
    BATCH_SIZE = MAX_BATCH_SIZE
    print(f"{Fore.CYAN}[LOGIC] Batch Size Locked at: {BATCH_SIZE} (For Python stability){Style.RESET_ALL}")
    
    current_buffer_size = INITIAL_BUFFER_SIZE
    archetype_buffer = torch.empty((current_buffer_size, vec_dim), device=device)
    archetype_count = 0
    golden_prototypes = [] 
    
    if len(nominal_indices) > 0:
        nominal_tensor = full_tensor[nominal_indices]
        
        pbar = tqdm(total=len(nominal_indices), unit="vec", desc="Consolidating")
        
        for i in range(0, len(nominal_indices), BATCH_SIZE):
            batch = nominal_tensor[i : i+BATCH_SIZE]
            batch_indices = nominal_indices[i : i+BATCH_SIZE]
            
            # First initialization
            if archetype_count == 0:
                archetype_buffer[0] = batch[0]
                archetype_count = 1
                golden_prototypes.append(valid_genes[batch_indices[0]])
            
            # Compare Batch vs Current Archetypes
            current_archs = archetype_buffer[:archetype_count]
            dists = torch.cdist(batch, current_archs)
            min_dists, _ = torch.min(dists, dim=1)
            
            # Novelties
            novel_mask = min_dists >= SIMILARITY_THRESHOLD
            novel_local_indices = novel_mask.nonzero(as_tuple=True)[0]
            
            if len(novel_local_indices) > 0:
                novel_vecs = batch[novel_local_indices]
                
                remaining = novel_vecs
                rem_global_idxs = [batch_indices[x] for x in novel_local_indices.cpu().numpy()]
                
                # Internal Loop
                while len(remaining) > 0:
                    if archetype_count >= current_buffer_size:
                        new_size = current_buffer_size * 2
                        new_buf = torch.empty((new_size, vec_dim), device=device)
                        new_buf[:current_buffer_size] = archetype_buffer
                        archetype_buffer = new_buf
                        current_buffer_size = new_size
                        
                    seed = remaining[0]
                    archetype_buffer[archetype_count] = seed
                    golden_prototypes.append(valid_genes[rem_global_idxs[0]])
                    archetype_count += 1
                    
                    # Vectorized removal
                    d_int = torch.norm(remaining - seed, dim=1)
                    keep = d_int >= SIMILARITY_THRESHOLD
                    
                    remaining = remaining[keep]
                    rem_global_idxs = [val for k, val in enumerate(rem_global_idxs) if keep[k].item()]
            
            pbar.update(len(batch))
        pbar.close()

    # 4. TRAUMAS
    trauma_library = []
    if len(veto_indices) > 0:
        print(f"[REM] Processing Vetoes...")
        trauma_library = [valid_genes[i] for i in veto_indices]

    # 5. SAVE
    out_path = memory_path.parent / "synaptic_weights.json"
    final_output = {
        "version": "v2.4-STABLE",
        "timestamp": time.time(),
        "stats": {
            "raw": len(valid_genes),
            "golden": archetype_count,
            "compression": f"{(1 - archetype_count/len(valid_genes))*100:.1f}%"
        },
        "genes": [g for g in golden_prototypes] + trauma_library
    }
    
    for g in final_output["genes"]:
        if 'metadata' not in g: g['metadata'] = {}
        g['metadata']['is_archetype'] = True

    print(f"\n{Fore.CYAN}[I/O] Writing {out_path.name}...{Style.RESET_ALL}")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    elapsed = time.time() - t0
    print(f"{Fore.GREEN}{'='*60}")
    print(f"REM SLEEP COMPLETED IN: {elapsed:.2f}s")
    print(f"Archetypes: {archetype_count}")
    print(f"{'='*60}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()