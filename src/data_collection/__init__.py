if __name__ == "__main__":
  from news import collect_news
  from upbit_chart import get_chart_data
  from fear_greed_index import get_fear_greed_index
else:
  from data_collection.news import collect_news
  from data_collection.upbit_chart import get_chart_data
  from data_collection.fear_greed_index import get_fear_greed_index

__all__ = ["collect_news", "get_chart_data", "get_fear_greed_index"]