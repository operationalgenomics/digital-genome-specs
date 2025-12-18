"""
cmapss_loader.py
================
Loader for NASA C-MAPSS Turbofan Degradation Dataset.
"""

import pandas as pd
from typing import Generator, List, Dict, Any
from pathlib import Path
import logging

# FIX: Absolute imports to prevent "attempted relative import" errors
from validation.datasets.base_loader import BaseLoader, LoaderConfig, PraxeologicalTriple
from digital_genome_core import SafetyLevel, OperationalGene, PraxeologicalCodon

logger = logging.getLogger("validation.datasets.cmapss")

class CMAPSSConfig(LoaderConfig):
    """Configuration specific to C-MAPSS data structure."""
    columns: List[str] = [
        'unit_number', 'time_in_cycles', 'op_setting_1', 'op_setting_2', 'op_setting_3',
        's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 
        's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21'
    ]

class CMAPSSLoader(BaseLoader):
    
    @property
    def dataset_name(self) -> str:
        return "NASA C-MAPSS Turbofan"

    @property
    def dataset_description(self) -> str:
        return "Run-to-failure simulation data of turbofan engines."

    @property
    def dataset_url(self) -> str:
        # Using a reliable direct link for the zip file
        return "https://data.nasa.gov/api/views/xaut-bemq/rows.csv?accessType=DOWNLOAD"

    def load(self) -> pd.DataFrame:
        if not self.config.data_path.exists():
            raise FileNotFoundError(f"C-MAPSS data not found at: {self.config.data_path}")
        
        # C-MAPSS text files are space-separated
        df = pd.read_csv(
            self.config.data_path, 
            sep=r"\s+", 
            header=None, 
            names=self.config.columns
        )
        return df

    def parse(self, raw_data: pd.DataFrame) -> List[Dict[str, Any]]:
        return raw_data.to_dict('records')

    def extract_triple(self, record: Dict[str, Any]) -> PraxeologicalTriple:
        unit_id = f"Turbofan_Unit_{int(record['unit_number'])}"
        
        # Simple threshold logic for state (s11 is static pressure)
        # In production, this would be a trained anomaly detector
        state = "nominal"
        if record.get('s11', 0) > 47.5: 
            state = "degraded"
        
        return PraxeologicalTriple(
            entity=unit_id,
            action="operate_cycle",
            state=state,
            source_record=record,
            confidence=1.0
        )

    def extract_context(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "cycle": record['time_in_cycles'],
            "op_settings": [record['op_setting_1'], record['op_setting_2']],
            # Extract key sensors for context vector
            "T24": record.get('s2'),
            "T30": record.get('s3'),
            "Nf": record.get('s9')
        }

    def group_into_genes(self, codons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        genes_map = {}
        
        for codon in codons:
            # Safely access unit_number from parameters
            unit_num = codon.get('parameters', {}).get('unit_number')
            if unit_num is None: continue
            
            if unit_num not in genes_map:
                genes_map[unit_num] = []
            genes_map[unit_num].append(codon)
            
        genes = []
        for unit_num, unit_codons in genes_map.items():
            unit_codons.sort(key=lambda x: x['context']['cycle'])
            max_cycles = unit_codons[-1]['context']['cycle']
            
            gene = {
                "uid": f"cmapss:gene:unit_{unit_num}",
                "name": f"Turbofan_Lifecycle_Unit_{unit_num}",
                "purpose": "Generate thrust",
                "version": "1.0.0",
                "status": "active",
                "codons": unit_codons,
                "activation_conditions": ["mission_start"],
                "postconditions": [f"cycles={max_cycles}"],
                "metadata": {"domain": "aerospace", "total_life": max_cycles}
            }
            genes.append(gene)
            
        return genes