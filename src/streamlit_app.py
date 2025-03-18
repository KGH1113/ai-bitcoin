import streamlit as st
import pandas as pd
import asyncio
import datetime
import pyupbit
from prisma import Client

# Initialize Prisma client
client = Client()

# Async function to load data using Prisma
async def load_data():
  await client.connect()
  trades = await client.trade.find_many()
  reflections = await client.reflection.find_many()
  insights = await client.insights.find_many()
  await client.disconnect()
  return trades, reflections, insights

def convert_to_dataframe(data, columns):
  """Converts a list of Prisma objects to a DataFrame using specified columns."""
  rows = []
  for item in data:
    row = {}
    for col in columns:
      row[col] = getattr(item, col, None)
    rows.append(row)
  return pd.DataFrame(rows)

def get_market_data(start_date):
  """Fetch daily OHLCV data from pyupbit starting from start_date until today."""
  today = datetime.date.today()
  days = (today - start_date).days + 1
  df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=days)
  if df is None:
    st.error("Failed to fetch market data from pyupbit")
    st.stop()
  # Convert index to plain date objects for easy lookup
  df.index = df.index.date
  return df

def get_price_at_date(trade_date, market_df):
  """Return the closing price for a trade date from the market dataframe."""
  date_key = trade_date.date()
  try:
    price = market_df.loc[date_key, "close"]
    return price
  except Exception:
    return None

def compute_strategy_return(trades_df, market_df):
  """
  Computes the strategy return.
  - For each BUY: add (price * amount) to total cost and increase net position.
  - For each SELL: add (price * amount) to total revenue and decrease net position.
  If there is an open (unclosed) position, its value is added at the latest market price.
  """
  trades_df_sorted = trades_df.sort_values(by="tradedTime")
  total_buy_cost = 0.0
  total_sell_revenue = 0.0
  net_position = 0  # in BTC

  for _, row in trades_df_sorted.iterrows():
    price = get_price_at_date(row["tradedTime"], market_df)
    if price is None:
      continue
    if row["decision"].upper() == "BUY":
      total_buy_cost += price * row["amount"]
      net_position += row["amount"]
    elif row["decision"].upper() == "SELL":
      total_sell_revenue += price * row["amount"]
      net_position -= row["amount"]

  if net_position > 0:
    # Use the latest market close for open positions
    current_price = market_df.iloc[-1]["close"]
    open_position_value = current_price * net_position
  else:
    open_position_value = 0

  final_value = total_sell_revenue + open_position_value
  if total_buy_cost > 0:
    strategy_return = (final_value - total_buy_cost) / total_buy_cost * 100
  else:
    strategy_return = 0
  return strategy_return

def compute_market_return(market_df):
  """Computes market return from the first available price to the latest price."""
  first_price = market_df.iloc[0]["close"]
  last_price = market_df.iloc[-1]["close"]
  market_return = (last_price - first_price) / first_price * 100
  return market_return

def main():
  st.title("AI Bitcoin Trading Bot Dashboard")
  st.write("Visualize trades, reflections, insights, and performance returns.")

  # Load data from the Prisma DB
  with st.spinner("Loading data from the database..."):
    try:
      trades, reflections, insights = asyncio.run(load_data())
    except Exception as e:
      st.error(f"Error loading data from DB: {e}")
      return

  # Define columns to extract for each model
  trades_columns = ["id", "decision", "reason", "amount", "tradedTime", "reflectionId"]
  reflections_columns = ["id", "reflection", "recommendedActions", "marketTrends", "insightsId"]
  insights_columns = ["id", "successes", "challenges"]

  trades_df = convert_to_dataframe(trades, trades_columns)
  reflections_df = convert_to_dataframe(reflections, reflections_columns)
  insights_df = convert_to_dataframe(insights, insights_columns)

  # Ensure tradedTime is in datetime format and determine the start date for market data
  if not trades_df.empty:
    trades_df["tradedTime"] = pd.to_datetime(trades_df["tradedTime"])
    min_trade_date = trades_df["tradedTime"].min().date()
  else:
    st.warning("No trade data available. Using a default 30-day period for market data.")
    min_trade_date = datetime.date.today() - datetime.timedelta(days=30)

  # Fetch market data using pyupbit
  market_df = get_market_data(min_trade_date)

  # Compute performance returns
  strategy_return = compute_strategy_return(trades_df, market_df) if not trades_df.empty else 0
  market_return = compute_market_return(market_df)

  st.subheader("Performance Metrics")
  col1, col2 = st.columns(2)
  col1.metric("Strategy Return", f"{strategy_return:.2f}%")
  col2.metric("Market Return", f"{market_return:.2f}%")

  # Display a chart for the market price
  st.subheader("Market Price (KRW-BTC)")
  st.line_chart(market_df["close"])

  # Create tabs to show detailed data from the DB
  tab1, tab2, tab3 = st.tabs(["Trades", "Reflections", "Insights"])

  with tab1:
    st.header("Trade History")
    if not trades_df.empty:
      st.dataframe(trades_df.sort_values(by="tradedTime", ascending=False))
      st.subheader("Trade Amounts Over Time")
      trades_sorted = trades_df.sort_values("tradedTime")
      st.line_chart(trades_sorted.set_index("tradedTime")["amount"])
      st.subheader("Trade Decision Distribution")
      decision_counts = trades_df["decision"].value_counts()
      st.bar_chart(decision_counts)
    else:
      st.write("No trade data available.")

  with tab2:
    st.header("Trade Reflections")
    if not reflections_df.empty:
      st.dataframe(reflections_df)
    else:
      st.write("No reflections data available.")

  with tab3:
    st.header("Insights")
    if not insights_df.empty:
      st.dataframe(insights_df)
    else:
      st.write("No insights data available.")

if __name__ == "__main__":
  main()