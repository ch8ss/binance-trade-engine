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
BASE_URL = 'https://testnet.binance.vision'

class BinanceClient:
    def __init__(self):
        self.api_key = (os.getenv('API_KEY') or '').strip()
        self.api_secret = (os.getenv('API_SECRET') or '').strip()
        self.base_url = BASE_URL

        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in .env")

    def _sign(self, query_string):
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def send_request(self, method, endpoint, params=None):
        if params is None:
            params = {}

        params['timestamp'] = int(time.time() * 1000)

        query_string = urllib.parse.urlencode(params)
        signature = self._sign(query_string)
        full_query = query_string + '&signature=' + signature

        headers = {'X-MBX-APIKEY': self.api_key}
        url = self.base_url + endpoint + '?' + full_query

        logger.info(f"Sending {method} request to {endpoint} with params: {params}")

        try:
            response = requests.request(method, url, headers=headers)
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