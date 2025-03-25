import openai_integration as ai
import upbit_integration as upbit
import data_collection

import db_integration as db

import asyncio
import json
import os
import time
import requests

from dotenv import load_dotenv
load_dotenv()

def main(test = False):
  chart_data = data_collection.get_chart_data()
  krw_balance = upbit.get_krw_balance()
  btc_balance = upbit.get_btc_balance()
  news_data = json.dumps(data_collection.collect_news())
  past_trade_data = json.dumps(asyncio.run(db.get_past_trades(10)))
  fear_greed_index = json.dumps(data_collection.get_fear_greed_index())
  try:
    trade_fee = float(os.getenv("TRADE_FEE"))
  except:
    raise Exception("Unexpected trade fee value in env variable")
  
  # Get the trading decision from the AI
  trade = ai.get_trade_decision(
    chart_data=chart_data,
    past_trading_data=past_trade_data,
    current_krw_balance=krw_balance,
    current_btc_balance=btc_balance,
    news_data=news_data,
    fear_greed_index=fear_greed_index,
    trade_fee=trade_fee,
  )

  # Get the reflection from the AI
  reflection = ai.get_reflection(
    trade_data=json.dumps(trade),
    past_trade_data=past_trade_data,
    current_market_data=chart_data
  )

  # Record the trade in the database
  asyncio.run(
    db.record_trade(
      decision=trade["decision"],
      reason=trade["reason"],
      amount=trade["amount"],
      reflection=reflection["reflection"],
      recommended_actions=reflection["recommended_actions"],
      market_trends=reflection["market_trends"],
      successes=reflection["insights"]["successes"],
      challenges=reflection["insights"]["challenges"]
    )
  )

  if test:
    return

  # Execute the trade
  if trade["decision"] == "BUY":
    upbit.buy_btc(trade["amount"])
  elif trade["decision"] == "SELL":
    upbit.sell_btc(trade["amount"])
  elif trade["decision"] == "HOLD":
    pass

  log = "{0}: {1} {2}KRW".format(time.time(), trade["decision"], trade["amount"])

  try:
    puuush_id = os.getenv("PUUUSH_ID")
    url = "https://puuu.sh/notify/" + puuush_id
    payload = {
      "title": "AI-BITCOIN trade (TEST RUN)",
      "body": log
    }
    requests.post(url, json=payload)
  except:
    print("Error sending notification.")
  
  print(log)
  print()
  print()

if __name__ == "__main__":
  isTest = os.getenv("TEST")
  if isTest == "true":
    main(test=True)
  else:
    main()