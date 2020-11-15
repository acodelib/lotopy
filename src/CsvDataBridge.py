from src import Result, DataBridgeAbs
import pandas as pd
from datetime import datetime as dt


class CsvDataBridge(DataBridgeAbs):
    """CSV persistence"""

    def __init__(self, folder_path="./data/"):
        self._game_history_file = folder_path + "game_history.csv"
        self._outgoing_email = folder_path + "emails_outgoing.csv"

    def saveResultUnit(self, result: Result):
        """Appends Result data to a CSV file"""
        df = result.game_table
        df.to_csv(self._game_history_file, encoding="utf-8", mode="a", index=False, header=False)

    def saveResults(self, *args):
        """Appends Results data to a CSV file. Can take one or more result parameters"""
        for result in args:
            self.saveResultUnit(result)

    def fetchAllHistory(self):
        pass

    def recordOutgoingEmail(self, *args):
        """Logs info about outgoing emails"""

        db_columns = ["Email_Id", "Timestamp", "Address_List"]
        new_email_id = self.getNewEmailId()
        email_tmstamp = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

        data_row = (new_email_id, email_tmstamp) + args
        df_to_save =  pd.DataFrame(data=[data_row])
        df_to_save.to_csv(self._outgoing_email, encoding="utf-8", mode="a", index=False, header=False)

    def getNewEmailId(self):
        """Not abstract as other concretes for DataBridge might implement some type of autoincrement
           Returns a new increment of the Email_Id Column"""
        email_ids_table = pd.read_csv(self._outgoing_email, usecols=["Email_Id"])
        last_id = email_ids_table["Email_Id"].max()

        return 1 if pd.isna(last_id) else last_id + 1

    def getNewGameId(self):
        pass