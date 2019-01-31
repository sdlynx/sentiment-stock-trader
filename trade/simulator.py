"""
Code for simulating trading algorithms
"""

from datetime import date, timedelta
from dotenv import load_dotenv, find_dotenv
import logger
from trade_simulator import TradeSimulator
from datastore import DataAPI
from algorithms import HeikinAshiAlgorithm

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.init_logger(logger.get_logger())

def daterange(date1, date2):
    """
    Function to create date range
    """

    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

START_DATE = date.today() - timedelta(days=365)
END_DATE = date.today()

def main():
    """
    Executes all logic
    """

    trader = TradeSimulator()
    data_api = DataAPI(positions_table_name='positions_simulated')
    data_api.connect()

    # skip all behavior if market is closed
    if not trader.market_is_open():
        _logger.info("Market is closed, no trading will occur")
        return

    date_range = daterange(START_DATE, END_DATE)
    for date_entry in date_range:
        _logger.info("Simulating Heikin-Ashi on %s", date_entry)
        HeikinAshiAlgorithm.execute(trader, data_api, date_entry)

    _logger.info("Date range: %s to %s", START_DATE, END_DATE)
    _logger.info("Total profit: $%d (%d%%)", trader.get_profit(), (100 * trader.get_profit_percent()))

    data_api.reset_positions(tag='HA')

if __name__ == "__main__":
    # calling main function
    main()