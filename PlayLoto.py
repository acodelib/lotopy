from src import Game649, Result, GameJoker, CsvDataBridge, Configurations, EmailOutbox
import timeit as tm

data_engine = CsvDataBridge()
emailer     = EmailOutbox(Configurations(), data_engine)

rs_loto = Game649().playMaxNaturalSize()
rs_joker = GameJoker().playMaxNaturalSize()

# data_engine.saveResults(result_loto, result_joker)

mail = rs_loto.getHtmlPrint() + "\n" + rs_joker.getHtmlPrint() + "\n"

emailer.sendEmailAndRecord(mail, "Loto game play")

