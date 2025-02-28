from dotenv import load_dotenv
from openai import OpenAI
import json
from prompts import (
  trade_decision_prompt_raw,
  reflection_prompt_raw,
  fill_prompt
)

load_dotenv()

client = OpenAI()

def parse_response(res):
  parsed_res = res
  if "```" in res:
    parsed_res = parsed_res.replace("```", "")
  if "json" in res:
    parsed_res = parsed_res.replace("json", "")
  
  return parsed_res

def get_trade_decision(
  chart_data: str,
  past_trading_data: str,
  news_data: str,
  current_krw_balance: int,
  current_btc_balance: int,
):
  prompt = fill_prompt(
    trade_decision_prompt_raw,
    CHART_DATA=chart_data,
    PAST_TRADING_DATA=past_trading_data,
    CURRENT_KRW_BALANCE=str(current_krw_balance),
    CURRENT_BTC_BALANCE=str(current_btc_balance),
    NEWS=news_data
  )

  response = client.chat.completions.create(
    model="o1-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      },
    ]
  )

  parsed_response = parse_response(response.choices[0].message.content)
  try:
    result = json.loads(parsed_response)
  except json.decoder.JSONDecodeError:
    print("Error parsing AI's response...")
    get_trade_decision(
      chart_data=chart_data,
      past_trading_data=past_trading_data,
      news_data=news_data,
      current_krw_balance=current_krw_balance,
      current_btc_balance=current_btc_balance
    )
  return result


def get_reflection(
  trade_data: str,
  past_trade_data: str,
  current_market_data: str
):
  prompt = fill_prompt(
    reflection_prompt_raw,
    TRADING_DATA=trade_data,
    PAST_TRADING_DATA=past_trade_data,
    CURRENT_MARKET_DATA=current_market_data
  )

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      },
    ]
  )

  parsed_response = parse_response(response.choices[0].message.content)
  try:
    result = json.loads(parsed_response)
  except json.decoder.JSONDecodeError:
    print("Error parsing AI's response...")
    get_reflection()
  return result
