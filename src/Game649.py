from src.GameAbs import GameAbs
from src.Result import Result
from random import randint
import timeit

class Game649(GameAbs):
    """Concrete implementation in the form of a Lotot 6/49 game play"""
    MAX_PER_UNIT = 49
    MIN_PER_UNIT = 6
    GAME_NAME = "Loto649"

    def __init__(self):
        self.__last_result = Result(self)
        self.__session_numbers = []
        self.__session_units = []
        self.__residual_number = 0

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def drawNumbers(self, numbers_count):
        self.__session_numbers.clear()

        for _ in range(0, numbers_count):
            n = randint(1, Game649.MAX_PER_UNIT)
            while n in self.__session_numbers:
                n = randint(1, Game649.MAX_PER_UNIT)
            self.__session_numbers.append(n)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playSingleGameUnit(self):
        """One line of 6 out of 49"""
        game_unit = "Line 1"
        self.__last_result = Result(self)  # looks like this is the best way to empty
        self.drawNumbers(Game649.MIN_PER_UNIT)
        self.__session_numbers.sort()
        for i, n in enumerate(self.__session_numbers):
            self.__last_result.appendNumber(n, f"P{i}", game_unit)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def playMaxNaturalSize(self):
        """Plays full 8 lines. This is 48 numbers. Number 49 will be regarded as rezidual"""

        self.drawNumbers(Game649.MAX_PER_UNIT)
        self.__last_result = Result(self)  # looks like this is the best way to empty
        start_of_unit = 0
        end_of_unit = Game649.MIN_PER_UNIT

        while start_of_unit < len(self.__session_numbers) - 1:
            unit = self.__session_numbers[start_of_unit:end_of_unit]
            unit.sort()
            self.__session_units.append(unit)
            for position, number in enumerate(unit):
                self.__last_result.appendNumber(number, f"N-{position + 1}", f"Line-{int(start_of_unit / Game649.MIN_PER_UNIT + 1)}")
            start_of_unit = end_of_unit
            end_of_unit = end_of_unit + Game649.MIN_PER_UNIT
        self.__last_result.residual = self.__session_numbers[-1]

        return self.__last_result
# ----------------------------------------------------------------------------------------------------------------------------------------------------
    def getRawResult(self):
        return self.__session_numbers

    def printRawGame(self):
        for unit in self.__session_units:
            print(unit)
        print(f"residual number: {self.__residual_number}")

if __name__ == "__main__":
    start_tm = timeit.default_timer()

    loto649 = Game649()
    loto649.playMaxNaturalSize()
    loto649.printRawGame()

    print(timeit.default_timer() - start_tm)
