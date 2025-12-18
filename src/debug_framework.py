"""
debug_framework.py
==================
DIGITAL GENOME MASTER DEBUGGER vRELEASE-5.2 (INTEGRATION FIX)
==================
Changes:
- TRANSLATION: Renamed 'verificar_hardware_e_configurar' to English.
- INTEGRATION: Now automatically triggers 'mission_reporter' after processing.
- DATA FIX: Added 'was_adapted' flag to JSON output for correct reporting.
"""

import sys
import os
import json
import time
import logging
import gzip
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init
init(autoreset=True)

sys.path.append(os.path.dirname(__file__))

from digital_genome_core import DigitalGenome, OperationalGene, PraxeologicalCodon, StateVector
from cognitive_core import BatchCognitiveSystem 
import mission_reporter 
from graph_core import FederatedGraphEngine 

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

BATCH_SIZE = 1000 

BATCH_CONFIG = {
    "datasets": [
        "cmapss/nasa-turbofan-engine-rul-prediction-main/data/train_FD001.txt",
        "cmapss/nasa-turbofan-engine-rul-prediction-main/data/train_FD002.txt",
        "bpi/BPI Challenge 2017/BPI Challenge 2017.xes",
        "cmapss/nasa-turbofan-engine-rul-prediction-main/data/train_FD003.txt",
        "cmapss/nasa-turbofan-engine-rul-prediction-main/data/train_FD004.txt"
    ],
    "sample_limit": None, 
    "anomaly_threshold": 2.0,
    "save_interval": 10000 
}

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

logging.basicConfig(filename='system.log', level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger("MASTER_DEBUG")

PROJECT_ROOT = Path(__file__).resolve().parent.parent 
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)
REAL_DATA_DIR = PROJECT_ROOT / "data/raw"

def print_banner(title):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Style.BRIGHT}{title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def verify_hardware_and_configure():
    """
    Checks for GPU availability and configures processing parameters accordingly.
    """
    print(f"{Style.BRIGHT}[HARDWARE] Analyzing Processing Environment...{Style.RESET_ALL}")
    if HAS_TORCH and torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        torch.backends.cudnn.benchmark = True 
        _ = torch.ones(1).cuda()
        print(f"{Fore.GREEN}   >>> GPU DETECTED: {gpu_name} <<<{Style.RESET_ALL}")
        pop_size = 50000 
        print(f"   >>> MERISTIC ENGINE: HYPER-THREADING MODE (Population: {pop_size:,})")
        return {"population_size": pop_size, "device": "gpu"}
    else:
        print(f"{Fore.YELLOW}   >>> GPU NOT FOUND. <<<{Style.RESET_ALL}")
        return {"population_size": 50, "device": "cpu"}

class ValidationReporter:
    def __init__(self, session_name: str):
        self.session_id = f"{session_name}_{int(time.time())}"
        self.results = []
        self.stats = {"accepted": 0, "adapted": 0, "recalled": 0, "warning": 0, "veto": 0, "total": 0}

    def log_batch_decisions(self, decisions: List[Dict]):
        for d in decisions:
            cand = d['candidates'][0]
            verdict = cand['verdict']
            
            is_adapted = "ADAPTED" in verdict
            is_recalled = "RECALLED" in verdict
            is_veto = "VETO" in verdict
            
            self.stats["total"] += 1
            if is_veto: self.stats["veto"] += 1
            elif is_recalled: self.stats["recalled"] += 1
            elif is_adapted: self.stats["adapted"] += 1
            else: self.stats["accepted"] += 1

            # FIX: Added 'was_adapted' so mission_reporter can generate the "Apollo 13" table
            self.results.append({
                "gene_uid": cand['gene_uid'],
                "verdict": verdict,
                "was_adapted": is_adapted, 
                "craft_performance": cand.get('craft_performance', 0.0)
            })

    def save(self) -> Path:
        filename = RESULTS_DIR / f"VOYAGER_run_{self.session_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"session": self.session_id, "stats": self.stats, "data": self.results}, f, indent=2)
        return filename

# --- LOADERS ---
def parse_xes_to_dataframe(filepath: Path, limit: Optional[int]) -> pd.DataFrame:
    print(f"   [PARSER] Reading Semantic Context from {filepath.name}...")
    data = []
    open_func = gzip.open if filepath.suffix == '.gz' else open
    try:
        context = ET.iterparse(open_func(filepath, 'rb'), events=('end',))
        count = 0
        for event, elem in context:
            if elem.tag.endswith('event'):
                row = {}
                context_str = []
                for child in elem:
                    key = child.get('key')
                    val = child.get('value')
                    if key and val:
                        try:
                            num_val = float(val)
                            row[key] = num_val
                        except: context_str.append(val)
                if row:
                    row['_context_text'] = " ".join(context_str)
                    data.append(row)
                    count += 1
                elem.clear()
                if limit and count >= limit: break
        return pd.DataFrame(data)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] XML Parsing failed: {e}{Style.RESET_ALL}")
        return pd.DataFrame()

