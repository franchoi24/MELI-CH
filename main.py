
from models.dna_request import DnaRequest
from services.mutant_service import MutantService
from services.database import get_session, create_db_and_tables
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from contextlib import asynccontextmanager
from validators.validate_mutant_request import is_dna_valid

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]



@app.on_event("startup")
def on_startup():
    create_db_and_tables()
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/mutant")
async def check_mutant(dna_request: DnaRequest, session: SessionDep):
    dna = dna_request.dna
    recursive = dna_request.recursive
    is_dna_valid(dna)
    mutant_service = MutantService()
    is_mutant = mutant_service.is_mutant(dna, recursive, session)
    if not is_mutant:
        raise HTTPException(status_code=403, detail="Not a mutant")
    return {"is_mutant": is_mutant}

@app.get("/stats")
async def get_stats(session: SessionDep):
    mutant_service = MutantService()
    stats = mutant_service.get_stats(session)
    return stats