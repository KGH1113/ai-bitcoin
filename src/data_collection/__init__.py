if __name__ == "__main__":
  from news import collect_news
  from upbit_chart import get_chart_data
else:
  from data_collection.news import collect_news
  from data_collection.upbit_chart import get_chart_data

__all__ = ["collect_news", "get_chart_data"]