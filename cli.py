import argparse
from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order
from bot.logging_config import setup_logging

logger = setup_logging()

def print_order_summary(symbol, side, order_type, quantity, price=None):
    print("\n========== ORDER SUMMARY ==========")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("====================================\n")

def print_order_response(response):
    print("\n========== ORDER RESPONSE ==========")
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Executed   : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price  : {response.get('avgPrice', 'N/A')}")
    print("=====================================\n")

def main():
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')

    parser.add_argument('--symbol',   required=True,  help='Trading pair e.g. BTCUSDT')
    parser.add_argument('--side',     required=True,  help='BUY or SELL')
    parser.add_argument('--type',     required=True,  help='MARKET or LIMIT', dest='order_type')
    parser.add_argument('--quantity', required=True,  help='Order quantity e.g. 0.01')
    parser.add_argument('--price',    required=False, help='Price (required for LIMIT orders)')

    args = parser.parse_args()

    # Print what the user is about to send
    print_order_summary(
        args.symbol,
        args.side,
        args.order_type,
        args.quantity,
        args.price
    )

    try:
        client = BinanceClient()

        if args.order_type.upper() == 'MARKET':
            response = place_market_order(
                client,
                args.symbol,
                args.side,
                args.quantity
            )
        elif args.order_type.upper() == 'LIMIT':
            if not args.price:
                print("ERROR: --price is required for LIMIT orders")
                logger.error("LIMIT order attempted without price")
                return
            response = place_limit_order(
                client,
                args.symbol,
                args.side,
                args.quantity,
                args.price
            )
        else:
            print(f"ERROR: Unknown order type: {args.order_type}")
            return

        print_order_response(response)
        print("SUCCESS: Order placed successfully.")
        logger.info("Order completed successfully.")

    except ValueError as e:
        print(f"VALIDATION ERROR: {e}")
        logger.error(f"Validation error: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()