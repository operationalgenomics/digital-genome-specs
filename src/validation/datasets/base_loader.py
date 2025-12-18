"""
Base Loader Interface for Dataset Transformation
=================================================

This module defines the abstract interface that all dataset loaders must implement.
The interface ensures consistent transformation from raw data formats into
Praxeological Codons that can be evaluated by the Four Parallel Motors.

DESIGN PRINCIPLES:
------------------
1. Separation of Concerns: Loading, parsing, and transformation are distinct steps
2. Reproducibility: Same input always produces same output (deterministic hashing)
3. Traceability: Each codon maintains lineage to its source record
4. Validation: Schema compliance is verified at transformation time

TRANSFORMATION PIPELINE:
------------------------
Raw Data → Parse → Extract Triples → Create Codons → Assemble Genes → Validate

The pipeline preserves the Foucauldian nature of the source data: we register
what actually happened, without interpretation or normalization beyond what is
necessary for structural compatibility.

Author: Carlos Eduardo Favini
License: MIT
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Iterator, Generator
from enum import Enum
from pathlib import Path
import hashlib
import json
import time
import logging

# Configure logging for the validation module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("validation.datasets")


# ============================================================================
# CONFIGURATION STRUCTURES
# ============================================================================

@dataclass
class LoaderConfig:
    """
    Base configuration for dataset loaders.
    
    Each specific loader extends this with domain-specific parameters.
    The configuration is immutable once created to ensure reproducibility.
    
    Attributes:
        data_path: Path to the raw data file or directory
        output_path: Path where transformed data will be stored
        cache_enabled: Whether to cache intermediate results
        validation_enabled: Whether to validate schema compliance
        max_records: Maximum number of records to process (None = all)
        random_seed: Seed for any stochastic operations (reproducibility)
    """
    data_path: Path
    output_path: Optional[Path] = None
    cache_enabled: bool = True
    validation_enabled: bool = True
    max_records: Optional[int] = None
    random_seed: int = 42
    
    def __post_init__(self):
        """Converts string paths to Path objects if necessary."""
        if isinstance(self.data_path, str):
            self.data_path = Path(self.data_path)
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes configuration for logging and reproducibility."""
        return {
            "data_path": str(self.data_path),
            "output_path": str(self.output_path) if self.output_path else None,
            "cache_enabled": self.cache_enabled,
            "validation_enabled": self.validation_enabled,
            "max_records": self.max_records,
            "random_seed": self.random_seed
        }


@dataclass
class TransformationResult:
    """
    The result of transforming a dataset into Praxeological structures.
    
    This structure captures both the transformed data and metadata about
    the transformation process, enabling full reproducibility and audit.
    
    Attributes:
        codons: List of Praxeological Codons extracted from the data
        genes: List of Operational Genes assembled from codons
        metadata: Information about the transformation process
        statistics: Summary statistics of the transformed data
        warnings: Any issues encountered during transformation
        transformation_hash: Deterministic hash of the entire result
    """
    codons: List[Dict[str, Any]]
    genes: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    statistics: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    transformation_hash: str = ""
    
    def __post_init__(self):
        """Computes the deterministic hash after initialization."""
        if not self.transformation_hash:
            self.transformation_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """
        Computes a deterministic hash of the transformation result.
        
        This hash enables verification that two transformations of the
        same data with the same configuration produce identical results.
        """
        # Create a canonical representation for hashing
        canonical = json.dumps({
            "codons_count": len(self.codons),
            "genes_count": len(self.genes),
            "codon_hashes": sorted([c.get("uid", "") for c in self.codons]),
            "gene_hashes": sorted([g.get("uid", "") for g in self.genes])
        }, sort_keys=True)
        
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the complete result for storage."""
        return {
            "codons": self.codons,
            "genes": self.genes,
            "metadata": self.metadata,
            "statistics": self.statistics,
            "warnings": self.warnings,
            "transformation_hash": self.transformation_hash
        }
    
    def save(self, path: Path) -> None:
        """Persists the result to a JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Transformation result saved to {path}")
    
    @classmethod
    def load(cls, path: Path) -> 'TransformationResult':
        """Loads a previously saved transformation result."""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(
            codons=data["codons"],
            genes=data["genes"],
            metadata=data["metadata"],
            statistics=data["statistics"],
            warnings=data.get("warnings", []),
            transformation_hash=data["transformation_hash"]
        )


