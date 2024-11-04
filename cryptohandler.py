import json
import logging
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

coingecko_api_key = os.getenv("COINGECKO_API_KEY")
