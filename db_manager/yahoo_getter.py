import yfinance as yf

class Ticker():

    def __init__(self, ticker_ID: str="AAPL", **kwargs) -> None:
        """well should this just get lots of metadata on a particular ticker? Yeah I guess so"""
        __dict__ = {}
        self.ticker_ID=ticker_ID
        self.__dict__.update(**kwargs)
        self._set_ticker()
    
    def _set_ticker(self):
        self.ticker = yf.Ticker(self.ticker_ID)