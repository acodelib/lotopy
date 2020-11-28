import timeit as tm

class DataConnectorCSV():
    """Delegates file open/close operations. Meant to make the system more tastable"""

    GAMES = 1
    GAME_RESULTS = 2
    OUTGOING_EMAIL = 3

    def __init__(self, folder_path="./data/"):
        self._game_results_file_path    = folder_path + "game_results.csv"
        self._games_file_path           = folder_path + "games.csv"
        self._outgoing_email_file_path  = folder_path + "emails_outgoing.csv"

        self._opened_handles = []

    def getReadDataHandle(self, what_object_option: int):
        return self._openObjectByOptionAndMode(what_object_option, 'r')

    def getWriteDataHandle(self, what_object_option: int):
        return self._openObjectByOptionAndMode(what_object_option, 'w')

    def getAppendDataHandle(self, what_object_option: int):
        return self._openObjectByOptionAndMode(what_object_option, 'a')

    def _openObjectByOptionAndMode(self, object_option, open_mode):
        if object_option == DataConnectorCSV.GAMES:
            new_handle = open(self._games_file_path, open_mode, encoding="utf-8", newline="")
        elif object_option == DataConnectorCSV.GAME_RESULTS:
            new_handle = open(self._game_results_file_path, open_mode, encoding="utf-8", newline="")
        elif object_option == DataConnectorCSV.OUTGOING_EMAIL:
            new_handle = open(self._outgoing_email_file_path, open_mode, encoding="utf-8", newline="")
        else:
            raise NotImplementedError("Choose only static OPTIONS available in DataConnectorCSV")

        self._opened_handles.append(new_handle)
        return new_handle

    def closeHandle(self, handle):
        handle.close()
        self._opened_handles.remove(handle)

    def closeAllOpenHandles(self):
        for handle in self._opened_handles:
            handle.close()
        self._opened_handles.clear()