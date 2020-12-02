from src.Result import GameResult

class ResultSet():
    """Holds multiple results"""

    def __init__(self):
        self.results = []
        self.game_name = ""
        self.game_time = ""
        self._column_names = ['Unit Name']
        self.residual = 0

    def addResult(self, result: GameResult):
        self._setResultSetType(result)
        self._makeSureOnlyOneTypeOfGame(result)
        self.results.append(result)

# --------------------------------------------------------------------------------------------------------------------
    def _setResultSetType(self, result: GameResult):
        """ This would set a Game type for all results. If trying to insert a different
            Game than the first then it will yield an exception """
        if len(self.results) == 0:
            self.game_name = result.game_name
            self.game_time = result.game_time
            self._column_names.extend(result.names)

    def _makeSureOnlyOneTypeOfGame(self, result: GameResult):
        if result.game_name != self.game_name:
            raise TypeError(f"Warning, new result of type {result.game_name} is not of the same type as the others in the list")

# --------------------------------------------------------------------------------------------------------------------
    def getHtmlPrint(self):
        printer = f"<p>Game Name: {self.game_name} , Play Time: {self.game_time}, Results:</p>\n"
        printer = printer + '<table style="border-collapse: collapse;" border = 1;" >\n'

        printer = printer + "<tr>\n"
        for name in self._column_names:
            printer = printer + f' <th style="padding:3px">{name}</th>\n'
        printer = printer + "</tr>\n"
        for result in self.results:
            printer = printer + "<tr>\n"
            printer = printer + f' <td style="padding:3px">{result.game_unit}</td>\n'
            for number in result.numbers:
                printer = printer + f" <td>{number}</td>\n"
            printer = printer + "</tr>\n"
        printer = printer + "</table>\n"
        printer = printer +"<br<br>" if self.residual == 0 else printer + f"\n-------> NOTE residual value: {self.residual}<br><br>"

        return printer
# --------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        printer_string = f"Game Name: {self.game_name} , Play Time: {self.game_time}, Results:"
        describe_residual = "" if self.residual == 0 else f"\n-----------------------------> NOTE residual value: {self.residual}"
        col_width = self._getMaxColumnWidth()
        lines = ""
        for row in self._print_elements:
            row = "".join(str(value).ljust(col_width + 2) for value in row)
            lines = lines + "\n" + row
        return printer_string + lines + describe_residual

    def _getMaxColumnWidth(self):
        cell_lengths = []
        for values_list in self._print_elements:
            for element in values_list:
                if type(element) == str:
                    cell_lengths.append(len(element))
        return max(cell_lengths)

    @property
    def _print_elements(self):
        elements = [self._column_names]
        for r in self.results:
            with_unit_name = [r.game_unit]
            with_unit_name.extend(r.numbers)
            elements.append(with_unit_name)
        return elements

if __name__ == '__main__':
    rss = ResultSet()
    rs = GameResult("Loto649", "Line-1")
    rs.addNumber("N1", 19)
    rs.addNumber("N2", 44)
    rs.addNumber("N3", 32)
    rs.addNumber("N4", 16)
    rs.addNumber("N5", 17)
    rs.addNumber("N6", 1)
    rss.addResult(rs)
    rs = GameResult("Loto649", "Line-2")
    rs.addNumber("N1", 22)
    rs.addNumber("N2", 1)
    rs.addNumber("N3", 43)
    rs.addNumber("N4", 11)
    rs.addNumber("N5", 34)
    rs.addNumber("N6", 19)
    rss.addResult(rs)
    rss.residual = 49
    print(rss)
    print(rss.getHtmlPrint())
