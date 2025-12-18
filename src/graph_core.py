"""
Graph Core - The Federated Connectome (v3.0 - Total Knowledge Share)
====================================================================
Changes:
- REMOVED ELITISM: Now propagates ALL knowledge, including failures (Vetoes).
  "Learning what NOT to do is as important as learning what to do."
- ATOMIC UTILITY: Acceptance threshold is strictly > 0. No margin ignored.
- UPDATED TOPOLOGY: Includes FD002/FD004 in the simulation map.

REFERENCE: Favini, C. E. (2025). Operational Genomics. Chapter 7.
"""

import json
import logging
import networkx as nx
from pathlib import Path
from typing import List, Dict, Set, Tuple

logger = logging.getLogger("GraphCore")

class FederatedGraphEngine:
    def __init__(self):
        self.G = nx.DiGraph()
        self.tenants: Set[str] = set()

    def _derive_tenant_from_source(self, source_file: str) -> str:
        if not source_file: return "UNKNOWN_UNIT"
        clean_name = Path(source_file).stem 
        if "train_" in clean_name:
            return f"UNIT_{clean_name.replace('train_', '')}" 
        elif "BPI" in clean_name:
            return "DEPT_FINANCE" 
        return f"UNIT_{clean_name}"

    def load_memory_into_graph(self, json_path: str):
        path = Path(json_path)
        if not path.exists():
            logger.warning(f"Memory file not found: {path}")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for gene_data in data.get("genes", []):
            source_file = gene_data['metadata'].get('source_file', 'unknown')
            tenant_id = self._derive_tenant_from_source(source_file)
            self.tenants.add(tenant_id)
            
            verdict = gene_data.get('last_verdict', 'UNKNOWN')
            # CP Interpretation logic
            cp_score = 0.5
            if "ADAPTED" in verdict: cp_score = 0.95
            elif "RECALLED" in verdict: cp_score = 0.98
            elif "NOMINAL" in verdict: cp_score = 0.90
            elif "VETO" in verdict: cp_score = 0.0 # Knowledge of Failure
            
            # If explicit CP exists in data, use it (more precise)
            if 'craft_performance' in gene_data:
                cp_score = gene_data['craft_performance']

            node_id = f"{tenant_id}::{gene_data['uid']}"
            
            self.G.add_node(
                node_id,
                type="GENE",
                tenant=tenant_id,
                name=gene_data['name'],
                domain="MECHANICAL" if "FD" in tenant_id else "FINANCIAL", 
                cp=cp_score,
                provenance="NATIVE", 
                raw_data=gene_data
            )
            
            concept_name = source_file
            concept_id = f"CONCEPT::{concept_name}"
            
            self.G.add_node(concept_id, type="CONCEPT", domain="GLOBAL")
            self.G.add_edge(concept_id, node_id, relation="INDEXES")
            count += 1

        logger.info(f"🕸️ GRAPH: Distributed {count} genes across {len(self.tenants)} Tenants: {list(self.tenants)}")

    def secure_federation_protocol(self, source_tenant: str, target_tenant: str):
        """
        Implements 'Total Knowledge' Federation:
        1. Source Selection: ALL genes are candidates. (Successes AND Failures).
        2. Gap Filling: If target lacks the gene, take it (even if CP=0.0).
        3. Improvement: If target has it, take source ONLY if source_CP > target_CP.
        """
        logger.info(f"🛡️ FEDERATION PROTOCOL: {source_tenant} -> {target_tenant}")
        
        # 1. ANALOGY CHECK
        source_domain = "MECHANICAL" if "FD" in source_tenant else "FINANCIAL"
        target_domain = "MECHANICAL" if "FD" in target_tenant else "FINANCIAL"
        
        transfer_type = "DIRECT_COPY"
        if source_domain != target_domain:
            transfer_type = "STRUCTURAL_ANALOGY"
            logger.info(f"   ✨ MERISTIC ANALOGY: {source_domain} -> {target_domain}")

        # 2. CANDIDATE SELECTION (NO FILTER - TOTAL TRANSPARENCY)
        candidates = []
        for node, attrs in self.G.nodes(data=True):
            if attrs.get('tenant') == source_tenant and attrs.get('type') == "GENE":
                # We take everything. Even CP 0.0 (Vetos).
                candidates.append((node, attrs))
        
        if not candidates:
            logger.info("   -> Source tenant is empty.")
            return 0

        # 3. UTILITY & GAP CHECK
        accepted = 0
        gap_fills = 0
        upgrades = 0
        redundant = 0
        
        for src_id, src_attrs in candidates:
            # Heuristic to find counterpart: same vector suffix (e.g. "Vec100")
            gene_suffix = src_attrs['name'].split('_')[-1] 
            
            target_counterpart = None
            current_cp = -1.0 # Start lower than possible 0.0 to ensure 0.0 overwrites "Nothing"
            
            for t_node, t_attrs in self.G.nodes(data=True):
                if t_attrs.get('tenant') == target_tenant and t_attrs['name'].endswith(gene_suffix):
                    target_counterpart = t_node
                    current_cp = t_attrs.get('cp', 0)
                    break
            
            new_cp = src_attrs.get('cp', 0)
            
            if target_counterpart:
                # SCENARIO: Target already knows this situation.
                # Only accept if new is STRICTLY better.
                if new_cp > current_cp: 
                    self._replicate_gene(src_id, src_attrs, target_tenant, reason=f"UPGRADE_{transfer_type}")
                    upgrades += 1
                    accepted += 1
                else:
                    redundant += 1
            else:
                # SCENARIO: Gap (Target is ignorant).
                # Accept EVERYTHING. Even a Veto (CP=0).
                # Learning "Don't do X" (CP=0) is valuable if you didn't know X existed.
                self._replicate_gene(src_id, src_attrs, target_tenant, reason=f"GAP_FILL_{transfer_type}")
                gap_fills += 1
                accepted += 1

        logger.info(f"   ✅ SYNCHRONIZED: {accepted} (Gaps: {gap_fills} | Upgrades: {upgrades})")
        logger.info(f"   💤 SKIPPED: {redundant} (No strategic gain)")
        return accepted

    def _replicate_gene(self, src_id, src_attrs, target_tenant, reason):
        original_uid = src_id.split("::")[-1]
        new_id = f"{target_tenant}::{original_uid}"
        
        new_attrs = src_attrs.copy()
        new_attrs['tenant'] = target_tenant
        new_attrs['provenance'] = f"FEDERATED::{src_attrs['tenant']}::{reason}"
        if "ANALOGY" in reason: new_attrs['adaptation_pending'] = True 
        
        self.G.add_node(new_id, **new_attrs)
        
        # Ontology Link
        for pred in self.G.predecessors(src_id):
            if self.G.nodes[pred].get('type') == "CONCEPT":
                self.G.add_edge(pred, new_id, relation="INDEXES")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    federation = FederatedGraphEngine()
    
    print("--- 1. LOADING FLEET MEMORY ---")
    federation.load_memory_into_graph("data/cortex/genome_memory.json")
    
    tenants = list(federation.tenants)
    print(f"Detected Tenants: {tenants}")
    
    # Simulation Logic
    source_mech = "UNIT_FD001"
    target_mech = "UNIT_FD003"
    
    source_mech2 = "UNIT_FD002"
    target_mech2 = "UNIT_FD004"
    
    source_fin = "DEPT_FINANCE"
    
    # Run Validations if tenants exist
    if source_mech in tenants and target_mech in tenants:
        print(f"\n--- 2. FEDERATION: {source_mech} -> {target_mech} ---")
        federation.secure_federation_protocol(source_mech, target_mech)

    if source_mech2 in tenants and target_mech2 in tenants:
        print(f"\n--- 3. FEDERATION: {source_mech2} -> {target_mech2} ---")
        federation.secure_federation_protocol(source_mech2, target_mech2)
            
    if source_fin in tenants and source_mech in tenants:
        print(f"\n--- 4. FEDERATION: {source_fin} -> {source_mech} (Analogy) ---")
        federation.secure_federation_protocol(source_fin, source_mech)