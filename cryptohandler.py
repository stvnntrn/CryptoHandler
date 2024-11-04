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
    def __init__(self, base_currency: str = "usd"):
        self.base_currency = base_currency

    def _api_request(self, url: str):
        """
        Sends a Get request to the specified URL and returns the parsed JSON data.

        This method is a protected utility for making API requests. It handles HTTP errors and JSON decoding issues, providing clear error messages if something goes wrong.

        Args:
            url(str): The API endpoint URL to send the GET request to.

        Returns:
            dict: The JSON response data parsed into a dictionary.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
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
            raise JSONDecodeError(f"Response from {url} could not be decoded as JSON.")
        except RequestException as e:
            raise RequestException(f"Request failed: {e} for URL: {url}")

    def list_crypto_currencies(self, base_currency="usd"):
        """
        Fetches and displays a list of cryptocurrency markets for the specified base currency.

        This method constructs an API request to CoinGecko to retrieve the latest cryptocurrency market data,
        converting values to the specified base currency. The retrieved data is then printed to the console.

        Args:
            base_currency (str): The fiat currency code to use for market data conversion.
            Defaults to "usd". Other valid values may include "eur", "gbp", etc.

        Returns:
            list: A list of dictionaries containing market data for cryptocurrencies.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={base_currency}"
            currencies = self._api_request(url=url)
            return currencies
        except HTTPError:
            raise HTTPError(f"HTTP error occurred: {HTTPError}")
        except JSONDecodeError:
            raise JSONDecodeError(f"JSON decode error occurred: {JSONDecodeError}")
        except RequestException as e:
            raise RequestException(f"Request error occurred: {e}")
