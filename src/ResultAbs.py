from abc import abstractmethod, ABC


class ResultAbs(ABC):
    """ Abstraction of the result of a Loto Game result"""

    @abstractmethod
    def addNumber(self, name, value):
        pass
