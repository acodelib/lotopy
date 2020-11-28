from src.GameAbs import GameAbs
from src.Result import Result
from src.ResultSet import ResultSet
from random import randint
import math
import timeit


class GameJoker(GameAbs):
    MAX_PER_UNIT = 45
    MIN_PER_UNIT = 5
    GAME_NAME = "LotoJoker"

    def __init__(self):

        self._session_numbers     = []
        self._session_jokers      = []
        self._session_units       = []

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def drawNumbers(self, numbers_count):
        self._session_numbers.clear()
        self._session_jokers.clear()

        for _ in range(0, numbers_count):
            n = randint(1, GameJoker.MAX_PER_UNIT)
            while n in self._session_numbers:
                n = randint(1, GameJoker.MAX_PER_UNIT)
            self._session_numbers.append(n)

        for _ in range(0, math.ceil(numbers_count / 5)):
            j = randint(1, 20) # hardcoded, but not much portability between game types...
            while j in self._session_jokers:
                j = randint(1, 20)
            self._session_jokers.append(j)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playSingleGameUnit(self) -> Result:
        """Plays 1 line with 1 joker"""

        new_result = Result(GameJoker.GAME_NAME, "Line-1")
        self.drawNumbers(GameJoker.MIN_PER_UNIT)
        self._session_numbers.sort()
        for i, n in enumerate(self._session_numbers):
            new_result.addNumber(f"N-{i+1}", n)
        new_result.addNumber("J", self._session_jokers[0])

        return new_result
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playMaxGameUnits(self) -> ResultSet:
        """Plays full 9 lines with 9 jokers"""

        self.drawNumbers(GameJoker.MAX_PER_UNIT)
        start_of_unit  = 0
        end_of_unit    = GameJoker.MIN_PER_UNIT
        joker_count    = 0
        new_result_set = ResultSet()

        while start_of_unit < len(self._session_numbers) - 1:
            line_no = int(start_of_unit / GameJoker.MIN_PER_UNIT + 1)
            unit = self._session_numbers[start_of_unit:end_of_unit]
            unit.sort()
            self._session_units.append(unit)
            game_unit = f"Line-{line_no}"
            new_result = Result(GameJoker.GAME_NAME, game_unit)
            for position, number in enumerate(unit):
                new_result.addNumber(f"N-{position + 1}", number)
            new_result.addNumber(f"J", self._session_jokers[joker_count])
            start_of_unit = end_of_unit
            end_of_unit = end_of_unit + GameJoker.MIN_PER_UNIT
            joker_count = joker_count + 1
            new_result_set.addResult(new_result)

        return new_result_set
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def getRawResult(self):
        return self._session_numbers

    def printRawGame(self):
        for it, unit in enumerate(self._session_units):
            print(unit)
        print(self._session_jokers)


if __name__ == "__main__":
    start_tm = timeit.default_timer()

    joker = GameJoker()
    r = joker.playSingleGameUnit()
    print(r)
    rs = joker.playMaxGameUnits()
    print(rs)


    print(timeit.default_timer() - start_tm)