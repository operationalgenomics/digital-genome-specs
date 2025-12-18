"""
BPI Challenge 2017 Dataset Loader
==================================

This module transforms the BPI Challenge 2017 event log into Praxeological
Codons suitable for validation of the Digital Genome framework.

DATASET DESCRIPTION:
--------------------
The BPI Challenge 2017 dataset contains event logs from a Dutch financial
institution's loan application process. It records the complete lifecycle
of loan applications from initial submission through final decision.

Source: 4TU.ResearchData
URL: https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884
Format: XES (eXtensible Event Stream)
Volume: ~1.2 million events, ~31,500 cases

PRAXEOLOGICAL STRUCTURE:
------------------------
Each event in the log represents a purposeful action:
- Entity: The resource (employee/system) performing the action
- Action: The activity being executed
- State: The lifecycle transition (start, complete, etc.)

The process itself encodes intention: the stated purpose of each case is
to evaluate and decide on a loan application. This makes BPI 2017 ideal
for testing the Praxeological Motor's ability to detect intention-realization
failures (cases where the process deviates from its purpose).

GROUND TRUTH:
-------------
The dataset includes case outcomes:
- Application accepted/rejected
- Offer made/not made
- Customer accepted/rejected offer

This allows us to correlate M_P scores with actual outcomes, validating
that the motor correctly identifies praxeological failures.

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import time
import logging
import gzip
import xml.etree.ElementTree as ET

from .base_loader import (
    BaseLoader,
    LoaderConfig,
    TransformationResult,
    PraxeologicalTriple
)

logger = logging.getLogger("validation.datasets.bpi")


# ============================================================================
# BPI-SPECIFIC CONFIGURATION
# ============================================================================

@dataclass
class BPIConfig(LoaderConfig):
    """
    Configuration specific to BPI Challenge dataset loading.
    
    Extends the base configuration with parameters relevant to
    process mining event logs in XES format.
    
    Attributes:
        include_incomplete_cases: Whether to include cases without final outcome
        min_events_per_case: Minimum events required to form a valid gene
        activity_filter: Optional list of activities to include (None = all)
        extract_offers: Whether to extract offer sub-process separately
    """
    include_incomplete_cases: bool = False
    min_events_per_case: int = 2
    activity_filter: Optional[List[str]] = None
    extract_offers: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes BPI-specific configuration."""
        base = super().to_dict()
        base.update({
            "include_incomplete_cases": self.include_incomplete_cases,
            "min_events_per_case": self.min_events_per_case,
            "activity_filter": self.activity_filter,
            "extract_offers": self.extract_offers
        })
        return base


# ============================================================================
# XES NAMESPACE HANDLING
# ============================================================================

# XES standard namespaces
XES_NS = {
    'xes': 'http://www.xes-standard.org/',
    'default': 'http://www.xes-standard.org/'
}


def parse_xes_value(element: ET.Element) -> Tuple[str, Any]:
    """
    Extracts key-value pair from an XES attribute element.
    
    XES stores attributes as typed elements (<string>, <int>, <date>, etc.)
    with 'key' and 'value' attributes.
    
    Args:
        element: An XES attribute element
        
    Returns:
        Tuple of (attribute_key, attribute_value)
    """
    key = element.get('key', '')
    value = element.get('value', '')
    
    # Type conversion based on element tag
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    
    if tag == 'int':
        try:
            value = int(value)
        except ValueError:
            pass
    elif tag == 'float':
        try:
            value = float(value)
        except ValueError:
            pass
    elif tag == 'boolean':
        value = value.lower() == 'true'
    elif tag == 'date':
        # Keep as string for now; will be parsed during codon assembly
        pass
    
    return key, value


# ============================================================================
# BPI CHALLENGE LOADER
# ============================================================================

