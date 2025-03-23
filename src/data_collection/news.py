import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json
from newspaper import Article
from newspaper import Config

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36" # User agent for the Article parser

def collect_news(query="Stock Market Bitcoin", page_size=10):
  url = "https://newsapi.org/v2/everything"
  params = {
    "q": query,
    "sortBy": "publishedAt",
    "language": "en",
    "pageSize": page_size,
    "apiKey": NEWS_API_KEY
  }
  response = requests.get(url, params=params)
  data = response.json()

  if data["status"] != "ok":
    raise Exception(f"News API error: {data.get("message", "Unknown error")}")

  articles = data["articles"]
  
  # print(json.dumps(articles))

  news_result = []
  for article in articles:
    if len(news_result) >= 10:
      break

    title = article["title"]
    published_at = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    url = article["url"]
    
    config = Config()
    config.browser_user_agent = user_agent
    article = Article(url, config=config)
    # Download and parse the article
    try:
      article.download()
      article.parse()
    except: # Skip to the next article if website of article is not accessible with bots.
      print("Not accessable")
      continue

    news_result.append({
      "title": title,
      "published_at": str(published_at),
      "url": url,
      "content": article.text
    })
  
  return news_result

if __name__ == "__main__":
  print(json.dumps(collect_news()))