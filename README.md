# Binance Spot Testnet Trading Bot

A command-line trading bot that places MARKET, LIMIT, and STOP_LOSS_LIMIT orders on the Binance Spot Testnet using HMAC-SHA256 signed requests. Supports both CLI flag mode and an interactive prompt mode.

---

## Setup

### Step 1 — Clone the repo

```bash
git clone https://github.com/ch8ss/binance-trade-engine
cd binance-trade-engine
```

### Step 2 — Install dependencies

```bash
pip3 install -r requirements.txt
```

This installs: `requests`, `python-dotenv`, `rich`

### Step 3 — Get your Testnet API keys

1. Go to [testnet.binance.vision](https://testnet.binance.vision)
2. Click **Log in with GitHub**
3. Navigate to **Generate HMAC_SHA256 Key**
4. Copy your **API Key** and **Secret Key** — the secret is only shown once

### Step 4 — Create a `.env` file

In the project root, create a file called `.env` and paste your keys:

```
API_KEY=your_api_key_here
API_SECRET=your_secret_key_here
```

> Never commit this file — it's already in `.gitignore`

---

## How to Run

There are two ways to use the bot:

### Option A — Interactive mode (no flags needed)

Just run:

```bash
python3 cli.py
```

The bot will prompt you for each field one at a time:

```
Symbol (BTCUSDT):   → press Enter to use default, or type e.g. ETHUSDT
Side:               → type BUY or SELL
Order Type:         → type MARKET, LIMIT, or STOP_LOSS_LIMIT
Quantity:           → type e.g. 0.001
Limit Price:        → (only asked for LIMIT / STOP_LOSS_LIMIT)
Stop Price:         → (only asked for STOP_LOSS_LIMIT)
```

---

### Option B — CLI flag mode

Pass everything as arguments directly:

**MARKET order**
```bash
python3 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**LIMIT order**
```bash
python3 cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000
```

**STOP_LOSS_LIMIT order**
```bash
python3 cli.py --symbol BTCUSDT --side SELL --type STOP_LOSS_LIMIT --quantity 0.001 --stop-price 75000 --price 74900
```
> Triggers a LIMIT SELL at `74900` once the price drops to `75000`

---

### All CLI arguments

| Argument        | Required | Description                                       |
|-----------------|----------|---------------------------------------------------|
| `--symbol`      | Yes      | Trading pair e.g. `BTCUSDT`                       |
| `--side`        | Yes      | `BUY` or `SELL`                                   |
| `--type`        | Yes      | `MARKET`, `LIMIT`, or `STOP_LOSS_LIMIT`           |
| `--quantity`    | Yes      | Order quantity e.g. `0.001`                       |
| `--price`       | No*      | Required for `LIMIT` and `STOP_LOSS_LIMIT`        |
| `--stop-price`  | No*      | Trigger price — required for `STOP_LOSS_LIMIT`    |

---

## Project Structure

```
binance-trade-engine/
├── bot/
│   ├── client.py          # BinanceClient — HMAC signing and HTTP requests
│   ├── orders.py          # place_market_order, place_limit_order, place_stop_limit_order
│   ├── validators.py      # Input validation for all order parameters
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # Entry point — interactive mode and CLI flag mode
├── requirements.txt
├── trading_bot.log        # Auto-generated, logs every request and response
└── .env                   # Not committed — holds your API keys
```

---

## Assumptions

- Targets the **Binance Spot Testnet** (`testnet.binance.vision`) — no real funds involved
- API keys must come from the Spot Testnet specifically — real exchange keys or Futures testnet keys will not work
- All requests are signed with HMAC-SHA256 as per the Binance API spec
- LIMIT and STOP_LOSS_LIMIT orders default to `timeInForce: GTC` (Good Till Cancelled)
- Minimum quantity for BTCUSDT is `0.001`
