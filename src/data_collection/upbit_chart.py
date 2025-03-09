import pyupbit

def get_chart_data():
  """
  Fetches daily OHLCV chart data for the KRW-BTC pair and returns it as a JSON string.

  This function retrieves the open, high, low, close, and volume data for KRW-BTC for the past 30 days 
  using the pyupbit library's get_ohlcv method with a daily interval. The resulting DataFrame is then 
  converted to a JSON format.

  Returns:
    str: A JSON string representing the OHLCV data for KRW-BTC.

  Raises:
    Exception: Propagates exceptions raised by pyupbit.get_ohlcv if the data retrieval fails.
  """
  
  df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
  return df.to_json()

if __name__ == "__main__":
  result = get_chart_data()
  print(result)
