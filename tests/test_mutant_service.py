import unittest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from services.mutant_service import MutantService
from models.dna_stat import DnaStat
from repositories.dna_stat_repository import DnaStatRepository
from enums.direction import Direction

class TestMutantService(unittest.TestCase):
    def setUp(self):
        self.service = MutantService()
        self.mock_session = MagicMock(spec=Session)
        self.mock_repo = MagicMock(spec=DnaStatRepository)
    
    @patch('services.mutant_service.DnaStatRepository')
    def test_is_mutant_with_recursive(self, MockRepo):
        MockRepo.return_value = self.mock_repo
        dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        self.mock_repo.add_stat = MagicMock()

        with patch.object(self.service, '_is_mutant_recursive', return_value=True):
            result = self.service.is_mutant(dna, recursive=True, session=self.mock_session)
            self.assertTrue(result)
            self.mock_repo.add_stat.assert_called_once()
    
    @patch('services.mutant_service.DnaStatRepository')
    def test_is_mutant_without_recursive(self, MockRepo):
        MockRepo.return_value = self.mock_repo
        dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        self.mock_repo.add_stat = MagicMock()
        
        # Test non-recursive version
        with patch.object(self.service, '_is_mutant', return_value=True):
            result = self.service.is_mutant(dna, recursive=False, session=self.mock_session)
            self.assertTrue(result)
            self.mock_repo.add_stat.assert_called_once()
    
    def test_is_mutant_iterative(self):
        dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        result = self.service._is_mutant(dna)
        self.assertTrue(result)
    
    def test_is_mutant_recursive(self):
        dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        result = self.service._is_mutant_recursive(dna)
        self.assertTrue(result)

    def test_is_mutant_iterative_false(self):
        dna = ["ATGCGA", "CTGTGC", "TTATGT", "AGAATG", "CCCCTA", "TCACTG"]
        result = self.service._is_mutant(dna)
        self.assertFalse(result)
    
    def test_is_mutant_recursive_false(self):
        dna = ["ATGCGA", "CTGTGC", "TTATGT", "AGAATG", "CCCCTA", "TCACTG"]
        result = self.service._is_mutant_recursive(dna)
        self.assertFalse(result)
    
    def test_is_mutant_empty_dna(self):
        result = self.service.is_mutant([], recursive=False, session=self.mock_session)
        self.assertFalse(result)

    def test_check_right(self):
        dna = ["AAAA", "TTTT", "CCCC", "GGGG"]
        result = self.service._check_right(dna, len(dna), len(dna[0]))
        self.assertTrue(result)

    def test_check_right_false(self):
        dna = ["AAAA", "DCDC", "DCDC", "DCDC"]
        result = self.service._check_right(dna, len(dna), len(dna[0]))
        self.assertFalse(result)

    def test_check_down(self):
        dna = ["ATGC", "ATGC", "ATGC", "ATGC"]
        result = self.service._check_down(dna, len(dna), len(dna[0]))
        self.assertTrue(result)

    def test_check_down_false(self):
        dna = ["ATGC", "AGTA", "ATGC", "ATGC"]
        result = self.service._check_down(dna, len(dna), len(dna[0]))
        self.assertFalse(result)
    
    def test_check_diag_right(self):
        dna = ["ATGCT", "CATTT", "TTATT", "AGAAT", "AGAAT"]
        result = self.service._check_diag_right(dna, len(dna), len(dna[0]))
        self.assertTrue(result)

    def test_check_diag_right_false(self):
        dna = ["ATGCT", "CAGTT", "TTATT", "AGAAT", "AGAAT"]
        result = self.service._check_diag_right(dna, len(dna), len(dna[0]))
        self.assertFalse(result)
    
    
    def test_check_diag_left(self):
        dna = ["TGCAC", "AGACC", "TACCC", "ACCCC", "ACCCC"]
        result = self.service._check_diag_left(dna, len(dna), len(dna[0]))
        self.assertTrue(result)

    def test_check_diag_false(self):
        dna = ["TGCAC", "AGACC", "TACCC", "ACCCT", "ACCCC"]
        result = self.service._check_diag_left(dna, len(dna), len(dna[0]))
        self.assertTrue(result)

    def test_get_stats(self):
        with patch.object(DnaStatRepository, 'count_mutants_and_humans', return_value=(10, 5)):
            result = self.service.get_stats(self.mock_session)
            self.assertEqual(result['count_mutant_dna'], 10)
            self.assertEqual(result['count_human_dna'], 5)
            self.assertEqual(result['ratio'], 2.0)
    
    def test_get_stats_zero_stats(self):
        with patch.object(DnaStatRepository, 'count_mutants_and_humans', return_value=(0, 0)):
            result = self.service.get_stats(self.mock_session)
            self.assertEqual(result['count_mutant_dna'], 0)
            self.assertEqual(result['count_human_dna'], 0)
            self.assertEqual(result['ratio'], 0)

    def test_get_stats_zero_humans(self):
        with patch.object(DnaStatRepository, 'count_mutants_and_humans', return_value=(1, 0)):
            result = self.service.get_stats(self.mock_session)
            self.assertEqual(result['count_mutant_dna'], 1)
            self.assertEqual(result['count_human_dna'], 0)
            self.assertEqual(result['ratio'], 1)

if __name__ == '__main__':
    unittest.main()
