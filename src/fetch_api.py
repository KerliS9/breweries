import requests
import math


def fetch_api(url, params):
  try:
    response = requests.get(url, params)
    if response.status_code == 200:
      return response.json()
  except Exception as ex:
    raise Exception(f'Check API: {ex}')


def get_total_breweries():
   base_url = "https://api.openbrewerydb.org/v1/breweries/meta"
   response_meta = fetch_api(base_url, params={"page": None, "per_page": None})
   return response_meta


def get_list_breweries():
    base_url = "https://api.openbrewerydb.org/v1/breweries"

    response_meta = get_total_breweries()
    if response_meta is not None:
        total_breweries = response_meta["total"]
        per_page = response_meta['per_page']
        total_pages = math.ceil(total_breweries / per_page)

    all_breweries = []
    for page in range(1, total_pages + 1):
        list_breweries = fetch_api(base_url, params={"page": page, "per_page": per_page})
        if list_breweries is not None:
            all_breweries.extend(list_breweries)

    print('get_list_breweries:', len(all_breweries))
    return all_breweries
