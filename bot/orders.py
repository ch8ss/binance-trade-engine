from bot.validators import validate_order
from bot.logging_config import setup_logging

logger = setup_logging()

ORDER_ENDPOINT = '/fapi/v1/order'

def place_market_order(client, symbol, side, quantity):
    # Validate inputs
    symbol, side, order_type, quantity, _ = validate_order(
        symbol, side, 'MARKET', quantity
    )

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
    }

    logger.info(f"Placing MARKET order: {params}")

    try:
        response = client.send_request('POST', ORDER_ENDPOINT, params)
        logger.info(f"MARKET order placed successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to place MARKET order: {e}")
        raise


def place_limit_order(client, symbol, side, quantity, price):
    # Validate inputs
    symbol, side, order_type, quantity, price = validate_order(
        symbol, side, 'LIMIT', quantity, price
    )

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'quantity': quantity,
        'price': price,
        'timeInForce': 'GTC',
    }

    logger.info(f"Placing LIMIT order: {params}")

    try:
        response = client.send_request('POST', ORDER_ENDPOINT, params)
        logger.info(f"LIMIT order placed successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to place LIMIT order: {e}")
        raise