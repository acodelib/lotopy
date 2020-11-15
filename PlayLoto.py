from src import Game649, Result, GameJoker, CsvDataBridge, Configurations, EmailOutbox
import timeit as tm

data_engine = CsvDataBridge()
emailer     = EmailOutbox(Configurations(), data_engine)

result_loto = Game649().playMaxNaturalSize()
result_joker = GameJoker().playMaxNaturalSize()

data_engine.saveResults(result_loto, result_joker)

mail = f"New games session:\n\n Loto 649 game: \n {str(result_loto)} \n\n Joker Game: \n {str(result_joker)}"

emailer.sendEmailAndRecord(mail, "Loto game play")

