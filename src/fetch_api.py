import requests
import json

def fetch_api(url, params):
  try:
    response = requests.get(url, params)
    if response.status_code == 200:
      return response.json()
  except Exception as ex:
    raise Exception(f'Check API: {ex}')


def get_list_breweries():
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    all_breweries = []
    page = 1
    per_page = 200

    while True:
        list_breweries = fetch_api(base_url, params={"page": page, "per_page": per_page})
        if not list_breweries:
            break
        all_breweries.extend(list_breweries)
        page += 1
    print('get_list_breweries:', len(all_breweries))
    return all_breweries
