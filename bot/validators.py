VALID_SIDES = ['BUY', 'SELL']
VALID_ORDER_TYPES = ['MARKET', 'LIMIT', 'STOP_LOSS_LIMIT']

def validate_order(symbol, side, order_type, quantity, price=None):
    
    # Validate symbol
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string e.g. BTCUSDT")
    symbol = symbol.upper().strip()

    # Validate side
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got: {side}")

    # Validate order type
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be MARKET or LIMIT, got: {order_type}")

    # Validate quantity
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a valid positive number")

    # Validate price — only required for LIMIT
    if order_type.upper() == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be a positive number")
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid positive number")

    return symbol, side.upper(), order_type.upper(), quantity, price