# ============================================================================
# PRAXEOLOGICAL TRIPLE EXTRACTION
# ============================================================================

@dataclass
class PraxeologicalTriple:
    """
    The fundamental structure extracted from raw data: Entity → Action → State.
    
    This triple represents the atomic unit of intentional behavior observed
    in the source data. Each raw record (event log entry, sensor reading,
    transaction) is decomposed into one or more triples.
    
    The triple is not yet a full Codon — it lacks context, timestamp binding,
    and hash registration. These are added during codon assembly.
    
    Attributes:
        entity: The agent or object performing/receiving the action
        action: The operation being performed
        state: The resulting or target state
        source_record: Reference to the original data record
        confidence: How certain we are about this extraction [0, 1]
    """
    entity: str
    action: str
    state: str
    source_record: Dict[str, Any]
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity": self.entity,
            "action": self.action,
            "state": self.state,
            "source_record_hash": hashlib.sha256(
                json.dumps(self.source_record, sort_keys=True).encode()
            ).hexdigest()[:16],
            "confidence": self.confidence
        }


# ============================================================================
# ABSTRACT BASE LOADER
# ============================================================================

class BaseLoader(ABC):
    """
    Abstract base class for all dataset loaders.
    
    This class defines the interface that every domain-specific loader must
    implement. The interface follows a pipeline pattern:
    
    1. load(): Read raw data from source
    2. parse(): Convert to internal representation
    3. extract_triples(): Identify Entity-Action-State structures
    4. assemble_codons(): Create full Praxeological Codons
    5. assemble_genes(): Group codons into Operational Genes
    6. validate(): Verify schema compliance
    7. transform(): Execute the complete pipeline
    
    Subclasses must implement the abstract methods that define domain-specific
    logic. The base class provides common utilities and the pipeline orchestration.
    
    CRITICAL: Loaders must be deterministic. Given the same input and config,
    they must produce byte-identical output. This is essential for scientific
    reproducibility.
    """
    
    def __init__(self, config: LoaderConfig):
        """
        Initializes the loader with configuration.
        
        Args:
            config: LoaderConfig instance with transformation parameters
        """
        self.config = config
        self.raw_data: Optional[Any] = None
        self.parsed_data: Optional[List[Dict[str, Any]]] = None
        self._transformation_start: Optional[float] = None
        
        logger.info(f"Initialized {self.__class__.__name__} with config: {config.to_dict()}")
    
    # ========================================================================
    # ABSTRACT METHODS - Must be implemented by subclasses
    # ========================================================================
    
    @property
    @abstractmethod
    def dataset_name(self) -> str:
        """Returns the canonical name of this dataset."""
        pass
    
    @property
    @abstractmethod
    def dataset_description(self) -> str:
        """Returns a description of the dataset and its source."""
        pass
    
    @property
    @abstractmethod
    def dataset_url(self) -> str:
        """Returns the URL where the dataset can be downloaded."""
        pass
    
    @abstractmethod
    def load(self) -> Any:
        """
        Loads raw data from the configured source.
        
        This method handles file I/O, decompression, and any format-specific
        parsing required to get the data into memory.
        
        Returns:
            The raw data in its native format (DataFrame, list, etc.)
        """
        pass
    
    @abstractmethod
    def parse(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Converts raw data into a normalized list of records.
        
        Each record is a dictionary representing one atomic observation
        from the source data. The structure depends on the data domain.
        
        Args:
            raw_data: Data returned by load()
            
        Returns:
            List of dictionaries, one per source record
        """
        pass
    
    @abstractmethod
    def extract_triple(self, record: Dict[str, Any]) -> PraxeologicalTriple:
        """
        Extracts the Entity-Action-State triple from a single record.
        
        This is the core transformation logic that recognizes intentional
        structure in raw data. Domain expertise is encoded here.
        
        Args:
            record: A single parsed record
            
        Returns:
            PraxeologicalTriple representing the intentional action
        """
        pass
    
    @abstractmethod
    def extract_context(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts contextual features from a record.
        
        Context captures the circumstances under which the action occurred.
        This becomes the 'ctx' vector in the Praxeological Codon.
        
        Args:
            record: A single parsed record
            
        Returns:
            Dictionary of contextual features
        """
        pass
    
    @abstractmethod
    def group_into_genes(
        self, 
        codons: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Groups related codons into Operational Genes.
        
        A gene represents a complete functional sequence. How codons are
        grouped depends on the domain — by case ID, session, transaction, etc.
        
        Args:
            codons: List of assembled codons
            
        Returns:
            List of gene dictionaries
        """
        pass
    
    # ========================================================================
    # COMMON METHODS - Provided by base class
    # ========================================================================
    
    def assemble_codon(
        self,
        triple: PraxeologicalTriple,
        context: Dict[str, Any],
        timestamp: float,
        sequence_position: int
    ) -> Dict[str, Any]:
        """
        Assembles a complete Praxeological Codon from extracted components.
        
        This method creates the full codon structure as defined in the
        Digital Genome schema, including the cryptographic hash that
        ensures immutability.
        
        Args:
            triple: The Entity-Action-State triple
            context: Contextual features dictionary
            timestamp: Unix timestamp of the observation
            sequence_position: Position within the parent gene
            
        Returns:
            Complete codon dictionary conforming to schema
        """
        # Create the base codon structure
        codon = {
            "entity_id": triple.entity,
            "action_id": triple.action,
            "target_state_id": triple.state,
            "parameters": triple.source_record,
            "context": context,
            "timestamp": timestamp,
            "sequence_position": sequence_position,
            "extraction_confidence": triple.confidence,
            "safety_level": "info"  # Default; can be overridden by domain logic
        }
        
        # Compute the deterministic UID (hash of content)
        uid_source = json.dumps({
            "entity": codon["entity_id"],
            "action": codon["action_id"],
            "state": codon["target_state_id"],
            "timestamp": codon["timestamp"],
            "context_hash": hashlib.sha256(
                json.dumps(context, sort_keys=True).encode()
            ).hexdigest()
        }, sort_keys=True)
        
        codon["uid"] = hashlib.sha256(uid_source.encode()).hexdigest()
        
        return codon
    
    def extract_triples(
        self, 
        records: List[Dict[str, Any]]
    ) -> Generator[Tuple[PraxeologicalTriple, Dict[str, Any]], None, None]:
        """
        Extracts triples and contexts from all records.
        
        This is a generator to support memory-efficient processing of
        large datasets.
        
        Args:
            records: List of parsed records
            
        Yields:
            Tuples of (PraxeologicalTriple, context_dict)
        """
        for record in records:
            try:
                triple = self.extract_triple(record)
                context = self.extract_context(record)
                yield (triple, context)
            except Exception as e:
                logger.warning(f"Failed to extract triple from record: {e}")
                continue
    
    def assemble_codons(
        self,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Assembles codons from all records.
        
        Args:
            records: List of parsed records
            
        Returns:
            List of assembled codon dictionaries
        """
        codons = []
        
        for i, (triple, context) in enumerate(self.extract_triples(records)):
            # Extract timestamp from source record or use sequence position
            timestamp = triple.source_record.get(
                "timestamp",
                triple.source_record.get("time:timestamp", time.time())
            )
            
            # Handle various timestamp formats
            if isinstance(timestamp, str):
                try:
                    from datetime import datetime
                    # Try ISO format first
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.timestamp()
                except:
                    timestamp = float(i)  # Fall back to sequence position
            
            codon = self.assemble_codon(triple, context, timestamp, i)
            codons.append(codon)
        
        logger.info(f"Assembled {len(codons)} codons from {len(records)} records")
        return codons
    
    def validate_codon(self, codon: Dict[str, Any]) -> List[str]:
        """
        Validates a codon against the schema requirements.
        
        Args:
            codon: Codon dictionary to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Required fields
        required = ["entity_id", "action_id", "target_state_id", "uid"]
        for field in required:
            if field not in codon or not codon[field]:
                errors.append(f"Missing required field: {field}")
        
        # UID format (64-char hex)
        if "uid" in codon and len(codon["uid"]) != 64:
            errors.append(f"Invalid UID length: {len(codon['uid'])} (expected 64)")
        
        return errors
    
    def validate_gene(self, gene: Dict[str, Any]) -> List[str]:
        """
        Validates a gene against the schema requirements.
        
        Args:
            gene: Gene dictionary to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Required fields
        required = ["uid", "name", "purpose", "codons"]
        for field in required:
            if field not in gene or not gene[field]:
                errors.append(f"Missing required field: {field}")
        
        # Must have at least one codon
        if "codons" in gene and len(gene["codons"]) == 0:
            errors.append("Gene must contain at least one codon")
        
        return errors
    
    def transform(self) -> TransformationResult:
        """
        Executes the complete transformation pipeline.
        
        This is the main entry point for dataset transformation. It orchestrates
        all the steps in the pipeline and returns the complete result.
        
        Returns:
            TransformationResult containing all transformed data and metadata
        """
        self._transformation_start = time.time()
        warnings = []
        
        # Step 1: Load raw data
        logger.info(f"Loading data from {self.config.data_path}")
        self.raw_data = self.load()
        
        # Step 2: Parse into records
        logger.info("Parsing raw data into records")
        self.parsed_data = self.parse(self.raw_data)
        
        # Apply max_records limit if configured
        if self.config.max_records:
            self.parsed_data = self.parsed_data[:self.config.max_records]
            logger.info(f"Limited to {self.config.max_records} records")
        
        # Step 3: Assemble codons
        logger.info("Assembling Praxeological Codons")
        codons = self.assemble_codons(self.parsed_data)
        
        # Step 4: Validate codons if enabled
        if self.config.validation_enabled:
            logger.info("Validating codons")
            for i, codon in enumerate(codons):
                errors = self.validate_codon(codon)
                if errors:
                    warnings.extend([f"Codon {i}: {e}" for e in errors])
        
        # Step 5: Group into genes
        logger.info("Assembling Operational Genes")
        genes = self.group_into_genes(codons)
        
        # Step 6: Validate genes if enabled
        if self.config.validation_enabled:
            logger.info("Validating genes")
            for i, gene in enumerate(genes):
                errors = self.validate_gene(gene)
                if errors:
                    warnings.extend([f"Gene {i}: {e}" for e in errors])
        
        # Compute statistics
        elapsed = time.time() - self._transformation_start
        statistics = {
            "total_records": len(self.parsed_data),
            "total_codons": len(codons),
            "total_genes": len(genes),
            "avg_codons_per_gene": len(codons) / len(genes) if genes else 0,
            "transformation_time_seconds": round(elapsed, 2),
            "records_per_second": round(len(self.parsed_data) / elapsed, 2) if elapsed > 0 else 0
        }
        
        # Build metadata
        metadata = {
            "dataset_name": self.dataset_name,
            "dataset_description": self.dataset_description,
            "dataset_url": self.dataset_url,
            "loader_class": self.__class__.__name__,
            "config": self.config.to_dict(),
            "transformation_timestamp": time.time(),
            "validation_warnings_count": len(warnings)
        }
        
        result = TransformationResult(
            codons=codons,
            genes=genes,
            metadata=metadata,
            statistics=statistics,
            warnings=warnings
        )
        
        logger.info(f"Transformation complete: {statistics}")
        
        # Save if output path configured
        if self.config.output_path:
            result.save(self.config.output_path)
        
        return result