class BPILoader(BaseLoader):
    """
    Loader for BPI Challenge 2017 event log data.
    
    This loader transforms XES-format process mining logs into Praxeological
    Codons and Operational Genes. Each case (loan application) becomes a gene,
    and each event within the case becomes a codon.
    
    PRAXEOLOGICAL MAPPING:
    ----------------------
    XES Event → Praxeological Codon
    - concept:name (activity) → action_id
    - org:resource → entity_id  
    - lifecycle:transition → target_state_id
    - time:timestamp → timestamp
    - All other attributes → context
    
    XES Trace → Operational Gene
    - case:concept:name → gene name/UID seed
    - All events in trace → codons sequence
    - case:LoanGoal → purpose
    - Final outcome → postconditions (ground truth)
    
    IMPORTANT ACTIVITIES IN BPI 2017:
    ---------------------------------
    The process contains three sub-processes:
    1. Application (A_): Initial submission and validation
    2. Offer (O_): Offer creation and customer response  
    3. Workflow (W_): Internal workflow activities
    
    Key activities for praxeological evaluation:
    - A_Submitted: Application submitted (intention declared)
    - A_Accepted: Application accepted (intention potentially realized)
    - A_Denied: Application denied (intention blocked)
    - O_Created: Offer created (intermediate realization)
    - O_Accepted: Offer accepted by customer (full realization)
    - O_Refused: Offer refused (realization failed)
    """
    
    def __init__(self, config: BPIConfig):
        """
        Initializes the BPI loader.
        
        Args:
            config: BPIConfig with transformation parameters
        """
        super().__init__(config)
        self.config: BPIConfig = config  # Type hint refinement
        
        # BPI-specific state
        self._case_outcomes: Dict[str, Dict[str, Any]] = {}
        self._activity_counts: Dict[str, int] = defaultdict(int)
    
    # ========================================================================
    # ABSTRACT METHOD IMPLEMENTATIONS
    # ========================================================================
    
    @property
    def dataset_name(self) -> str:
        return "BPI Challenge 2017"
    
    @property
    def dataset_description(self) -> str:
        return (
            "Event log from a Dutch financial institution's loan application "
            "process. Contains ~31,500 cases with ~1.2 million events tracking "
            "the complete lifecycle from application submission through final "
            "decision. Published as part of the Business Process Intelligence "
            "Challenge 2017."
        )
    
    @property
    def dataset_url(self) -> str:
        return "https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884"
    
    def load(self) -> ET.Element:
        """
        Loads the XES file and returns the root element.
        
        Handles both plain XES and gzipped XES files.
        
        Returns:
            ElementTree root element containing the log
        """
        path = self.config.data_path
        
        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {path}\n"
                f"Download from: {self.dataset_url}"
            )
        
        logger.info(f"Loading XES file: {path}")
        
        # Handle gzipped files
        if path.suffix == '.gz':
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                tree = ET.parse(f)
        else:
            tree = ET.parse(path)
        
        root = tree.getroot()
        logger.info(f"Loaded XES log with {len(list(root))} top-level elements")
        
        return root
    
    def parse(self, raw_data: ET.Element) -> List[Dict[str, Any]]:
        """
        Parses XES XML into a list of event records.
        
        The XES format structures data as:
        <log>
            <trace> (one per case)
                <event> (one per activity execution)
                    <string key="concept:name" value="A_Submitted"/>
                    <date key="time:timestamp" value="2016-01-01T00:00:00"/>
                    ...
                </event>
                ...
            </trace>
            ...
        </log>
        
        Args:
            raw_data: Root element of the XES document
            
        Returns:
            List of event dictionaries with case context included
        """
        events = []
        
        # Find all traces (cases)
        # Handle namespace variations in XES files
        traces = raw_data.findall('.//trace', XES_NS)
        if not traces:
            traces = raw_data.findall('.//{http://www.xes-standard.org/}trace')
        if not traces:
            # Try without namespace
            traces = raw_data.findall('.//trace')
        
        logger.info(f"Found {len(traces)} traces (cases) in log")
        
        for trace_idx, trace in enumerate(traces):
            # Extract case-level attributes
            case_attrs = {}
            for attr in trace:
                if attr.tag.endswith(('string', 'int', 'float', 'date', 'boolean')):
                    key, value = parse_xes_value(attr)
                    case_attrs[key] = value
            
            case_id = case_attrs.get('concept:name', f'case_{trace_idx}')
            
            # Store case outcome for ground truth
            self._case_outcomes[case_id] = {
                'ApplicationType': case_attrs.get('ApplicationType'),
                'LoanGoal': case_attrs.get('LoanGoal'),
                'RequestedAmount': case_attrs.get('RequestedAmount'),
            }
            
            # Find all events in this trace
            trace_events = trace.findall('.//{http://www.xes-standard.org/}event')
            if not trace_events:
                trace_events = trace.findall('.//event')
            
            for event_idx, event in enumerate(trace_events):
                # Extract event-level attributes
                event_attrs = {'case_id': case_id}
                event_attrs.update(case_attrs)  # Include case context
                
                for attr in event:
                    if attr.tag.endswith(('string', 'int', 'float', 'date', 'boolean')):
                        key, value = parse_xes_value(attr)
                        event_attrs[key] = value
                
                # Add sequence position within case
                event_attrs['_sequence_position'] = event_idx
                event_attrs['_case_length'] = len(trace_events)
                
                # Track activity for statistics
                activity = event_attrs.get('concept:name', 'Unknown')
                self._activity_counts[activity] += 1
                
                # Apply activity filter if configured
                if self.config.activity_filter:
                    if activity not in self.config.activity_filter:
                        continue
                
                events.append(event_attrs)
        
        logger.info(f"Parsed {len(events)} events from {len(traces)} cases")
        logger.info(f"Activity distribution: {dict(self._activity_counts)}")
        
        return events
    
    def extract_triple(self, record: Dict[str, Any]) -> PraxeologicalTriple:
        """
        Extracts the praxeological triple from a BPI event.
        
        MAPPING RATIONALE:
        - Entity: The resource (employee/system) executing the activity represents
          the agent whose intention drives the action.
        - Action: The activity name (concept:name) is the operation being performed.
        - State: The lifecycle transition indicates the outcome of this atomic step.
        
        Args:
            record: A single parsed event dictionary
            
        Returns:
            PraxeologicalTriple with entity, action, state
        """
        # Entity: Who/what performed this action
        # In BPI 2017, org:resource identifies the actor
        entity = record.get('org:resource', 'System')
        if not entity or entity == 'None':
            entity = 'AutomatedSystem'
        
        # Action: What operation was performed
        # concept:name is the standard XES attribute for activity name
        action = record.get('concept:name', 'UnknownActivity')
        
        # State: What is the result/transition of this action
        # lifecycle:transition indicates the event type (start, complete, etc.)
        lifecycle = record.get('lifecycle:transition', 'complete')
        
        # Construct a meaningful state from action + lifecycle
        # This captures the teleological outcome of this atomic step
        state = f"{action}_{lifecycle}"
        
        # Confidence is based on data completeness
        confidence = 1.0
        if entity == 'AutomatedSystem':
            confidence *= 0.9  # Slightly less certain about automated actors
        if action == 'UnknownActivity':
            confidence *= 0.5  # Significantly less certain
        
        return PraxeologicalTriple(
            entity=entity,
            action=action,
            state=state,
            source_record=record,
            confidence=confidence
        )
    
    def extract_context(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts contextual features from a BPI event.
        
        The context vector captures the circumstances under which the action
        occurred. For BPI 2017, this includes:
        - Case attributes (loan amount, type, goal)
        - Process position (how far into the case)
        - Temporal features (time of day, day of week if extractable)
        
        Args:
            record: A single parsed event dictionary
            
        Returns:
            Dictionary of contextual features for the codon
        """
        context = {}
        
        # Case-level context (static throughout the case)
        context['application_type'] = record.get('ApplicationType', 'Unknown')
        context['loan_goal'] = record.get('LoanGoal', 'Unknown')
        context['requested_amount'] = record.get('RequestedAmount', 0)
        
        # Process position context
        context['sequence_position'] = record.get('_sequence_position', 0)
        context['case_length'] = record.get('_case_length', 1)
        context['relative_position'] = (
            record.get('_sequence_position', 0) / 
            max(record.get('_case_length', 1), 1)
        )
        
        # Resource context
        context['resource'] = record.get('org:resource', 'Unknown')
        context['lifecycle'] = record.get('lifecycle:transition', 'complete')
        
        # Offer-related context (specific to BPI 2017)
        if 'OfferID' in record:
            context['offer_id'] = record['OfferID']
        if 'NumberOfTerms' in record:
            context['number_of_terms'] = record['NumberOfTerms']
        if 'MonthlyCost' in record:
            context['monthly_cost'] = record['MonthlyCost']
        if 'CreditScore' in record:
            context['credit_score'] = record['CreditScore']
        if 'FirstWithdrawalAmount' in record:
            context['first_withdrawal'] = record['FirstWithdrawalAmount']
        
        return context
    
    def group_into_genes(
        self,
        codons: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Groups codons into genes by case ID.
        
        In BPI 2017, each case (loan application) represents a complete
        functional sequence — an Operational Gene. The case has a clear
        purpose (evaluate loan application) and a measurable outcome.
        
        GENE STRUCTURE:
        - name: Derived from case ID
        - purpose: "Process loan application for {LoanGoal}"
        - codons: All events in the case, ordered by timestamp
        - postconditions: Outcome (accepted/denied/withdrawn)
        
        Args:
            codons: List of assembled codons
            
        Returns:
            List of gene dictionaries
        """
        # Group codons by case ID
        cases: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        for codon in codons:
            case_id = codon['parameters'].get('case_id', 'unknown')
            cases[case_id].append(codon)
        
        genes = []
        
        for case_id, case_codons in cases.items():
            # Skip cases with too few events
            if len(case_codons) < self.config.min_events_per_case:
                continue
            
            # Sort codons by timestamp
            case_codons.sort(key=lambda c: c.get('timestamp', 0))
            
            # Determine case outcome (ground truth)
            outcome = self._determine_case_outcome(case_codons)
            
            # Skip incomplete cases if configured
            if not self.config.include_incomplete_cases:
                if outcome['status'] == 'incomplete':
                    continue
            
            # Extract case metadata
            first_codon = case_codons[0]
            case_context = first_codon.get('context', {})
            
            # Build gene purpose from loan goal
            loan_goal = case_context.get('loan_goal', 'Unknown')
            purpose = f"Process loan application for {loan_goal}"
            
            # Compute gene UID from case ID
            gene_uid = hashlib.sha256(
                f"bpi2017:gene:{case_id}".encode()
            ).hexdigest()
            
            # Determine activation conditions from first activity
            first_activity = first_codon.get('action_id', '')
            activation = [f"activity={first_activity}"]
            
            # Build postconditions from outcome
            postconditions = [
                f"outcome={outcome['status']}",
                f"final_activity={outcome['final_activity']}"
            ]
            if outcome.get('offer_accepted') is not None:
                postconditions.append(
                    f"offer_accepted={outcome['offer_accepted']}"
                )
            
            gene = {
                "uid": gene_uid,
                "name": f"LoanApplication_{case_id}",
                "purpose": purpose,
                "version": "1.0.0",
                "status": "active",
                "codons": case_codons,
                "activation_conditions": activation,
                "postconditions": postconditions,
                "metadata": {
                    "case_id": case_id,
                    "application_type": case_context.get('application_type'),
                    "requested_amount": case_context.get('requested_amount'),
                    "loan_goal": loan_goal,
                    "outcome": outcome
                },
                "created_at": time.time()
            }
            
            genes.append(gene)
        
        logger.info(f"Assembled {len(genes)} genes from {len(cases)} cases")
        
        return genes
    
    # ========================================================================
    # BPI-SPECIFIC HELPER METHODS
    # ========================================================================
    
    def _determine_case_outcome(
        self,
        case_codons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Determines the outcome of a case based on its activities.
        
        BPI 2017 outcomes are determined by which final activities occurred:
        - A_Denied → Application denied (intention blocked)
        - A_Cancelled → Application cancelled (intention withdrawn)
        - O_Accepted → Offer accepted (intention realized)
        - O_Refused → Offer refused (intention failed)
        - O_Cancelled → Offer cancelled (intention abandoned)
        
        This ground truth allows us to validate whether M_P correctly
        identifies cases where intention was vs wasn't realized.
        
        Args:
            case_codons: List of codons for a single case
            
        Returns:
            Dictionary with outcome status and details
        """
        # Collect all activities in the case
        activities = [c.get('action_id', '') for c in case_codons]
        
        outcome = {
            'status': 'incomplete',
            'final_activity': activities[-1] if activities else 'None',
            'offer_accepted': None,
            'application_accepted': None
        }
        
        # Check for definitive outcomes
        if 'A_Denied' in activities:
            outcome['status'] = 'denied'
            outcome['application_accepted'] = False
            
        elif 'A_Cancelled' in activities:
            outcome['status'] = 'cancelled'
            outcome['application_accepted'] = False
            
        elif 'O_Accepted' in activities:
            outcome['status'] = 'accepted'
            outcome['offer_accepted'] = True
            outcome['application_accepted'] = True
            
        elif 'O_Refused' in activities:
            outcome['status'] = 'refused'
            outcome['offer_accepted'] = False
            outcome['application_accepted'] = True  # App was accepted, offer refused
            
        elif 'O_Cancelled' in activities:
            outcome['status'] = 'offer_cancelled'
            outcome['offer_accepted'] = False
            outcome['application_accepted'] = True
            
        elif 'O_Created' in activities:
            # Offer was created but no final response
            outcome['status'] = 'pending_offer_response'
            outcome['application_accepted'] = True
            
        elif 'A_Accepted' in activities:
            outcome['status'] = 'pending_offer'
            outcome['application_accepted'] = True
        
        return outcome
    
    def get_outcome_distribution(self) -> Dict[str, int]:
        """
        Returns the distribution of case outcomes after transformation.
        
        Useful for understanding the dataset balance and stratifying
        experiments.
        
        Returns:
            Dictionary mapping outcome status to count
        """
        distribution = defaultdict(int)
        for case_id, outcome in self._case_outcomes.items():
            status = outcome.get('status', 'unknown')
            distribution[status] += 1
        return dict(distribution)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def load_bpi2017(
    data_path: str,
    max_records: Optional[int] = None
) -> TransformationResult:
    """
    Convenience function to load and transform BPI Challenge 2017 data.
    
    Args:
        data_path: Path to the XES file
        max_records: Maximum events to process (None = all)
        
    Returns:
        TransformationResult with codons and genes
    """
    config = BPIConfig(
        data_path=Path(data_path),
        max_records=max_records
    )
    loader = BPILoader(config)
    return loader.transform()


def download_bpi2017(target_path: Path) -> Path:
    """
    Downloads the BPI Challenge 2017 dataset.
    
    Note: The dataset requires acceptance of terms on 4TU.ResearchData.
    This function provides instructions rather than automatic download.
    
    Args:
        target_path: Directory where the file should be saved
        
    Returns:
        Expected path of the downloaded file
    """
    expected_file = target_path / "BPI_Challenge_2017.xes.gz"
    
    if expected_file.exists():
        logger.info(f"Dataset already exists: {expected_file}")
        return expected_file
    
    instructions = f"""
    ============================================================
    BPI Challenge 2017 Dataset Download Instructions
    ============================================================
    
    The dataset must be downloaded manually due to licensing terms.
    
    1. Visit: https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884
    2. Accept the terms of use
    3. Download "BPI_Challenge_2017.xes.gz"
    4. Save to: {target_path}
    
    Expected file: {expected_file}
    ============================================================
    """
    
    print(instructions)
    logger.info("Dataset download instructions provided")
    
    return expected_file


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == "__main__":
    """
    Test the BPI loader with a sample or the full dataset.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python bpi_loader.py <path_to_xes_file> [max_records]")
        print("\nThis will transform the BPI Challenge 2017 dataset into")
        print("Praxeological Codons and Operational Genes.")
        sys.exit(1)
    
    data_path = sys.argv[1]
    max_records = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    print(f"\nLoading BPI Challenge 2017 from: {data_path}")
    if max_records:
        print(f"Limiting to {max_records} records")
    
    result = load_bpi2017(data_path, max_records)
    
    print(f"\n{'='*60}")
    print("TRANSFORMATION RESULTS")
    print(f"{'='*60}")
    print(f"Total codons: {result.statistics['total_codons']}")
    print(f"Total genes: {result.statistics['total_genes']}")
    print(f"Avg codons/gene: {result.statistics['avg_codons_per_gene']:.2f}")
    print(f"Transform time: {result.statistics['transformation_time_seconds']}s")
    print(f"Hash: {result.transformation_hash[:32]}...")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings[:5]:
            print(f"  - {w}")
        if len(result.warnings) > 5:
            print(f"  ... and {len(result.warnings) - 5} more")
    
    print(f"\n{'='*60}")
