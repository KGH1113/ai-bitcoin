import requests
import json

url = "https://api.alternative.me/fng/?limit="

def get_fear_greed_index():
  """
  Retrieves the fear and greed index value from a remote API.

  This function constructs a URL by appending the character "2" to a base URL, sends a GET request to the
  constructed URL, and parses the JSON response. It then extracts and returns the "value" field from the first
  element in the "data" list.

  Returns:
    The fear and greed index value extracted from the JSON response.

  Raises:
    KeyError: If the expected keys ('data' or 'value') are not present in the JSON response.
    json.JSONDecodeError: If the response text is not valid JSON.
    requests.RequestException: For issues encountered during the HTTP request.

  Note:
    This function requires that the variables 'url', 'requests', and 'json' are defined in the surrounding scope.
  """

  _url = "{0}2".format(url) # Construct the URL
  res = requests.request("GET", _url) # Send the GET request

  parsed = json.loads(res.text) # Parse the JSON response
  data = parsed["data"] # Extract the 'data' field from the response

  return data[0]["value"] # Extract and return the 'value' field from the first element in the 'data' list

if __name__ == "__main__":
  print(get_fear_greed_index())
