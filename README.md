# Binance Spot Testnet Trading Bot

A command-line trading bot that places MARKET and LIMIT orders on the Binance Spot Testnet using HMAC-SHA256 signed requests.

## Setup

**1. Clone the repository**
```bash
git clone <repo-url>
cd Binance_Project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file** in the project root with your Binance Spot Testnet API credentials:
```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
```

> To generate testnet keys, visit [testnet.binance.vision/key/generate](https://testnet.binance.vision/key/generate) and log in as a test user.

## How to Run

### Place a MARKET order
```bash
python3 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order
```bash
python3 cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000
```

### Place a STOP_LOSS_LIMIT order
```bash
python3 cli.py --symbol BTCUSDT --side SELL --type STOP_LOSS_LIMIT --quantity 0.001 --stop-price 75000 --price 74900
```
> The order sits in the book and triggers a LIMIT sell at `74900` when the price drops to `75000`.

### All CLI arguments

| Argument        | Required | Description                                        |
|-----------------|----------|----------------------------------------------------|
| `--symbol`      | Yes      | Trading pair e.g. `BTCUSDT`                        |
| `--side`        | Yes      | `BUY` or `SELL`                                    |
| `--type`        | Yes      | `MARKET`, `LIMIT`, or `STOP_LOSS_LIMIT`            |
| `--quantity`    | Yes      | Order quantity e.g. `0.001`                        |
| `--price`       | No*      | Required for `LIMIT` and `STOP_LOSS_LIMIT` orders  |
| `--stop-price`  | No*      | Trigger price — required for `STOP_LOSS_LIMIT`     |

### Example output
```
========== ORDER SUMMARY ==========
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
====================================

========== ORDER RESPONSE ==========
  Order ID   : 7996982
  Status     : FILLED
  Executed   : 0.00100000
  Avg Price  : N/A
=====================================

SUCCESS: Order placed successfully.
```

All requests and responses are logged to `trading_bot.log`.

## Project Structure

```
Binance_Project/
├── bot/
│   ├── client.py        # BinanceClient — handles signing and HTTP requests
│   ├── orders.py        # place_market_order / place_limit_order
│   ├── validators.py    # Input validation for all order parameters
│   └── logging_config.py
├── cli.py               # Entry point — argument parsing and output formatting
├── requirements.txt
└── trading_bot.log      # Auto-generated log file
```

## Assumptions

- Targets the **Binance Spot Testnet** (`testnet.binance.vision`) using the `/api/v3/order` endpoint.
- API keys must be generated specifically from the Spot Testnet — keys from the real exchange or the Futures testnet will not work.
- Requests are authenticated with HMAC-SHA256 signatures as per the Binance API specification.
- LIMIT and STOP_LOSS_LIMIT orders use `timeInForce: GTC` (Good Till Cancelled) by default.
- No real funds are used; the testnet provides simulated balances.
