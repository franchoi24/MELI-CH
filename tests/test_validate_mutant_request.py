import pytest
from fastapi import HTTPException
from validators.validate_mutant_request import is_dna_valid  # Adjust the import according to where your is_dna_valid function is

def test_is_dna_valid_none():
    with pytest.raises(HTTPException) as exc_info:
        is_dna_valid(None)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "DNA matrix must not be null"

def test_is_dna_valid_invalid_length():
    dna = [
        "ATGC",
        "CAGT",
        "TTAC"
    ]
    with pytest.raises(HTTPException) as exc_info:
        is_dna_valid(dna)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Matrix must be square"

def test_is_dna_valid_non_square():
    dna = [
        "ATGC",
        "CAGT"
    ]
    with pytest.raises(HTTPException) as exc_info:
        is_dna_valid(dna)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Matrix must be square"

def test_is_dna_valid_non_uppercase():
    dna = [
        "ATGC",
        "Cagt",
        "TTAC",
        "GGTA"
    ]
    with pytest.raises(HTTPException) as exc_info:
        is_dna_valid(dna)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "All rows must be uppercase"

def test_is_dna_valid_invalid_characters():
    dna = [
        "ATGC",
        "CAGX",
        "TTAC",
        "GGTA"
    ]
    with pytest.raises(HTTPException) as exc_info:
        is_dna_valid(dna)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "All rows must contain only A, C, G, or T"

def test_is_dna_valid_valid_dna():
    dna = [
        "ATGC",
        "CAGT",
        "TTAC",
        "GGTA"
    ]
    is_dna_valid(dna)
