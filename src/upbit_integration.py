import pyupbit
import os
from dotenv import load_dotenv

load_dotenv()

upbit = pyupbit.Upbit(
  os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY")
)

def get_krw_balance():
  return upbit.get_balance("KRW")

def get_btc_balance():
  return upbit.get_balance("KRW-BTC")*pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]

def buy_btc(krw_ammount: float):
  if krw_ammount > 5000:
    upbit.buy_market_order("KRW-BTC", krw_ammount*0.9995)
  else:
    raise Exception("Minimum buy ammount is 5000 KRW")
  
def sell_btc(krw_ammount: float):
  current_price = pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]
  if krw_ammount * current_price > 5000:
    upbit.sell_market_order("KRW-BTC", krw_ammount)
  else:
    raise Exception("Minimum sell ammount is 5000 KRW")

if __name__ == "__main__":
  print(get_btc_balance())
