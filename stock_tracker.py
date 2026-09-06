"""Stock Price Tracker & Analysis Tool.

A price chart is created and saved, and furthermore, a year's summary of financial data is saved."""

from pathlib import Path
import sys
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


# This is the default stock ticker that is utilized.

DEFAULT_TICKER = "AAPL"
LOOKBACK_PERIOD = "1y"


def get_ticker_from_command_line() -> str:
    """Return a ticker from the command line, or use Apple by default."""

    # The sys.argv is a parameter that takes into acount the argument after initial call.

    if len(sys.argv) > 1:
        return sys.argv[1].upper()
    return DEFAULT_TICKER


def fetch_closing_prices(ticker_symbol: str) -> pd.Series:
    """Download one year of daily closing prices for one stock."""

    # Yahoo finance has to accept data requests and update stock information accordingly. This is saved in a panda data frame.
   
    stock_data = yf.Ticker(ticker_symbol).history(
        period=LOOKBACK_PERIOD,
        interval="1d",
        auto_adjust=False,
    )

    # This only occurs when invalid inputs are present (for example, ticker is incorrect).
   
    if stock_data.empty or "Close" not in stock_data:
        raise ValueError(
            f"No price data was returned for '{ticker_symbol}'. "
            "Check the ticker symbol and your internet connection."
        )

    # Only focusing on closing prices, disregarded format errors and ensuring that a colum is made.
   
    closing_prices = stock_data["Close"].squeeze().dropna()
    if not isinstance(closing_prices, pd.Series) or closing_prices.empty:
        raise ValueError(f"No closing-price data was returned for '{ticker_symbol}'.")

    closing_prices.name = "Close"
    return closing_prices


def calculate_metrics(closing_prices: pd.Series) -> dict[str, Union[float, pd.Series]]:
    """Calculate summary metrics and daily percentage returns."""

    # Here, daily returns is calculated and determined from data frame. This takes into account days that have no comparative days.
    
    daily_returns = closing_prices.pct_change().dropna()

    # Metrics are returned accordingly here. 
    return {
        # This is the price level for stocks daily (avg).
        "average_close": float(np.mean(closing_prices)),

        # Standard deviation of parameters used to determine volatility.

        "volatility": float(np.std(daily_returns, ddof=1)),

        # Price ranges are recorded.

        "highest_close": float(np.max(closing_prices)),
        "lowest_close": float(np.min(closing_prices)),

        # Daily return is averaged here. 

        "average_daily_return": float(np.mean(daily_returns)),
        "daily_returns": daily_returns,
    }


def print_summary(
    ticker_symbol: str,
    closing_prices: pd.Series,
    metrics: dict[str, Union[float, pd.Series]],
) -> None:
    """Print a readable report of the analysis results."""

    # Information is saved for later use (in dictionary).

    daily_returns = metrics["daily_returns"]
    assert isinstance(daily_returns, pd.Series)

    # Information is printed in a readable format.

    print("\n" + "=" * 52)
    print(f"STOCK PRICE ANALYSIS: {ticker_symbol}")
    print("=" * 52)
    print(f"Period: {closing_prices.index[0].date()} to {closing_prices.index[-1].date()}")
    print(f"Trading days: {len(closing_prices)}")
    print("-" * 52)
    print(f"Average closing price: ${metrics['average_close']:,.2f}")
    print(f"Volatility (daily return std. dev.): {metrics['volatility']:.2%}")
    print(f"Highest closing price: ${metrics['highest_close']:,.2f}")
    print(f"Lowest closing price: ${metrics['lowest_close']:,.2f}")
    print(f"Average daily return: {metrics['average_daily_return']:.2%}")
    print(f"Daily returns calculated: {len(daily_returns)}")
    print("=" * 52)


def save_price_chart(
    ticker_symbol: str,
    closing_prices: pd.Series,
    output_path: Path,
) -> None:
    """Save a line chart of daily closing prices."""

    # From data frames (derived from Yahoo Finance), a linear chart summarizing performance is created.

    plt.figure(figsize=(11, 6))
    plt.plot(closing_prices.index, closing_prices, color="steelblue", linewidth=1.5)
    plt.title(f"{ticker_symbol} Closing Price - Last Year")
    plt.xlabel("Date")
    plt.ylabel("Closing price (USD)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    """Run the complete stock analysis."""
    ticker_symbol = get_ticker_from_command_line()

    # Invalid ticker catches in program.

    try:
        closing_prices = fetch_closing_prices(ticker_symbol)
        metrics = calculate_metrics(closing_prices)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print_summary(ticker_symbol, closing_prices, metrics)

    # Chart created is saved accordingly based on name. 

    chart_path = Path(f"{ticker_symbol}_stock_analysis.png")
    save_price_chart(ticker_symbol, closing_prices, chart_path)
    print(f"\nChart saved to: {chart_path}")

# Main call.

if __name__ == "__main__":
    main()