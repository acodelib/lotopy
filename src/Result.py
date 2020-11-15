import pandas as pd
import numpy as np
from src import GameAbs
from datetime import datetime as dt
from tabulate import tabulate


class Result():
    """ Encapsulation of 1 and only 1 game type result. Used to formalise result structure.
        To be consumed by storage objects"""

    def __init__(self, the_game: GameAbs):
        self.__the_game = the_game
        self.__game_name = the_game.GAME_NAME
        self.__game_columns = ['Game_Name', 'Timestamp', 'Unit', 'Name', 'Value']
        self.__game_table = pd.DataFrame(columns=self.__game_columns)
        self.__game_time = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        self.__residual = None

    @property
    def game_table(self):
        return self.__game_table

    @game_table.setter
    def game_table(self):
        raise PermissionError("Not intended for write access")

    @property
    def residual(self):
        return self.__residual

    @residual.setter
    def residual(self, value):
        self.__residual = value

    def appendNumber(self, number, number_name, game_unit_name):
        new_line = {'Game_Name': self.__game_name, 'Timestamp': self.__game_time,
                    'Unit': game_unit_name, 'Name': number_name, 'Value': number
                    }
        self.__game_table = self.__game_table.append(new_line, ignore_index=True)

    def getDataSet(self):
        pass

    def __str__(self):
        """Human readable output. Does that by pivoting the result table"""

        printer_string = ""
        names = self.__game_table["Name"].unique()
        units = self.__game_table["Unit"].unique()
        lines_list = []
        for unit in units:
            sr = self.__game_table.loc[self.__game_table["Unit"] == unit, "Value"]
            lines_list.append(sr.tolist())
        lines_df = pd.DataFrame(lines_list, columns=names)
        printer_string = printer_string + lines_df.__str__()
        printer_string = printer_string  + f"\n----------- Residual value: {self.residual}" if self.residual is not None else printer_string

        return printer_string