import pytest
from unittest.mock import patch
from src.fetch_api import get_list_breweries

@pytest.fixture
def mock_meta_response():
    return {"total": 400, "per_page": 200}

@patch("src.fetch_api.fetch_api")
@patch("src.fetch_api.get_total_breweries")
def test_successful_multiple_pages(mock_get_meta, mock_fetch):
    mock_get_meta.return_value = {"total": 400, "per_page": 200}
    mock_fetch.side_effect = [
        [{'id': f'brewery_{i}'} for i in range(1, 201)],
        [{'id': f'brewery_{i}'} for i in range(201, 401)],
        []
    ]
    result = get_list_breweries()
    assert len(result) == 400
    assert mock_fetch.call_count == 2
    mock_get_meta.assert_called_once()
    mock_fetch.assert_any_call(
        "https://api.openbrewerydb.org/v1/breweries",
        params={"page": 1, "per_page": 200}
    )
    mock_fetch.assert_any_call(
        "https://api.openbrewerydb.org/v1/breweries",
        params={"page": 2, "per_page": 200}
    )


@patch("src.fetch_api.fetch_api")
@patch("src.fetch_api.get_total_breweries")
def test_single_page(mock_get_meta, mock_fetch):
    mock_get_meta.return_value = {"total": 50, "per_page": 200}
    mock_fetch.side_effect = [
        [{'id': f'brewery_{i}'} for i in range(1, 51)],
        []
    ]
    result = get_list_breweries()

    assert len(result) == 50
    assert mock_fetch.call_count == 1
    mock_get_meta.assert_called_once()


@patch("src.fetch_api.fetch_api")
@patch("src.fetch_api.get_total_breweries")
def test_empty_response(mock_get_meta, mock_fetch):
    mock_get_meta.return_value = {"total": 0, "per_page": 200}
    mock_fetch.return_value = []
    result = get_list_breweries()
    assert result == []
    mock_fetch.assert_not_called()


@patch("src.fetch_api.fetch_api")
@patch("src.fetch_api.get_total_breweries")
def test_api_error(mock_get_meta, mock_fetch):
    mock_get_meta.return_value = {"total": 100, "per_page": 50}
    mock_fetch.side_effect = Exception("API is down")

    with pytest.raises(Exception, match="API is down"):
        get_list_breweries()


@patch("src.fetch_api.fetch_api")
@patch("src.fetch_api.get_total_breweries")
@patch("builtins.print")
def test_debug_print(mock_print, mock_get_meta, mock_fetch):
    mock_get_meta.return_value = {"total": 2, "per_page": 200}
    mock_fetch.side_effect = [
        [{'id': 'brewery_1'}, {'id': 'brewery_2'}],
        []
    ]
    get_list_breweries()
    mock_print.assert_called_with('get_list_breweries:', 2)
