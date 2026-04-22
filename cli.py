import argparse
import sys
from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order
from bot.logging_config import setup_logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

logger = setup_logging()
console = Console()


def print_order_summary(symbol, side, order_type, quantity, price=None, stop_price=None):
    table = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
    table.add_column("Field", style="bold cyan", width=14)
    table.add_column("Value", style="white")
    table.add_row("Symbol", symbol)
    table.add_row("Side", f"[green]{side}[/green]" if side == "BUY" else f"[red]{side}[/red]")
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))
    console.print(Panel(table, title="[bold cyan]Order Summary[/bold cyan]", border_style="cyan"))


def print_order_response(response):
    table = Table(box=box.ROUNDED, show_header=False, border_style="green")
    table.add_column("Field", style="bold green", width=14)
    table.add_column("Value", style="white")
    table.add_row("Order ID", str(response.get('orderId', 'N/A')))

    status = response.get('status', 'N/A')
    status_styled = f"[bold green]{status}[/bold green]" if status == "FILLED" else f"[yellow]{status}[/yellow]"
    table.add_row("Status", status_styled)
    table.add_row("Executed", str(response.get('executedQty', 'N/A')))
    table.add_row("Avg Price", str(response.get('avgPrice', 'N/A')))
    console.print(Panel(table, title="[bold green]Order Response[/bold green]", border_style="green"))


def prompt_order():
    console.print(Panel("[bold yellow]Binance Spot Testnet — Interactive Order Entry[/bold yellow]", border_style="yellow"))

    symbol = Prompt.ask("[cyan]Symbol[/cyan]", default="BTCUSDT").upper().strip()

    side = Prompt.ask("[cyan]Side[/cyan]", choices=["BUY", "SELL"]).upper()

    order_type = Prompt.ask(
        "[cyan]Order Type[/cyan]",
        choices=["MARKET", "LIMIT", "STOP_LOSS_LIMIT"]
    ).upper()

    while True:
        quantity_input = Prompt.ask("[cyan]Quantity[/cyan]")
        try:
            quantity = float(quantity_input)
            if quantity <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[red]Invalid quantity. Enter a positive number e.g. 0.001[/red]")

    price = None
    stop_price = None

    if order_type in ("LIMIT", "STOP_LOSS_LIMIT"):
        while True:
            price_input = Prompt.ask("[cyan]Limit Price[/cyan]")
            try:
                price = float(price_input)
                if price <= 0:
                    raise ValueError
                break
            except ValueError:
                console.print("[red]Invalid price. Enter a positive number e.g. 74900[/red]")

    if order_type == "STOP_LOSS_LIMIT":
        while True:
            stop_input = Prompt.ask("[cyan]Stop/Trigger Price[/cyan]")
            try:
                stop_price = float(stop_input)
                if stop_price <= 0:
                    raise ValueError
                break
            except ValueError:
                console.print("[red]Invalid stop price. Enter a positive number e.g. 75000[/red]")

    return symbol, side, order_type, quantity, price, stop_price


def run_order(client, symbol, side, order_type, quantity, price, stop_price):
    if order_type == 'MARKET':
        return place_market_order(client, symbol, side, quantity)
    elif order_type == 'LIMIT':
        if not price:
            console.print("[red]ERROR: price is required for LIMIT orders[/red]")
            return None
        return place_limit_order(client, symbol, side, quantity, price)
    elif order_type == 'STOP_LOSS_LIMIT':
        if not price or not stop_price:
            console.print("[red]ERROR: price and stop-price are both required for STOP_LOSS_LIMIT orders[/red]")
            return None
        return place_stop_limit_order(client, symbol, side, quantity, price, stop_price)
    else:
        console.print(f"[red]ERROR: Unknown order type: {order_type}[/red]")
        return None


def main():
    parser = argparse.ArgumentParser(description='Binance Spot Testnet Trading Bot')
    parser.add_argument('--symbol',     required=False, help='Trading pair e.g. BTCUSDT')
    parser.add_argument('--side',       required=False, help='BUY or SELL')
    parser.add_argument('--type',       required=False, help='MARKET, LIMIT, or STOP_LOSS_LIMIT', dest='order_type')
    parser.add_argument('--quantity',   required=False, help='Order quantity e.g. 0.001')
    parser.add_argument('--price',      required=False, help='Price (required for LIMIT and STOP_LOSS_LIMIT orders)')
    parser.add_argument('--stop-price', required=False, help='Trigger price (required for STOP_LOSS_LIMIT orders)', dest='stop_price')

    args = parser.parse_args()

    # Interactive mode if no args provided
    if not args.symbol:
        symbol, side, order_type, quantity, price, stop_price = prompt_order()
    else:
        symbol     = args.symbol
        side       = args.side
        order_type = args.order_type
        quantity   = args.quantity
        price      = args.price
        stop_price = args.stop_price

    print_order_summary(symbol, side, order_type.upper(), quantity, price, stop_price)

    try:
        client = BinanceClient()
        response = run_order(client, symbol, side, order_type.upper(), quantity, price, stop_price)
        if response:
            print_order_response(response)
            console.print("[bold green]SUCCESS: Order placed successfully.[/bold green]")
            logger.info("Order completed successfully.")

    except ValueError as e:
        console.print(f"[bold red]VALIDATION ERROR:[/bold red] {e}")
        logger.error(f"Validation error: {e}")
    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {e}")
        logger.error(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
