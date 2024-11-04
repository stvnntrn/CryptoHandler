import json
import logging
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, JSONDecodeError, RequestException

load_dotenv(override=True)

coingecko_api_key = os.getenv("COINGECKO_API_KEY")


class CryptoHandler:
    def __init__(self):
        pass

    def _api_request(self, url: str):
        headers = {"accept": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            return data
        except HTTPError:
            raise HTTPError(
                f"HTTP request failed with status code {response.status_code} for URL: {url}"
            )
        except JSONDecodeError:
            raise JSONDecodeError(
                f"Response from {url} could not be decoded as JSON."
            )
        except RequestException as e:
            raise RequestException(f"Request failed: {e} for URL: {url}")

    def list_currencies(self):
        pass
