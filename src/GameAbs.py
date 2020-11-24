from abc import ABCMeta, abstractmethod, ABC
from random import randint


class GameAbs(ABC):
    """ Abstract representation of a game session. Meant to be implemeted for each type of Loto Game"""

    @abstractmethod
    def drawNumbers(self, numbers_count):
        """Generates numbers with single occurrence in the session
                   Keeps results in internal list"""
        pass

    @abstractmethod
    def playSingleGameUnit(self):
        """ plays smallest possible unit of a game. Ex: loto 6/49: 6 numbers out of 1..49
            returns Result type
        """
        pass

    @abstractmethod
    def playMaxNaturalSize(self):
        pass

    @abstractmethod
    def getRawResult(self):
        pass
