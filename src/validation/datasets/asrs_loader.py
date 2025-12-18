"""
asrs_loader.py
==============
Loader for NASA Aviation Safety Reporting System (ASRS).

This module ingests narrative text reports from pilots and controllers.
It validates the Natural Language understanding of the Digital Genome,
converting unstructured narratives into structured Genes.

Relevance:
- Validates the Meristic Motor's ability to extract ontology from text.
- Validates the Praxeological Motor's ability to see intent in chaos.
"""

import pandas as pd
import hashlib
from typing import Generator, List, Dict, Any
from pathlib import Path
from .base_loader import BaseLoader, LoaderConfig, PraxeologicalTriple

class ASRSLoader(BaseLoader):
    
    @property
    def dataset_name(self) -> str:
        return "NASA ASRS (Aviation Safety Reporting System)"

    @property
    def dataset_description(self) -> str:
        return "Voluntary safety reports from aviation professionals."

    @property
    def dataset_url(self) -> str:
        return "https://asrs.arc.nasa.gov/search/database.html"

    def load(self) -> pd.DataFrame:
        # Assuming CSV export from ASRS DB
        if not self.config.data_path.exists():
            raise FileNotFoundError(f"ASRS data not found at: {self.config.data_path}")
        return pd.read_csv(self.config.data_path)

    def parse(self, raw_data: pd.DataFrame) -> List[Dict[str, Any]]:
        # Normalize columns (ASRS columns are usually uppercase)
        raw_data.columns = [c.lower().replace(" ", "_") for c in raw_data.columns]
        return raw_data.to_dict('records')

    def extract_triple(self, record: Dict[str, Any]) -> PraxeologicalTriple:
        """
        Extracts intent from narrative.
        Note: In a full production system, this would use an LLM/NLP model.
        For this loader, we use heuristic mapping based on event types.
        """
        # Entity usually implies the reporter (Pilot/Controller)
        entity = "Flight_Crew" 
        
        # Action derived from the anomaly type
        action_raw = str(record.get('anomaly', 'unknown_event'))
        action = action_raw.split(';')[0].strip().replace(" ", "_").lower()
        
        # State derived from outcome
        state = "incident_reported"
        if "Critical" in str(record.get('assessment', '')):
            state = "safety_compromised"
            
        return PraxeologicalTriple(
            entity=entity,
            action=action,
            state=state,
            source_record=record,
            confidence=0.8 # Text extraction is inherently fuzzy
        )

    def extract_context(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "narrative": record.get('narrative', '')[:500], # First 500 chars
            "weather": record.get('environment', 'unknown'),
            "flight_phase": record.get('flight_phase', 'unknown'),
            "location": record.get('location', 'unknown')
        }

    def group_into_genes(self, codons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        For ASRS, each Report (ACN number) is usually a single atomic event 
        sequence, so 1 Report = 1 Gene.
        """
        genes = []
        for codon in codons:
            acn = codon['parameters'].get('acn', 'unknown')
            
            gene = {
                "uid": f"asrs:gene:{acn}",
                "name": f"Safety_Event_{acn}",
                "purpose": "Execute flight operation safely",
                "version": "1.0.0",
                "status": "archived", # Historical data
                "codons": [codon], # Usually single-codon genes for text reports
                "activation_conditions": [f"phase={codon['context']['flight_phase']}"],
                "postconditions": ["reported"],
                "metadata": {
                    "domain": "aviation_safety",
                    "source": "ASRS"
                }
            }
            genes.append(gene)
        return genes