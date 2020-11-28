from src import Configurations, EmailOutbox, DataBridgeCSV, Game649, GameJoker, DataConnectorCSV


db = DataBridgeCSV()

print(db.getNewGameId())