from abc import ABCMeta, abstractmethod, ABC
from src import GameResult, GameResultSet


def abstracmethod():
    pass


class DataBridgeAbs(ABC):
    """Responsible for IO operations on persistent Game Data"""
    def __init__(self, folder_path):
        pass

    @abstractmethod
    def saveResult(self, result: GameResult):
        pass

    @abstractmethod
    def saveResultSet(self, result_set: GameResultSet):
        pass

    @abstractmethod
    def fetchAllHistory(self, ) -> GameResult:
        pass

    @abstractmethod
    def getNewEmailId(self):
        pass

    @abstractmethod
    def recordOutgoingEmail(self, *args):
        pass

    @abstractmethod
    def getNewGameId(self):
        pass

