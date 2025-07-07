import pytest
from unittest.mock import patch
from src.fetch_api import get_list_breweries

@patch("src.fetch_api.fetch_api")
def test_successful_multiple_pages(mock_fetch):
    mock_fetch.side_effect = [
        [{'id': f'brewery_{i}'} for i in range(1, 201)],
        [{'id': f'brewery_{i}'} for i in range(201, 401)],
        []
    ]

    result = get_list_breweries()

    assert len(result) == 400
    assert mock_fetch.call_count == 3
    mock_fetch.assert_any_call(
        "https://api.openbrewerydb.org/v1/breweries",
        params={"page": 1, "per_page": 200}
    )
    mock_fetch.assert_any_call(
        "https://api.openbrewerydb.org/v1/breweries",
        params={"page": 2, "per_page": 200}
    )

@patch("src.fetch_api.fetch_api")
def test_single_page(mock_fetch):
    mock_fetch.side_effect = [
        [{'id': f'brewery_{i}'} for i in range(1, 51)],
        []
    ]

    result = get_list_breweries()

    assert len(result) == 50
    assert mock_fetch.call_count == 2

@patch("src.fetch_api.fetch_api")
def test_empty_first_call(mock_fetch):
    mock_fetch.return_value = []

    result = get_list_breweries()

    assert result == []
    mock_fetch.assert_called_once()

@patch("src.fetch_api.fetch_api")
def test_api_error(mock_fetch):
    mock_fetch.side_effect = Exception("API is down")

    with pytest.raises(Exception, match="API is down"):
        get_list_breweries()

@patch("src.fetch_api.fetch_api")
@patch("builtins.print")
def test_debug_print(mock_print, mock_fetch):
    mock_fetch.side_effect = [
        [{'id': 'brewery_1'}, {'id': 'brewery_2'}],
        []
    ]

    get_list_breweries()

    mock_print.assert_called_with('get_list_breweries:', 2)
