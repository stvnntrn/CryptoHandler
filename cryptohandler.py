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

        try:
            self.supported_currencies = self.get_supported_currencies()
            self.supported_crypto_currencies = self.get_crypto_currencies()
        except (HTTPError, RequestException) as api_error:
            logging.error(f"API or network issue: {api_error}")
        except JSONDecodeError as json_error:
            logging.error(
                f"Failed to decode JSON data while fetching supported currencies: {json_error}"
            )

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
        headers = {"accept": "application/json", "x-cg-demo-api-key": coingecko_api_key}

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

    def _is_valid_crypto_id(self, id: str) -> bool:
        """
        Checks if the provided cryptocurrency ID is valid by comparing it against
        the list of supported cryptocurrencies.

        Args:
            id (str): The unique identifier for the cryptocurrency to validate.

        Returns:
            bool: True if the cryptocurrency ID exists in the supported list; otherwise, raises ValueError.

        Raises:
            ValueError: If the provided cryptocurrency ID does not exist in the supported list.
        """
        for currency in self.supported_crypto_currencies:
            if currency["id"] == id:
                return True
        raise ValueError(
            f"Provided cryptocurrency ID '{id}' does not exist in supported list."
        )

    def get_supported_currencies(self) -> list[str]:
        """
        Fetches a list of supported fiat currencies from the CoinGecko API.

        This method makes an API request to retrieve the currencies that are supported
        for price conversion against cryptocurrencies. The response is parsed and
        returned as a list.

        Returns:
            list: A list of strings representing the supported fiat currencies.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
        try:
            url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
            supported_currencies = self._api_request(url=url)
            return supported_currencies
        except HTTPError:
            raise HTTPError("HTTP error occurred")
        except JSONDecodeError:
            raise JSONDecodeError("JSON decode error occurred")
        except RequestException as e:
            raise RequestException(f"Request error occurred: {e}")

    def get_crypto_currencies(self) -> list[dict]:
        """
        Fetches a list of all supported cryptocurrencies, providing basic information including coin ID, name, and symbol.

        This method sends an API request to CoinGecko to retrieve an updated list of all supported coins on the platform.
        The data returned includes the coin's unique identifier (ID), name, and symbol.

        Returns:
            list[dict]: A list of dictionaries, each containing 'id', 'name', and 'symbol' for supported cryptocurrencies.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
        try:
            url = "https://api.coingecko.com/api/v3/coins/list"
            crypto_currencies = self._api_request(url=url)
            return crypto_currencies
        except HTTPError:
            raise HTTPError("HTTP error occurred")
        except JSONDecodeError:
            raise JSONDecodeError("JSON decode error occurred")
        except RequestException as e:
            raise RequestException(f"Request error occurred: {e}")

    def get_crypto_currencies_detailed(self, base_currency="usd") -> list[Dict]:
        """
        Fetches detailed market data for cryptocurrencies, including price, market cap, and trading volume.

        This method sends an API request to CoinGecko to retrieve the latest cryptocurrency market data,
        such as current price, market capitalization, and 24-hour trading volume, for the specified base currency.
        Before making the request, it verifies that the base currency is supported.

        Args:
            base_currency (str): The fiat currency code to use for market data conversion (default: "usd").
                Must be one of the supported currencies returned by the API, such as "usd", "eur", "gbp", etc.

        Returns:
            list[Dict]: A list of dictionaries containing detailed market data for cryptocurrencies, including
            'current_price', 'market_cap', 'total_volume', and other market-related metrics.

        Raises:
            ValueError: If the provided base currency is not supported.
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
        try:
            if base_currency in self.supported_currencies:
                url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={base_currency}"
            else:
                raise ValueError(f"Unsupported currency provided: {base_currency}")
            crypto_currencies = self._api_request(url=url)
            return crypto_currencies
        except HTTPError:
            raise HTTPError("HTTP error occurred")
        except JSONDecodeError:
            raise JSONDecodeError("JSON decode error occurred")
        except RequestException as e:
            raise RequestException(f"Request error occurred: {e}")

    def get_specific_crypto(self, id: str):
        """
        Fetches detailed information for a specific cryptocurrency by its unique ID.

        Args:
            id (str): The unique ID of the cryptocurrency to fetch.

        Returns:
            dict: A dictionary containing detailed information about the cryptocurrency.

        Raises:
            ValueError: If the provided cryptocurrency ID does not exist in the supported list.
            HTTPError: If the HTTP request returns an unsuccessful status code.
            JSONDecodeError: If the response cannot be decoded as JSON.
            RequestException: If a network-related error occurs or the request fails for another reason.
        """
        try:
            self._is_valid_crypto_id(id)
            url = f"https://api.coingecko.com/api/v3/coins/{id}"
            coin_data = self._api_request(url=url)
            return coin_data
        except HTTPError:
            raise HTTPError("HTTP error occurred")
        except JSONDecodeError:
            raise JSONDecodeError("JSON decode error occurred")
        except RequestException as e:
            raise RequestException(f"Request error occurred: {e}")
