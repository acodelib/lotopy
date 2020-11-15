from abc import abstractmethod, ABC
from src.GameAbs import GameAbs


class ResultAbs(ABC):
    """ Abstraction of the result of a Loto Game result"""

    def __init__(self, game):
        self.game = GameAbs()
        self.game = game
        self.__numbers = {}

    @abstractmethod
    def addNumber(self, number, name, group_name):
        pass

    @abstractmethod
    def printResults(self):
        pass
