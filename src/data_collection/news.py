from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import json
from newspaper import Article
from newspaper import Config

load_dotenv()

def collect_news():
  params = {
    "api_key": os.getenv("SERPAPI_API_KEY"),
    "engine": "google",
    "q": "Stock Market Bitcoin",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "tbm": "nws"
  }

  search = GoogleSearch(params)
  pages = search.pagination()

  news_results = []
  user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

  for page_num, page in enumerate(list(pages), start=1):
    if len(news_results) >= 10:
      break

    print("extracting data from the page {}".format(page_num))

    for news_result in page["news_results"]:
      config = Config()
      config.browser_user_agent = user_agent
      article = Article(news_result["link"], config=config)
      try:
        article.download()
        article.parse()
      except:
        continue
      
      news_results.append({
        "position": news_result["position"],
        "link": news_result["link"],
        "content": {
          "title": article.title,
          "text": article.text
        },
        "source": news_result["source"],
        "date_published": news_result["date"],
      })
  
  return news_results

if __name__ == "__main__":
  print(json.dumps(collect_news(), indent=2, ensure_ascii=False))