from src import Result, DataBridgeAbs, ResultSet
import pandas as pd
from datetime import datetime as dt
import timeit as tm
import csv



class CsvDataBridge(DataBridgeAbs):
    """CSV persistence"""

    def __init__(self, folder_path="./data/"):
        self._game_results_file_path     = folder_path + "game_results.csv"
        self._game_results_file_handle   = None
        self._games_file_path            = folder_path + "games.csv"
        self._games_file_handle          = None
        self._outgoing_email_file_path   = folder_path + "emails_outgoing.csv"
        self._game_id                    = None

# ---------------------------------------------------------------------------------------------------------------------
    def saveResult(self, result: Result):
        """Appends Result data to CSV _games_file and _game_results_file"""
        start = tm.default_timer()
        game_id = self.getNewGameId()
        print(f"getID time:{tm.default_timer() - start}")
        self._writeGameHeaderInfo(result, game_id)
        #self._writeGameValueDetails(result, game_id)

        #df = result.game_table
        #df.to_csv(self._game_history_file, encoding="utf-8", mode="a", index=False, header=False)

    def saveResultSet(self, result_set: ResultSet):
        """Appends Results data to a CSV file. Can take one or more result parameters"""
        for result in result_set.results:
            self.saveResult(result)

    def getNewGameId(self):
        if self._game_id != None:
            self._game_id += 1
        else:           # using and else branch for logical clarity
            self._game_id = self._extractMaxIdDirectlyFromFile()
        return self._game_id

    def _extractMaxIdDirectlyFromFile(self):
        ids_list = []
        with open(self._games_file_path, 'r', encoding="utf-8", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for ix, row in enumerate(reader):
                if ix > 0 and len(row) > 0:
                    ids_list.append(int(row[0]))
        if len(ids_list) == 0:
            return 1
        ids_list.sort()
        return int(ids_list[-1]) + 1

    def _writeGameHeaderInfo(self, result: Result, id):
        game_id = id
        game_name = result.game_name
        unit = result.game_unit
        timestamp = result.game_time
        with open(self._games_file_path, 'a', encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerow([game_id, game_name, timestamp, unit])

    def _writeGameValueDetails(self, result: Result, id):
        game_id = id
        with open(self._game_results_file_path) as file:
            writer = csv.writer(file)
            for name, number in zip(result.names, result.numbers):
                writer.writerow([game_id, name, number])
# ---------------------------------------------------------------------------------------------------------------------
    def recordOutgoingEmail(self, *args):
        """Logs info about outgoing emails"""

        db_columns = ["Email_Id", "Timestamp", "Address_List"]
        new_email_id = self.getNewEmailId()
        email_tmstamp = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

        data_row = (new_email_id, email_tmstamp) + args
        df_to_save =  pd.DataFrame(data=[data_row])
        df_to_save.to_csv(self._outgoing_email_file_path, encoding="utf-8", mode="a", index=False, header=False)

    def getNewEmailId(self):
        """Not abstract as other concretes for DataBridge might implement some type of autoincrement
           Returns a new increment of the Email_Id Column"""
        email_ids_table = pd.read_csv(self._outgoing_email_file_path, usecols=["Email_Id"])
        last_id = email_ids_table["Email_Id"].max()

        return 1 if pd.isna(last_id) else last_id + 1

    def fetchAllHistory(self):
        pass