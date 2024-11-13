from enums.direction import Direction
from multiprocessing import Lock
from sqlalchemy.orm import Session
from models.dna_stat import DnaStat
from repositories.dna_stat_repository import DnaStatRepository

class MutantService:
    def __init__(self):
        self.pattern_found = 0
        self.lock = Lock()
        pass

    def is_mutant(self, dna: list[str], recursive: bool, session: Session) -> bool:
        if not dna:
            return False
        is_mutant = False
        if recursive:
            is_mutant = self._is_mutant_recursive(dna)
        else:
            is_mutant = self._is_mutant(dna)
        rows = len(dna)
        cols = len(dna[0])
        stat = DnaStat(dna="".join(dna), rows=rows, cols=cols, is_mutant=is_mutant)
        dna_stat_repository = DnaStatRepository(session)
        dna_stat_repository.add_stat(stat)
        return is_mutant

    def _is_mutant(self, dna: list[str]) -> bool:
        if not dna:
            return False
        
        n = len(dna)
        m = len(dna[0])

        # RIGHT
        for row in dna:
            for i in range(m - 3):
                if len(set(row[i:i + 4])) == 1 and self._mutant_check():
                    return True

        # DOWN
        for col in range(m):
            for row in range(n - 3):
                if len(set(dna[row + i][col] for i in range(4))) == 1 and self._mutant_check():
                    return True

        # DIAG_RIGHT
        for row in range(n - 3):
            for col in range(m - 3):
                if len(set(dna[row + i][col + i] for i in range(4))) == 1 and self._mutant_check():
                    return True
 
        # DIAG_LEFT
        for row in range(n - 3):
            for col in range(3, m):
                if len(set(dna[row + i][col - i] for i in range(4))) == 1 and self._mutant_check():
                    return True
        return False
    
    def _mutant_check(self):
        with self.lock:
            if self.pattern_found == 1:
                return True
            else:
                self.pattern_found += 1
                return False

    def _is_mutant_recursive(self, dna: list[str]) -> bool:
        if not dna:
            return False

        n = len(dna)
        m = len(dna[0])


        for row in range(n):
            for col in range(m):
                for direction in Direction:
                    if self._mutant_check_r(dna, row, col, direction, dna[row][col], 0):
                        return True

        return False

    def _mutant_check_r(self, dna: list[str], row: int, col: int, direction: Direction, char: str, count: int) -> bool:
        if count == 4:
            return self._mutant_check()
        
        if not (0 <= row < len(dna) and 0 <= col < len(dna[0])):
            return False

        if dna[row][col] == char:
            return self._mutant_check_r(
                dna, row + direction.row_step, col + direction.col_step, direction, char, count + 1
            )

        return False

    def get_stats(self, session: Session) -> DnaStatRepository:
        mutants_count, humans_count = DnaStatRepository(session).count_mutants_and_humans()
        if humans_count == 0:
            if mutants_count == 0:
                ratio = 0
            else:
                ratio = 1
        else:
            ratio = mutants_count / humans_count
        return {"count_mutant_dna": mutants_count, "count_human_dna": humans_count, "ratio": ratio}