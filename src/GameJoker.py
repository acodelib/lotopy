from src.GameAbs import GameAbs
from src.Result import Result
from random import randint
import math
import timeit


class GameJoker(GameAbs):
    MAX_PER_UNIT = 45
    MIN_PER_UNIT = 5
    GAME_NAME = "LotoJoker"

    def __init__(self):
        self.__last_result         = Result(self)
        self.__session_numbers     = []
        self.__session_jokers      = []
        self.__session_units       = []

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def drawNumbers(self, numbers_count):
        self.__session_numbers.clear()
        self.__session_jokers.clear()

        for _ in range(0, numbers_count):
            n = randint(1, GameJoker.MAX_PER_UNIT)
            while n in self.__session_numbers:
                n = randint(1, GameJoker.MAX_PER_UNIT)
            self.__session_numbers.append(n)

        for _ in range(0, math.ceil(numbers_count / 5)):
            j = randint(1, 20) # hardcoded, but not much portability between game types...
            while j in self.__session_jokers:
                j = randint(1, 20)
            self.__session_jokers.append(j)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playSingleGameUnit(self):
        """Plays 1 line with 1 joker"""

        game_unit = "Line 1"
        self.__last_result = Result(self)  # looks like this is the best way to empty
        self.drawNumbers(GameJoker.MIN_PER_UNIT)
        self.__session_numbers.sort()
        for i, n in enumerate(self.__session_numbers):
            self.__last_result.appendNumber(n, f"P{i}", game_unit)
        self.__last_result.appendNumber(self.__session_jokers, "J", game_unit)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playMaxNaturalSize(self):
        """Plays full 9 lines with 9 jokers"""

        self.drawNumbers(GameJoker.MAX_PER_UNIT)
        self.__last_result  = Result(self)  # looks like this is the best way to empty
        start_of_unit               = 0
        end_of_unit                 = GameJoker.MIN_PER_UNIT
        joker_count         = 0

        while start_of_unit < len(self.__session_numbers) - 1:
            line_no = int(start_of_unit / GameJoker.MIN_PER_UNIT + 1)
            unit = self.__session_numbers[start_of_unit:end_of_unit]
            unit.sort()
            self.__session_units.append(unit)
            for position, number in enumerate(unit):
                self.__last_result.appendNumber(number, f"N-{position + 1}", f"Line-{line_no}")
            self.__last_result.appendNumber(self.__session_jokers[joker_count], f"J", f"Line-{line_no}")
            start_of_unit = end_of_unit
            end_of_unit = end_of_unit + GameJoker.MIN_PER_UNIT
            joker_count = joker_count + 1

        return self.__last_result
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def getRawResult(self):
        return self.__session_numbers

    def printRawGame(self):
        for it, unit in enumerate(self.__session_units):
            print(unit)
        print(self.__session_jokers)


if __name__ == "__main__":
    start_tm = timeit.default_timer()

    joker = GameJoker()
    r = joker.playMaxNaturalSize()
    #joker.printRawGame()
    r.printMe()
    df = r.game_table
    df.to_csv("./games_history.csv", header=True, encoding="utf-8", mode="w", index=False,)
    print(timeit.default_timer() - start_tm)