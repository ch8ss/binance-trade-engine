import hmac
import hashlib
import time
import requests
import urllib.parse
import os
from dotenv import load_dotenv
from bot.logging_config import setup_logging

load_dotenv()
logger = setup_logging()

BASE_URL = 'https://testnet.binancefuture.com'

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv('lv1DddTMM7cctKdmyHSgbAq85LxGFXVBACotsolNyP0yvFtGx0cX9j4VN7lLbBYY')
        self.api_secret = os.getenv('KpqBDvDd7Z1JsgcFH8LXLebUI5pHaJKTQqwMDlnRtrzJ2EGZiW6DtRnJREC7cT9q')
        self.base_url = BASE_URL

        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in .env")

    def _sign(self, params):
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def send_request(self, method, endpoint, params=None):
        if params is None:
            params = {}

        # Add timestamp
        params['timestamp'] = int(time.time() * 1000)

        # Sign the request
        params['signature'] = self._sign(params)

        headers = {'X-MBX-APIKEY': self.api_key}
        url = self.base_url + endpoint

        logger.info(f"Sending {method} request to {endpoint} with params: {params}")

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params if method == 'GET' else None,
                data=params if method == 'POST' else None
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"Response received: {data}")
            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | Response: {response.text}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Connection error - check your internet or the testnet URL")
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise