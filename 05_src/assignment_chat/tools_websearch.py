from langchain.tools import tool
import requests
import json
from utils.logger import get_logger
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field


_logs = get_logger(__name__)
load_dotenv()
load_dotenv('.secrets')


class WebSearchData(BaseModel):
    """Structured web search data response."""
    position: int = Field(None, description="The position of the search result.")
    title: str = Field(..., description="The title of the search result.")
    url: str = Field(..., description="The URL of the search result.")
    description: str = Field(..., description="The description of the search result.")


@tool
def get_websearch(query:str, n_results: int = 5) -> list[WebSearchData]:
    """
    An API call to a web search service is made.
    The API call is to https://app.zenserp.com/api/v2/search
    and takes one parameter query.
    The response from the API is parsed and the top n_results are returned as a list of WebSearchData objects.
    Each WebSearchData object contains the position, title, url, and description of the search result.
    If there are no results, an empty list is returned.
    """
    _logs.debug(f'Getting web search results for query {query}')
    response = get_websearch_from_service(query)
    results = get_websearch_from_response(response, n_results)
    _logs.debug(f'Web search results: {results}')
    return results



def get_websearch_from_service(query:str):
    url = "https://app.zenserp.com/api/v2/search"
    headers = { 
        "apikey": os.getenv('ZENSERP_API_KEY')
    }
    params = {
        "q": query
    }
    response = requests.get(url, headers=headers, params=params)
    _logs.debug(f"Web search API response status: {response.status_code}")
    return response


def get_websearch_from_response(response:requests.Response, n_results: int) -> list[WebSearchData]:
    resp_dict = json.loads(response.text)
    organic_results = []

    for item in resp_dict.get("organic", []):
        _logs.info(f"Processing organic search result: {item}")
        # Skip items that are not normal organic results
        if not all(key in item for key in ["position", "title", "url", "description"]):
            continue

        try:
            rec = WebSearchData(
                position=item["position"],
                title=item["title"],
                url=item["url"],
                description=item["description"]
            )

            organic_results.append(rec)
        except Exception as e:  
            _logs.error(f"Error parsing search result: {e}")
            continue
        if len(organic_results) >= n_results:
            break
    _logs.debug(f"Extracted {len(organic_results)} organic search results.") 
    _logs.debug(f"Parsed web search results: {organic_results}")
    return organic_results

