import unittest
from src.Game649 import Game649
from src.GameResult import GameResult
from src.WinningsDetector import WinningsDetector


class TestGames(unittest.TestCase):

# ------------------------------------------------ FIXTURES -----------------------------------------------------------
    def make649Result(self, numbers: list):
        numbers_names = ["N-1", "N-2", "N-3", "N-4", "N-5", "N-6"]
        return self._getResultFixture("Game649", numbers_names, numbers)

    def makeJokerResult(self, numbers: list):
        numbers_names = ["N-1", "N-2", "N-3", "N-4", "N-5", "J"]
        return self._getResultFixture("Game649", numbers_names, numbers)

    def _getResultFixture(self, game_type: str, names: list, numbers: list) -> GameResult:
        result = GameResult(game_type, "Line-1")
        for ix, name in enumerate(names):
            result.addNumber(name, numbers[ix])
        return result

# ---------------------------------------------------------------------------------------------------------------------
    def test_WiningsRead_gamesAreOfSameType_True(self):
        expected = True
        game_1 = self.make649Result([22, 1, 2, 3, 4, 5])
        game_2 = self.make649Result([22, 1, 2, 3, 4, 5])
        wr = WinningsDetector(game_1, game_2)
        self.assertEqual(expected, wr.isSameTypeOfResults())

    def test_WiningsRead_gamesAreOfSameType_False(self):
        game_1 = self.make649Result([22, 1, 2, 3, 4, 5])
        game_2 = self.makeJokerResult([22, 1, 2, 3, 4, 5])
        p = WinningsDetector(game_1, game_2)
        self.assertRaises(TypeError, p.isSameTypeOfResults())

    def test_makeDict_649(self):
        game_1 = self.make649Result([22, 1, 2, 3, 4, 5])
        game_2 = self.makeJokerResult([22, 1, 2, 3, 4, 5])
        expected_1 = {"N-1": 22, "N-2": 1, "N-3": 2, "N-4": 3, "N-5": 4, "N-6": 5}
        p = WinningsDetector(game_1, game_2)
        self.assertEqual(expected_1, p.makeDictOutOfNameAndValue(game_1))

    def test_makeDict_Joker(self):
        game_1 = self.make649Result([22, 1, 2, 3, 4, 5])
        game_2 = self.makeJokerResult([22, 1, 2, 3, 4, 5])
        expected_1 = {"N-1": 22, "N-2": 1, "N-3": 2, "N-4": 3, "N-5": 4, "J": 5}
        p = WinningsDetector(game_1, game_2)
        self.assertEqual(expected_1, p.makeDictOutOfNameAndValue(game_2))

    def test_getComparison_loss649(self):
        game_1 = self.make649Result([1, 19, 44, 3, 4, 5])
        game_2 = self.make649Result([12, 9, 32, 6, 10, 15])
        p = WinningsDetector(game_1, game_2)
        expected = None
        self.assertEqual(expected, p.getWinning())

    def test_getComparison_3Numbers649(self):
        game_1 = self.make649Result([1, 19, 44, 3, 4, 5])
        game_2 = self.make649Result([12, 44, 32, 5, 10, 4])
        p = WinningsDetector(game_1, game_2)
        expected ="N-3 = N-2 = 44\nN-5 = N-6 = 4\nN-6 = N-4 = 5\n"
        self.assertEqual(expected, p.getWinning())

    def test_getComparison_loss2Numbers649(self):
        game_1 = self.make649Result([1, 19, 44, 3, 4, 5])
        game_2 = self.make649Result([12, 44, 32, 5, 10, 14])
        p = WinningsDetector(game_1, game_2)
        expected = None
        self.assertEqual(expected, p.getWinning())

    def test_getComparison_lossJoker(self):
        game_1 = self.makeJokerResult([1, 19, 44, 3, 4, 5])
        game_2 = self.makeJokerResult([12, 9, 32, 6, 10, 15])
        p = WinningsDetector(game_1, game_2)
        expected = None
        self.assertEqual(expected, p.getWinning())

    def test_getComparison_Jand3noJoker(self):
        game_1 = self.makeJokerResult([1, 19, 44, 8, 5, 6])
        game_2 = self.makeJokerResult([11, 44, 32, 8, 5, 6])
        p = WinningsDetector(game_1, game_2)
        expected = "N-3 = N-2 = 44\nN-4 = N-4 = 8\nN-5 = N-5 = 5\nJ = J = 6\n"
        self.assertEqual(expected, p.getWinning())

    def test_getComparison_onJJoker(self):
        game_1 = self.makeJokerResult([1, 19, 44, 8, 5, 6])
        game_2 = self.makeJokerResult([11, 16, 32, 28, 15, 6])
        p = WinningsDetector(game_1, game_2)
        expected = None
        self.assertEqual(expected, p.getWinning())