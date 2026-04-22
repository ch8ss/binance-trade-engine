from bot.validators import validate_order
from bot.logging_config import setup_logging

logger = setup_logging()

ORDER_ENDPOINT = '/api/v3/order'

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


def place_stop_limit_order(client, symbol, side, quantity, price, stop_price):
    symbol, side, order_type, quantity, price = validate_order(
        symbol, side, 'STOP_LOSS_LIMIT', quantity, price
    )

    try:
        stop_price = float(stop_price)
        if stop_price <= 0:
            raise ValueError("Stop price must be a positive number")
    except (TypeError, ValueError):
        raise ValueError("Stop price must be a valid positive number")

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'STOP_LOSS_LIMIT',
        'quantity': quantity,
        'price': price,
        'stopPrice': stop_price,
        'timeInForce': 'GTC',
    }

    logger.info(f"Placing STOP_LOSS_LIMIT order: {params}")

    try:
        response = client.send_request('POST', ORDER_ENDPOINT, params)
        logger.info(f"STOP_LOSS_LIMIT order placed successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to place STOP_LOSS_LIMIT order: {e}")
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