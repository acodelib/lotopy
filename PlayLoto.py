from src import Game649, GameResult, GameJoker, DataBridgeCSV, Configurations, EmailOutbox
import timeit as tm

data_engine = DataBridgeCSV ()
emailer     = EmailOutbox(Configurations(), data_engine)



rs_loto = Game649().playMaxGameUnits()
rs_joker = GameJoker().playMaxGameUnits()

data_engine.saveResultSet(rs_loto)
data_engine.saveResultSet(rs_joker)

mail = rs_loto.getHtmlPrint() + "\n" + rs_joker.getHtmlPrint() + "\n"

emailer.sendEmailAndRecord(mail, "Loto game play")



"""
TOTAL EXECT: 3.61, 7.89, 12.36
"""