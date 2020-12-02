from src import GameResult

class WinningsDetector():
    def __init__(self, left: GameResult, right: GameResult):
        self.left = left
        self.right = right
        self.match_count = 0
        self._verbose_match = ""

        #self._min_match_count_for_game_type = 0
        self.isSameTypeOfResults()


    def isSameTypeOfResults(self):
        if self.left.game_name != self.right.game_name:
            raise TypeError("Results need to be of same type in order to compare them")
        else:
            return True

    def getWinning(self):
        left_dict = self.makeDictOutOfNameAndValue(self.left)
        right_dict = self.makeDictOutOfNameAndValue(self.right)

        for left_name, left_value in left_dict.items():
            for right_name, right_value in right_dict.items():
                #print(f"LN:{left_name} LV:{left_value} RN:{right_name} RV:{right_value}")
                if left_name[0] == right_name[0] and left_value == right_value:
                    self.match_count += 1
                    self._verbose_match = self._verbose_match + f"{left_name} = {right_name} = {left_value}\n"

        if self.match_count > 2 or (self.match_count > 1 and "J =" in self._verbose_match):
            return self._verbose_match
        else:
            return None

    def makeDictOutOfNameAndValue(self, result: GameResult):
        dict = {}
        for position, value in enumerate(result.names):
            dict[value] = result.numbers[position]
        return dict



