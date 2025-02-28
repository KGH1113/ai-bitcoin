import pyupbit

def get_chart_data():
  df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
  return df.to_json()

if __name__ == "__main__":
  result = get_chart_data()
  print(result)
