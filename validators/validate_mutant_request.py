from fastapi import HTTPException

def is_dna_valid(dna):
    if dna is None:
        raise HTTPException(status_code=400, detail="DNA matrix must not be null")
    if not all(len(row) == len(dna[0]) for row in dna):
        raise HTTPException(status_code=400, detail="All rows must be the same length")
    if not all(row.isupper() for row in dna):
        raise HTTPException(status_code=400, detail="All rows must be uppercase")
    if not all(all(char in "ACGT" for char in row) for row in dna):
        raise HTTPException(status_code=400, detail="All rows must contain only A, C, G, or T")
    if not len(dna) == len(dna[0]):
        raise HTTPException(status_code=400, detail="Matrix must be square")