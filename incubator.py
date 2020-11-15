from src import Configurations, EmailOutbox, CsvDataBridge, Game649, GameJoker

c = Configurations()

csv_db = CsvDataBridge()

v = csv_db.getNewEmailId()

print(v)