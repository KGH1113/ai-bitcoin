import pyupbit
import os
from dotenv import load_dotenv

load_dotenv()

upbit = pyupbit.Upbit(
  os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY")
)

try:
  trade_fee_env = float(os.getenv("TRADE_FEE"))
except:
  raise Exception("Unexpected trade fee value in env variable")
trade_fee = 1 - (trade_fee_env / 100)

def get_krw_balance():
  """
  Retrieve the account balance in Korean Won (KRW) via the Upbit API.

  This function calls the Upbit API to obtain the balance associated with the 'KRW' currency.
  It abstracts the call to the underlying 'get_balance' method provided by the Upbit client.

  Returns:
    float: The available balance in Korean Won.
  """

  return upbit.get_balance("KRW")

def get_btc_balance():
  """
  Calculate and return the value of Bitcoin held in the account, converted to KRW.

  This function retrieves the balance of Bitcoin using the upbit API, and then converts
  the balance into Korean Won by multiplying it with the current ask price taken from the
  orderbook. The ask price is obtained from the most recent orderbook entry.

  Returns:
    float: The value of the Bitcoin balance expressed in KRW.
  """
  
  return upbit.get_balance("KRW-BTC")*pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]

def buy_btc(krw_ammount: float):
  """
  Executes a market order to buy Bitcoin using the Upbit API.

  This function attempts to buy Bitcoin using a market order with the given KRW amount.
  If the provided amount is above the minimum threshold (5000 KRW), it executes the order while applying
  a deduction factor (0.9995) to account for fees. Otherwise, it raises an exception.

  Args:
    krw_ammount (float): The amount in Korean Won (KRW) to be used for purchasing Bitcoin. Must be greater than 5000.

  Raises:
    Exception: If the provided amount is less than or equal to 5000 KRW, indicating that the minimum required amount is not met.
  """
  if upbit.get_balance("KRW") < krw_ammount * trade_fee:
    # Balance overed
    raise Exception("BTC you want to buy is over the balance")
  if krw_ammount * trade_fee < 5000:
    # Minimum buy amount not satisfied
    raise Exception("Minimum buy ammount is 5000 KRW")
  else:
    # Success
    upbit.buy_market_order("KRW-BTC", krw_ammount * trade_fee)
  
def sell_btc(krw_ammount: float):
  """
  Sell Bitcoin based on a given KRW amount.

  This function retrieves the current Bitcoin ask price from the orderbook, then calculates
  the total sell value by multiplying the provided KRW amount with the current price. If the 
  resulting value exceeds 5000 KRW, it executes a market sell order for Bitcoin. Otherwise, it
  raises an exception indicating that the minimum sell amount requirement is not met.

  Parameters:
    krw_ammount (float): The amount in KRW to use for computing the sell order value.

  Raises:
    Exception: If the computed total sell value is 5000 KRW or less.
  """
  
  current_price = pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]

  if upbit.get_balance("KRW-BTC") * current_price < krw_ammount * trade_fee:
    # Balance overed
    raise Exception("BTC you want to sell is over the balance")
  elif krw_ammount * trade_fee < 5000:
    # Minimum sell amount not satisfied
    raise Exception("Minimum sell ammount is 5000 KRW")
  else:
    # Success
    upbit.sell_market_order("KRW-BTC", (krw_ammount * trade_fee) / current_price)

if __name__ == "__main__":
  print(get_krw_balance(), get_btc_balance())
