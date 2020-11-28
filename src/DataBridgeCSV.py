from src import Result, DataBridgeAbs, ResultSet, DataConnectorCSV
import pandas as pd
from datetime import datetime as dt
import timeit as tm
import csv



class DataBridgeCSV(DataBridgeAbs):
    """CSV persistence"""

    def __init__(self, use_external_data_connector=None):
        self._connector = DataConnectorCSV() if use_external_data_connector is None else use_external_data_connector
        self._game_id            = None
        self._games_handle       = None
        self._game_result_handle = None
# ---------------------------------------------------------------------------------------------------------------------
    def saveResult(self, result: Result):
        """Appends Result data to CSV _games_file and _game_results_file"""

        game_id = self.getNewGameId()
        close_the_handle_flag = False
        if self._games_handle is None:
            self._games_handle = self._connector.getAppendDataHandle(DataConnectorCSV.GAMES)
            self._game_result_handle = self._connector.getAppendDataHandle(DataConnectorCSV.GAME_RESULTS)
            close_the_handle_flag = True

        self._writeGameHeaderInfo(result, game_id)
        self._writeGameValueDetails(result, game_id)

        if close_the_handle_flag:
            self._connector.closeAllOpenHandles()

    def saveResultSet(self, result_set: ResultSet):
        self._games_handle = self._connector.getAppendDataHandle(DataConnectorCSV.GAMES)
        self._game_result_handle = self._connector.getAppendDataHandle(DataConnectorCSV.GAME_RESULTS)
        for result in result_set.results:
            self.saveResult(result)
        self._connector.closeAllOpenHandles()

    def getNewGameId(self):
        if self._game_id is not None:
            self._game_id += 1
        else:           # using and else branch for logical clarity
            self._game_id = self._extractMaxIdDirectlyFromConnector()
        return self._game_id

    def _writeGameHeaderInfo(self, result: Result, id):
        game_id = id
        game_name = result.game_name
        unit = result.game_unit
        timestamp = result.game_time
        writer = csv.writer(self._games_handle, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([game_id, game_name, timestamp, unit])

    def _writeGameValueDetails(self, result: Result, id):
        game_id = id
        writer = csv.writer(self._game_result_handle, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        for name, number in zip(result.names, result.numbers):
            writer.writerow([game_id, name, number])

    def _extractMaxIdDirectlyFromConnector(self):
        ids_list = []
        file = self._connector.getReadDataHandle(DataConnectorCSV.GAMES)
        reader = csv.reader(file, delimiter=",")
        for ix, row in enumerate(reader):
            if ix > 0 and len(row) > 0:
                ids_list.append(int(row[0]))
        self._connector.closeHandle(file)
        if len(ids_list) == 0:
            return 1
        ids_list.sort()
        return int(ids_list[-1]) + 1
# ---------------------------------------------------------------------------------------------------------------------
    def recordOutgoingEmail(self, *args):
        """Logs info about outgoing emails"""

        db_columns = ["Email_Id", "Timestamp", "Address_List"]
        new_email_id = self.getNewEmailId()
        email_tmstamp = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

        file = self._connector.getAppendDataHandle(DataConnectorCSV.OUTGOING_EMAIL)
        writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([new_email_id, email_tmstamp] + list(args))
        self._connector.closeHandle(file)
        """
        data_row = (new_email_id, email_tmstamp) + args
        df_to_save =  pd.DataFrame(data=[data_row])
        df_to_save.to_csv(self._outgoing_email_file_path, encoding="utf-8", mode="a", index=False, header=False)
        """

    def getNewEmailId(self):
        """Not abstract as other concretes for DataBridge might implement some type of autoincrement
           Returns a new increment of the Email_Id Column"""
        ids_list = []
        file = self._connector.getReadDataHandle(DataConnectorCSV.OUTGOING_EMAIL)
        reader = csv.reader(file, delimiter=",")
        for ix, row in enumerate(reader):
            if ix > 0 and len(row) > 0:
                ids_list.append(int(row[0]))
        self._connector.closeHandle(file)
        if len(ids_list) == 0:
            return 1
        ids_list.sort()
        return int(ids_list[-1]) + 1

    def fetchAllHistory(self):
        pass