import requests
import json

url = "https://api.alternative.me/fng/?limit="

def get_fear_greed_index():
  _url = "{0}2".format(url)
  res = requests.request("GET", _url)

  parsed = json.loads(res.text)
  data = parsed["data"]

  return data[0]["value"]

if __name__ == "__main__":
  print(get_fear_greed_index())
