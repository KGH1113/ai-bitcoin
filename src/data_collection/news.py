from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import json
from newspaper import Article
from newspaper import Config

load_dotenv()

def collect_news():
  """
  Collect news articles related to 'Stock Market Bitcoin' using a Google News search.
  This function uses the SerpAPI Google search engine to retrieve news results,
  paginates through the search results, and then downloads and parses each news article
  using the provided link. The parsing is performed by an Article parser which extracts
  the title and text content of the article. The news extraction stops once at least 10
  news results have been collected. Each news result includes its position, link,
  title, full text, source, and published date.

  Returns:
    list[dict]: A list of dictionaries, each containing details of a news article with keys:
      - "position": The position of the news result as given by the search engine.
      - "link": The URL to the news article.
      - "content": A dictionary with two keys:
        - "title": The title of the news article.
        - "text": The main textual content of the article.
      - "source": The source of the news article.
      - "date_published": The publication date of the news article.
  """

  # Set up the search parameters
  params = {
    "api_key": os.getenv("SERPAPI_API_KEY"),
    "engine": "google",
    "q": "Stock Market Bitcoin",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "tbm": "nws"
  }

  # Perform the search and paginate through the results
  search = GoogleSearch(params)
  pages = search.pagination()

  news_results = [] # List to store the extracted news results
  user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36" # User agent for the Article parser

  # Iterate over the search result pages
  for page_num, page in enumerate(list(pages), start=1):
    # Stop collecting news if we have at least 10 results
    if len(news_results) >= 10:
      break

    for news_result in page["news_results"]:
      config = Config()
      config.browser_user_agent = user_agent
      article = Article(news_result["link"], config=config)
      # Download and parse the article
      try:
        article.download()
        article.parse()
      except: # Skip to the next article if website of article is not accessible with bots.
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
