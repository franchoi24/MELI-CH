
from sqlmodel import Field, SQLModel


class DnaStat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dna: str = Field(index=True)
    rows: int
    cols: int
    is_mutant: bool


