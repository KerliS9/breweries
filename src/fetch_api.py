import requests
import json

def fetch_api(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
  except Exception as ex:
    raise Exception(f'Check API: {ex}')


def get_list_breweries():
  url = 'https://api.openbrewerydb.org/v1/breweries'
  list_breweries = fetch_api(url)
  print(len(list_breweries))
  return list_breweries


// GET https://api.openbrewerydb.org/v1/breweries?per_page=3
