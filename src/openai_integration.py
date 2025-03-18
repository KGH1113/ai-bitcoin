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

def get_trade_decision(
  chart_data: str,
  past_trading_data: str,
  news_data: str,
  current_krw_balance: int,
  current_btc_balance: int,
  fear_greed_index: str,
  trade_fee: float,
):
  """
  Get trading decision from AI based on provided market and account data.

  This function formats a prompt using the provided chart data, past trading data,
  news data, current KRW and BTC balances, as well as the current fear-greed index.
  It then calls the AI completion API to obtain a trading decision and attempts
  to parse the AI's response as JSON. If parsing fails, the function prints an error
  message and recursively retries the decision-making process.

  Parameters:
    chart_data (str): Chart data in string format.
    past_trading_data (str): Past trading activity data.
    news_data (str): Latest news data relevant to the trade decision.
    current_krw_balance (int): Current balance of KRW.
    current_btc_balance (int): Current balance of BTC.
    fear_greed_index (str): Current fear-greed index as a string.
    trade_fee (fload): Trade fee of 

  Returns:
    dict: The trading decision parsed from the AI response.

  Notes:
    In case of a JSON parsing error, the function recursively retries obtaining
    a valid response.
  """

  # Fill the blanks in prompt with the provided data
  prompt = fill_prompt(
    trade_decision_prompt_raw,
    CHART_DATA=chart_data,
    PAST_TRADING_DATA=past_trading_data,
    CURRENT_KRW_BALANCE=str(current_krw_balance),
    CURRENT_BTC_BALANCE=str(current_btc_balance),
    NEWS=news_data,
    FEAR_GREED_INDEX=fear_greed_index,
    TRADE_FEE=trade_fee,
  )

  # Call the AI model to get a trading decision
  response = client.chat.completions.create(
    model="o3-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ],
    response_format={
      "type": "json_schema",
      "json_schema": {
        "name": "trade_decision",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
            "decision": {
              "type": "string",
              "description": "The decision being made, BUY, SELL or HOLD"
            },
            "reason": {
              "type": "string",
              "description": "The reason for the decision."
            },
            "amount": {
              "type": "number",
              "description": "The amout(KRW) you want to buy at the moment based on the data provided."
            }
          },
          "required": [
            "decision",
            "reason",
            "amount"
          ],
          "additionalProperties": False
        }
      }
    },
    reasoning_effort="high"
  )

  return json.loads(response.choices[0].message.content)


def get_reflection(
  trade_data: str,
  past_trade_data: str,
  current_market_data: str
):
  """
  Generate a reflection by processing trading and market data through an AI model.

  This function builds a prompt using the provided current trading data, past trading data,
  and current market data. It then sends this prompt to an AI chat model and retrieves a response.
  The response is parsed as JSON and returned as a Python object.

  Parameters:
    trade_data (str): A string containing the current trading data.
    past_trade_data (str): A string containing historical trading data.
    current_market_data (str): A string detailing the current market conditions.

  Returns:
    object: The parsed JSON response from the AI, typically a dictionary or list based on the content.

  Behavior:
    If the response cannot be parsed as valid JSON, the function prints an error message and
    recursively calls itself to attempt generating a valid reflection.

  Note:
    This function assumes that the helper functions `fill_prompt` and `parse_response`, the 
    variable `reflection_prompt_raw`, and the `client` for the AI model API are defined and 
    available in the module's context.
  """

  # Fill the blanks in prompt with the provided data
  prompt = fill_prompt(
    reflection_prompt_raw,
    TRADING_DATA=trade_data,
    PAST_TRADING_DATA=past_trade_data,
    CURRENT_MARKET_DATA=current_market_data
  )

  # Call the AI model to get a reflection
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
      }
    ],
    response_format={
      "type": "json_schema",
      "json_schema": {
        "name": "trading_assistant_analysis",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
            "reflection": {
              "type": "string",
              "description": "A brief reflection on the recent trading decisions."
            },
            "insights": {
              "type": "object",
              "description": "Insights on what worked well and what didn't.",
              "properties": {
                "successes": {
                  "type": "string",
                  "description": "Insights on what worked well."
                },
                "challenges": {
                  "type": "string",
                  "description": "Insights on what didn't work well."
                }
              },
              "required": [
                "successes",
                "challenges"
              ],
              "additionalProperties": False
            },
            "recommended_actions": {
              "type": "string",
              "description": "Suggestions for improvement in future trading decisions."
            },
            "market_trends": {
              "type": "string",
              "description": "Any patterns of trends you notice in the market data."
            }
          },
          "required": [
            "reflection",
            "insights",
            "recommended_actions",
            "market_trends"
          ],
          "additionalProperties": False
        }
      }
    },
    temperature=1,
    max_completion_tokens=10000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return json.loads(response.choices[0].message.content)
