from sqlmodel import Session, select
from typing import List
from models.dna_stat import DnaStat

class DnaStatRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stats(self) -> List[DnaStat]:
        """Fetch all DNA stats from the database."""
        statement = select(DnaStat)
        results = self.session.exec(statement)
        return results.all()

    def count_mutants_and_humans(self):
        """Count the number of mutants and humans."""
        mutants_count = self.session.exec(select(DnaStat).where(DnaStat.is_mutant == True)).all()
        humans_count = self.session.exec(select(DnaStat).where(DnaStat.is_mutant == False)).all()

        return len(mutants_count), len(humans_count)
    
    def add_stat(self, stat: DnaStat):
        self.session.add(stat)
        self.session.commit()