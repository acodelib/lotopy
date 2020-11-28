from src.GameAbs import GameAbs
from src.Result import Result
from src.ResultSet import ResultSet
from random import randint
import timeit


class Game649(GameAbs):
    """Concrete implementation in the form of a Lotot 6/49 game play"""
    MAX_PER_UNIT = 49
    MIN_PER_UNIT = 6
    GAME_NAME = "Loto649"

    def __init__(self):
        self._session_numbers = []
        self._session_units = []
        self._residual_number = 0

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    def drawNumbers(self, numbers_count):
        self._session_numbers.clear()

        for _ in range(0, numbers_count):
            n = randint(1, Game649.MAX_PER_UNIT)
            while n in self._session_numbers:
                n = randint(1, Game649.MAX_PER_UNIT)
            self._session_numbers.append(n)

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playSingleGameUnit(self) -> Result:
        """One line of 6 out of 49"""

        new_result = Result(Game649.GAME_NAME, "Line-1")
        self.drawNumbers(Game649.MIN_PER_UNIT)
        self._session_numbers.sort()
        for i, n in enumerate(self._session_numbers):
            new_result.addNumber(f"N-{i+1}", n)
        return new_result

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playMaxGameUnits(self) -> ResultSet:
        """Plays full 8 lines. This is 48 numbers. Number 49 will be regarded as residual"""

        self.drawNumbers(Game649.MAX_PER_UNIT)
        start_of_unit = 0
        end_of_unit = Game649.MIN_PER_UNIT
        new_result_set = ResultSet()

        while start_of_unit < len(self._session_numbers) - 1:
            unit = self._session_numbers[start_of_unit:end_of_unit]
            unit.sort()
            self._session_units.append(unit)
            game_unit = f"Line-{int(start_of_unit / Game649.MIN_PER_UNIT + 1)}"
            new_result = Result(Game649.GAME_NAME, game_unit)
            for position, number in enumerate(unit):
                new_result.addNumber(f"N-{position + 1}", number)
            start_of_unit = end_of_unit
            end_of_unit = end_of_unit + Game649.MIN_PER_UNIT
            new_result_set.addResult(new_result)
        new_result_set.residual = self._session_numbers[-1]

        return new_result_set

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    def getRawResult(self):
        return self._session_numbers

    def printRawGame(self):
        for unit in self._session_units:
            print(unit)
        print(f"residual number: {self._session_numbers[-1]}")


if __name__ == "__main__":
    start_tm = timeit.default_timer()

    loto649 = Game649()
    r = loto649.playSingleGameUnit()
    print(r)
    rs = loto649.playMaxGameUnits()

    print(rs)
    print(timeit.default_timer() - start_tm)
