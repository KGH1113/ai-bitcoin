import asyncio
from prisma import Prisma

async def record_trade(
	decision: str,
  reason: str,
  amount: int,
  reflection: str,
  recommended_actions: str,
  market_trends: str,
  successes: str,
  challenges: str
):
  """
  Record a trade transaction along with its associated insights and reflection details.

  This asynchronous function connects to a Prisma client, creates records in a relational order:
  first creating an Insights record, then a Reflection record linked to the Insights, and finally
  a Trade record linked to the Reflection. The Prisma client is disconnected after the records are created.

  Parameters:
    decision (str): The trade decision, eg., BUY, SELL, HOLD.
    reason (str): The rationale for making the trade decision.
    amount (int): The amount involved in the trade.
    reflection (str): A textual reflection on the trade or the market conditions.
    recommended_actions (str): Suggested actions resulting from the reflection.
    market_trends (str): Observations on current market trends.
    successes (str): Information regarding the successful aspects of previous trades.
    challenges (str): Information regarding challenges encountered in previous trades.

  Returns:
    The newly created trade record.
  """

  prisma = Prisma()
  await prisma.connect()

  # Create the Insights record
  new_insights = await prisma.insights.create(
    data={
      "successes": successes,
      "challenges": challenges
    }
  )

  # Create the Reflection record linked to Insights
  new_reflection = await prisma.reflection.create(
    data={
      "reflection": reflection,
      "recommendedActions": recommended_actions,
      "marketTrends": market_trends,
      "insightsId": new_insights.id
    }
  )

  # Create the Trade record linked to Reflection
  new_trade = await prisma.trade.create(
    data={
      "decision": decision,
      "reason": reason,
      "amount": amount,
      "reflectionId": new_reflection.id
    }
  )

  await prisma.disconnect()

  return new_trade
  
async def get_past_trades(count: int):
  """
  Retrieve and format the most recent trades asynchronously.
  This function connects to the Prisma database and retrieves the most recent trades based on the
  specified count, ordering them by their traded time in descending order. It includes associated
  reflection details and nested insights for each trade. After fetching the data, the connection is closed
  and the trades are formatted into a list of dictionaries suitable for further processing or returning as
  a response.
  
  Parameters:
    count (int): The number of past trades to retrieve.
  Returns:
    List[Dict]: A list of formatted trade dictionaries, where each dictionary contains:
      - id: The unique identifier of the trade.
      - decision: The decision made for the trade.
      - reason: The reason for the trade decision.
      - amount: The trade amount.
      - tradedTime (str or None): The ISO formatted trade time, or None if not available.
      - reflection (dict or None): A dictionary with reflection details including:
        - id: The identifier of the reflection.
        - reflection: The reflection text or details.
        - recommendedActions: The recommended actions based on the reflection.
        - marketTrends: Insights on market trends.
        - insights (dict or None): Nested insights dictionary with:
          - id: The identifier of the insights record.
          - successes: The successes observed.
          - challenges: The challenges noted.
  Raises:
    Exception: Any exceptions raised during database connection, querying, or disconnection.
  """

  prisma = Prisma()
  await prisma.connect()

  # Fetch the most recent `count` trades, ordered by tradedTime descending
  past_trades = await prisma.trade.find_many(
    take=count,
    order={
      "tradedTime": "desc"
    },
    include={
      "reflection": {
        "include": {
          "insights": True
        }
      }
    }
  )

  await prisma.disconnect()

  # Format the trades for response
  formatted_trades = [
    {
      "id": trade.id,
      "decision": trade.decision,
      "reason": trade.reason,
      "amount": trade.amount,
      "tradedTime": trade.tradedTime.isoformat() if trade.tradedTime else None,
      "reflection": {
        "id": trade.reflection.id,
        "reflection": trade.reflection.reflection,
        "recommendedActions": trade.reflection.recommendedActions,
        "marketTrends": trade.reflection.marketTrends,
        "insights": {
          "id": trade.reflection.insights.id,
          "successes": trade.reflection.insights.successes,
          "challenges": trade.reflection.insights.challenges,
        } if trade.reflection.insights else None
      } if trade.reflection else None
    }
    for trade in past_trades
  ]
  
  return formatted_trades

if __name__ == "__main__":
  print(asyncio.run(get_past_trades(10)))