def load_universal_dataset(rel_path: str) -> List[OperationalGene]:
    data_path = REAL_DATA_DIR / rel_path
    if not HAS_PANDAS or not data_path.exists(): return []
    try:
        df = pd.DataFrame()
        if '.xes' in data_path.name:
            df = parse_xes_to_dataframe(data_path, BATCH_CONFIG["sample_limit"])
        else:
            df = pd.read_csv(data_path, sep=r"\s+", header=None, engine='python', nrows=BATCH_CONFIG["sample_limit"])
            df = df.dropna(axis=1, how='all')
            df.columns = [f"signal_{i}" for i in range(df.shape[1])]
            df['_context_text'] = "Turbofan Engine Sensor Run"
        if df.empty: return []

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats_mean = df[numeric_cols].mean()
        genes = []
        print(f"   [MATH] Transforming {len(df)} vectors into Genes...")
        
        for idx, row in tqdm(df.iterrows(), total=len(df), unit="gene", desc="Synthesis"):
            gene_name = f"Stream_{data_path.stem.split('.')[0]}_Vec{idx}"
            context_text = row.get('_context_text', 'Unknown Data')
            g = OperationalGene.create(name=gene_name, purpose=f"Process: {context_text}", executor="Universal", action="process", target=f"row_{idx}")
            g.metadata = {"source_file": data_path.name, "anomalies": []}
            
            for col in numeric_cols:
                val = row[col]
                mean = stats_mean[col]
                std = df[col].std()
                z = abs((val - mean) / (std + 1e-9))
                
                vec = StateVector(StateVector.ARCHETYPE_NOMINAL)
                if z > 2.0: vec = StateVector(StateVector.ARCHETYPE_ENTROPY_MAX)
                elif z > 1.4: vec = StateVector(StateVector.ARCHETYPE_DEVIATION)
                
                g.add_codon(PraxeologicalCodon(str(col), "emit", vec, {"value": float(val)}))
            genes.append(g)
        return genes
    except Exception: return []

def main():
    print_banner(f"DIGITAL GENOME | VOYAGER TENSOR EDITION v5.2 (INTEGRATED)")
    # Function name refactored to English
    hw = verify_hardware_and_configure()
    
    genome = DigitalGenome(name="Voyager_Prime", memory_path="data/cortex/genome_memory.json")
    
    system = BatchCognitiveSystem(genome)
    system.meristic.evolution_engine.population_size = hw["population_size"]
    system.meristic.evolution_engine.device = 'cuda' if hw['device'] == 'gpu' else 'cpu'
    
    grand_stats = {"accepted": 0, "adapted": 0, "recalled": 0, "veto": 0, "total": 0}
    
    for d_file in BATCH_CONFIG["datasets"]:
        print_banner(f"STREAM: {d_file}")
        genes = load_universal_dataset(d_file)
        if not genes: continue
        
        reporter = ValidationReporter(f"univ_{Path(d_file).stem}")
        
        with tqdm(total=len(genes), unit="vec", desc="GPU Processing") as pbar:
            for i in range(0, len(genes), BATCH_SIZE):
                batch = genes[i : i + BATCH_SIZE]
                
                # 1. PROCESS (GPU)
                decisions = system.process_batch(batch)
                
                # 2. COMMIT TO MEMORY
                for gene_idx, decision in enumerate(decisions):
                    gene = batch[gene_idx]
                    cand_data = decision['candidates'][0]
                    
                    # Update gene with result
                    gene.last_verdict = cand_data['verdict']
                    
                    # Persist to Cortex Object
                    genome.insert_gene_as_neuron(gene, plasticity=0.1)

                # 3. LOG & UPDATE
                reporter.log_batch_decisions(decisions)
                pbar.update(len(batch))
                s = reporter.stats
                pbar.set_postfix(
                    NOM=f"{s['accepted']}",
                    ADP=f"{s['adapted']}",
                    REC=f"{s['recalled']}",
                    VTO=f"{s['veto']}"
                )
                
                # Disk Save Intermediate
                if i > 0 and i % BATCH_CONFIG["save_interval"] == 0:
                    reporter.save()
                    genome.save_memory()

        # 4. FINAL SAVE AND REPORT GENERATION
        last_json_path = reporter.save()
        
        # Integration Fix: Automatically trigger the Markdown report generation
        print(f"\n{Fore.CYAN}[REPORT] Triggering Mission Reporter for {last_json_path.name}...{Style.RESET_ALL}")
        try:
            mission_reporter.generate_report_for_file(last_json_path)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Report generation failed: {e}{Style.RESET_ALL}")

        for k in grand_stats: 
            if k in reporter.stats: grand_stats[k] += reporter.stats[k]

    print_banner("MEMORY CONSOLIDATION")
    genome.save_memory()
    print(f"{Fore.GREEN}>>> Genome Memory Updated ({len(genome.genes)} genes).{Style.RESET_ALL}")

    print_banner("FEDERATED SPACE PROTOCOL")
    try:
        fed = FederatedGraphEngine()
        fed.load_memory_into_graph("data/cortex/genome_memory.json")
        fed.secure_federation_protocol("UNIT_FD001", "UNIT_FD003")
        fed.secure_federation_protocol("UNIT_FD002", "UNIT_FD004")
        fed.secure_federation_protocol("DEPT_FINANCE", "UNIT_FD001")
    except Exception as e: print(e)

    print(f"\n{Fore.GREEN}MISSION COMPLETE.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()