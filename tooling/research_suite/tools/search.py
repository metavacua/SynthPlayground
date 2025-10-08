import os
import json
import requests
from typing import Literal, Dict, Any, List

# Define constants from the original TypeScript file
BING_ENDPOINT = 'https://api.bing.microsoft.com/v7.0/search'
GOOGLE_ENDPOINT = 'https://customsearch.googleapis.com/customsearch/v1'
EXA_ENDPOINT = 'https://api.exa.ai/search'

# Define a type for the time filter, similar to TypeScript
TimeFilter = Literal['24h', 'week', 'month', 'year', 'all']

# --- Helper Functions (Ported from TypeScript) ---

def get_bing_freshness(time_filter: TimeFilter) -> str:
    """Maps a time filter to the 'freshness' parameter for the Bing API."""
    if time_filter == '24h':
        return 'Day'
    if time_filter == 'week':
        return 'Week'
    if time_filter == 'month':
        return 'Month'
    if time_filter == 'year':
        return 'Year'
    return ''

def get_google_date_restrict(time_filter: TimeFilter) -> str | None:
    """Maps a time filter to the 'dateRestrict' parameter for the Google API."""
    if time_filter == '24h':
        return 'd1'
    if time_filter == 'week':
        return 'w1'
    if time_filter == 'month':
        return 'm1'
    if time_filter == 'year':
        return 'y1'
    return None

# --- Main Search Function ---

def perform_search(
    query: str,
    time_filter: TimeFilter = 'all',
    provider: str = 'google',
    is_test_query: bool = False
) -> Dict[str, Any]:
    """
    Performs a web search using the specified provider (Google, Bing, or Exa).
    This function is a Python port of the logic in `app/api/search/route.ts`.
    """
    if not query:
        return {"error": "Query parameter is required", "status": 400}

    # Return dummy results for test queries
    if query.lower() == 'test' or is_test_query:
        return {
            "webPages": {
                "value": [
                    {"id": "test-1", "url": "https://example.com/test-1", "name"
: "Test Result 1", "snippet": "This is a test search result..."},
                    {"id": "test-2", "url": "https://example.com/test-2", "name"
: "Test Result 2", "snippet": "Another test result..."},
                    {"id": "test-3", "url": "https://example.com/test-3", "name"
: "Test Result 3", "snippet": "A third test result..."},
                ]
            }
        }

    # --- Provider-Specific Logic ---

    if provider == 'exa':
        api_key = os.environ.get("EXA_API_KEY")
        if not api_key:
            return {"error": "Exa search API is not properly configured.", "status": 500}

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
        payload = {
            'query': query, 'type': 'auto', 'numResults': 10,
            'contents': {'text': {'maxCharacters': 500}}
        }
        try:
            response = requests.post(EXA_ENDPOINT, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Transform Exa results to match the common format
            return {
                "webPages": {
                    "value": [
                        {
                            "id": item.get("id", item.get("url")), "url": item.get("url"),
                            "name": item.get("title", "Untitled"), "snippet": item.get("text", ""),
                        } for item in data.get("results", [])
                    ]
                }
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch search results from Exa: {e}", "status": 500}

    elif provider == 'google':
        api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        cx = os.environ.get("GOOGLE_SEARCH_CX")
        if not api_key or not cx:
            return {"error": "Google search API is not properly configured.", "status": 500}

        params = {'q': query, 'key': api_key, 'cx': cx, 'num': 10, 'safe': 'active'}
        date_restrict = get_google_date_restrict(time_filter)
        if date_restrict:
            params['dateRestrict'] = date_restrict

        try:
            response = requests.get(GOOGLE_ENDPOINT, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Transform Google results
            return {
                "webPages": {
                    "value": [
                        {
                            "id": item.get("cacheId", item.get("link")), "url": item.get("link"),
                            "name": item.get("title"), "snippet": item.get("snippet"),
                        } for item in data.get("items", [])
                    ]
                }
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch search results from Google: {e}", "status": 500}

    else:  # Default to Bing
        api_key = os.environ.get("AZURE_SUB_KEY")
        if not api_key:
            return {"error": "Bing search API is not properly configured.", "status": 500}

        params = {'q': query, 'count': 10, 'mkt': 'en-US', 'safeSearch': 'Moderate'}
        freshness = get_bing_freshness(time_filter)
        if freshness:
            params['freshness'] = freshness

        headers = {'Ocp-Apim-Subscription-Key': api_key}
        try:
            response = requests.get(BING_ENDPOINT, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json() # Bing's format is the default
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch search results from Bing: {e}", "status": 500}