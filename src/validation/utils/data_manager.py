"""
data_manager.py
===============
Ensures Data Sovereignty and Reproducibility for the Digital Genome.

This module handles the atomic acquisition and verification of datasets.
It implements a "Trust but Verify" architecture:
1. Download from canonical sources.
2. Verify SHA-256 checksums against the Golden Master record.
3. Prevent execution if data integrity is compromised.

This ensures that any scientist, anywhere, running this code will use
the EXACT same bytes as the original author, preserving the validity
of the experimental results.
"""

import os
import requests
import hashlib
import logging
import zipfile
import tarfile
import gzip
import shutil
from pathlib import Path
from typing import Optional  # <--- Esta linha estava faltando!
from tqdm import tqdm  # Requires: pip install tqdm

logger = logging.getLogger("DataManager")

class DataIntegrityError(Exception):
    """Raised when the dataset on disk does not match the scientific record."""
    pass

def calculate_sha256(file_path: Path, chunk_size: int = 8192) -> str:
    """Computes the SHA-256 fingerprint of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return ""

def download_file(url: str, dest_path: Path) -> None:
    """Downloads a file with a progress bar."""
    logger.info(f"Initiating download from: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        # Ensure directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                bar.update(size)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise

def extract_file(archive_path: Path, extract_to: Path) -> None:
    """Smart extractor for zip, tar, and gz files."""
    logger.info(f"Extracting {archive_path} to {extract_to}...")
    
    if str(archive_path).endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif str(archive_path).endswith('.tar.gz') or str(archive_path).endswith('.tgz'):
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(extract_to)
    elif str(archive_path).endswith('.gz') and not str(archive_path).endswith('.tar.gz'):
        # For single .gz files (like BPI logs), decompress to same folder removing .gz extension
        output_file = extract_to / archive_path.stem
        with gzip.open(archive_path, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logger.info(f"Decompressed to {output_file}")

def ensure_dataset(
    name: str,
    target_path: Path,
    url: str,
    expected_hash: Optional[str] = None,
    extract: bool = False
) -> Path:
    """
    The Enforcer Function.
    Ensures the file exists AND matches the cryptographic signature.
    """
    target_path = Path(target_path)
    
    # 1. Check existence and integrity
    if target_path.exists():
        if expected_hash:
            logger.info(f"Verifying integrity for {name}...")
            current_hash = calculate_sha256(target_path)
            if current_hash != expected_hash:
                logger.warning(f"❌ {name}: Hash Mismatch!")
                logger.warning(f"   Expected: {expected_hash}")
                logger.warning(f"   Found:    {current_hash}")
                logger.warning("   Deleting corrupted file and re-downloading...")
                target_path.unlink()
            else:
                logger.info(f"✅ {name}: Integrity Verified.")
                return target_path
        else:
            logger.info(f"✅ {name}: Found (No hash verification requested).")
            return target_path

    # 2. Download
    logger.info(f"Dataset {name} not found or corrupted. Downloading...")
    download_file(url, target_path)
    
    # 3. Verify Download
    if expected_hash:
        new_hash = calculate_sha256(target_path)
        if new_hash != expected_hash:
            logger.error(f"CRITICAL: Downloaded file for {name} has wrong hash.")
            logger.error(f"Expected: {expected_hash}")
            logger.error(f"Got:      {new_hash}")
            raise DataIntegrityError(f"Integrity check failed for {name}")
    else:
        # If we don't have a hash yet, print it so the scientist can record it
        calc_hash = calculate_sha256(target_path)
        logger.info(f"⚠️  No hash provided for verification.")
        logger.info(f"   RECORD THIS HASH FOR REPRODUCIBILITY: {calc_hash}")

    # 4. Extract if needed
    if extract:
        extract_file(target_path, target_path.parent)

    return target_path