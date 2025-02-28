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