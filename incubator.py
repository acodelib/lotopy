from src import Game649, GameResult, GameJoker, DataBridgeCSV, Configurations, EmailOutbox, WinningsDetector
import timeit as tm
from concurrent.futures import Future, Executor
from concurrent.futures.process import ProcessPoolExecutor

# data_engine = DataBridgeCSV ()
# rs_joker = GameJoker().playMaxGameUnits()


rc = Game649().playSingleGameUnit()
ranges = []
total_no_of_results = 1000000
unit = int(total_no_of_results / 8)
start = 0
end = unit
while end <= total_no_of_results:
    ranges.append([start, end])
    start = end
    end = end + unit


def genResults(the_range):
    print(f"start:{the_range[0]} - end:{the_range[1]}")
    rs_store = []
    for i in range(the_range[0], the_range[1]):
        rs_loto = Game649().playMaxGameUnits()
        rs_store.append(rs_loto)
    for rs in rs_store:
        for r in rs.results:
            wd = WinningsDetector(rc, r)
            wd.getWinning()
            if wd.match_count > 5:
                print(wd.match_count)

if __name__ == "__main__":
    start = tm.default_timer()
    prl = ProcessPoolExecutor(4)
    future_results = prl.map(genResults, ranges)
    prl.shutdown()
    rs_store = []

    end = tm.default_timer() - start
    print(end)


