from abc import ABCMeta, abstractmethod, ABC
from src import Result, ResultSet


def abstracmethod():
    pass


class DataBridgeAbs(ABC):
    """Responsible for IO operations on persistent Game Data"""
    def __init__(self, folder_path):
        pass

    @abstractmethod
    def saveResult(self, result: Result):
        pass

    @abstractmethod
    def saveResultSet(self, result_set: ResultSet):
        pass

    @abstractmethod
    def fetchAllHistory(self, ) -> Result:
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

