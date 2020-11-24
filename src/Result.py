import pandas as pd
import numpy as np
from src import ResultAbs
from datetime import datetime as dt


class Result():
    """ POCO of a game result (numbers draw).
        Responsability: formalises result structure."""

    def __init__(self, game_name, game_unit):
        self.game_name = game_name
        self.game_unit = game_unit
        self.game_time = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        self.numbers   = []
        self.names     = []

    def addNumber(self, name, value):
        self.numbers.append(value)
        self.names.append(name)

# -------------------------------------------------------------------------------------------------------------------
    def getHtmlPrint(self):
        printer = f"<p>Game Name: {self.game_name} , Play Time: {self.game_time}, Results:</p><br>\n"
        printer = printer + '<table style="border-collapse: collapse;" >\n'

        printer = printer + "<tr>\n"
        for name in self.names:
            printer = printer + f" <th>{name}</th>\n"
        printer = printer + "</tr>\n<tr>\n"
        for number in self.numbers:
            printer = printer + f" <td>{number}</td>\n"
        printer = printer + "</tr>\n"
        printer = printer + "</table>\n<br>"

        return printer
# ---------------------------------------private --------------------------------------------------------------------
    def __str__(self):
        printer_string = f"Game Name: {self.game_name} , Play Time: {self.game_time}, Results:"

        col_width = self._getMaxColumnWidth()
        line = ""
        for row in self._print_elements:
            row = "".join(str(value).ljust(col_width + 5) for value in row)
            line = line + "\n" + row
        return printer_string + line

    def _getMaxColumnWidth(self):
        cell_lengths = []
        for values_list in self._print_elements:
            for element in values_list:
                if type(element) == str:
                    cell_lengths.append(len(element))
        return max(cell_lengths)

    @property
    def _print_elements(self):
        return [self.names, self.numbers]


if __name__ == '__main__':
    rs = Result("Loto649", "Line-1")
    rs.addNumber("N1", 19)
    rs.addNumber("N2", 44)
    rs.addNumber("N3", 32)
    rs.addNumber("N4", 16)
    rs.addNumber("N5", 17)
    rs.addNumber("N6", 1)
    print(rs)
    print(rs.getHtmlPrint())
