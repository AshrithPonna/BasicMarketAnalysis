"""Stock Price Tracker & Analysis Tool.

How to run:
    python3 -m pip install yfinance pandas numpy matplotlib
    python3 stock_tracker.py              # Analyze the default AAPL ticker
    python3 stock_tracker.py MSFT         # Analyze a different ticker

A price chart is created and saved, and furthermore, a year's summary of financial data is saved."""

from pathlib import Path
import sys
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


# Change this value to analyze another stock, such as "TSLA" or "MSFT".
DEFAULT_TICKER = "AAPL"
LOOKBACK_PERIOD = "1y"


def get_ticker_from_command_line() -> str:
    """Return a ticker from the command line, or use Apple by default."""
    # sys.argv contains the words typed after the script name in the terminal.
    # For example, `python3 stock_tracker.py MSFT` makes sys.argv[1] "MSFT".
    if len(sys.argv) > 1:
        return sys.argv[1].upper()
    return DEFAULT_TICKER


def fetch_closing_prices(ticker_symbol: str) -> pd.Series:
    """Download one year of daily closing prices for one stock."""
    # yfinance sends a request to Yahoo Finance and returns the result as a
    # pandas DataFrame. Each row represents one trading day.
    stock_data = yf.Ticker(ticker_symbol).history(
        period=LOOKBACK_PERIOD,
        interval="1d",
        auto_adjust=False,
    )

    # An invalid ticker, network problem, or missing data can produce an empty
    # DataFrame. Stop with a helpful message instead of failing later.
    if stock_data.empty or "Close" not in stock_data:
        raise ValueError(
            f"No price data was returned for '{ticker_symbol}'. "
            "Check the ticker symbol and your internet connection."
        )

    # We only need the Close column. A closing price is the stock's final traded
    # price for that day. squeeze() handles different yfinance return shapes.
    closing_prices = stock_data["Close"].squeeze().dropna()
    if not isinstance(closing_prices, pd.Series) or closing_prices.empty:
        raise ValueError(f"No closing-price data was returned for '{ticker_symbol}'.")

    closing_prices.name = "Close"
    return closing_prices


def calculate_metrics(closing_prices: pd.Series) -> dict[str, Union[float, pd.Series]]:
    """Calculate summary metrics and daily percentage returns."""
    # A daily return measures the relative price change from one trading day to
    # the next. For example, 100 to 103 is a 3% return. The first day has no
    # previous day for comparison, so pct_change() creates one missing value.
    daily_returns = closing_prices.pct_change().dropna()

    # Standard deviation measures how spread out the daily returns are. We use
    # it as a simple volatility measure: larger volatility means less stable
    # daily movements. ddof=1 calculates the sample standard deviation.
    return {
        # The average closing price summarizes the typical daily price level.
        "average_close": float(np.mean(closing_prices)),
        # Volatility is calculated from returns, rather than dollar prices, so
        # it is comparable across stocks with different price levels.
        "volatility": float(np.std(daily_returns, ddof=1)),
        # These describe the historical range of closing prices in this sample.
        "highest_close": float(np.max(closing_prices)),
        "lowest_close": float(np.min(closing_prices)),
        # This is the arithmetic mean of the daily percentage changes.
        "average_daily_return": float(np.mean(daily_returns)),
        "daily_returns": daily_returns,
    }


def print_summary(
    ticker_symbol: str,
    closing_prices: pd.Series,
    metrics: dict[str, Union[float, pd.Series]],
) -> None:
    """Print a readable report of the analysis results."""
    # The daily returns Series is kept in the metrics dictionary so it can be
    # reused for a histogram or other analysis later.
    daily_returns = metrics["daily_returns"]
    assert isinstance(daily_returns, pd.Series)

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
    # A line chart makes the stock's price trend and large movements easy to
    # see. The image is saved instead of only displayed so it can be shared.
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

    # Keep data-fetching errors user-friendly. For example, this catches an
    # invalid ticker without showing a long traceback to a beginner.
    try:
        closing_prices = fetch_closing_prices(ticker_symbol)
        metrics = calculate_metrics(closing_prices)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print_summary(ticker_symbol, closing_prices, metrics)
    # Save the chart in the current project folder with the ticker in its name.
    chart_path = Path(f"{ticker_symbol}_stock_analysis.png")
    save_price_chart(ticker_symbol, closing_prices, chart_path)
    print(f"\nChart saved to: {chart_path}")


if __name__ == "__main__":
    main()